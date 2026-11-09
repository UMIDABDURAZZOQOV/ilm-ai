"""Explicit per-process PostgreSQL budget; no URL/credential logging or retries."""
import os


def bounded_int(env, name, default, minimum, maximum):
    try:
        value = int(env.get(name, default))
    except (ValueError, TypeError):
        raise ValueError(f'invalid_{name}') from None
    if not minimum <= value <= maximum:
        raise ValueError(f'invalid_{name}')
    return value


def postgres_engine_options(url, env=None):
    env = os.environ if env is None else env
    if not url.startswith(('postgresql:', 'postgresql+psycopg2:')):
        raise ValueError('postgres_pool_requires_supported_driver')
    size = bounded_int(env, 'DB_POOL_SIZE', 5, 1, 32)
    overflow = bounded_int(env, 'DB_MAX_OVERFLOW', 0, 0, 16)
    timeout = bounded_int(env, 'DB_POOL_TIMEOUT_SECONDS', 2, 1, 10)
    connect = bounded_int(env, 'DB_CONNECT_TIMEOUT_SECONDS', 3, 1, 10)
    statement = bounded_int(env, 'DB_STATEMENT_TIMEOUT_MS', 15000, 1000, 120000)
    lock = bounded_int(env, 'DB_LOCK_TIMEOUT_MS', 2000, 100, 10000)
    idle = bounded_int(env, 'DB_IDLE_TRANSACTION_TIMEOUT_MS', 30000, 1000, 120000)
    return dict(pool_size=size, max_overflow=overflow, pool_timeout=timeout,
                pool_pre_ping=True, pool_recycle=300, pool_use_lifo=True,
                hide_parameters=True, connect_args={
                    'connect_timeout': connect,
                    'options': f'-c statement_timeout={statement} -c lock_timeout={lock} '
                               f'-c idle_in_transaction_session_timeout={idle}',
                })
