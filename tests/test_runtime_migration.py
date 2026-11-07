"""Full migration chain in a fresh, disposable loopback PostgreSQL schema."""

import importlib.util
import json
import os
from pathlib import Path
import secrets
import sys
from urllib.parse import urlsplit
import pytest
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
from services.database_url import normalize_database_url


@pytest.fixture
def fresh_postgres():
    filename = os.getenv("ILM_TEST_POSTGRES_URL_FILE")
    if not filename:
        pytest.skip("Explicit loopback staging URL file required")
    value = Path(filename).read_text().strip()
    uri = urlsplit(value)
    assert (
        uri.scheme == "postgresql"
        and uri.hostname in {"127.0.0.1", "localhost"}
        and "staging" in uri.path
    )
    assert os.getenv("ENVIRONMENT") != "production"
    admin = create_engine(normalize_database_url(value))
    schema = "ilm_migration_" + secrets.token_hex(8)
    try:
        with admin.begin() as db:
            db.execute(text(f'CREATE SCHEMA "{schema}"'))
    except SQLAlchemyError:
        admin.dispose()
        # Driver traceback locals can contain the private DSN/password. Report
        # a fixed error without driver frames when the owned test server is off.
        pytest.fail("Owned loopback PostgreSQL test server unavailable", pytrace=False)
    engine = create_engine(
        normalize_database_url(value),
        connect_args={"options": f"-csearch_path={schema}"},
    )
    try:
        yield engine
    finally:
        engine.dispose()
        with admin.begin() as db:
            db.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        admin.dispose()


def test_owned_connection_failure_does_not_expose_private_driver_state(tmp_path, monkeypatch):
    filename = tmp_path / "postgres-url.private"
    filename.write_text(
        "postgresql://test:PRIVATE-TEST-PASSWORD@127.0.0.1:55461/owned_staging",
        encoding="utf8",
    )
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("ILM_TEST_POSTGRES_URL_FILE", str(filename))
    disposed = []

    class UnavailableEngine:
        def begin(self):
            raise SQLAlchemyError("PRIVATE-DRIVER-STATE")

        def dispose(self):
            disposed.append(True)

    monkeypatch.setattr(sys.modules[__name__], "create_engine", lambda *a, **k: UnavailableEngine())
    with pytest.raises(pytest.fail.Exception) as error:
        next(fresh_postgres.__wrapped__())
    assert str(error.value) == "Owned loopback PostgreSQL test server unavailable"
    assert error.value.pytrace is False
    assert disposed == [True]


def test_full_chain_supports_current_runtime_without_create_all(fresh_postgres):
    from services.models import Base
    from services.reviewed_mobile_release import expected_rows
    from services.account_models import AccountBase

    directory = Path(__file__).resolve().parents[1] / "alembic/versions"
    with fresh_postgres.begin() as connection:
        from alembic import command
        from alembic.config import Config

        configuration = Config(str(directory.parents[1] / "alembic.ini"))
        configuration.set_main_option("script_location", str(directory.parent))
        configuration.attributes["connection"] = connection
        command.upgrade(configuration, "head")
        inspector = inspect(connection)
        metadata = [
            Base.metadata,
            AccountBase.metadata,
            *[spec[0].metadata for spec in expected_rows()[0].values()],
        ]
        for item in metadata:
            for table in item.tables.values():
                assert inspector.has_table(table.name), table.name
                assert set(table.c.keys()) <= {
                    c["name"] for c in inspector.get_columns(table.name)
                }, table.name
        assert (
            connection.exec_driver_sql("SELECT count(*) FROM users").scalar_one() == 0
        )
        # Last additive migration is safe to rehearse twice without deleting rows.
        with Operations.context(MigrationContext.configure(connection)):
            path = directory / "0017_runtime_foundation.py"
            spec = importlib.util.spec_from_file_location(
                "last_additive_revision", path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.upgrade()
    from sqlalchemy.orm import Session
    from services.models import User
    from services.reviewed_publication_import import import_reviewed_publication

    with Session(fresh_postgres) as db, db.begin():
        db.add(
            User(
                name="Synthetic preserved learner",
                email="owned-staging@example.test",
                xp_total=137,
            )
        )
        db.flush()
        uid = db.query(User.id).scalar()
        result = import_reviewed_publication(db)
        assert result["biology_lessons_inserted"] == 406
        assert result["reviewed_rows_inserted"] > 1000
    with Session(fresh_postgres) as db, db.begin():
        assert import_reviewed_publication(db) == {
            "biology_lessons_inserted": 0,
            "reviewed_rows_inserted": 0,
            "progress_rows_modified": 0,
        }
        assert db.get(User, uid).xp_total == 137
    # Complete publication gate must accept the imported exact content set.
    from services.reviewed_mobile_release import publication_db

    patch = pytest.MonkeyPatch()
    patch.setenv("MOBILE_REVIEWED_RELEASE", "true")
    patch.setenv(
        "MOBILE_PUBLICATION_REVIEW_REFERENCE",
        "automated technical rehearsal, not expert signoff",
    )
    try:
        with Session(fresh_postgres) as db:
            gate = publication_db(db)
            assert next(gate) is db
            gate.close()
    finally:
        patch.undo()
    assert_production_entrypoint_contract(fresh_postgres, uid)


def assert_production_entrypoint_contract(engine, uid):
    """Real local main:app over the migrated PG schema, with no lifespan/provider.

    This is production-entrypoint API acceptance, not a hosted OAuth test. Only
    public GETs and deliberately unauthenticated requests are sent. No production
    data, mail, Telegram, scheduler or external authentication is used.
    """
    import importlib
    from fastapi.testclient import TestClient
    from sqlalchemy.orm import Session, sessionmaker
    from services import db as storage, scheduler
    from services.models import User

    patch = pytest.MonkeyPatch()
    previous = sys.modules.pop("main", None)
    revision = "a" * 40  # Synthetic identity, never presented as a deployed SHA.
    env = dict(
        ENVIRONMENT="production",
        DEPLOYMENT_STAGE="",
        PYTHON_DOTENV_DISABLED="1",
        SECRET_KEY=secrets.token_urlsafe(48),
        JWT_SECRET=secrets.token_urlsafe(48),
        AUTH_STORAGE="database",
        ALLOWED_ORIGINS="https://owned-staging.example.test",
        MOBILE_REVIEWED_RELEASE="true",
        MOBILE_PUBLICATION_REVIEW_REFERENCE="synthetic technical entrypoint test",
        MOBILE_OAUTH_REDIRECT_URI="https://owned-staging.example.test/auth/google-callback-mobile",
        MOBILE_RELEASE_APP_SCHEME="ilmai",
        ACCOUNT_DELETION_ENABLED="false",
        RENDER_GIT_COMMIT=revision,
        GOOGLE_CLIENT_ID="",
        GOOGLE_CLIENT_SECRET="",
        TELEGRAM_BOT_TOKEN="",
        SENTRY_DSN="",
        GEMINI_API_KEY="",
        GEMINI_API_KEYS="",
        OPENAI_API_KEY="",
        NVIDIA_API_KEY="",
        NVIDIA_API_KEYS="",
    )
    for key, value in env.items():
        patch.setenv(key, value)
    patch.setattr(storage, "engine", engine)
    patch.setattr(storage, "SessionLocal", sessionmaker(bind=engine))
    patch.setattr(storage, "IS_PRODUCTION", True)

    def forbidden_startup():
        raise AssertionError("No scheduler or lifecycle should run in this test")

    patch.setattr(scheduler, "start_scheduler", forbidden_startup)
    try:
        module = importlib.import_module("main")
        # Not entering TestClient's context deliberately avoids application
        # lifespan, notification/webhook work and any configured external service.
        client = TestClient(module.app, base_url="https://owned-staging.example.test")
        try:
            specification = client.get("/openapi.json").json()
            actual = {
                method.upper() + " " + path
                for path, operations in specification["paths"].items()
                for method in operations
                if method in {"get", "post", "head", "put", "patch", "delete", "options"}
            }
            fixture = json.loads(
                (Path(__file__).parent / "fixtures/production_legacy_routes_20261107.json")
                .read_text(encoding="utf8")
            )
            assert set(fixture["method_paths"]) <= actual
            health = client.get("/health")
            assert health.status_code == 200
            assert health.json() == dict(status="ok", revision=revision, mobile_contract_version=2)
            auth = client.get("/auth/mobile/config")
            assert auth.status_code == 200
            assert auth.json()["mobile_auth_version"] == 2
            assert auth.json()["google_configured"] is False
            assert client.get("/mobile/skills/config").json()["mobile_curriculum_version"] == 2
            subjects = {"biologiya", "fizika", "kimyo", "jahon_tarixi", "ozbekiston_tarixi"}
            for grade in range(5, 12):
                response = client.get("/mobile/skills/subjects", params={"grade": grade})
                assert response.status_code == 200
                rows = response.json()
                assert subjects <= {row["slug"] for row in rows}
                if grade == 5:
                    assert [row["slug"] for row in rows if row["available"]] == ["biologiya"]
            for subject in sorted(subjects):
                response = client.get(f"/mobile/skills/subjects/{subject}/grades")
                assert response.status_code == 200 and response.json()["grades"]
            assert client.get(f"/mobile/skills/{uid}/tree", params={"subject": "biologiya", "grade": 7}).status_code == 401
            assert client.get("/account/deletion/config").json()["available"] is False
            assert not any("test-login" in path for path in specification["paths"])
            with Session(engine) as db:
                assert db.get(User, uid).xp_total == 137
        finally:
            client.close()
    finally:
        sys.modules.pop("main", None)
        if previous is not None:
            sys.modules["main"] = previous
        patch.undo()
