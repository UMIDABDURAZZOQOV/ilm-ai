"""Full migration chain in a fresh, disposable loopback PostgreSQL schema."""

import importlib.util
import os
from pathlib import Path
import secrets
from urllib.parse import urlsplit
import pytest
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import create_engine, inspect, text
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
    with admin.begin() as db:
        db.execute(text(f'CREATE SCHEMA "{schema}"'))
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
