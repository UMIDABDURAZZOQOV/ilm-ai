"""Isolated failure injection; never imports main, provider networks or learner DBs."""
import asyncio
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import threading

from fastapi import FastAPI
import httpx
import pytest
from sqlalchemy import create_engine, text, Column, Integer
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.pool import QueuePool

from services.database_pool import postgres_engine_options
from services.reliability import install_reliability, release_read_transaction
from services.study_help_provider import EvidenceSelector, SelectorUnavailable
from run_backend import server_options


def test_pool_and_launch_bounds_do_not_depend_on_connection_success():
    options = postgres_engine_options('postgresql://unused', {})
    assert options['pool_size'] == 5 and options['max_overflow'] == 0
    assert options['pool_pre_ping'] and options['pool_timeout'] == 2
    assert options['connect_args']['connect_timeout'] == 3
    assert 'statement_timeout=15000' in options['connect_args']['options']
    assert server_options({})['workers'] == 1
    with pytest.raises(ValueError, match='multiple_workers'):
        server_options({'APP_WORKERS': '2'})
    assert server_options({'APP_WORKERS': '2', 'SCHEDULER_ENABLED': 'false'})['workers'] == 2


@pytest.mark.parametrize('name,value', [('DB_POOL_SIZE', '0'), ('DB_MAX_OVERFLOW', '-1'),
                                      ('DB_POOL_TIMEOUT_SECONDS', 'nan'), ('DB_STATEMENT_TIMEOUT_MS', '999999999')])
def test_invalid_resource_configuration_fails_closed(name, value):
    with pytest.raises(ValueError, match='invalid_'):
        postgres_engine_options('postgresql://unused', {name: value})


def test_read_connection_is_returned_before_provider_and_pending_writes_are_rejected(tmp_path):
    engine = create_engine('sqlite:///'+str(tmp_path/'owned.db'), poolclass=QueuePool,
                           pool_size=1, max_overflow=0)
    with Session(engine) as db:
        db.execute(text('SELECT 1'))
        assert engine.pool.checkedout() == 1
        release_read_transaction(db)
        assert engine.pool.checkedout() == 0
        base = declarative_base()
        class Owned(base):
            __tablename__ = 'owned'
            id = Column(Integer, primary_key=True)
        db.add(Owned(id=1))
        with pytest.raises(RuntimeError, match='unexpected_pending_write'):
            release_read_transaction(db)
    engine.dispose()


def test_circuit_recovery_uses_one_half_open_probe():
    now = [0]
    selector = EvidenceSelector(['synthetic-only'], 'test', clock=lambda: now[0])
    context = {'evidence': []}
    selector._select = lambda _: (_ for _ in ()).throw(SelectorUnavailable())
    for _ in range(3):
        with pytest.raises(SelectorUnavailable):
            selector.select(context)
    now[0] = 31
    entered, release = threading.Event(), threading.Event()
    def probe(_):
        entered.set()
        assert release.wait(2)
        return ['e1']
    selector._select = probe
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(selector.select, context)
        assert entered.wait(1)
        with pytest.raises(SelectorUnavailable):
            selector.select(context)
        release.set()
        assert future.result() == ['e1']
    selector._select = lambda _: ['e1']
    assert selector.select(context) == ['e1']


class ProbeEngine:
    def __init__(self):
        self.broken = False
        self.calls = 0
        self.pool = object()
    @contextmanager
    def connect(self):
        self.calls += 1
        if self.broken:
            raise OperationalError('private-statement', {}, Exception('secret-material'))
        yield self
    def execute(self, _):
        return None
    def dispose(self):
        pass


def test_dependency_failure_is_not_liveness_failure_and_recovers():
    async def scenario():
        app, engine = FastAPI(), ProbeEngine()
        state = install_reliability(app, engine)
        state.started = True
        @app.get('/catalogue')
        async def catalogue():
            with engine.connect():
                return {'ok': True}
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://lab') as client:
            assert (await client.get('/readyz')).status_code == 200
            engine.broken = True
            assert (await client.get('/readyz')).status_code == 503
            result = await client.get('/catalogue')
            assert result.status_code == 503 and 'secret-material' not in result.text
            assert (await client.get('/livez')).status_code == 200
            engine.broken = False
            assert (await client.get('/readyz')).status_code == 200
            state.draining = True
            assert (await client.get('/catalogue')).status_code == 503
            assert (await client.get('/readyz')).status_code == 503
            assert (await client.get('/livez')).status_code == 200
        await state.shutdown()
    asyncio.run(scenario())


def test_slow_readiness_has_one_actual_probe_even_after_timeout():
    async def scenario():
        engine = ProbeEngine()
        entered, release = threading.Event(), threading.Event()
        def slow():
            engine.calls += 1
            entered.set()
            release.wait(2)
        app = FastAPI()
        state = install_reliability(app, engine, probe_timeout=.02)
        state.started = True
        state._probe = slow
        try:
            assert await state.readiness() is False
            assert entered.is_set()
            assert not any(await asyncio.gather(*(state.readiness() for _ in range(50))))
            assert engine.calls == 1
        finally:
            release.set()
            await state.shutdown()
    asyncio.run(scenario())


def test_ai_bulkhead_and_cancellation_preserve_core_capacity():
    async def scenario():
        app, engine = FastAPI(), ProbeEngine()
        state = install_reliability(app, engine, env={'HTTP_MAX_INFLIGHT': '8', 'HTTP_MAX_STUDY_HELP': '1'})
        state.started = True
        gate, entered = asyncio.Event(), asyncio.Event()
        @app.post('/mobile/study-help')
        async def help_request():
            entered.set()
            await gate.wait()
            return {'ok': True}
        @app.get('/catalogue')
        async def catalogue():
            return {'subjects': 'synthetic-only'}
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://lab') as client:
            pending = asyncio.create_task(client.post('/mobile/study-help'))
            await entered.wait()
            assert (await client.post('/mobile/study-help')).status_code == 503
            assert (await client.get('/catalogue')).status_code == 200
            assert (await client.get('/livez')).status_code == 200
            pending.cancel()
            with pytest.raises(asyncio.CancelledError):
                await pending
            assert sum(state.active.values()) == 0
            assert state.rejected['study_help'] == 1
            assert state.requests[('study_help', 4)] == 1  # Client cancellation, not a server 5xx.
        await state.shutdown()
    asyncio.run(scenario())


def test_metrics_are_opt_in_bounded_and_contain_no_paths_or_headers():
    async def scenario():
        app, engine = FastAPI(), ProbeEngine()
        token = 'synthetic-lab-metrics-token-1234567890'
        state = install_reliability(app, engine, env={'METRICS_BEARER_TOKEN': token})
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://lab') as client:
            assert (await client.get('/ops/metrics')).status_code == 404
            assert (await client.get('/ops/metrics', headers=[(b'authorization', b'Bearer \xff')])).status_code == 404
            for index in range(50):
                await client.get(f'/unknown/private-{index}?token=hidden', headers={'Authorization': 'Bearer hidden'})
            result = await client.get('/ops/metrics', headers={'Authorization': 'Bearer '+token})
            assert result.status_code == 200
            assert len(result.text.splitlines()) < 60
            assert all(s not in result.text for s in [token, 'hidden', 'private-', 'Authorization'])
        await state.shutdown()
    asyncio.run(scenario())
