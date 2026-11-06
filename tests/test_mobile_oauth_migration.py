"""Migration-only in-memory databases. No application/server/DB module imports."""

import importlib.util
from pathlib import Path

from alembic.migration import MigrationContext
from alembic.operations import Operations
import pytest
import sqlalchemy as sa


spec = importlib.util.spec_from_file_location(
    "mobile_migration",
    Path(__file__).resolve().parents[1] / "alembic/versions/0014_mobile_oauth_state.py",
)
migration = importlib.util.module_from_spec(spec)
spec.loader.exec_module(migration)


@pytest.fixture
def db():
    engine = sa.create_engine("sqlite:///:memory:")
    with engine.begin() as conn:
        conn.execute(sa.text("PRAGMA foreign_keys=ON"))
        conn.execute(
            sa.text("CREATE TABLE users (id INTEGER PRIMARY KEY, xp INTEGER NOT NULL)")
        )
        conn.execute(
            sa.text(
                "CREATE TABLE retained_progress (user_id INTEGER, lesson TEXT, done INTEGER)"
            )
        )
        conn.execute(sa.text("INSERT INTO users VALUES (41,250),(42,50)"))
        conn.execute(
            sa.text("INSERT INTO retained_progress VALUES (41,'stable-existing-key',1)")
        )
        with Operations.context(MigrationContext.configure(conn)):
            yield conn
    engine.dispose()


def snapshot(db):
    return [
        db.execute(sa.text("SELECT * FROM " + table)).all()
        for table in ("users", "retained_progress")
    ]


def test_additive_upgrade_and_repeat_preserve_existing_account_ids_xp_progress(db):
    before = snapshot(db)
    migration.upgrade()
    migration.upgrade()
    assert snapshot(db) == before
    names = sa.inspect(db).get_table_names()
    assert "oauth_states" in names and "mobile_login_grants" in names


def test_grant_ownership_and_defaults_are_enforced(db):
    migration.upgrade()
    sql = sa.text(
        "INSERT INTO mobile_login_grants (code_hash,challenge,user_id,expires_at) "
        "VALUES (:code,'reviewed-test-challenge',:uid,'2026-11-06 20:00:00')"
    )
    db.execute(sql, {"code": "test-code-hash-a", "uid": 41})
    assert db.execute(sa.text("SELECT consumed FROM mobile_login_grants")).scalar() == 0
    with pytest.raises(sa.exc.IntegrityError):
        db.execute(sql, {"code": "test-code-hash-b", "uid": 999})


def test_incompatible_existing_table_is_not_silently_replaced(db):
    db.execute(sa.text("CREATE TABLE mobile_login_grants (code_hash TEXT PRIMARY KEY)"))
    before = snapshot(db)
    with pytest.raises(RuntimeError, match="requires_review"):
        migration.upgrade()
    assert snapshot(db) == before
    assert "oauth_states" not in sa.inspect(db).get_table_names()


def test_rollback_does_not_destroy_active_grants_or_existing_progress(db):
    migration.upgrade()
    before = snapshot(db)
    with pytest.raises(RuntimeError, match="rollback_application_only"):
        migration.downgrade()
    assert snapshot(db) == before
    assert "mobile_login_grants" in sa.inspect(db).get_table_names()
