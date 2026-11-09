"""Process-local admission, bounded readiness and secret-free aggregate metrics.

No distributed quota, database mutation, cancellation of committed writes or
automatic replay is implemented here. The dedicated readiness executor has no
unbounded queue: its slot is released only when the actual DB probe finishes.
"""
import asyncio
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import hmac
import os
import threading
import time

from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.requests import Request
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, TimeoutError as PoolTimeout
from services.database_pool import bounded_int

BUCKETS = (.05, .1, .25, .5, 1, 2, 5, 15, 30)


def release_read_transaction(db):
    if db.new or db.dirty or db.deleted:
        raise RuntimeError('study_help_unexpected_pending_write')
    db.close()


def lane(path):
    if path.endswith('/study-help'):
        return 'study_help'
    if path.startswith('/auth/') or path.startswith('/account/deletion/'):
        return 'auth'
    if path in {'/health', '/livez', '/readyz', '/ops/metrics'}:
        return 'health'
    return 'core'


class ReliabilityState:
    def __init__(self, engine, *, env=None, probe_timeout=1.0):
        self.engine = engine
        env = os.environ if env is None else env
        self.maximum = bounded_int(env, 'HTTP_MAX_INFLIGHT', 32, 4, 128)
        self.help_maximum = bounded_int(env, 'HTTP_MAX_STUDY_HELP', 4, 1, 8)
        self.auth_maximum = bounded_int(env, 'HTTP_MAX_AUTH', 8, 1, 16)
        self.started = False
        self.draining = False
        self.active = Counter()
        self.requests = Counter()
        self.durations = Counter()
        self.duration_sum = Counter()
        self.rejected = Counter()
        self.peak_inflight = 0
        self._lock = threading.Lock()
        self._probe_slot = threading.BoundedSemaphore(1)
        self._probe_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix='readiness')
        self._probe_timeout = probe_timeout

    def reserve(self, kind):
        with self._lock:
            if self.draining:
                self.rejected[kind] += 1
                return False
            total = sum(self.active.values())
            maximum = self.help_maximum if kind == 'study_help' else self.auth_maximum
            if total >= self.maximum or (kind in {'study_help', 'auth'} and self.active[kind] >= maximum):
                self.rejected[kind] += 1
                return False
            self.active[kind] += 1
            self.peak_inflight = max(self.peak_inflight, total + 1)
            return True

    def finish(self, kind, status, elapsed, reserved):
        with self._lock:
            if reserved:
                self.active[kind] -= 1
            self.requests[(kind, status // 100)] += 1
            self.duration_sum[kind] += elapsed
            for limit in BUCKETS:
                if elapsed <= limit:
                    self.durations[(kind, limit)] += 1
            self.durations[(kind, float('inf'))] += 1

    def _probe(self):
        with self.engine.connect() as connection:
            connection.execute(text('SELECT 1'))

    async def readiness(self):
        if not self.started or self.draining or not self._probe_slot.acquire(blocking=False):
            return False
        try:
            future = self._probe_executor.submit(self._probe)
        except RuntimeError:
            self._probe_slot.release()
            return False
        future.add_done_callback(lambda _: self._probe_slot.release())
        try:
            wrapped = asyncio.wrap_future(future)
            wrapped.add_done_callback(lambda done: done.exception() if not done.cancelled() else None)
            await asyncio.wait_for(asyncio.shield(wrapped), self._probe_timeout)
            return True
        except Exception:
            return False

    def metrics(self):
        with self._lock:
            lines = ['# TYPE ilm_http_requests_total counter']
            for (kind, status), count in sorted(self.requests.items()):
                lines.append(f'ilm_http_requests_total{{lane="{kind}",status_class="{status}xx"}} {count}')
            lines.append('# TYPE ilm_http_duration_seconds histogram')
            for (kind, limit), count in sorted(self.durations.items()):
                label = '+Inf' if limit == float('inf') else str(limit)
                lines.append(f'ilm_http_duration_seconds_bucket{{lane="{kind}",le="{label}"}} {count}')
            for kind, elapsed in sorted(self.duration_sum.items()):
                lines.append(f'ilm_http_duration_seconds_sum{{lane="{kind}"}} {elapsed}')
                lines.append(f'ilm_http_duration_seconds_count{{lane="{kind}"}} {self.durations[(kind, float("inf"))]}')
            for kind, count in sorted(self.active.items()):
                lines.append(f'ilm_http_inflight{{lane="{kind}"}} {count}')
            for kind, count in sorted(self.rejected.items()):
                lines.append(f'ilm_http_rejected_total{{lane="{kind}"}} {count}')
            pool = self.engine.pool
            if callable(getattr(pool, 'checkedout', None)):
                lines.append(f'ilm_db_pool_checked_out {pool.checkedout()}')
                lines.append(f'ilm_db_pool_size {pool.size()}')
            return '\n'.join(lines) + '\n'

    async def shutdown(self):
        self.draining = True
        self._probe_executor.shutdown(wait=False, cancel_futures=True)
        self.engine.dispose()


class AdmissionMiddleware:
    def __init__(self, app, state):
        self.app, self.state = app, state

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)
        kind = lane(scope.get('path', ''))
        started = time.monotonic()
        status = 500
        response_started = False
        reserved = kind != 'health'
        if reserved and not self.state.reserve(kind):
            response = JSONResponse({'detail': 'server_busy_try_again'}, status_code=503,
                                    headers={'Retry-After': '2', 'Cache-Control': 'no-store'})
            self.state.finish(kind, 503, time.monotonic()-started, False)
            return await response(scope, receive, send)

        async def observe(message):
            nonlocal status, response_started
            if message['type'] == 'http.response.start':
                response_started, status = True, message['status']
            await send(message)

        try:
            await self.app(scope, receive, observe)
        except asyncio.CancelledError:
            status = 499
            raise
        except (OperationalError, PoolTimeout):
            if response_started:
                raise
            status = 503
            response = JSONResponse({'detail': 'database_temporarily_unavailable'}, status_code=503,
                                    headers={'Retry-After': '2', 'Cache-Control': 'no-store'})
            await response(scope, receive, observe)
        finally:
            self.state.finish(kind, status, time.monotonic()-started, reserved)


def install_reliability(app, engine, *, env=None, probe_timeout=1.0):
    state = ReliabilityState(engine, env=env, probe_timeout=probe_timeout)
    app.state.reliability = state
    app.add_middleware(AdmissionMiddleware, state=state)

    async def started():
        state.started = True
    app.router.add_event_handler('startup', started)

    @app.get('/livez', include_in_schema=False)
    async def live():
        return JSONResponse({'status': 'alive'}, headers={'Cache-Control': 'no-store'})

    @app.get('/readyz', include_in_schema=False)
    async def ready():
        ok = await state.readiness()
        return JSONResponse({'status': 'ready' if ok else 'not_ready'}, status_code=200 if ok else 503,
                            headers={'Cache-Control': 'no-store'})

    @app.get('/ops/metrics', include_in_schema=False)
    async def metrics(request: Request):
        token = (os.environ if env is None else env).get('METRICS_BEARER_TOKEN', '')
        supplied = request.headers.get('authorization', '')
        if len(token) < 32 or len(supplied) > 1024 or not hmac.compare_digest(supplied.encode(), ('Bearer '+token).encode()):
            return JSONResponse({'detail': 'not_found'}, status_code=404, headers={'Cache-Control': 'no-store'})
        return PlainTextResponse(state.metrics(), headers={'Cache-Control': 'no-store'})

    app.router.add_event_handler('shutdown', state.shutdown)
    return state
