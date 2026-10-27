"""Opt-in loopback PostgreSQL staging; only our random disposable schema."""

import os
import secrets
from pathlib import Path

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from test_mathematics_preview import P, finish, make_preview
from test_mathematics_preview import (
    test_parallel_first_completions_award_only_once as check_parallel,
)

from services.database_url import normalize_database_url
from services.mathematics_curriculum import import_course, staging_url
from services.models import User


def test_math_postgres_immutable_import_all_five_and_parallel_reward(monkeypatch):
    filename = os.getenv("ILM_TEST_POSTGRES_URL_FILE")
    if not filename:
        pytest.skip("opt-in local PostgreSQL URL file not supplied")
    monkeypatch.setenv("ENVIRONMENT", "test")
    url = normalize_database_url(Path(filename).read_text().strip())
    staging_url(make_url(url))
    admin = create_engine(url)
    schema = "math_preview_" + secrets.token_hex(8)
    with admin.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA "{schema}"'))
    engine = create_engine(url, connect_args={"options": f"-csearch_path={schema}"})
    try:
        client, factory = make_preview(engine, monkeypatch)
        with client:
            check_parallel((client, factory))
            for number in range(2, 6):
                assert finish(client, number)[-1]["xp_awarded"] == 10
            assert finish(client, 5)[-1]["xp_awarded"] == 0
            assert all(
                l["state"] == "completed"
                for l in client.get(P + "/catalog").json()["lessons"]
            )
        with factory.begin() as db:
            assert db.get(User, 1).xp_total == 187 and db.get(User, 2).xp_total == 0
            assert import_course(db) == {"created": 0, "skipped": 5}
    finally:
        engine.dispose()
        with admin.begin() as connection:
            connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        admin.dispose()
