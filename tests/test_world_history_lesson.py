"""Real first paragraph: exact-source validation and authoritative common-v2 API."""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import timedelta
import json
import os
import subprocess
import sys
from uuid import uuid4

from fastapi import FastAPI
from fastapi.testclient import TestClient
import httpx
import jwt
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from services import db as database, tokens, users
from services.models import Base, StudyEvent, StudySession, User, UserLessonProgress
from services.chemistry_grading import grade_answer
from services.world_history_curriculum import import_lesson, import_reviewed_lessons, install_schema
from services.world_history_models import WorldHistoryBase, WorldHistoryAssessment, WorldHistoryLesson, WorldHistoryProgress
from services.world_history_lessons import load_lessons, validate_lesson
from services.world_history_validation import DIRECTORY, fingerprint, load_catalog, read_json
from services import world_history_runtime as runtime
from services.study import utcnow
from routers.world_history_preview import router

PREFIX = '/preview/world_history/v2'


@pytest.fixture
def history(tmp_path, monkeypatch):
    monkeypatch.setenv('ENVIRONMENT', 'test')
    monkeypatch.setenv('WORLD_HISTORY_PREVIEW_ENABLED', 'true')
    engine = create_engine(f"sqlite:///{tmp_path/'world_history_staging.db'}",
                           connect_args={'check_same_thread': False, 'timeout': 30})
    @event.listens_for(engine, 'connect')
    def foreign_keys(conn, _):
        conn.execute('PRAGMA foreign_keys=ON')
    Base.metadata.create_all(engine)
    install_schema(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    for module in (database, tokens, users):
        monkeypatch.setattr(module, 'SessionLocal', factory)
    monkeypatch.setattr(tokens, 'JWT_SECRET', 'history-tests-only-secret-at-least-32-characters')
    monkeypatch.setattr(tokens, 'USE_DB', True)
    monkeypatch.setattr(users, 'USE_DB', True)
    with factory.begin() as db:
        db.add_all([User(id=n, name='Synthetic history QA', email=f'history{n}@example.test',
                        xp_total=137 if n == 42 else 0, streak_days=3 if n == 42 else 0) for n in [1, 2, 42]])
        db.flush()
        from services.curriculum import import_curriculum, load_documents
        bio = import_curriculum(db, *load_documents())
        db.add(UserLessonProgress(user_id=42, lesson_id=bio['lesson_id'], stars=2,
                                 attempts=1, xp_earned=137, completed_at=utcnow()))
        import_reviewed_lessons(db)
    app = FastAPI()
    app.include_router(router)
    def get_db():
        with factory() as db:
            yield db
    app.dependency_overrides[database.get_db] = get_db
    class FreshHistoryAuth(httpx.Auth):
        def auth_flow(self, request):
            # Keep real JWT verification; long/suspended runs need a fresh default.
            # Explicit owner/expired-token headers must retain their exact meaning.
            if 'Authorization' not in request.headers:
                request.headers['Authorization'] = f'Bearer {tokens.create_access_token(1)}'
            yield request

    with TestClient(app) as client:
        client.auth = FreshHistoryAuth()
        yield client, factory, monkeypatch
    engine.dispose()


def start(client, request_id=None):
    key = load_lessons()[0]['key']
    response = client.post(f'{PREFIX}/lessons/{key}/start', json={
        'assessment_version': 2, 'request_id': str(request_id or uuid4())})
    assert response.status_code == 200, response.text
    return response.json()


def test_history_fixture_preserves_explicit_expired_jwt_rejection(history):
    client, _, _ = history
    expired = jwt.encode({'sub': '1', 'iat': 0, 'exp': 1}, tokens.JWT_SECRET, algorithm='HS256')
    assert client.get(PREFIX + '/catalog', headers={'Authorization': f'Bearer {expired}'}).status_code == 401
    assert client.get(PREFIX + '/catalog').status_code == 200


def answer_for(q, correct=True):
    spec = q['grading_spec']
    if q['response_kind'] == 'concept_selection':
        return {'choice_id': spec['expected'] if correct else next(i for i in spec['choice_ids'] if i != spec['expected'])}
    return {'value': spec['expected'] if correct else 'boshqa javob'}


def send(client, attempt, q, answer):
    return client.post(f"{PREFIX}/attempts/{attempt['attempt_id']}/answers", json={
        'assessment_version': 2, 'assessment_key': q['key'], 'answer': answer})


def answer_all(client, attempt, correct=True):
    for q in load_lessons()[0]['assessments']:
        response = send(client, attempt, q, answer_for(q, correct))
        assert response.status_code == 200, response.text
        assert response.json()['is_correct'] is correct


def finish(client, attempt):
    return client.post(f"{PREFIX}/attempts/{attempt['attempt_id']}/complete", json={'assessment_version': 2})


def test_first_history_paragraph_teaches_reviewed_facts_and_retains_open_review():
    lesson = load_lessons()[0]
    assert len(lesson['content']['cards']) == 13
    assert len(lesson['facts']) == 22
    assert len(lesson['assessments']) == 14
    assert sum(q['response_kind'] == 'short_text' for q in lesson['assessments']) == 4
    assert {p for r in lesson['source_refs'] for p in r['pdf_pages']} == set(range(5, 14))
    assert lesson['content']['reflections'][0]['automatic_score'] is False
    assert all(lesson['facts'][i]['automatic_assessment_allowed']
               for q in lesson['assessments'] for i in q['fact_ids'])
    assert len(runtime.KIND) <= StudySession.__table__.c.kind.type.length


@pytest.mark.parametrize('change', ['page', 'digest', 'region', 'ocr', 'answer', 'untaught', 'private',
                                  'kind', 'prerequisite', 'alias', 'solution', 'citation', 'interpretation', 'open_score'])
def test_source_fact_or_key_mutations_fail_even_if_top_level_digest_is_refreshed(change):
    lesson = deepcopy(load_lessons()[0])
    review = read_json(DIRECTORY / 'grade6_paragraph01_review.json')
    q = lesson['assessments'][0]
    if change == 'page': lesson['facts']['archaeologist']['source_refs'][0]['pdf_pages'] = [99]
    if change == 'digest': review['source_pages'][0]['page_image_sha256'] = '0'*64
    if change == 'region': lesson['source_refs'][-1]['regions'] = ['topic_body']
    if change == 'ocr': review['source_pages'][0]['verification'] = 'ocr_candidate'
    if change == 'answer': q['grading_spec']['verified_answer'] = 'Manbasiz'
    if change == 'untaught': lesson['content']['cards'][1]['fact_ids'] = ['archaeologist']
    if change == 'private': q['public']['expected'] = q['grading_spec']['expected']
    if change == 'kind': q['response_kind'] = 'essay'
    if change == 'prerequisite': lesson['prerequisite_ids'] = ['invented']
    if change == 'alias': lesson['assessments'][-1]['grading_spec']['aliases'].append('noto‘g‘ri')
    if change == 'solution': q['grading_spec']['solution'][0]['body'] = 'Unreviewed historical assertion'
    if change == 'citation': q['source_refs'] = []
    if change == 'interpretation': q['fact_ids'] = ['social-model']
    if change == 'open_score': lesson['content']['reflections'][0]['automatic_score'] = True
    # Test semantic contracts as well as immutable review digests.
    review['lesson_sha256'] = fingerprint(lesson)
    review['approved_content_sha256'] = fingerprint(lesson['content'])
    review['approved_assessments_sha256'] = fingerprint(lesson['assessments'])
    review['approved_fact_sha256'] = {i: fingerprint(f) for i, f in lesson['facts'].items()}
    with pytest.raises(ValueError):
        validate_lesson(load_catalog(), lesson, review)


@pytest.mark.parametrize('value, correct', [('Antropolog', True), (' ANTROPOLOGLAR. ', True),
                                         ('arxeolog', False), ('antropolog yoki etnograf', False), ('antropolo', False)])
def test_objective_frq_accepts_only_explicit_aliases(value, correct):
    spec = load_lessons()[0]['assessments'][10]['grading_spec']
    assert (grade_answer(spec, {'value': value}) == 'correct') is correct


def test_start_hides_keys_and_resume_preserves_immutable_snapshot(history):
    client, factory, _ = history
    request = uuid4()
    attempt = start(client, request)
    forbidden = {'grading_spec', 'expected', 'aliases', 'choice_ids', 'verified_answer', 'facts', 'correct_answer'}
    def check(value):
        if isinstance(value, dict):
            assert not forbidden & value.keys()
            for child in value.values(): check(child)
        elif isinstance(value, list):
            for child in value: check(child)
    check(attempt)
    q = load_lessons()[0]['assessments'][0]
    with factory.begin() as db:
        row = db.get(WorldHistoryAssessment, q['key'])
        row.grading_spec = {**row.grading_spec, 'expected': 'a'}
    assert send(client, attempt, q, answer_for(q)).json()['is_correct'] is True
    assert start(client, request)['answers'][q['key']]['is_correct'] is True


def test_once_only_xp_and_existing_biology_progress_preserved(history):
    client, factory, _ = history
    attempt = start(client)
    answer_all(client, attempt)
    response = finish(client, attempt)
    assert response.status_code == 200
    result = response.json()
    assert (result['score'], result['total'], result['xp_awarded'], result['stars']) == (14, 14, 20, 3)
    assert finish(client, attempt).json() == result
    with factory() as db:
        assert db.get(User, 1).xp_total == 20
        old = db.get(User, 42)
        assert (old.xp_total, old.streak_days) == (137, 3)
        assert db.query(UserLessonProgress).filter_by(user_id=42).one().stars == 2
        assert db.query(StudyEvent).filter_by(user_id=1, kind=runtime.KIND).count() == 1
    catalog = client.get(PREFIX + '/catalog').json()
    assert catalog['source_sections'] == 46 and not catalog['grade_content_complete']
    assert catalog['available_grades'] == list(range(6, 12))
    assert len(catalog['chapters']) == 5 and len(catalog['source_units']) == 46
    assert catalog['lessons'][0]['state'] == 'completed'


def test_order_account_isolation_incomplete_and_changed_replays_rejected(history):
    client, _, _ = history
    attempt = start(client)
    questions = load_lessons()[0]['assessments']
    assert send(client, attempt, questions[1], answer_for(questions[1])).status_code == 409
    assert send(client, attempt, questions[0], answer_for(questions[0])).status_code == 200
    assert send(client, attempt, questions[0], answer_for(questions[0])).status_code == 200
    assert send(client, attempt, questions[0], answer_for(questions[0], False)).status_code == 409
    other = {'Authorization': f'Bearer {tokens.create_access_token(2)}'}
    assert client.post(f"{PREFIX}/attempts/{attempt['attempt_id']}/complete", json={'assessment_version': 2}, headers=other).status_code == 404
    assert finish(client, attempt).status_code == 409


@pytest.mark.parametrize('extra', [{'score': 100}, {'is_correct': True}, {'user_id': 42}])
def test_client_cannot_submit_score_correctness_or_identity(history, extra):
    client, _, _ = history
    attempt = start(client)
    q = load_lessons()[0]['assessments'][0]
    response = client.post(f"{PREFIX}/attempts/{attempt['attempt_id']}/answers", json={
        'assessment_version': 2, 'assessment_key': q['key'], 'answer': answer_for(q), **extra})
    assert response.status_code == 422


def test_failure_retry_and_replay_do_not_farm_xp(history):
    client, factory, _ = history
    failed = start(client)
    answer_all(client, failed, False)
    assert finish(client, failed).json()['xp_awarded'] == 0
    for expected_xp in (20, 0):
        attempt = start(client)
        answer_all(client, attempt)
        assert finish(client, attempt).json()['xp_awarded'] == expected_xp
    with factory() as db:
        assert db.get(User, 1).xp_total == 20
        assert db.get(WorldHistoryProgress, (1, load_lessons()[0]['key'])).attempts == 3


def test_expiry_and_preview_gates_fail_closed(history):
    client, factory, patch = history
    attempt = start(client)
    with factory.begin() as db:
        db.get(StudySession, attempt['attempt_id']).started_at = utcnow() - timedelta(hours=25)
    assert finish(client, attempt).status_code == 409
    patch.setenv('ENVIRONMENT', 'production')
    assert client.get(PREFIX + '/catalog').status_code == 404
    patch.setenv('ENVIRONMENT', 'test')
    patch.setenv('WORLD_HISTORY_PREVIEW_ENABLED', 'false')
    assert client.get(PREFIX + '/catalog').status_code == 404


def test_parallel_completions_award_first_pass_xp_once(history):
    client, factory, _ = history
    attempts = [start(client), start(client)]
    for attempt in attempts: answer_all(client, attempt)
    def complete(attempt):
        with factory() as db: return runtime.complete(db, 1, attempt['attempt_id'])
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(complete, attempts))
    assert sum(r['xp_awarded'] for r in results) == 20


def test_missing_prerequisite_never_unlocks_later_import(history):
    client, factory, _ = history
    with factory.begin() as db:
        gap_sequence = max(d['sequence'] for d in load_lessons() if d['grade'] == 6) + 2
        db.add(WorldHistoryLesson(key='test-gap', subject='jahon_tarixi', grade=6, sequence=gap_sequence,
                                 revision=1, topic_id='test-gap', content_sha256='0'*64,
                                 title='Synthetic gap', content={'source_refs': []}))
    rows = client.get(PREFIX + '/catalog').json()['lessons']
    assert next(r for r in rows if r['key'] == 'test-gap')['state'] == 'locked'
    response = client.post(PREFIX + '/lessons/test-gap/start', json={'assessment_version': 2, 'request_id': str(uuid4())})
    assert response.status_code == 403


def test_history_import_is_immutable_and_schema_not_in_legacy_startup(history):
    _, factory, _ = history
    lesson = load_lessons()[0]
    assert not set(WorldHistoryBase.metadata.tables) & set(Base.metadata.tables)
    with factory.begin() as db:
        assert import_lesson(db, lesson)['created'] is False
        bad = deepcopy(lesson)
        bad['content']['cards'][0]['body'] = 'Unreviewed change'
        with pytest.raises(ValueError): import_lesson(db, bad)


def test_pure_dry_run_never_imports_database_or_models():
    code = "import runpy,sys; runpy.run_module('scripts.import_world_history_curriculum',run_name='__main__'); assert 'services.db' not in sys.modules; assert 'services.models' not in sys.modules"
    env = {**os.environ, 'ENVIRONMENT': 'production', 'DATABASE_URL': 'postgresql://invalid.example/production'}
    result = subprocess.run([sys.executable, '-c', code], cwd=DIRECTORY.parents[2], env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_fixture_export_uses_actual_safe_public_api(history):
    client, _, _ = history
    catalog = client.get(PREFIX + '/catalog').json()
    attempt = start(client)
    public = deepcopy(attempt)
    answers = {}
    for i, q in enumerate(load_lessons()[0]['assessments']):
        response = send(client, attempt, q, answer_for(q, i != 0))
        assert response.status_code == 200
        answers[q['key']] = response.json()
    result = finish(client, attempt).json()
    assert (result['score'], result['total'], result['xp_awarded']) == (13, 14, 20)
    assert all('grading_spec' not in json.dumps(p) for p in (catalog, public, answers, result))
    target = os.getenv('WORLD_HISTORY_WRITE_MOBILE_FIXTURES')
    if target:
        from pathlib import Path
        directory = Path(target)
        directory.mkdir(parents=True, exist_ok=True)
        sid = 'whv2:900006:11111111-1111-4111-8111-111111111111'
        public['attempt_id'] = result['attempt_id'] = sid
        public['expires_at'] = '2099-01-01T00:00:00+00:00'
        result['elapsed_seconds'] = 180
        for name, value in [('catalog', catalog), ('lesson', public), ('results', {'answers': answers, 'result': result})]:
            (directory/f'world_history_{name}.json').write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
