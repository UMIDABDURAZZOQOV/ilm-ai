"""Real integrated contracts on owned SQLite and fresh PostgreSQL schemas."""
import hashlib
import json
import os
from pathlib import Path
import secrets
import sqlite3
from uuid import uuid4

import pytest
from scripts import serve_mobile_beta as server


@pytest.fixture(scope='module', params=['sqlite','postgres'])
def beta_api(request, tmp_path_factory):
    path=tmp_path_factory.mktemp('integrated-'+request.param)/'owned'
    server.configure(path,False,8930)
    from services import db as database, tokens, users, mobile_oauth
    from services.beta_models import BetaBase
    from sqlalchemy import create_engine,text
    from sqlalchemy.engine import make_url
    from sqlalchemy.orm import sessionmaker
    patch=pytest.MonkeyPatch()
    patch.setattr(tokens,'JWT_SECRET',os.environ['JWT_SECRET'])
    admin=None
    if request.param=='postgres':
        filename=os.getenv('ILM_TEST_POSTGRES_URL_FILE')
        if not filename: pytest.skip('Explicit local PostgreSQL staging URL file is required')
        url=make_url(Path(filename).read_text().strip())
        assert url.get_backend_name()=='postgresql' and url.host in {'127.0.0.1','localhost'} and 'staging' in url.database
        admin=create_engine(url)
        schema='beta_integration_'+secrets.token_hex(8)
        with admin.begin() as connection: connection.execute(text(f'CREATE SCHEMA "{schema}"'))
        engine=create_engine(url,connect_args={'options':f'-csearch_path={schema}'})
        factory=sessionmaker(bind=engine,autoflush=False,autocommit=False)
        for module in (database,tokens,users,mobile_oauth): patch.setattr(module,'SessionLocal',factory)
        patch.setattr(database,'engine',engine)
        server.initialize(path,seed_user=False)
    else:
        source=os.getenv('ILM_BETA_REVIEWED_DB_FILE')
        if source:
            source=Path(source)
            assert json.loads((source.parent/'server.json').read_text())['integrated_beta_sandbox']==1
            origin=sqlite3.connect(f'file:{source.as_posix()}?mode=ro',uri=True)
            target=sqlite3.connect(path/server.DB_NAME)
            origin.backup(target); target.close(); origin.close()
        else:
            server.initialize(path,seed_user=False)
        engine=database.engine
        factory=database.SessionLocal
    BetaBase.metadata.create_all(engine)
    from starlette.testclient import TestClient
    client=TestClient(server.create_app(),base_url='http://127.0.0.1:8930',client=('127.0.0.1',12345))
    secret=secrets.token_urlsafe(32)
    response=client.post('/beta/auth/test-login',json={'installation_secret':secret})
    assert response.status_code==200,response.text
    account=response.json()
    client.headers['Authorization']='Bearer '+account['access_token']
    yield client,factory,account,secret
    client.close(); engine.dispose(); patch.undo()
    if admin: admin.dispose()


def test_catalogue_counts_and_grade_filter_are_real(beta_api):
    client,_,_,_=beta_api
    data=client.get('/beta/skills/subjects').json()
    expected={'biologiya':406,'fizika':316,'kimyo':268,'ozbekiston_tarixi':172,'jahon_tarixi':219}
    assert {s['slug']:s['ready_lessons'] for s in data if s['available']}==expected
    assert {s['slug'] for s in data if not s['available']}=={'matematika','ona_tili'}
    by_grade={5:{'biologiya'},6:{'biologiya','fizika','jahon_tarixi'},7:set(expected),11:set(expected)}
    for grade,subjects in by_grade.items():
        response=client.get('/beta/skills/subjects',params={'grade':grade})
        assert response.status_code==200,response.text
        assert {s['slug'] for s in response.json() if s['available']}==subjects


def test_all_1381_units_use_normal_path_and_exact_source_order(beta_api):
    client,_,account,_=beta_api
    total=0
    for subject in client.get('/beta/skills/subjects').json():
        if not subject['available']: continue
        slug=subject['slug']
        grades=client.get(f'/beta/skills/subjects/{slug}/grades')
        assert grades.status_code==200,grades.text
        for grade in grades.json()['grades']:
            response=client.get(f"/beta/skills/{account['user_id']}/tree",params={'subject':slug,'grade':grade['grade']})
            assert response.status_code==200,(slug,grade,response.text)
            tree=response.json()
            lessons=[lesson for unit in tree['units'] for lesson in unit['lessons']]
            assert len(lessons)==grade['ready_lessons']
            total+=len(lessons)
            if slug!='biologiya':
                assert [l['order_index'] for l in lessons]==list(range(1,len(lessons)+1))
                assert len({l['assessment_key'] for l in lessons})==len(lessons)
                assert all(l['source_refs'] and l['assessment_subject']==slug for l in lessons)
                assert lessons[0]['status']=='unlocked'
                assert all(l['status']=='locked' for l in lessons[1:])
                assert all(u['exam']['status']=='none' for u in tree['units'])
    assert total==1381
    assert client.get(f"/beta/skills/{account['user_id']}/tree",params={'subject':'fizika','grade':5}).status_code==404
    assert client.get('/beta/skills/subjects/matematika/grades').status_code==404


def test_profile_settings_preferences_and_account_ownership(beta_api):
    client,_,account,_=beta_api
    uid=account['user_id']
    response=client.post(f'/beta/skills/{uid}/preferences',json={'subject':'fizika','grade':'6','daily_goal_xp':20})
    assert response.status_code==200,response.text
    assert client.get(f'/beta/skills/{uid}/preferences').json()['preferences']['subject']=='fizika'
    assert client.post(f'/beta/skills/{uid}/preferences',json={'subject':'matematika'}).status_code==422
    assert client.get(f'/beta/skills/{uid+100000}/profile').status_code==403
    response=client.post('/auth/complete-onboarding',json={'user_id':uid,'name':'Beta learner','age':14})
    assert response.status_code==200,response.text
    assert client.get(f'/auth/profile/{uid}').json()['age']==14
    profile=client.get(f'/beta/skills/{uid}/profile')
    assert profile.status_code==200,profile.text
    assert len(profile.json()['subjects'])==5
    assert profile.json()['lessons_completed']==0


def correct_answer(question):
    spec=question['grading_spec']
    if spec['kind']=='concept_selection':
        return {'choice_id':spec.get('expected',spec.get('expected_choice'))}
    if spec['kind']=='short_text':
        return {'value':spec.get('expected',spec['aliases'][0])}
    if spec['kind']=='ordering':
        return {'order':spec.get('expected',spec.get('expected_order'))}
    raise AssertionError(('unexpected first paragraph question',spec['kind']))


def test_all_subjects_real_grading_resume_once_only_xp_and_shared_profile(beta_api):
    client,factory,account,_=beta_api
    uid=account['user_id']
    from services.models import StudySession
    awarded=0
    for slug,grade in [('fizika',6),('kimyo',7),('ozbekiston_tarixi',7),('jahon_tarixi',6)]:
        path=client.get(f'/beta/skills/{uid}/tree',params={'subject':slug,'grade':grade}).json()
        key=path['units'][0]['lessons'][0]['assessment_key']
        prefix=f'/beta/v2/{slug}'
        request=str(uuid4())
        response=client.post(f'{prefix}/lessons/{key}/start',json={'assessment_version':2,'request_id':request})
        assert response.status_code==200,response.text
        assert 'grading_spec' not in response.text and 'verified_answer' not in response.text
        attempt=response.json()
        assert attempt['content']['cards'] and 'examples' in attempt['content']
        with factory() as db:
            questions=db.get(StudySession,attempt['attempt_id']).questions['assessments']
        for index,q in enumerate(questions):
            data={'assessment_version':2,'assessment_key':q['key'],'answer':correct_answer(q)}
            answer_path=f"{prefix}/attempts/{attempt['attempt_id']}/answers"
            result=client.post(answer_path,json=data)
            assert result.status_code==200 and result.json()['is_correct'],result.text
            assert client.post(answer_path,json=data).json()==result.json()
            if index==0:
                resumed=client.post(f'{prefix}/lessons/{key}/start',json={'assessment_version':2,'request_id':request})
                assert resumed.json()['attempt_id']==attempt['attempt_id']
                assert q['key'] in resumed.json()['answers']
        completion=f"{prefix}/attempts/{attempt['attempt_id']}/complete"
        done=client.post(completion,json={'assessment_version':2})
        assert done.status_code==200 and done.json()['passed'],done.text
        assert done.json()['stars']==3 and done.json()['elapsed_seconds']>=0
        assert client.post(completion,json={'assessment_version':2}).json()==done.json()
        awarded+=done.json()['xp_awarded']
        fresh=client.get(f'/beta/skills/{uid}/tree',params={'subject':slug,'grade':grade}).json()
        lessons=[l for u in fresh['units'] for l in u['lessons']]
        assert lessons[0]['status']=='completed' and lessons[1]['status']=='unlocked'
    outline=client.get(f'/beta/skills/{uid}/curriculum',params={'subject':'biologiya','grade':5}).json()
    lesson=outline['chapters'][0]['topics'][0]['lesson_ids'][0]
    start=client.post(f'/beta/skills/lessons/{lesson}/start',json={'user_id':uid,'language':'uz'})
    assert start.status_code==200,start.text
    issued=start.json()
    data={'user_id':uid,'attempt_id':issued['attempt_id'],'results':[
        {'question_id':q['id'],'answer_index':q['options'].index(q['correct_answer']),'is_correct':False}
        for q in issued['questions']]}
    done=client.post(f'/beta/skills/lessons/{lesson}/complete',json=data)
    assert done.status_code==200,done.text
    awarded+=done.json()['xp_awarded']
    assert client.post(f'/beta/skills/lessons/{lesson}/complete',json=data).json()==done.json()
    profile=client.get(f'/beta/skills/{uid}/profile').json()
    assert profile['lessons_completed']==5 and profile['xp_total']==awarded==80
    assert all(s['completed']==1 for s in profile['subjects'])
    assert sum(profile['activity'].values())==5


def test_runtime_login_restores_same_account_and_auth_refresh(beta_api):
    client,_,account,secret=beta_api
    again=client.post('/beta/auth/test-login',json={'installation_secret':secret})
    assert again.status_code==200,again.text
    assert again.json()['user_id']==account['user_id']
    assert again.json()['needs_onboarding'] is False
    refreshed=client.post('/auth/refresh',json={'refresh_token':again.json()['refresh_token']})
    assert refreshed.status_code==200,refreshed.text
    client.headers['Authorization']='Bearer '+refreshed.json()['access_token']
    assert client.get(f"/beta/skills/{account['user_id']}/profile").json()['xp_total']==80


def test_beta_is_local_only_and_unconfigured_google_is_honest(beta_api,monkeypatch):
    client,_,_,_=beta_api
    assert client.get('/beta/config').json()['google_configured'] is False
    assert client.get('/auth/google-login').status_code==503
    assert client.get('/health',headers={'x-forwarded-for':'127.0.0.1'}).status_code==403
    assert client.get('/health',headers={'host':'example.com'}).status_code==400
    assert client.post('/qa/pair',json={}).status_code==404
    assert client.get('/preview/physics/v2/catalog').status_code==404
    assert client.post('/auth/signup',json={}).status_code==404
    monkeypatch.setenv('BETA_SERVER_MODE','staging')
    assert client.post('/beta/auth/test-login',json={'installation_secret':secrets.token_urlsafe(32)}).status_code==404
    monkeypatch.setenv('ILM_BETA_ENABLED','false')
    assert client.get('/beta/skills/subjects').status_code==404


def test_beta_callback_only_rewrites_the_existing_safe_mobile_return_uri(beta_api,monkeypatch):
    from routers import auth
    from starlette.responses import RedirectResponse
    client,_,_,_=beta_api
    async def existing_callback(*args):
        return RedirectResponse('ilmai://auth/callback?code=one-time-test-code&state=test-state')
    monkeypatch.setattr(auth,'google_callback_mobile',existing_callback)
    result=client.get('/auth/google-callback-mobile',follow_redirects=False)
    assert result.headers['location']=='ilmai-beta://auth/callback?code=one-time-test-code&state=test-state'
    async def unsafe_callback(*args):
        return RedirectResponse('ilmai://auth/callback?access_token=must-never-be-forwarded')
    monkeypatch.setattr(auth,'google_callback_mobile',unsafe_callback)
    assert client.get('/auth/google-callback-mobile',follow_redirects=False).status_code==503


def test_public_attempt_keeps_every_verified_teaching_section(beta_api):
    from services import beta_curriculum as beta
    from services.models import StudySession
    client,factory,_,_=beta_api
    for subject,(runtime,model,_,_) in beta.ADAPTERS.items():
        with factory() as db:
            lesson=db.query(model).order_by(model.grade,model.sequence).first()
            key=lesson.key
        response=client.post(f'/beta/v2/{subject}/lessons/{key}/start',json={
            'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text
        attempt=response.json()
        with factory() as db:
            snapshot=db.get(StudySession,attempt['attempt_id']).questions['content']
        for section in ('cards','formulas','examples','reflections'):
            assert attempt['content'][section]==snapshot.get(section,[])
        assert 'grading_spec' not in response.text and '"expected"' not in response.text
