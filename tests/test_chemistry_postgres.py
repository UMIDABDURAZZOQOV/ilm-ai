"""Opt-in real PostgreSQL: same explicit loopback staging guard as Biology."""
from concurrent.futures import ThreadPoolExecutor

import pytest

from test_postgres_staging import postgres_stage
from test_chemistry_lesson import start,answer_all,finish,PREFIX
from routers.chemistry_preview import router
from services.chemistry_curriculum import install_schema,import_lesson
from services.chemistry_validation import load_lessons
from services.models import User,UserLessonProgress,SkillLesson,SkillQuestion,StudyEvent
from services import chemistry_runtime as runtime


def test_real_postgres_chemistry_schema_import_snapshot_and_parallel_completion(postgres_stage,monkeypatch):
    client,factory,engine=postgres_stage
    monkeypatch.setenv('ENVIRONMENT','test');monkeypatch.setenv('CHEMISTRY_PREVIEW_ENABLED','true')
    client.app.include_router(router)
    with factory() as db:
        before=(db.query(SkillLesson).count(),db.query(SkillQuestion).count())
        old=(db.get(User,42).xp_total,db.get(User,42).streak_days,
             db.query(UserLessonProgress).filter_by(user_id=42).one().stars)
    install_schema(engine);install_schema(engine)
    with factory.begin() as db:
        for lesson in load_lessons():
            assert import_lesson(db,lesson)['created'] is True
            assert import_lesson(db,lesson)['created'] is False
    a=start(client);b=start(client)
    assert 'grading_spec' not in str(a) and 'expected' not in str(a)
    answer_all(client,a);answer_all(client,b)
    def complete(attempt):
        with factory() as db:return runtime.complete(db,1,attempt['attempt_id'])
    with ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(complete,[a,b]))
    assert sum(r['xp_awarded'] for r in results)==20
    assert finish(client,a).json()==results[0]
    with factory() as db:
        assert db.get(User,1).xp_total==20
        assert (db.query(SkillLesson).count(),db.query(SkillQuestion).count())==before
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days,
                db.query(UserLessonProgress).filter_by(user_id=42).one().stars)==old
        assert db.query(StudyEvent).filter_by(user_id=1,kind=runtime.KIND).count()==2
