"""Disposable synthetic accounts only; never use hosted users or send mail."""

from datetime import timedelta
import importlib.util
from pathlib import Path

from alembic.migration import MigrationContext
from alembic.operations import Operations
import pytest

from test_account_deletion import setup as _setup_fixture
from services import deletion_reauth as service, users, tokens, email
from services.deletion_reauth_models import DeletionReauth, ManualDeletionRequest
from services.account_models import DeletionChallenge
from services.models import User, UserLessonProgress
from services.mobile_oauth import pkce_challenge
from services.study import utcnow

setup = _setup_fixture


@pytest.fixture
def owned(setup, monkeypatch):
    client, factory, delivered, root, token = setup
    spec = importlib.util.spec_from_file_location(
        "reauth_migration",
        Path(__file__).parents[1] / "alembic/versions/0018_deletion_reauth.py",
    )
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)
    with factory().get_bind().begin() as connection:
        with Operations.context(MigrationContext.configure(connection)):
            migration.upgrade()
    monkeypatch.setenv("EMAIL_FREE_ACCOUNT_DELETION", "true")
    monkeypatch.setattr(email, "is_email_configured", lambda: False)
    with factory() as db:
        db.get(User, 1).password = users.hash_password("fixture-password-123")
        db.commit()
    return setup


def password(client, **body):
    return client.post(
        "/account/deletion/reauth/password",
        json={"password": "fixture-password-123", **body},
    )


def test_email_free_signup_login_and_honest_recovery(owned, monkeypatch):
    client, factory, delivered, *_ = owned
    from routers import auth

    monkeypatch.setenv("EMAIL_FREE_AUTHENTICATION", "true")
    monkeypatch.setattr(auth, "track_user_signup", lambda *args, **kwargs: None)
    monkeypatch.setattr(auth, "track_user_login", lambda *args, **kwargs: None)

    def no_code(*args, **kwargs):
        raise AssertionError("email_free_signup_must_not_send_email")

    monkeypatch.setattr(auth, "issue_code", no_code)
    body = {
        "name": "Disposable fixture",
        "email": "new-owned@example.org",
        "password": "new-fixture-password",
    }
    created = client.post("/auth/signup", json=body)
    assert created.status_code == 200, created.text
    assert created.json()["verification_required"] is False
    uid = created.json()["user_id"]
    with factory() as db:
        assert db.get(User, uid).email_verified is False
    login = client.post("/auth/login", json={k: body[k] for k in ["email", "password"]})
    assert login.status_code == 200 and login.json()["user_id"] == uid
    assert delivered == []
    for address in ["new-owned@example.org", "unknown@example.org"]:
        response = client.post("/auth/password-reset/request", json={"email": address})
        assert response.status_code == 503
        assert (
            response.json()["detail"]
            == "secure_password_recovery_requires_delivery_service"
        )


def test_password_proof_deletes_owned_data_without_email_and_retry_is_idempotent(owned):
    client, factory, delivered, _, old = owned
    refresh = tokens.create_refresh_token(1)
    response = password(client)
    assert response.status_code == 200, response.text
    proof = response.json()
    assert delivered == [] and proof["expires_in_seconds"] == 300
    payload = {k: proof[k] for k in ["request_id", "proof"]}
    payload["confirmation"] = "DELETE"
    result = client.post("/account/deletion/reauth/confirm", json=payload)
    assert result.status_code == 200, result.text
    assert result.json() == {"state": "deleted", "account_revoked": True}
    assert (
        tokens.verify_access_token(old) is None
        and tokens.verify_refresh_token(refresh) is None
    )
    client.headers.pop("Authorization")
    assert (
        client.post("/account/deletion/reauth/confirm", json=payload).json()
        == result.json()
    )
    with factory() as db:
        assert db.get(User, 2).xp_total == 160
        assert db.query(UserLessonProgress).filter_by(user_id=2).one().xp_earned == 160


def test_wrong_password_missing_session_and_user_injection_denied(owned):
    client, *_ = owned
    assert password(client, password="wrong").status_code == 401
    assert password(client, user_id=2).status_code == 422
    client.headers.pop("Authorization")
    assert password(client).status_code == 401


def test_other_account_cannot_use_proof_or_password(owned):
    client, factory, *_ = owned
    body = password(client).json()
    body.pop("expires_in_seconds")
    body["confirmation"] = "DELETE"
    client.headers["Authorization"] = "Bearer " + tokens.create_access_token(2)
    assert client.post("/account/deletion/reauth/confirm", json=body).status_code == 403
    with factory() as db:
        assert db.get(User, 1).xp_total == 80


def test_explicit_consent_fresh_identity_and_expiry_required(owned):
    client, factory, *_ = owned
    body = password(client).json()
    body.pop("expires_in_seconds")
    body["confirmation"] = "no"
    assert client.post("/account/deletion/reauth/confirm", json=body).status_code == 400
    body["confirmation"] = "DELETE"
    with factory() as db:
        db.get(User, 1).password = users.hash_password("changed-password-123")
        db.commit()
    assert client.post("/account/deletion/reauth/confirm", json=body).status_code == 401
    with factory() as db:
        row = db.query(DeletionReauth).filter_by(challenge_id=body["request_id"]).one()
        row.expires_at = utcnow() - timedelta(seconds=1)
        db.commit()
    assert client.post("/account/deletion/reauth/confirm", json=body).status_code == 400


def test_session_expiry_does_not_authorize_unconsumed_mobile_proof(owned):
    client, *_ = owned
    body = password(client).json()
    body.pop("expires_in_seconds")
    body["confirmation"] = "DELETE"
    client.headers["Authorization"] = "Bearer expired-or-invalid"
    assert client.post("/account/deletion/reauth/confirm", json=body).status_code == 401


def test_web_password_flow_and_manual_claim_cannot_delete(owned):
    client, factory, delivered, *_ = owned
    client.headers.pop("Authorization")
    manual = client.post(
        "/account/deletion/manual-request",
        json={
            "account_email": "learner1@example.org",
            "contact_email": "other@example.org",
            "reason": "Cannot access my original account.",
        },
    )
    assert manual.status_code == 200
    assert manual.json()["account_deleted"] is False
    with factory() as db:
        row = db.get(ManualDeletionRequest, manual.json()["request_id"])
        assert (
            "example.org" not in row.encrypted_details
            and db.get(User, 1).xp_total == 80
        )
    response = client.post(
        "/account/deletion/web/password",
        json={"email": "learner1@example.org", "password": "fixture-password-123"},
    )
    assert response.status_code == 200, response.text
    body = response.json()
    body.pop("expires_in_seconds")
    body["confirmation"] = "DELETE"
    assert (
        client.post("/account/deletion/reauth/confirm", json=body).json()["state"]
        == "deleted"
    )
    assert delivered == []
    with factory() as db:
        assert db.query(ManualDeletionRequest).count() == 0


def test_reauth_binding_expiry_does_not_break_existing_cleanup_worker(owned):
    client, factory, *_ = owned
    response = password(client)
    with factory() as db:
        row = (
            db.query(DeletionReauth)
            .filter_by(challenge_id=response.json()["request_id"])
            .one()
        )
        challenge = db.get(DeletionChallenge, row.challenge_id)
        row.expires_at = challenge.expires_at = utcnow() - timedelta(days=2)
        db.commit()
        from services.account_deletion_worker import process_pending

        assert process_pending(db) == {"processed": 0, "completed": 0}
        assert db.query(DeletionReauth).count() == 0
        assert db.query(DeletionChallenge).count() == 0
        assert db.get(User, 1).xp_total == 80


@pytest.mark.parametrize(
    "subject,expected", [("wrong-provider-sub", 403), ("owned-provider-sub", 200)]
)
def test_google_subject_pkce_state_one_use_and_no_login_grants(
    owned, monkeypatch, subject, expected
):
    client, factory, *_ = owned
    from services import google_oauth

    monkeypatch.setattr(
        google_oauth, "GOOGLE_CLIENT_ID", "fixture.apps.googleusercontent.com"
    )
    monkeypatch.setattr(google_oauth, "GOOGLE_CLIENT_SECRET", "synthetic-only")
    monkeypatch.setenv(
        "MOBILE_OAUTH_REDIRECT_URI",
        "https://staging.example.test/auth/google-callback-mobile",
    )
    with factory() as db:
        user = db.get(User, 1)
        user.oauth_provider = "google"
        user.oauth_provider_id = "owned-provider-sub"
        user.password = None
        db.commit()
    verifier = "v" * 64
    response = client.post(
        "/account/deletion/reauth/google",
        json={"code_challenge": pkce_challenge(verifier)},
    )
    assert response.status_code == 200, response.text
    state = response.json()["state"]
    assert (
        "max_age=0" in response.json()["auth_url"]
        and "nonce=" in response.json()["auth_url"]
    )
    monkeypatch.setattr(service, "verify_google_identity", lambda *args: subject)
    import asyncio

    with factory() as db:
        if expected == 403:
            from fastapi import HTTPException

            with pytest.raises(HTTPException) as error:
                asyncio.run(service.google_callback(db, state, "fixture-code"))
            assert error.value.status_code == 403
            return
        code, surface = asyncio.run(service.google_callback(db, state, "fixture-code"))
        assert surface == "mobile"
    assert (
        client.post(
            "/auth/mobile/exchange", json={"code": code, "code_verifier": verifier}
        ).status_code
        == 400
    )
    assert (
        client.post(
            "/account/deletion/reauth/exchange",
            json={"code": code, "code_verifier": "x" * 64},
        ).status_code
        == 400
    )
    exchanged = client.post(
        "/account/deletion/reauth/exchange",
        json={"code": code, "code_verifier": verifier},
    )
    assert exchanged.status_code == 200, exchanged.text
    assert (
        client.post(
            "/account/deletion/reauth/exchange",
            json={"code": code, "code_verifier": verifier},
        ).status_code
        == 400
    )
    with factory() as db:
        assert db.query(User).count() == 2
        assert db.query(DeletionChallenge).count() == 1
