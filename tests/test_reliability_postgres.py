"""Actual PostgreSQL faults on fresh owned schemas, never production/staging hosts.

Requires the existing explicitly provisioned loopback CI/test database URL file.
Terminates only a backend PID obtained from this test's own connection or a child
Popen object created by the test. Does not stop PostgreSQL or other workers.
"""
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import secrets
import subprocess
import sys
import time

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

from services.database_pool import postgres_engine_options
from services.database_url import normalize_database_url


@pytest.fixture
def owned_pg():
    filename = os.getenv('ILM_TEST_POSTGRES_URL_FILE')
    if not filename:
        pytest.skip('explicit isolated loopback PostgreSQL file required')
    url = make_url(normalize_database_url(Path(filename).read_text().strip()))
    assert url.get_backend_name() == 'postgresql'
    assert url.host in {'127.0.0.1','localhost'} and 'staging' in (url.database or '')
    schema = 'reliability_'+secrets.token_hex(8)
    options = postgres_engine_options(url.render_as_string(hide_password=False), {})
    options['connect_args']['options'] += f' -c search_path={schema}'
    engine = create_engine(url, **options)
    admin = create_engine(url, pool_size=1, max_overflow=0, hide_parameters=True,
                          connect_args={'connect_timeout':3, 'options':'-c statement_timeout=5000 -c lock_timeout=1000'})
    with admin.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA "{schema}"'))
    try:
        with engine.begin() as connection:
            connection.execute(text('CREATE TABLE awards (account INTEGER, request_id TEXT, '
                                    'amount INTEGER NOT NULL, PRIMARY KEY(account, request_id))'))
        yield engine, admin, schema, filename
    finally:
        engine.dispose()
        with admin.begin() as connection:
            connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        admin.dispose()


def test_parallel_duplicate_writes_keep_accounts_isolated_and_connections_returned(owned_pg):
    engine, _, _, _ = owned_pg
    def award(index):
        with engine.begin() as connection:
            connection.execute(text('INSERT INTO awards VALUES (:account,:request_id,10) ON CONFLICT DO NOTHING'),
                               {'account':index%10, 'request_id':'same-request'})
    with ThreadPoolExecutor(max_workers=10) as executor:
        list(executor.map(award, range(50)))
    assert engine.pool.checkedout() == 0
    with engine.connect() as connection:
        rows = connection.execute(text('SELECT account,COUNT(*),SUM(amount) FROM awards GROUP BY account')).all()
    assert len(rows) == 10 and all(count == 1 and total == 10 for _,count,total in rows)
    assert engine.pool.checkedout() == 0


def test_pre_ping_reconnects_only_the_owned_stale_connection(owned_pg):
    engine, admin, _, _ = owned_pg
    with engine.connect() as connection:
        owned_pid = connection.execute(text('SELECT pg_backend_pid()')).scalar_one()
    with admin.begin() as connection:
        assert connection.execute(text('SELECT pg_backend_pid()')).scalar_one() != owned_pid
        assert connection.execute(text('SELECT pg_terminate_backend(:pid)'), {'pid':owned_pid}).scalar_one()
    with engine.connect() as connection:
        assert connection.execute(text('SELECT 1')).scalar_one() == 1
        assert connection.execute(text('SELECT pg_backend_pid()')).scalar_one() != owned_pid
    assert engine.pool.checkedout() == 0


def test_owned_worker_process_crash_rolls_back_uncommitted_write(owned_pg, tmp_path):
    engine, _, schema, filename = owned_pg
    ack = tmp_path/'owned-transaction-open'
    code = '''
import re,sys,time
from pathlib import Path
from sqlalchemy import create_engine,text
from sqlalchemy.engine import make_url
from services.database_url import normalize_database_url
url=make_url(normalize_database_url(Path(sys.argv[1]).read_text().strip()))
assert url.host in {'127.0.0.1','localhost'} and 'staging' in url.database
schema=sys.argv[2]
assert re.fullmatch(r'reliability_[0-9a-f]{16}',schema)
engine=create_engine(url,hide_parameters=True,connect_args={'connect_timeout':3,'options':'-c statement_timeout=5000 -c search_path='+schema})
with engine.begin() as connection:
    connection.execute(text("INSERT INTO awards VALUES (999,'uncommitted-worker',10)"))
    Path(sys.argv[3]).touch(exist_ok=False)
    time.sleep(60)
'''
    child = subprocess.Popen([sys.executable, '-X','utf8','-c',code,filename,schema,str(ack)],
                             cwd=Path(__file__).resolve().parents[1],
                             stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        deadline = time.monotonic()+15
        while not ack.exists() and child.poll() is None and time.monotonic() < deadline:
            time.sleep(.05)
        assert ack.exists(), 'owned_child_did_not_open_transaction'
    finally:
        if child.poll() is None:
            child.terminate()
            try:
                child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait(timeout=5)
    with engine.connect() as connection:
        assert connection.execute(text('SELECT COUNT(*) FROM awards WHERE account=999')).scalar_one() == 0
        assert connection.execute(text('SELECT 1')).scalar_one() == 1
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO awards VALUES (999,'uncommitted-worker',10)"))
