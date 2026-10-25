"""Separate module gives the full-course rehearsal its own fresh PG schema.

The frozen first-batch migration/import test must still start from seven rows.
"""

import os
import subprocess
import sys

from sqlalchemy import text
from test_physics_v2 import finish, migration, start
from test_postgres_staging import postgres_stage as postgres_stage  # noqa: PLC0414 - pytest fixture export

from routers.physics_preview import router
from services import tokens
from services.models import User, UserLessonProgress


def test_postgres_all_reviewed_batches_append_without_legacy_changes(
    postgres_stage, monkeypatch
):
    from sqlalchemy import inspect
    from test_physics_course import new_answer
    from test_physics_v2 import correct, submit

    from services.assessment_models import CurriculumLessonV2
    from services.physics_curriculum import load_course

    client, factory, engine = postgres_stage
    monkeypatch.setenv("PHYSICS_PREVIEW_ENABLED", "true")
    monkeypatch.setenv("ENVIRONMENT", "test")
    if "curriculum_v2_lessons" not in inspect(engine).get_table_names():
        with engine.begin() as conn:
            migration(conn)
    with engine.connect() as conn:
        schema = conn.execute(text("SELECT current_schema()")).scalar_one()
    raw_url = engine.url.set(
        drivername="postgresql",
        query={**engine.url.query, "options": f"-csearch_path={schema}"},
    )
    for _ in range(2):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "scripts.import_physics_preview",
                "--import-content",
                "--all-reviewed",
            ],
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
        assert result.returncode == 0, result.stderr
    with factory.begin() as db:
        assert db.query(CurriculumLessonV2).count() == 81
        db.add(
            User(
                id=900003, name="Course QA", email="course-qa@example.test", xp_total=0
            )
        )
    client.app.include_router(router)
    old_header = client.headers["Authorization"]
    client.headers["Authorization"] = f"Bearer {tokens.create_access_token(900003)}"
    try:
        for document in load_course():
            for lesson in document["lessons"]:
                issued = start(client, lesson["sequence"], grade=document["grade"])
                assert issued.status_code == 200, issued.text
                attempt = issued.json()
                for q in lesson["assessments"]:
                    answer = (
                        correct(q)
                        if document["grade"] == 6 and lesson["sequence"] < 8
                        else new_answer(lesson, q)
                    )
                    graded = submit(client, attempt, q["key"], answer)
                    assert graded.status_code == 200 and graded.json()["is_correct"], (
                        graded.text
                    )
                result = finish(client, attempt)
                assert result.status_code == 200 and result.json()["xp_awarded"] == 10
                assert finish(client, attempt).json() == result.json()
        with factory() as db:
            assert db.get(User, 900003).xp_total == 810
            assert (
                db.get(User, 42).xp_total == 137 and db.get(User, 42).streak_days == 3
            )
            assert db.query(UserLessonProgress).filter_by(user_id=42).one().stars == 2
    finally:
        client.headers["Authorization"] = old_header
