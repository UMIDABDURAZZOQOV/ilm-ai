"""Synthetic accounts and owned disposable DB/files only. No real email or users."""

from datetime import timedelta
import importlib.util
import json
import os
from pathlib import Path
import secrets
from urllib.parse import urlsplit

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from alembic.operations import Operations
from alembic.migration import MigrationContext
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker

from services import db as database, tokens, users, mobile_oauth, email
from services.models import (
    User,
    SkillSubject,
    SkillUnit,
    SkillLesson,
    UserLessonProgress,
    StudySession,
    AssistantMessage,
    EmailVerificationCode,
    SkillClass,
    SkillClassMember,
    SkillClassAssignment,
    ParentChildLink,
    CheckoutSession,
)
from services.account_models import DeletionChallenge, DeletionJob
from services.account_ownership import USER_FILES, DELETED_PROVIDER, DIRECT_OWNERS
from services.study import utcnow

spec = importlib.util.spec_from_file_location(
    "account_migration",
    Path(__file__).resolve().parents[1] / "alembic/versions/0016_account_deletion.py",
)
migration = importlib.util.module_from_spec(spec)
spec.loader.exec_module(migration)


@pytest.fixture(params=["sqlite", "postgresql"])
def setup(tmp_path, monkeypatch, request):
    from services.assessment_models import AssessmentBase
    from services.chemistry_models import ChemistryBase
    from services.world_history_models import WorldHistoryBase
    from services.uzbekistan_history_models import HistoryBase

    admin = schema = None
    if request.param == "postgresql":
        filename = os.getenv("ILM_TEST_POSTGRES_URL_FILE")
        if not filename:
            pytest.skip("Explicit loopback PostgreSQL test URL file required")
        from services.database_url import normalize_database_url

        url = Path(filename).read_text().strip()
        parsed = urlsplit(url)
        assert (
            parsed.scheme == "postgresql"
            and parsed.hostname in {"127.0.0.1", "localhost"}
            and "staging" in parsed.path
        )
        assert os.getenv("ENVIRONMENT") != "production"
        admin = create_engine(normalize_database_url(url))
        schema = "ilm_deletion_" + secrets.token_hex(8)
        with admin.begin() as connection:
            connection.execute(text(f'CREATE SCHEMA "{schema}"'))
        engine = create_engine(
            normalize_database_url(url),
            connect_args={"options": f"-csearch_path={schema}"},
        )
    else:
        engine = create_engine(
            "sqlite:///" + (tmp_path / "owned.db").as_posix(),
            connect_args={"check_same_thread": False, "timeout": 10},
        )

        @event.listens_for(engine, "connect")
        def foreign_keys(connection, _):
            connection.execute("PRAGMA foreign_keys=ON")

    for metadata in [
        database.Base.metadata,
        AssessmentBase.metadata,
        ChemistryBase.metadata,
        WorldHistoryBase.metadata,
        HistoryBase.metadata,
    ]:
        metadata.create_all(engine)
    with engine.begin() as connection:
        with Operations.context(MigrationContext.configure(connection)):
            migration.upgrade()
    factory = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
    for module in (database, tokens, users, mobile_oauth):
        monkeypatch.setattr(module, "SessionLocal", factory)
    monkeypatch.setattr(
        tokens, "JWT_SECRET", "synthetic-token-signing-secret-for-owned-tests"
    )
    monkeypatch.setattr(tokens, "USE_DB", True)
    monkeypatch.setattr(users, "USE_DB", True)
    root = tmp_path / "files"
    root.mkdir()
    for key, value in {
        "ENVIRONMENT": "test",
        "AUTH_STORAGE": "database",
        "ACCOUNT_DELETION_ENABLED": "true",
        "ACCOUNT_DELETION_POLICY_REFERENCE": "synthetic fixture only",
        "ACCOUNT_DELETION_SECRET": "synthetic-deletion-secret-for-owned-tests-only",
        "ACCOUNT_DELETION_STORAGE_ROOT": str(root),
    }.items():
        monkeypatch.setenv(key, value)
    delivered = []
    monkeypatch.setattr(email, "is_email_configured", lambda: True)
    monkeypatch.setattr(
        email,
        "send_verification_code",
        lambda address, code, purpose: (
            delivered.append((address, code, purpose)) or True
        ),
    )
    with factory() as db:
        db.add_all(
            [
                User(
                    id=i,
                    name=f"Synthetic {i}",
                    age=12,
                    email=f"learner{i}@example.org",
                    email_verified=True,
                    xp_total=80 * i,
                    password="synthetic-old-hash",
                )
                for i in (1, 2)
            ]
        )
        db.flush()
        db.add(
            SkillSubject(
                id=1,
                slug="fixture",
                name_uz="Fixture",
                name_ru="Fixture",
                name_en="Fixture",
            )
        )
        db.flush()
        db.add(
            SkillUnit(
                id=1,
                order_index=1,
                subject_id=1,
                slug="fixture",
                title_uz="Fixture",
                title_ru="Fixture",
                title_en="Fixture",
            )
        )
        db.flush()
        db.add(
            SkillLesson(
                id=1,
                order_index=1,
                unit_id=1,
                slug="fixture",
                title_uz="Fixture",
                title_ru="Fixture",
                title_en="Fixture",
            )
        )
        db.flush()
        for uid in (1, 2):
            db.add(
                UserLessonProgress(
                    user_id=uid, lesson_id=1, stars=2, xp_earned=80 * uid
                )
            )
            db.add(
                StudySession(
                    id=f"session-{uid}",
                    user_id=uid,
                    kind="fixture",
                    scope="fixture",
                    questions={},
                    started_at=utcnow(),
                )
            )
            db.add(
                AssistantMessage(
                    user_id=uid, role="user", content=f"private fixture {uid}"
                )
            )
        db.add(
            EmailVerificationCode(
                email="learner1@example.org",
                code="000000",
                purpose="signup",
                expires_at=utcnow() + timedelta(minutes=5),
            )
        )
        db.add(SkillClass(id=1, teacher_id=1, name="Owned class", join_code="TEST42"))
        db.flush()
        db.add(SkillClassMember(class_id=1, student_id=2))
        db.add(SkillClassAssignment(class_id=1, title="Fixture assignment"))
        db.add(ParentChildLink(parent_id=1, child_id=2))
        db.commit()
        if engine.dialect.name == "postgresql":
            db.execute(
                text(
                    "SELECT setval(pg_get_serial_sequence('users','id'), (SELECT max(id) FROM users))"
                )
            )
            db.commit()
    for directory in USER_FILES:
        folder = root / directory
        folder.mkdir(parents=True, exist_ok=True)
        for uid in (1, 2):
            (folder / f"user_{uid}.json").write_text(json.dumps({"fixture_owner": uid}))
    feedback = root / "data/feedback/feedback.jsonl"
    feedback.parent.mkdir(parents=True)
    feedback.write_text(
        "".join(
            json.dumps(
                {
                    "email": f"learner{i}@example.org",
                    "submitted_at": (utcnow() - timedelta(seconds=2)).isoformat(),
                }
            )
            + "\n"
            for i in (1, 2)
        ),
        encoding="utf8",
    )
    (root / "users.json").write_text(json.dumps([{"id": 1}, {"id": 2}]))
    app = FastAPI()
    from routers.account_deletion import install
    from routers.auth import router as auth

    install(app)
    app.include_router(auth)

    def dependency():
        with factory() as db:
            yield db

    app.dependency_overrides[database.get_db] = dependency
    with TestClient(app) as client:
        token = tokens.create_access_token(1)
        client.headers["Authorization"] = "Bearer " + token
        yield client, factory, delivered, root, token
    engine.dispose()
    if admin is not None:
        with admin.begin() as connection:
            connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        admin.dispose()


def challenge(setup):
    client, _, delivered, _, _ = setup
    response = client.post("/account/deletion/me/request")
    assert response.status_code == 200, response.text
    assert delivered[-1][2] == "account_deletion"
    return {
        "request_id": response.json()["request_id"],
        "code": delivered[-1][1],
        "confirmation": "DELETE",
    }


@pytest.mark.parametrize("provider", ["password", "google"])
def test_verified_delete_revokes_all_sessions_keeps_other_users_and_is_idempotent(
    setup, provider
):
    client, factory, _, root, old_access = setup
    with factory() as db:
        user = db.get(User, 1)
        if provider == "google":
            user.oauth_provider = "google"
            user.oauth_provider_id = "verified-synthetic-sub"
            user.password = None
        db.commit()
    refresh = tokens.create_refresh_token(1)
    body = challenge(setup)
    response = client.post("/account/deletion/confirm", json=body)
    assert response.status_code == 200, response.text
    assert response.json() == {"state": "deleted", "account_revoked": True}
    assert client.post("/account/deletion/confirm", json=body).json() == response.json()
    assert tokens.verify_access_token(old_access) is None
    assert tokens.verify_refresh_token(refresh) is None
    assert tokens.rotate_refresh_token(refresh) is None
    assert users.find_user_by_id(1) is None
    assert client.get("/auth/profile/1").status_code == 401
    with factory() as db:
        old = db.get(User, 1)
        other = db.get(User, 2)
        assert old.oauth_provider == DELETED_PROVIDER and old.oauth_provider_id is None
        assert old.name == "Deleted account" and old.email != "learner1@example.org"
        assert old.password is None and old.xp_total == 0 and old.age is None
        assert other.xp_total == 160 and other.email == "learner2@example.org"
        assert db.query(UserLessonProgress).filter_by(user_id=1).count() == 0
        assert db.query(UserLessonProgress).filter_by(user_id=2).one().xp_earned == 160
        assert db.query(StudySession).filter_by(user_id=1).count() == 0
        assert db.query(AssistantMessage).filter_by(user_id=1).count() == 0
        assert db.query(AssistantMessage).filter_by(user_id=2).count() == 1
        assert db.query(SkillLesson).count() == 1
        assert db.query(SkillClass).count() == 0
        assert (
            db.query(EmailVerificationCode)
            .filter_by(email="learner1@example.org")
            .count()
            == 0
        )
        assert db.query(DeletionJob).one().email_hash is None
    for directory in USER_FILES:
        assert not (root / directory / "user_1.json").exists()
        assert (root / directory / "user_2.json").exists()
    assert json.loads((root / "users.json").read_text()) == [{"id": 2}]
    assert (
        "learner1@example.org"
        not in (root / "data/feedback/feedback.jsonl").read_text()
    )


def test_code_reauthentication_and_explicit_confirmation_are_required(setup):
    client, factory, _, _, _ = setup
    body = challenge(setup)
    assert (
        client.post(
            "/account/deletion/confirm", json={**body, "confirmation": "NO"}
        ).status_code
        == 400
    )
    for _ in range(5):
        assert (
            client.post(
                "/account/deletion/confirm", json={**body, "code": "invalid"}
            ).status_code
            == 422
        )
    # Invalid shape never verifies. Five well-formed wrong codes consume the limit.
    wrong = "111111" if body["code"] != "111111" else "222222"
    for _ in range(5):
        assert (
            client.post(
                "/account/deletion/confirm", json={**body, "code": wrong}
            ).status_code
            == 400
        )
    assert client.post("/account/deletion/confirm", json=body).status_code == 400
    with factory() as db:
        assert db.get(User, 1).xp_total == 80
        assert db.query(DeletionJob).count() == 0


def test_public_web_flow_needs_no_app_token_and_does_not_reveal_account_identity(setup):
    client, _, delivered, _, _ = setup
    client.headers.clear()
    page = client.get("/account-deletion")
    assert page.status_code == 200 and "ILM AI" in page.text
    assert "frame-ancestors" in page.headers["content-security-policy"]
    assert client.post("/account/deletion/me/request").status_code == 401
    response = client.post(
        "/account/deletion/request", json={"email": "learner1@example.org"}
    )
    assert response.status_code == 200
    assert not {"user_id", "email", "code", "account_exists"} & response.json().keys()
    body = {
        "request_id": response.json()["request_id"],
        "code": delivered[-1][1],
        "confirmation": "DELETE",
    }
    assert (
        client.post("/account/deletion/confirm", json=body).json()["state"] == "deleted"
    )


def test_file_failure_is_pending_not_success_and_can_retry_after_network_loss(
    setup, monkeypatch
):
    from services import account_file_cleanup

    client, factory, _, root, token = setup
    body = challenge(setup)
    original = account_file_cleanup.purge_account_files
    monkeypatch.setattr(
        account_file_cleanup,
        "purge_account_files",
        lambda *args: (_ for _ in ()).throw(OSError("synthetic locked file")),
    )
    result = client.post("/account/deletion/confirm", json=body).json()
    assert result == {"state": "pending_cleanup", "account_revoked": True}
    assert tokens.verify_access_token(token) is None
    assert (root / "vectors/user_1.json").exists()
    monkeypatch.setattr(account_file_cleanup, "purge_account_files", original)
    client.headers.clear()  # Lost response/expired login can retry with the same OTP proof.
    assert (
        client.post("/account/deletion/confirm", json=body).json()["state"] == "deleted"
    )
    with factory() as db:
        assert db.query(DeletionJob).one().state == "complete"


def test_deleted_id_cannot_be_resurrected_or_receive_late_writes(setup):
    from sqlalchemy.exc import IntegrityError

    client, factory, _, _, token = setup
    assert (
        client.post("/account/deletion/confirm", json=challenge(setup)).json()["state"]
        == "deleted"
    )
    with factory() as db:
        db.add(AssistantMessage(user_id=1, role="user", content="late request"))
        with pytest.raises(IntegrityError, match="account_deleted"):
            db.commit()
    with factory() as db:
        user = db.get(User, 1)
        user.name = "stale profile restore"
        with pytest.raises(IntegrityError, match="account_deleted"):
            db.commit()
    new = users.create_user_with_oauth(
        "New account", "learner1@example.org", provider_id="synthetic-fresh-sub"
    )
    assert new["id"] > 2 and new["xp_total"] == 0
    assert tokens.verify_access_token(token) is None


def test_paid_record_requires_real_retention_review_and_is_not_falsely_deleted(setup):
    client, factory, _, _, token = setup
    with factory() as db:
        db.add(
            CheckoutSession(
                session_id="real-financial-fixture", user_id=1, data={"fixture": True}
            )
        )
        db.commit()
    result = client.post("/account/deletion/confirm", json=challenge(setup)).json()
    assert result == {"state": "retention_review", "account_revoked": False}
    assert tokens.verify_access_token(token) == 1
    with factory() as db:
        assert db.query(DeletionJob).one().state == "retention_review"
        assert db.query(CheckoutSession).count() == 1


def test_pinned_ownership_inventory_and_migration_are_consistent():
    assert migration.OWNERS == DIRECT_OWNERS


def test_migration_rejects_unknown_ownership_before_any_new_table():
    from sqlalchemy import inspect

    engine = create_engine("sqlite:///:memory:")
    with engine.begin() as connection:
        connection.exec_driver_sql(
            "CREATE TABLE users (id INTEGER PRIMARY KEY, oauth_provider VARCHAR(50))"
        )
        connection.exec_driver_sql(
            "CREATE TABLE assistant_messages (id INTEGER PRIMARY KEY, unreviewed_owner INTEGER)"
        )
        before = set(inspect(connection).get_table_names())
        with Operations.context(MigrationContext.configure(connection)):
            with pytest.raises(
                RuntimeError, match="account_ownership_schema_requires_review"
            ):
                migration.upgrade()
        assert set(inspect(connection).get_table_names()) == before
    engine.dispose()


def test_expired_code_and_forged_owner_cannot_delete(setup):
    client, factory, _, _, _ = setup
    assert (
        client.post(
            "/account/deletion/request",
            json={"email": "learner2@example.org", "user_id": 1},
        ).status_code
        == 422
    )
    body = challenge(setup)
    with factory() as db:
        db.get(DeletionChallenge, body["request_id"]).expires_at = utcnow() - timedelta(
            seconds=1
        )
        db.commit()
    assert client.post("/account/deletion/confirm", json=body).status_code == 400
    with factory() as db:
        assert db.get(User, 1).xp_total == 80 and db.get(User, 2).xp_total == 160


def test_unknown_email_and_cooldown_do_not_expose_identity(setup):
    client, _, delivered, _, _ = setup
    response = client.post(
        "/account/deletion/request", json={"email": "unknown@example.org"}
    )
    assert response.status_code == 200 and delivered == []
    assert set(response.json()) == {"request_id", "message", "expires_in_seconds"}
    assert (
        client.post(
            "/account/deletion/request", json={"email": "unknown@example.org"}
        ).status_code
        == 429
    )


def test_delivery_failure_never_deletes_or_reveals_error(setup, monkeypatch):
    client, factory, _, _, _ = setup
    monkeypatch.setattr(email, "send_verification_code", lambda *a, **k: False)
    response = client.post("/account/deletion/me/request")
    assert response.status_code == 503 and "delivery_failed" in response.text
    with factory() as db:
        assert db.query(DeletionJob).count() == 0
        assert db.get(User, 1).email == "learner1@example.org"
        assert db.query(DeletionChallenge).one().consumed


def test_failed_transaction_keeps_profile_progress_and_tokens(setup, monkeypatch):
    from services import account_deletion

    client, factory, _, _, token = setup
    body = challenge(setup)
    original = account_deletion._scrub_user

    def fail(user):
        original(user)
        raise RuntimeError("synthetic transaction failure")

    monkeypatch.setattr(account_deletion, "_scrub_user", fail)
    with pytest.raises(RuntimeError, match="synthetic transaction failure"):
        client.post("/account/deletion/confirm", json=body)
    with factory() as db:
        assert db.get(User, 1).xp_total == 80
        assert db.query(UserLessonProgress).filter_by(user_id=1).count() == 1
        assert db.query(DeletionJob).count() == 0
    assert tokens.verify_access_token(token) == 1


def test_missing_write_barrier_fails_before_deleting(setup):
    client, factory, _, _, _ = setup
    with factory() as db:
        if db.get_bind().dialect.name == "sqlite":
            db.execute(
                text(
                    "DROP TRIGGER account_guard_skilltree_class_assignments_class_id_update"
                )
            )
        else:
            db.execute(
                text(
                    "DROP TRIGGER account_guard_skilltree_class_assignments_class_id ON skilltree_class_assignments"
                )
            )
        db.commit()
    assert client.post("/account/deletion/me/request").status_code == 503
    with factory() as db:
        assert db.get(User, 1).xp_total == 80


def test_pending_cleanup_worker_does_not_start_new_deletions(setup, monkeypatch):
    from services import account_file_cleanup
    from services.account_deletion_worker import process_pending

    client, factory, _, _, _ = setup
    body = challenge(setup)
    original = account_file_cleanup.purge_account_files
    monkeypatch.setattr(
        account_file_cleanup,
        "purge_account_files",
        lambda *a: (_ for _ in ()).throw(OSError()),
    )
    assert (
        client.post("/account/deletion/confirm", json=body).json()["state"]
        == "pending_cleanup"
    )
    monkeypatch.setattr(account_file_cleanup, "purge_account_files", original)
    with factory() as db:
        assert process_pending(db) == {"processed": 1, "completed": 1}
        assert db.get(User, 2).xp_total == 160


def test_unsafe_file_layout_stays_pending_without_erasing_other_accounts(setup):
    client, factory, _, root, _ = setup
    # An unknown legacy layout must never be interpreted as an empty user list.
    (root / "users.json").write_text('{"unexpected": true}', encoding="utf8")
    result = client.post("/account/deletion/confirm", json=challenge(setup)).json()
    assert result == {"state": "pending_cleanup", "account_revoked": True}
    assert json.loads((root / "users.json").read_text()) == {"unexpected": True}
    assert (root / "vectors/user_2.json").exists()
    with factory() as db:
        assert db.get(User, 2).xp_total == 160


def test_repeated_financial_review_request_is_idempotent(setup):
    client, factory, _, _, _ = setup
    with factory() as db:
        db.get(User, 1).subscription_tier = "paid"
        db.commit()
    body = challenge(setup)
    assert (
        client.post("/account/deletion/confirm", json=body).json()["state"]
        == "retention_review"
    )
    with factory() as db:
        db.get(DeletionChallenge, body["request_id"]).created_at = utcnow() - timedelta(
            minutes=2
        )
        db.commit()
    assert client.post("/account/deletion/confirm", json=challenge(setup)).json() == {
        "state": "retention_review",
        "account_revoked": False,
    }
    with factory() as db:
        assert db.query(DeletionJob).count() == 1


def test_database_flag_cannot_promote_a_cached_file_auth_runtime(setup, monkeypatch):
    client, factory, _, _, _ = setup
    monkeypatch.setattr(users, "USE_DB", False)
    response = client.get("/account/deletion/config")
    assert response.status_code == 200 and response.json()["available"] is False
    with factory() as db:
        from services.account_deletion import require_ready
        from fastapi import HTTPException

        with pytest.raises(HTTPException) as failure:
            require_ready(db)
        assert failure.value.status_code == 503
        assert db.get(User, 1).xp_total == 80
