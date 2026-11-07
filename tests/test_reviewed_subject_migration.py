"""Pinned migration tests use in-memory databases, no application DB imports."""

import importlib.util
from pathlib import Path

from alembic.migration import MigrationContext
from alembic.operations import Operations
import pytest
import sqlalchemy as sa

spec = importlib.util.spec_from_file_location(
    "reviewed_subject_migration",
    Path(__file__).resolve().parents[1]
    / "alembic/versions/0015_reviewed_subject_schemas.py",
)
migration = importlib.util.module_from_spec(spec)
spec.loader.exec_module(migration)


@pytest.fixture
def db():
    engine = sa.create_engine("sqlite:///:memory:")
    with engine.begin() as connection:
        connection.exec_driver_sql("PRAGMA foreign_keys=ON")
        connection.exec_driver_sql(
            "CREATE TABLE users (id INTEGER PRIMARY KEY, xp INTEGER)"
        )
        connection.exec_driver_sql(
            "CREATE TABLE study_sessions (id VARCHAR(96) PRIMARY KEY)"
        )
        connection.exec_driver_sql("INSERT INTO users VALUES (41,250),(42,80)")
        connection.exec_driver_sql("INSERT INTO study_sessions VALUES ('old-session')")
        with Operations.context(MigrationContext.configure(connection)):
            yield connection
    engine.dispose()


def test_additive_idempotent_schema_preserves_users_and_existing_sessions(db):
    before = db.exec_driver_sql("SELECT * FROM users").all()
    migration.upgrade()
    migration.upgrade()
    assert db.exec_driver_sql("SELECT * FROM users").all() == before
    assert db.exec_driver_sql("SELECT * FROM study_sessions").all() == [
        ("old-session",)
    ]
    for table in migration.definitions():
        migration.validate_existing(sa.inspect(db), table)
    assert len(sa.inspect(db).get_table_names()) == 14
    with pytest.raises(RuntimeError, match="rollback_application_only"):
        migration.downgrade()


def test_schema_conflict_is_rejected_before_any_partial_create(db):
    db.exec_driver_sql(
        "CREATE TABLE world_history_preview_lessons (key INTEGER PRIMARY KEY)"
    )
    before = set(sa.inspect(db).get_table_names())
    with pytest.raises(RuntimeError, match="require_review"):
        migration.upgrade()
    assert set(sa.inspect(db).get_table_names()) == before


def test_foreign_keys_prevent_unowned_progress(db):
    migration.upgrade()
    with pytest.raises(sa.exc.IntegrityError):
        db.execute(
            sa.text(
                "INSERT INTO chemistry_preview_progress "
                "(user_id,lesson_key,best_score_pct,attempts,xp_earned) "
                "VALUES (999,'missing',0,0,0)"
            )
        )
