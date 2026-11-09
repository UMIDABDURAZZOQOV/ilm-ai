"""Resource-gated in-process ASGI experiment; NOT production capacity evidence.

There is deliberately no target-URL option. Only a newly created app, a disposable
SQLite ledger, synthetic JWTs and a mocked provider are used. No main:app import,
learner database, credentials, Google/NVIDIA calls, hosting or public traffic.
"""
import argparse
import asyncio
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import re
import shutil
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
# The script also works by absolute path; imports below need the checkout root.
# ruff: noqa: E402

import httpx
import jwt
import psutil
from fastapi import FastAPI, Request, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from starlette.concurrency import run_in_threadpool
from services.reliability import install_reliability
from services.study_help_provider import EvidenceSelector, SelectorUnavailable

SYNTHETIC_SIGNING_KEY = 'component-lab-only-never-a-service-credential-123456'


class MockProvider(EvidenceSelector):
    def __init__(self):
        super().__init__(['synthetic-not-an-api-key'], 'mock-only')
        self.broken = False
        self.actual_calls = 0
    def _select(self, _):
        self.actual_calls += 1
        time.sleep(.03)
        if self.broken:
            raise SelectorUnavailable
        return ['e1']


def percentile(data, fraction):
    return round(sorted(data)[max(0, math.ceil(len(data)*fraction)-1)]*1000, 3) if data else None


async def experiment(users, output):
    report = dict(checked_utc=datetime.now(timezone.utc).isoformat(), status='SIMULATED',
                  scope='in_process_component_ASGI_not_full_backend_or_HTTP_capacity',
                  production_or_hosted_staging_contacted=False, external_provider_calls=0,
                  requested_users=users, assumptions={'think_seconds': .05, 'max_requests_per_phase': 1000},
                  phases=[], chaos=[])
    process = psutil.Process()
    available = psutil.virtual_memory().available
    minimum = 768*1024**2 if users <= 10 else max(2*1024**3, users*8*1024**2)
    report['resource_preflight'] = dict(available_ram_bytes=available, required_ram_bytes=minimum,
                                       logical_cpus=psutil.cpu_count(),
                                       disk_free_bytes=shutil.disk_usage(output.parent).free)
    if available < minimum or shutil.disk_usage(output.parent).free < 512*1024**2:
        report.update(status='BLOCKED', reason='insufficient_free_ram_or_disk_no_load_executed')
        output.write_text(json.dumps(report, indent=2)+'\n')
        print(json.dumps(report, indent=2))
        return
    if users > 10:
        report.update(status='BLOCKED', reason='larger_workload_requires_separate_resource_and_operator_review')
        output.write_text(json.dumps(report, indent=2)+'\n')
        print(json.dumps(report, indent=2))
        return
    vm = psutil.virtual_memory()
    report['resource_preflight']['host_ram_bytes'] = vm.total
    peak_rss = process.memory_info().rss
    provider = MockProvider()
    faults = {'database': False, 'cache': False, 'latency': False, 'after_commit': False}
    with tempfile.TemporaryDirectory(prefix='ilm-reliability-owned-') as directory:
        engine = create_engine('sqlite:///'+str(Path(directory)/'synthetic.db'),
                               pool_size=2, max_overflow=0, pool_timeout=1)
        with engine.begin() as conn:
            conn.execute(text('CREATE TABLE lab_awards (account INTEGER, request_id TEXT, '
                              'amount INTEGER, PRIMARY KEY(account, request_id))'))
        app = FastAPI()
        state = install_reliability(app, engine, env={'HTTP_MAX_INFLIGHT':'16', 'HTTP_MAX_STUDY_HELP':'4'})
        state.started = True

        def check_db():
            if faults['database']:
                raise OperationalError('synthetic_outage', {}, Exception('synthetic_failure'))

        @app.get('/catalogue')
        async def catalogue():
            if faults['latency']:
                await asyncio.sleep(.03)
            check_db()
            with engine.connect() as conn:
                conn.execute(text('SELECT 1'))
            # Same response without optional cache; no fabricated lesson facts.
            return {'fixture': True, 'subjects': 5, 'cache_used': not faults['cache']}

        def identity(request):
            value = request.headers.get('Authorization', '').removeprefix('Bearer ')
            try:
                return int(jwt.decode(value, SYNTHETIC_SIGNING_KEY, algorithms=['HS256'])['sub'])
            except (jwt.PyJWTError, ValueError, KeyError):
                raise HTTPException(401, 'invalid_synthetic_session') from None

        @app.get('/auth/lab-session')
        async def session(request: Request):
            identity(request)
            return {'valid': True}

        @app.post('/lab/progress')
        async def progress(request: Request):
            account = identity(request)
            payload = await request.json()
            request_id = payload.get('request_id', '')
            if not re.fullmatch(r'[a-z0-9-]{1,50}', request_id):
                raise HTTPException(422, 'invalid_fixture_request')
            check_db()
            with engine.begin() as conn:
                conn.execute(text('INSERT OR IGNORE INTO lab_awards VALUES (:account,:request_id,10)'),
                             {'account':account, 'request_id':request_id})
            if faults['after_commit']:
                raise OperationalError('synthetic_response_loss', {}, Exception('synthetic_failure'))
            return {'accepted': True}

        @app.post('/mobile/study-help')
        async def help_request():
            try:
                ids = await run_in_threadpool(provider.select, {'evidence': []})
                return {'provider_status':'selected', 'ids':ids}
            except SelectorUnavailable:
                return {'provider_status':'unavailable', 'fixture_reviewed_fallback':True}

        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url='http://owned-asgi-lab') as client:
            abort = asyncio.Event()

            async def phase(name, concurrent, seconds):
                nonlocal peak_rss
                samples, statuses = [], {}
                admitted = 0
                state.peak_inflight = 0
                cpu_before = process.cpu_times()
                started = time.perf_counter()
                async def virtual_user(index):
                    nonlocal peak_rss, admitted
                    token = jwt.encode({'sub':str(index), 'exp':int(time.time())+300}, SYNTHETIC_SIGNING_KEY)
                    headers = {'Authorization':'Bearer '+token}
                    # Stagger endpoint mix. Starting every user on AI creates
                    # an all-AI burst rather than the declared mixed workload.
                    iteration = index
                    while time.perf_counter()-started < seconds and not abort.is_set():
                        if admitted >= 1000:
                            break
                        admitted += 1  # No await before reservation: strict shared cap.
                        measured = time.perf_counter()
                        try:
                            if iteration % 10 == 0:
                                request = client.post('/mobile/study-help')
                            elif iteration % 10 == 1:
                                request = client.get('/auth/lab-session', headers=headers)
                            elif iteration % 10 == 2:
                                request = client.post('/lab/progress', json={'request_id':'repeat-'+str(index)}, headers=headers)
                            else:
                                request = client.get('/catalogue')
                            response = await asyncio.wait_for(request, 2)
                            code = response.status_code
                        except asyncio.TimeoutError:
                            code = 599
                        samples.append(time.perf_counter()-measured)
                        statuses[code] = statuses.get(code, 0)+1
                        memory = process.memory_info().rss
                        peak_rss = max(peak_rss, memory)
                        if code >= 500 or memory > 192*1024**2 or psutil.virtual_memory().available < 384*1024**2:
                            abort.set()
                        iteration += 1
                        await asyncio.sleep(.05)
                await asyncio.gather(*(virtual_user(i) for i in range(concurrent)))
                elapsed = time.perf_counter()-started
                cpu_after = process.cpu_times()
                report['phases'].append(dict(name=name, concurrent_users=concurrent, requests=len(samples),
                    seconds=round(elapsed,3), rps=round(len(samples)/elapsed,3),
                    p50_ms=percentile(samples,.5), p95_ms=percentile(samples,.95), p99_ms=percentile(samples,.99),
                    status_counts=statuses, error_rate=sum(n for code,n in statuses.items() if code>=400)/max(1,len(samples)),
                    process_cpu_one_core_percent=round(100*((cpu_after.user+cpu_after.system)-(cpu_before.user+cpu_before.system))/elapsed,2),
                    process_peak_rss_bytes=peak_rss, db_checked_out_after=engine.pool.checkedout(),
                    max_admitted_requests=state.peak_inflight, admission_queue_capacity=0,
                    executor_queue_length_measured=None, aborted=abort.is_set()))

            try:
                for name, concurrent, seconds in [('baseline',1,2), ('small',users,3),
                    ('ramp-2',min(users,2),2), ('ramp-5',min(users,5),2), ('ramp-10',users,2),
                    ('spike',users,2), ('short-soak',users,15)]:
                    if abort.is_set():
                        break
                    await phase(name, concurrent, seconds)
                if not abort.is_set():
                    provider.broken = True
                    results = await asyncio.gather(*(client.post('/mobile/study-help') for _ in range(3)))
                    core = await client.get('/catalogue')
                    report['chaos'].append(dict(scenario='mock_AI_timeout', fallback_all=all(
                        r.json().get('fixture_reviewed_fallback') for r in results), core_status=core.status_code))
                    provider.broken = False
                    faults['database'] = True
                    failed = await client.get('/catalogue')
                    alive = await client.get('/livez')
                    faults['database'] = False
                    started = time.perf_counter()
                    restored = await client.get('/catalogue')
                    report['chaos'].append(dict(scenario='simulated_database_outage', failure_status=failed.status_code,
                        liveness_status=alive.status_code, restored_status=restored.status_code,
                        recovery_observed_ms=round((time.perf_counter()-started)*1000,3)))
                    faults['cache'] = True
                    fallback = await client.get('/catalogue')
                    faults['cache'] = False
                    report['chaos'].append(dict(scenario='simulated_cache_loss', status=fallback.status_code,
                                               uncached_path=fallback.json()['cache_used'] is False))
                    faults['latency'] = True
                    try:
                        await asyncio.wait_for(client.get('/catalogue'), .005)
                    except asyncio.TimeoutError:
                        report['chaos'].append(dict(scenario='simulated_network_delay_cancellation', cancelled=True,
                                                   inflight_released=sum(state.active.values()) == 0))
                    faults['latency'] = False
                    token = jwt.encode({'sub':'999','exp':int(time.time())+300}, SYNTHETIC_SIGNING_KEY)
                    headers = {'Authorization':'Bearer '+token}
                    faults['after_commit'] = True
                    lost = await client.post('/lab/progress', json={'request_id':'lost-response'}, headers=headers)
                    faults['after_commit'] = False
                    replay = await client.post('/lab/progress', json={'request_id':'lost-response'}, headers=headers)
                    with engine.connect() as conn:
                        count = conn.execute(text('SELECT COUNT(*),SUM(amount) FROM lab_awards WHERE account=999')).one()
                    report['chaos'].append(dict(scenario='synthetic_committed_response_lost_then_replayed',
                                               initial_status=lost.status_code, replay_status=replay.status_code,
                                               award_rows=count[0], award_sum=count[1]))
                report['aborted'] = abort.is_set()
                report['not_tested'] = ['full_main_app_capacity','real_PostgreSQL_outage','real_OAuth_or_NVIDIA',
                    'production_XP_under_load','worker_process_kill','CPU_memory_exhaustion','long_endurance','50_to_1000_users']
            finally:
                await state.shutdown()
    output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--users', type=int, choices=[1,10,50,100,500,1000], default=10)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or not args.output.parent.is_dir():
        raise SystemExit('new_existing_parent_output_required')
    asyncio.run(experiment(args.users, args.output))
