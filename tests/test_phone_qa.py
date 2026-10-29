"""Integration checks use a fresh owned DB outside Git, never the phone's progress."""
import json
from pathlib import Path

import pytest

from scripts import serve_phone_qa as qa


@pytest.fixture(scope='module')
def sandbox(tmp_path_factory):
    from starlette.testclient import TestClient
    root = tmp_path_factory.mktemp('owned') / 'sandbox'
    qa.sandbox_directory(str(root), False)
    qa.configure(root, False, 8925)
    counts = qa.initialize(root)
    app = qa.create_app(root, counts)
    client = TestClient(app, base_url='http://127.0.0.1:8925', client=('127.0.0.1', 12345))
    code = json.loads((root / 'pairing.json').read_text())['code']
    response = client.post('/qa/pair', json={'code': code})
    assert response.status_code == 200
    credentials = response.json()
    return root, app, client, credentials


def test_owned_directory_rejects_git_and_implicit_reuse(tmp_path):
    with pytest.raises(ValueError, match='outside_git'):
        qa.sandbox_directory(str(Path(__file__).parent / 'unsafe'), False)
    with pytest.raises(ValueError, match='explicit_resume'):
        qa.sandbox_directory(str(tmp_path), False)


def test_local_security_and_single_use_pairing(sandbox):
    from starlette.testclient import TestClient
    root, app, client, credentials = sandbox
    assert credentials['needs_onboarding'] is True
    code = json.loads((root / 'pairing.json').read_text())['code']
    assert client.post('/qa/pair', json={'code': code}).status_code == 401
    assert client.post('/qa/pair', json={'code': code, 'user_id': 1}).status_code == 422
    assert client.get('/qa/me').status_code == 401
    assert client.get('/health', headers={'x-forwarded-for': '127.0.0.1'}).status_code == 403
    assert client.get('/health', headers={'host': 'example.com'}).status_code == 400
    remote = TestClient(app, base_url='http://127.0.0.1:8925', client=('192.168.1.2', 12345))
    assert remote.get('/health').status_code == 403
    assert client.post('/auth/signup', json={}).status_code == 404
    assert client.get('/auth/mobile/config').json()['google_configured'] is False
    assert client.get('/mobile/tutor').status_code == 404


def test_five_authenticated_catalogs_and_idempotent_import(sandbox):
    root, app, client, credentials = sandbox
    client.headers['Authorization'] = 'Bearer ' + credentials['access_token']
    me = client.get('/qa/me')
    assert me.status_code == 200, me.text
    assert sum(me.json()['subjects'].values()) == 1381
    assert me.json()['xp_total'] == 0
    for path in ['/mobile/skills/subjects', '/preview/physics/v2/catalog',
                 '/preview/chemistry/v2/catalog', '/preview/world_history/v2/catalog',
                 '/preview/uzbekistan-history/v2/catalog']:
        result = client.get(path)
        assert result.status_code == 200, (path, result.text)
        assert 'grading_spec' not in result.text
    assert qa.initialize(root) == me.json()['subjects']
    assert client.get('/qa/me').json()['xp_total'] == 0


def test_expiry_and_attempt_limit(sandbox, monkeypatch):
    from starlette.testclient import TestClient
    root, _, _, _ = sandbox
    app = qa.create_app(root, {})
    client = TestClient(app, base_url='http://127.0.0.1:8925', client=('127.0.0.1', 12345))
    code = json.loads((root / 'pairing.json').read_text())['code']
    for _ in range(5):
        assert client.post('/qa/pair', json={'code': 'INVALID!'}).status_code == 401
    assert client.post('/qa/pair', json={'code': code}).status_code == 401
    app = qa.create_app(root, {})
    code = json.loads((root / 'pairing.json').read_text())['code']
    client = TestClient(app, base_url='http://127.0.0.1:8925', client=('127.0.0.1', 12345))
    now = qa.time.time()
    monkeypatch.setattr(qa.time, 'time', lambda: now + 601)
    assert client.post('/qa/pair', json={'code': code}).status_code == 401
