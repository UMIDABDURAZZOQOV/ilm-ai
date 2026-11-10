"""UI-013: real local queries only; no hosted DB, source data or XP mutation."""
from copy import deepcopy
from datetime import datetime, timezone

from fastapi import HTTPException
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from services import beta_curriculum as beta
from services.models import User, StudySession


def legacy():
    values = dict(streak=(1, [3, 7, 30]), lessons=(2, [1, 10, 25, 50]),
                  perfect=(1, [1, 5, 15]), questions=(40, [50, 200, 500]), xp=(20, [100, 500, 1000]))
    return {'achievements': [dict(id=f'{group}_{target}', group=group, target=target,
                                 progress=min(value, target), earned=value >= target)
                            for group, (value, targets) in values.items() for target in targets]}


@pytest.fixture
def owned(monkeypatch):
    engine = create_engine('sqlite://', connect_args={'check_same_thread': False},
                           poolclass=StaticPool)
    User.__table__.create(engine)
    StudySession.__table__.create(engine)
    for _, model, progress, _ in beta.ADAPTERS.values():
        model.__table__.create(engine)
        progress.__table__.create(engine)
    calls = []
    def checked_adapter(db, slug):
        calls.append(slug)
        return beta.ADAPTERS[slug]
    monkeypatch.setattr(beta, 'adapter', checked_adapter)
    now = datetime.now(timezone.utc)
    with Session(engine) as db:
        db.add_all([User(id=i, name='Synthetic', email=f'user{i}@example.test', xp_total=20)
                    for i in [1, 2]])
        for slug, (runtime, model, progress, _) in beta.ADAPTERS.items():
            for sequence, (uid, complete, score) in enumerate([
                (1, True, 100 if slug == 'fizika' else 90 if slug != 'jahon_tarixi' else 89),
                (2, True, 100), (1, False, 100),
            ], 1):
                key = f'{slug}-{sequence}'
                db.add(model(key=key, subject=slug, grade=7, sequence=sequence, revision=1,
                    topic_id=key, content_sha256='0'*64, title='Synthetic', content={}))
                db.add(progress(user_id=uid, lesson_key=key, completed_at=now if complete else None,
                                best_score_pct=score, attempts=3, xp_earned=10 if complete else 0))
            for suffix, uid, complete, total in [
                ('done', 1, True, 4), ('other', 2, True, 100),
                ('pending', 1, False, 100), ('malformed', 1, True, -1),
            ]:
                db.add(StudySession(id=f'{slug}-{suffix}', user_id=uid, kind=runtime.KIND,
                    scope=f'{slug}-1', questions={}, started_at=now,
                    completed_at=now if complete else None, response={'total': total}))
        runtime, model, progress, _ = beta.ADAPTERS['fizika']
        db.add(model(key='physics-extra', subject='fizika', grade=7, sequence=4, revision=1,
            topic_id='physics-extra', content_sha256='0'*64, title='Synthetic', content={}))
        db.add(progress(user_id=1, lesson_key='physics-extra', completed_at=now,
                        best_score_pct=80, attempts=2, xp_earned=10))
        db.add(StudySession(id='physics-replay', user_id=1, kind=runtime.KIND, scope='fizika-1',
            questions={}, started_at=now, completed_at=now, response={'total': 2}))
        db.add(StudySession(id='legacy-not-twice', user_id=1, kind='lesson', scope='1',
            questions={}, started_at=now, completed_at=now, response={'total': 100}))
        db.commit()
        yield db, calls
    engine.dispose()


def test_all_four_reviewed_subjects_join_legacy_once_and_keep_payload(owned):
    db, calls = owned
    original = legacy()
    before = deepcopy(original)
    result = beta.append_achievements(db, 1, original)
    tiers = {a['id']: a for a in result['achievements']}
    assert tiers['lessons_10']['progress'] == 7  # legacy2 + five distinct completions
    assert tiers['perfect_5']['progress'] == 4  # legacy1 + three >=90%, not pending
    assert tiers['questions_200']['progress'] == 58  # legacy40 + 16 + replay2
    assert tiers['questions_50']['earned'] is True
    assert tiers['xp_100']['progress'] == 20
    assert tiers['streak_3']['progress'] == 1
    assert set(calls) == set(beta.ADAPTERS)
    assert original == before
    assert beta.append_achievements(db, 1, original) == result
    assert db.get(User, 1).xp_total == 20
    assert not db.new and not db.dirty and not db.deleted


def test_account_filter_and_distinct_lesson_count_ignore_replay_attempts(owned):
    db, _ = owned
    empty = legacy()
    for a in empty['achievements']:
        a.update(progress=0, earned=False)
    rows = {a['id']: a for a in beta.append_achievements(db, 2, empty)['achievements']}
    assert rows['lessons_10']['progress'] == 4
    assert rows['perfect_5']['progress'] == 4
    assert rows['questions_500']['progress'] == 400


def test_runtime_capability_denial_is_not_bypassed(owned, monkeypatch):
    db, _ = owned
    def denied(*_):
        raise HTTPException(404, 'subject_not_available')
    monkeypatch.setattr(beta, 'adapter', denied)
    with pytest.raises(HTTPException) as error:
        beta.append_achievements(db, 1, legacy())
    assert error.value.status_code == 404


def test_user_without_reviewed_progress_keeps_legacy_tiers(owned):
    db, _ = owned
    original = legacy()
    assert beta.append_achievements(db, 999, original) == original


def test_already_capped_legacy_achievements_remain_earned(owned):
    db, _ = owned
    original = legacy()
    for a in original['achievements']:
        a.update(progress=a['target'], earned=True)
    assert beta.append_achievements(db, 1, original) == original


def test_reviewed_route_precedes_legacy_and_retains_owner_dependency(owned, monkeypatch):
    from contextlib import asynccontextmanager
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from routers import beta_mobile, skills
    from services.auth_deps import get_authenticated_user_id
    db, _ = owned
    async def isolated_db():
        yield db
    @asynccontextmanager
    async def published(_request, _db):
        yield
    monkeypatch.setattr(beta_mobile, 'bio_scope', published)
    monkeypatch.setattr(skills, 'get_achievements', lambda uid, db: legacy())
    app = FastAPI()
    app.include_router(beta_mobile.create_router('/mobile', isolated_db))
    app.dependency_overrides[get_authenticated_user_id] = lambda: 1
    with TestClient(app) as client:
        response = client.get('/mobile/skills/1/achievements')
        assert response.status_code == 200
        rows = {a['id']: a for a in response.json()['achievements']}
        assert rows['lessons_10']['progress'] == 7  # New route, not legacy2.
        assert client.get('/mobile/skills/2/achievements').status_code == 403
        app.dependency_overrides.clear()
        assert client.get('/mobile/skills/1/achievements').status_code == 401
