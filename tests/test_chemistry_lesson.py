"""Real sourced first paragraph plus authoritative isolated v2 API regressions."""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import timedelta
import json
import os
from pathlib import Path
import subprocess
import sys
from uuid import uuid4

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from services import db as database, tokens, users
from services.models import Base, StudyEvent, StudySession, User, UserLessonProgress
from services.chemistry_curriculum import import_lesson, import_reviewed_lessons, install_schema
from services.chemistry_grading import grade_answer, normalized_text
from services.chemistry_models import ChemistryBase, ChemistryAssessment, ChemistryLesson, ChemistryProgress
from services.chemistry_validation import load_catalog,load_lessons,read_json,validate_lesson,DIRECTORY
from services import chemistry_runtime as runtime
from services.study import utcnow
from routers.chemistry_preview import router

PREFIX='/preview/chemistry/v2'


@pytest.fixture(scope='module')
def reviewed_chemistry_documents():
    """One fully validated immutable snapshot for pure grading examples only.

    Source-mutation,loader,import and API tests still read/revalidate evidence.
    The teardown checksum also catches accidental mutation by a grading test.
    """
    from services.chemistry_validation import fingerprint
    documents=load_lessons();before=fingerprint(documents)
    yield documents
    assert fingerprint(documents)==before


@pytest.fixture
def chemistry(tmp_path,monkeypatch):
    monkeypatch.setenv('ENVIRONMENT','test')
    monkeypatch.setenv('CHEMISTRY_PREVIEW_ENABLED','true')
    engine=create_engine(f"sqlite:///{tmp_path/'chemistry_staging.db'}",connect_args={'check_same_thread':False,'timeout':30})
    @event.listens_for(engine,'connect')
    def foreign_keys(conn,_): conn.execute('PRAGMA foreign_keys=ON')
    Base.metadata.create_all(engine)
    install_schema(engine)
    factory=sessionmaker(bind=engine,expire_on_commit=False)
    for module in (database,tokens,users): monkeypatch.setattr(module,'SessionLocal',factory)
    monkeypatch.setattr(tokens,'JWT_SECRET','chemistry-tests-only-secret-at-least-32-characters')
    monkeypatch.setattr(tokens,'USE_DB',True);monkeypatch.setattr(users,'USE_DB',True)
    with factory.begin() as db:
        db.add_all([User(id=n,name='Synthetic QA learner',email=f'chemistry{n}@example.test',xp_total=137 if n==42 else 0,streak_days=3 if n==42 else 0) for n in [1,2,42]])
        db.flush()
        from services.curriculum import import_curriculum,load_documents
        bio=import_curriculum(db,*load_documents())
        db.add(UserLessonProgress(user_id=42,lesson_id=bio['lesson_id'],stars=2,attempts=1,xp_earned=137,completed_at=utcnow()))
        import_reviewed_lessons(db)
    app=FastAPI();app.include_router(router)
    def get_db():
        with factory() as db: yield db
    app.dependency_overrides[database.get_db]=get_db
    with TestClient(app,headers={'Authorization':f'Bearer {tokens.create_access_token(1)}'}) as client:
        yield client,factory,monkeypatch
    engine.dispose()


def start(client,request_id=None):
    key=load_lessons()[0]['key']
    response=client.post(f'{PREFIX}/lessons/{key}/start',json={'assessment_version':2,'request_id':str(request_id or uuid4())})
    assert response.status_code==200,response.text
    return response.json()


def send(client,attempt,q,answer):
    return client.post(f"{PREFIX}/attempts/{attempt['attempt_id']}/answers",json={'assessment_version':2,'assessment_key':q['key'],'answer':answer})


def answer_for(q,correct=True):
    spec=q['grading_spec']
    if q['response_kind']=='concept_selection':
        return {'choice_id':spec['expected'] if correct else next(i for i in spec['choice_ids'] if i!=spec['expected'])}
    return {'value':spec['expected'] if correct else 'boshqa javob'}


def answer_all(client,attempt,correct=True):
    for q in load_lessons()[0]['assessments']:
        r=send(client,attempt,q,answer_for(q,correct))
        assert r.status_code==200,r.text
        assert r.json()['is_correct'] is correct


def finish(client,attempt):
    return client.post(f"{PREFIX}/attempts/{attempt['attempt_id']}/complete",json={'assessment_version':2})


def test_reviewed_first_paragraph_has_real_taught_facts_mcq_and_frq():
    lesson=load_lessons()[0]
    assert len(lesson['content']['cards'])==8
    assert len(lesson['assessments'])==12
    assert [q['response_kind'] for q in lesson['assessments']].count('short_text')==3
    assert {p for r in lesson['source_refs'] for p in r['printed_pages']}==set(range(3,9))
    assert not lesson['content']['formulas']


def test_unresolved_source_contradiction_blocks_authorship_even_with_a_review_file():
    c=load_catalog();l=deepcopy(load_lessons()[0])
    l.update(book_id=c['books'][2]['id'],grade=9,topic_id='ch9-paragraph40')
    with pytest.raises(ValueError,match='unresolved_source_review_issue'):
        validate_lesson(c,l,read_json(DIRECTORY/'grade7_paragraph01_review.json'))


@pytest.mark.parametrize('mutation',['page','region','ocr','answer','untaught','private',
    'kind','prerequisite','alias','feedback','formula','citation','key','bibliography'])
def test_lesson_validation_rejects_unverified_facts_or_untaught_tasks(mutation):
    c=load_catalog();l=deepcopy(load_lessons()[0]);r=read_json(DIRECTORY/'grade7_paragraph01_review.json')
    q=l['assessments'][0]
    if mutation=='page':l['facts']['scope']['source_refs'][0]['printed_pages']=[99]
    if mutation=='region':q['source_refs'][0]['regions']=['right']
    if mutation=='ocr':r['source_pages'][0]['verification']='ocr_candidate'
    if mutation=='answer':q['grading_spec']['verified_answer']='Manbasiz javob'
    if mutation=='untaught':l['content']['cards'][0]['fact_ids']=['scope']
    if mutation=='private':q['public']['expected']='b'
    if mutation=='kind':q['response_kind']='chemical_equation'
    if mutation=='prerequisite':l['prerequisite_ids']=['fake']
    if mutation=='alias':l['assessments'][-1]['grading_spec']['aliases']=['unverified wrong alias']
    if mutation=='feedback':q['grading_spec']['feedback']={}
    if mutation=='formula':l['content']['formulas']=[{'body':'unreviewed'}]
    if mutation=='citation':q['source_refs']=[]
    if mutation=='key':l['assessments'][-1]['key']=q['key']
    if mutation=='bibliography':q['source_refs'][0]['year']=2099
    with pytest.raises(ValueError):validate_lesson(c,l,r)


@pytest.mark.parametrize('value,expected',[('Kimyo',True),(' KIMYO ',True),('kimyo fani.',True),
    ('matematika',False),('kimy',False),('kimyo yoki fizika',False)])
def test_text_frq_has_explicit_aliases_without_fuzzy_semantic_grading(value,expected):
    spec=next(q['grading_spec'] for q in load_lessons()[0]['assessments'] if q['response_kind']=='short_text')
    assert (grade_answer(spec,{'value':value})=='correct') is expected


@pytest.mark.parametrize('value',[True,12,[],{},'<script>',"__import__('os')",'x'*81,'kimyo\x00'])
def test_short_text_input_is_bounded_and_never_executes(value):
    spec=load_lessons()[0]['assessments'][-1]['grading_spec']
    assert grade_answer(spec,{'value':value})=='invalid_answer'


def test_uzbek_apostrophe_variants_are_normalized_only_for_text():
    assert normalized_text('Oʻzbek')==normalized_text('O‘zbek')==normalized_text("o'zbek")


def test_start_hides_all_private_specs_and_resume_keeps_server_snapshot(chemistry):
    client,factory,_=chemistry
    request_id=uuid4();attempt=start(client,request_id)
    forbidden={'grading_spec','expected','aliases','choice_ids','verified_answer','facts','correct_answer'}
    def check(value):
        if isinstance(value,dict):
            assert not forbidden & value.keys()
            for v in value.values():check(v)
        if isinstance(value,list):
            for v in value:check(v)
    check(attempt)
    q=load_lessons()[0]['assessments'][0]
    with factory.begin() as db:
        row=db.get(ChemistryAssessment,q['key'])
        row.grading_spec={**row.grading_spec,'expected':'a'}
    assert send(client,attempt,q,answer_for(q)).json()['is_correct'] is True
    resumed=start(client,request_id)
    assert resumed['attempt_id']==attempt['attempt_id']
    assert resumed['answers'][q['key']]['is_correct'] is True


def test_all_mixed_questions_award_once_and_preserve_biology(chemistry):
    client,factory,_=chemistry;a=start(client)
    answer_all(client,a)
    r=finish(client,a);assert r.status_code==200
    assert (r.json()['score'],r.json()['total'],r.json()['xp_awarded'],r.json()['stars'])==(12,12,20,3)
    assert finish(client,a).json()==r.json()
    with factory() as db:
        assert db.get(User,1).xp_total==20
        old=db.get(User,42)
        assert (old.xp_total,old.streak_days)==(137,3)
        assert db.query(UserLessonProgress).filter_by(user_id=42).one().stars==2
        assert db.query(StudyEvent).filter_by(user_id=1,kind=runtime.KIND).count()==1
    catalog=client.get(PREFIX+'/catalog').json()
    assert catalog['source_sections']==74 and not catalog['grade_content_complete']
    assert catalog['lessons'][0]['state']=='completed'


def test_unknown_order_foreign_attempt_and_changed_replay_are_rejected(chemistry):
    client,_,_=chemistry;a=start(client);qs=load_lessons()[0]['assessments']
    assert send(client,a,qs[1],answer_for(qs[1])).status_code==409
    assert send(client,a,qs[0],answer_for(qs[0])).status_code==200
    assert send(client,a,qs[0],answer_for(qs[0])).status_code==200
    assert send(client,a,qs[0],answer_for(qs[0],False)).status_code==409
    foreign={'Authorization':f'Bearer {tokens.create_access_token(2)}'}
    r=client.post(f"{PREFIX}/attempts/{a['attempt_id']}/complete",json={'assessment_version':2},headers=foreign)
    assert r.status_code==404
    assert finish(client,a).status_code==409


def test_format_error_does_not_disclose_solution_or_consume_answer(chemistry):
    client,_,_=chemistry;a=start(client);qs=load_lessons()[0]['assessments']
    for q in qs[:9]:assert send(client,a,q,answer_for(q)).status_code==200
    r=send(client,a,qs[9],{'value':'<script>'})
    assert r.status_code==422 and 'solution' not in r.text and 'expected' not in r.text
    assert send(client,a,qs[9],{'value':'  KIMYO FANI. '}).json()['is_correct'] is True
    assert send(client,a,qs[9],{'value':'kimyo'}).status_code==200


@pytest.mark.parametrize('payload',[{'score':100},{'is_correct':True},{'user_id':42}])
def test_client_score_and_identity_flags_are_not_accepted(chemistry,payload):
    client,_,_=chemistry;a=start(client);q=load_lessons()[0]['assessments'][0]
    r=client.post(f"{PREFIX}/attempts/{a['attempt_id']}/answers",json={
        'assessment_version':2,'assessment_key':q['key'],'answer':answer_for(q),**payload})
    assert r.status_code==422


def test_failure_retry_and_new_attempt_replay_do_not_farm_xp(chemistry):
    client,factory,_=chemistry
    a=start(client);answer_all(client,a,False)
    failed=finish(client,a).json();assert failed['xp_awarded']==0 and not failed['passed']
    b=start(client);answer_all(client,b);assert finish(client,b).json()['xp_awarded']==20
    c=start(client);answer_all(client,c);assert finish(client,c).json()['xp_awarded']==0
    with factory() as db:
        assert db.get(User,1).xp_total==20
        p=db.get(ChemistryProgress,(1,load_lessons()[0]['key']))
        assert p.attempts==3 and p.xp_earned==20


def test_expired_unfinished_attempt_and_disabled_preview_fail_closed(chemistry):
    client,factory,patch=chemistry;a=start(client)
    with factory.begin() as db:db.get(StudySession,a['attempt_id']).started_at=utcnow()-timedelta(hours=25)
    assert finish(client,a).status_code==409
    patch.setenv('ENVIRONMENT','production')
    assert client.get(PREFIX+'/catalog').status_code==404
    patch.setenv('ENVIRONMENT','test');patch.setenv('CHEMISTRY_PREVIEW_ENABLED','false')
    assert client.get(PREFIX+'/catalog').status_code==404


def test_parallel_completes_are_atomic_and_once_only(chemistry):
    client,factory,_=chemistry;a=start(client);b=start(client)
    answer_all(client,a);answer_all(client,b)
    def complete(attempt):
        with factory() as db:return runtime.complete(db,1,attempt['attempt_id'])
    with ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(complete,[a,b]))
    assert sum(r['xp_awarded'] for r in results)==20
    with factory() as db:assert db.get(User,1).xp_total==20


def test_missing_source_prerequisite_never_unlocks_later_import(chemistry):
    client,factory,_=chemistry
    gap_sequence=max(l['sequence'] for l in load_lessons() if l['grade']==7)+2
    with factory.begin() as db:
        db.add(ChemistryLesson(key='test-only-gap',subject='kimyo',grade=7,sequence=gap_sequence,revision=1,
            topic_id='test-only-gap',content_sha256='0'*64,title='Synthetic test gap',content={'source_refs':[]}))
    rows=client.get(PREFIX+'/catalog').json()['lessons']
    assert next(r for r in rows if r['key']=='test-only-gap')['state']=='locked'
    r=client.post(PREFIX+'/lessons/test-only-gap/start',json={'assessment_version':2,'request_id':str(uuid4())})
    assert r.status_code==403


def test_import_is_explicit_immutable_and_schema_is_not_legacy_startup(chemistry):
    _,factory,_=chemistry;l=load_lessons()[0]
    assert not set(ChemistryBase.metadata.tables)&set(Base.metadata.tables)
    with factory.begin() as db:
        assert import_lesson(db,l)['created'] is False
        bad=deepcopy(l);bad['content']['cards'][0]['body']='Unreviewed replacement'
        with pytest.raises(ValueError):import_lesson(db,bad)


def test_dry_run_does_not_import_db_even_with_a_production_url(tmp_path):
    source="import runpy,sys; runpy.run_module('scripts.import_chemistry_curriculum',run_name='__main__'); assert 'services.db' not in sys.modules; assert 'services.models' not in sys.modules"
    env={**os.environ,'ENVIRONMENT':'production','DATABASE_URL':'postgresql://invalid.example/production','PYTHONIOENCODING':'utf-8'}
    r=subprocess.run([sys.executable,'-c',source],cwd=DIRECTORY.parents[2],env=env,capture_output=True,text=True)
    assert r.returncode==0,r.stderr


def test_mobile_fixtures_come_from_the_real_authoritative_api(chemistry):
    client,_,_=chemistry
    catalog=client.get(PREFIX+'/catalog').json()
    attempt=start(client)
    public=deepcopy(attempt)
    answers={}
    for i,q in enumerate(load_lessons()[0]['assessments']):
        response=send(client,attempt,q,answer_for(q,correct=i!=0))
        assert response.status_code==200,response.text
        answers[q['key']]=response.json()
    result=finish(client,attempt).json()
    assert (result['score'],result['total'],result['xp_awarded'])==(11,12,20)
    assert all('grading_spec' not in json.dumps(p) for p in (catalog,public,answers,result))
    # Optional explicit fixture refresh; never exports JWTs, private specs or DBs.
    target=os.getenv('CHEMISTRY_WRITE_MOBILE_FIXTURES')
    if target:
        directory=Path(target);directory.mkdir(parents=True,exist_ok=True)
        sid='chv2:900003:11111111-1111-4111-8111-111111111111'
        public['attempt_id']=sid;public['expires_at']='2099-01-01T00:00:00+00:00'
        result['attempt_id']=sid;result['elapsed_seconds']=180
        for name,value in [('catalog',catalog),('lesson',public),('results',{'answers':answers,'result':result})]:
            (directory/f'chemistry_{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
