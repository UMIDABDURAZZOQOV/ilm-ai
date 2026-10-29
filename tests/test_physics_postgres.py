"""Real opt-in PostgreSQL: additive migration/import, all 7 lessons, concurrent XP.

Use only ILM_TEST_POSTGRES_URL_FILE with the isolated staging fixture.
"""

import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

from sqlalchemy import text
from test_physics_v2 import answer_all, finish, migration, start
from test_postgres_staging import postgres_stage as postgres_stage  # noqa: PLC0414 - pytest fixture export

from routers.physics_preview import router
from services import tokens
from services.assessment_models import AssessmentV2Progress, CurriculumAssessment
from services.models import StudyEvent, User, UserLessonProgress
from services.physics_curriculum import import_batch, load_batch


def test_postgres_physics_migration_all_seven_and_parallel_first_pass(
    postgres_stage, monkeypatch
):
    client, factory, engine = postgres_stage
    monkeypatch.setenv("PHYSICS_PREVIEW_ENABLED", "true")
    monkeypatch.setenv("ENVIRONMENT", "test")
    with engine.begin() as conn:
        migration(conn)
    # Exercise the actual CLI with a plain URL, private credentials in env, and
    # this new schema. No existing/public schema or production URL is used.
    with engine.connect() as conn:
        schema = conn.execute(text("SELECT current_schema()")).scalar_one()
    raw_url = engine.url.set(
        drivername="postgresql",
        query={**engine.url.query, "options": f"-csearch_path={schema}"},
    )
    cli = subprocess.run(
        [sys.executable, "-m", "scripts.import_physics_preview", "--import-content"],
        env={
            **os.environ,
            "ENVIRONMENT": "test",
            "DATABASE_URL": raw_url.render_as_string(hide_password=False),
        },
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert cli.returncode == 0, cli.stderr
    with factory.begin() as db:
        db.add(
            User(
                id=2,
                name="Parallel QA",
                email="parallel-physics@example.test",
                xp_total=0,
            )
        )
        import_batch(db, load_batch())
        import_batch(db, load_batch())
        assert db.query(CurriculumAssessment).count() == 43
        assert db.get(User, 42).xp_total == 137
    client.app.include_router(router)
    from test_physics_v2 import (
        test_all_seven_lessons_server_grading_xp_progress_and_legacy_isolation as exercise,
    )

    exercise((client, factory))
    old = client.headers["Authorization"]
    client.headers["Authorization"] = f"Bearer {tokens.create_access_token(2)}"
    try:
        first, second = start(client).json(), start(client).json()
        answer_all(client, first)
        answer_all(client, second)
        with ThreadPoolExecutor(max_workers=4) as pool:
            responses = list(
                pool.map(
                    lambda attempt: finish(client, attempt),
                    [first, first, second, second],
                )
            )
        assert all(r.status_code == 200 for r in responses), [r.text for r in responses]
        assert responses[0].json() == responses[1].json()
        assert responses[2].json() == responses[3].json()
        assert sorted({r.json()["xp_awarded"] for r in responses}) == [0, 10]
        with factory() as db:
            assert db.get(User, 2).xp_total == 10
            assert (
                db.query(AssessmentV2Progress).filter_by(user_id=2).one().attempts == 2
            )
            assert sum(e.xp for e in db.query(StudyEvent).filter_by(user_id=2)) == 10
            assert (
                db.get(User, 42).xp_total == 137 and db.get(User, 42).streak_days == 3
            )
            assert db.query(UserLessonProgress).filter_by(user_id=42).one().stars == 2
    finally:
        client.headers["Authorization"] = old
