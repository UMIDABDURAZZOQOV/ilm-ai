"""Bounded server launcher. Scaling requires the embedded scheduler disabled."""
import os
from services.database_pool import bounded_int


def server_options(env=None):
    env = os.environ if env is None else env
    workers = bounded_int(env, 'APP_WORKERS', 1, 1, 8)
    scheduler = env.get('SCHEDULER_ENABLED', 'true')
    if scheduler not in {'true', 'false'}:
        raise ValueError('invalid_SCHEDULER_ENABLED')
    if workers > 1 and scheduler != 'false':
        raise ValueError('multiple_workers_require_separate_scheduler')
    return dict(host='0.0.0.0', port=bounded_int(env, 'PORT', 8000, 1024, 65535),
                workers=workers, limit_concurrency=bounded_int(env, 'HTTP_MAX_CONNECTIONS', 64, 8, 256),
                backlog=bounded_int(env, 'HTTP_BACKLOG', 64, 8, 256),
                timeout_keep_alive=5, timeout_graceful_shutdown=20)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', **server_options())
