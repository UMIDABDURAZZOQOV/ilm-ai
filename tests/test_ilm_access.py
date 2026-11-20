from concurrent.futures import ThreadPoolExecutor
from secrets import token_urlsafe
from threading import Barrier
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine import make_url

from services.db import get_db
from services.models import User
from test_deletion_reauth import owned, setup  # noqa: F401


@pytest.fixture
def local_client(owned, monkeypatch):  # noqa: F811
    client, factory, *_ = owned
    monkeypatch.setenv("ILM_INDEPENDENT_AUTH_QA", "true")
    with TestClient(client.app, base_url="http://127.0.0.1:8930", client=("127.0.0.1", 5001)) as local:
        yield local, factory


def test_access_key_reconnects_to_same_owned_progress_and_can_delete(local_client):
    client, factory = local_client
    key = "ilm1_" + token_urlsafe(32)
    endpoint = "/auth/ilm/access"
    created = client.post(endpoint, json={"key": key, "mode": "create"})
    assert created.status_code == 200
    assert key not in created.text
    first = created.json()
    uid = first["user_id"]
    assert first["needs_onboarding"] and first["email"] == ""
    retried = client.post(endpoint, json={"key": key, "mode": "create"}).json()
    assert retried["user_id"] == uid

    with factory() as db:
        account = db.get(User, uid)
        alias = account.email
        assert db.query(User).filter(User.email == alias).count() == 1
        assert key not in alias and account.password is None
        account.xp_total = 42
        account.age = 25
        db.commit()

    assert client.post("/auth/logout", json={"refresh_token": first["refresh_token"]}).status_code == 200
    assert client.post("/auth/refresh", json={"refresh_token": first["refresh_token"]}).status_code == 401
    restored = client.post(endpoint, json={"key": key, "mode": "login"}).json()
    assert restored["user_id"] == uid and restored["needs_onboarding"] is False
    headers = {"Authorization": "Bearer " + restored["access_token"]}
    profile = client.get(f"/auth/profile/{uid}", headers=headers).json()
    assert profile["xp_total"] == 42 and profile["email"] == "" and alias not in str(profile)
    assert client.get("/auth/profile/2", headers=headers).status_code == 403
    assert client.post("/auth/signup", json={"email": alias, "name": "Fixture", "password": "fixture-only"}).status_code == 422
    assert client.post("/auth/login", json={"email": alias, "password": key}).status_code == 401

    wrong_key = "ilm1_" + token_urlsafe(32)
    assert client.post(endpoint, json={"key": wrong_key, "mode": "login"}).status_code == 401
    options = client.get("/account/deletion/reauth/options", headers=headers)
    assert options.json() == {"method": "access_key"}
    assert client.post("/account/deletion/reauth/password", headers=headers,
                       json={"password": wrong_key}).status_code == 401
    proof = client.post("/account/deletion/reauth/password", headers=headers, json={"password": key}).json()
    result = client.post("/account/deletion/reauth/confirm", headers=headers, json={
        "request_id": proof["request_id"], "proof": proof["proof"], "confirmation": "DELETE",
    })
    assert result.json() == {"state": "deleted", "account_revoked": True}
    assert client.post(endpoint, json={"key": key, "mode": "login"}).status_code == 401
    with factory() as db:
        assert db.get(User, 2).xp_total == 160


def test_concurrent_registration_allocates_one_learner(local_client):
    client, factory = local_client
    key = "ilm1_" + token_urlsafe(32)
    ready = Barrier(2)

    def signup():
        ready.wait(timeout=5)
        return client.post("/auth/ilm/access", json={"mode": "create", "key": key})

    with ThreadPoolExecutor(max_workers=2) as pool:
        left, right = [pool.submit(signup) for _ in range(2)]
        first, second = left.result(timeout=12), right.result(timeout=12)
    assert first.status_code == second.status_code == 200
    assert first.json()["user_id"] == second.json()["user_id"]
    assert first.json()["refresh_token"] != second.json()["refresh_token"]
    with factory() as db:
        assert db.query(User).count() == 3


def test_loopback_requests_cannot_write_to_a_remote_database(local_client, monkeypatch):
    client, _ = local_client
    remote = SimpleNamespace(url=make_url("postgresql://database.example.test/qa_staging"))
    monkeypatch.setitem(client.app.dependency_overrides, get_db, lambda: SimpleNamespace(get_bind=lambda: remote))
    response = client.post("/auth/ilm/access", json={
        "mode": "create", "key": "ilm1_" + token_urlsafe(32),
    })
    assert response.status_code == 404


def test_web_deletion_uses_key_without_opening_a_login_session(local_client):
    client, factory = local_client
    key = "ilm1_" + token_urlsafe(32)
    created = client.post("/auth/ilm/access", json={"mode": "create", "key": key}).json()
    assert "access_key" in client.get("/account/deletion/config").json()["reauthentication_methods"]
    proof = client.post("/account/deletion/web/access-key", json={"key": key}).json()
    assert proof["request_id"].startswith("daw_")
    assert not {"access_token", "refresh_token", "key"}.intersection(proof)
    with factory() as db:
        assert db.get(User, created["user_id"]).xp_total == 0
    result = client.post("/account/deletion/reauth/confirm", json={
        "request_id": proof["request_id"], "proof": proof["proof"], "confirmation": "DELETE",
    })
    assert result.json() == {"state": "deleted", "account_revoked": True}
    assert client.post("/account/deletion/web/access-key", json={"key": key}).status_code == 401


@pytest.mark.parametrize("restriction", ["production", "disabled", "forwarded", "web_origin", "untrusted_host"])
def test_access_key_route_requires_explicit_loopback_qa(local_client, monkeypatch, restriction):
    client, factory = local_client
    headers = {}
    if restriction == "production":
        monkeypatch.setenv("ENVIRONMENT", "production")
    elif restriction == "disabled":
        monkeypatch.delenv("ILM_INDEPENDENT_AUTH_QA")
    elif restriction == "forwarded":
        headers["X-Forwarded-For"] = "192.0.2.1"
    elif restriction == "web_origin":
        headers["Origin"] = "https://example.test"
    else:
        headers["Host"] = "example.test"
    response = client.post("/auth/ilm/access", headers=headers, json={
        "mode": "create", "key": "ilm1_" + token_urlsafe(32),
    })
    assert response.status_code == 404
    assert client.post("/account/deletion/web/access-key", headers=headers,
                       json={"key": "ilm1_" + token_urlsafe(32)}).status_code == 404
    with factory() as db:
        assert db.query(User).count() == 2
