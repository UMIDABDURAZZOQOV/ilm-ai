"""Opt-in real PostgreSQL, confined to a fresh schema in history staging."""
from concurrent.futures import ThreadPoolExecutor

from test_postgres_staging import postgres_stage  # noqa: F401
from test_world_history_lesson import start, answer_all, finish
from routers.world_history_preview import router
from services.world_history_curriculum import install_schema, import_reviewed_lessons
from services.world_history_lessons import load_lessons
from test_world_history_lesson import PREFIX, answer_for, send
from uuid import uuid4
from services.models import User, UserLessonProgress, SkillLesson, SkillQuestion, StudyEvent
from services import world_history_runtime as runtime


def test_real_postgres_history_import_snapshot_account_preservation_and_parallel_completion(postgres_stage, monkeypatch):
    client, factory, engine = postgres_stage
    monkeypatch.setenv('ENVIRONMENT', 'test')
    monkeypatch.setenv('WORLD_HISTORY_PREVIEW_ENABLED', 'true')
    client.app.include_router(router)
    with factory() as db:
        before = (db.query(SkillLesson).count(), db.query(SkillQuestion).count())
        old = (db.get(User, 42).xp_total, db.get(User, 42).streak_days,
               db.query(UserLessonProgress).filter_by(user_id=42).one().stars)
    install_schema(engine)
    install_schema(engine)
    with factory.begin() as db:
        assert all(r['created'] for r in import_reviewed_lessons(db))
        assert not any(r['created'] for r in import_reviewed_lessons(db))
    attempts = [start(client), start(client)]
    for attempt in attempts:
        assert 'grading_spec' not in str(attempt) and 'expected' not in str(attempt)
        answer_all(client, attempt)
    def complete(attempt):
        with factory() as db:
            return runtime.complete(db, 1, attempt['attempt_id'])
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(complete, attempts))
    assert sum(r['xp_awarded'] for r in results) == 20
    assert finish(client, attempts[0]).json() == results[0]
    with factory() as db:
        assert db.get(User, 1).xp_total == 20
        assert (db.query(SkillLesson).count(), db.query(SkillQuestion).count()) == before
        assert (db.get(User, 42).xp_total, db.get(User, 42).streak_days,
                db.query(UserLessonProgress).filter_by(user_id=42).one().stars) == old
        assert db.query(StudyEvent).filter_by(user_id=1, kind=runtime.KIND).count() == 2
    for lesson in load_lessons()[1:]:
        response = client.post(f"{PREFIX}/lessons/{lesson['key']}/start", json={
            'assessment_version': 2, 'request_id': str(uuid4())})
        assert response.status_code == 200, response.text
        attempt = response.json()
        for q in lesson['assessments']:
            response = send(client, attempt, q, answer_for(q))
            assert response.status_code == 200 and response.json()['is_correct']
        assert finish(client, attempt).json()['xp_awarded'] == 20
    with factory() as db:
        assert db.get(User, 1).xp_total == 120
        assert db.get(User, 42).xp_total == old[0]
