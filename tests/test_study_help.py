"""Study help uses disposable reviewed DB copies; never the phone's data."""
import json
from uuid import uuid4

import pytest
from tests.test_integrated_beta import beta_api, correct_answer


def ask(client, **kwargs):
    return client.post('/beta/study-help', json=dict(language='uz', **kwargs))


def test_all_four_v2_subjects_preanswer_feedback_and_no_progress_writes(beta_api):
    from services.models import StudySession, StudyEvent
    from services import beta_curriculum as beta
    client,factory,account,_=beta_api
    for subject,grade in [('fizika',6),('kimyo',7),('jahon_tarixi',6),('ozbekiston_tarixi',7)]:
        with factory() as db:
            before=db.query(StudyEvent).count()
        catalog=client.get(f'/beta/v2/{subject}/catalog',params={'grade':grade}).json()
        key=catalog['lessons'][0]['key']
        issued=client.post(f'/beta/v2/{subject}/lessons/{key}/start',json={'assessment_version':2,'request_id':str(uuid4())}).json()
        q=issued['questions'][0]
        params=dict(subject=subject,grade=grade,lesson_key=key,attempt_id=issued['attempt_id'],question_key=q['key'])
        before_answer=ask(client,**params)
        assert before_answer.status_code==200,before_answer.text
        body=before_answer.json()
        assert body['attempt_id']==issued['attempt_id'] and body['question_key']==q['key']
        assert body['provider_status']=='unconfigured' and not body['answered']
        assert body['evidence'] and body['source_refs']
        assert all(s['kind'] not in {'answer','solution','feedback'} for s in body['evidence'])
        assert 'grading_spec' not in before_answer.text and '"expected"' not in before_answer.text
        with factory() as db:
            raw=db.get(StudySession,issued['attempt_id']).questions['assessments'][0]
        submitted=client.post(f"/beta/v2/{subject}/attempts/{issued['attempt_id']}/answers",json={
            'assessment_version':2,'assessment_key':q['key'],'answer':correct_answer(raw)})
        assert submitted.status_code==200,submitted.text
        after=ask(client,**params,message='Yechimni tushuntir').json()
        assert after['answered'] and after['is_correct'] is True
        if q['response_kind']=='concept_selection':
            assert sum(o['matches_key'] for o in after['option_reviews'])==1
        assert any(s['kind']=='feedback' for s in after['evidence'])
        assert all(s['source_refs'] for s in after['evidence'])
        with factory() as db:
            assert db.query(StudyEvent).count()==before


def test_question_ownership_context_locked_lessons_and_existing_gates(beta_api,monkeypatch):
    from services import study_help
    study_help._requests.clear()
    client,_,account,_=beta_api
    catalog=client.get('/beta/v2/fizika/catalog',params={'grade':6}).json()
    key=catalog['lessons'][0]['key']
    issued=client.post(f'/beta/v2/fizika/lessons/{key}/start',json={'assessment_version':2,'request_id':str(uuid4())}).json()
    context=dict(subject='fizika',grade=6,attempt_id=issued['attempt_id'],question_key=issued['questions'][0]['key'])
    assert ask(client,**context).status_code==200
    assert ask(client,**dict(context,grade=7)).status_code==409
    assert ask(client,**dict(context,question_key='foreign')).status_code==404
    assert ask(client,**dict(context,attempt_id='v2:someone-else')).status_code==404
    assert ask(client,subject='fizika',grade=6,lesson_key=catalog['lessons'][1]['key']).status_code==403
    assert ask(client,subject='fizika',grade=6,correct_answer='client-injected').status_code==422
    auth=client.headers.pop('Authorization')
    assert ask(client,subject='fizika',grade=6).status_code==401
    client.headers['Authorization']=auth
    monkeypatch.setenv('PHYSICS_PREVIEW_ENABLED','false')
    assert ask(client,**context).status_code==404
    assert client.post('/skills/tutor/explain',json={}).status_code==404


def test_numeric_frq_and_mcq_correct_and_wrong_use_the_original_grader(beta_api):
    from services import study_help
    from services.models import StudySession
    from tests.test_physics_course import new_answer
    study_help._requests.clear()
    client,factory,_,_=beta_api
    key=client.get('/beta/v2/fizika/catalog',params={'grade':7}).json()['lessons'][0]['key']
    for correct in (True,False):
        issued=client.post(f'/beta/v2/fizika/lessons/{key}/start',json={'assessment_version':2,'request_id':str(uuid4())}).json()
        with factory() as db:
            raw=db.get(StudySession,issued['attempt_id']).questions['assessments']
        assert any(q['kind']=='numeric_quantity' for q in raw)
        for question in raw:
            answer=new_answer({'topic_id':'physics-7-section-1','sequence':1},question)
            if not correct:
                if question['kind']=='numeric_quantity': answer['value']='9999'
                else: answer['choice_id']=next(o['id'] for o in question['public']['options'] if o['id']!=answer['choice_id'])
            submitted=client.post(f"/beta/v2/fizika/attempts/{issued['attempt_id']}/answers",json={
                'assessment_version':2,'assessment_key':question['key'],'answer':answer})
            assert submitted.status_code==200,submitted.text
            assert submitted.json()['is_correct'] is correct
            response=ask(client,subject='fizika',grade=7,attempt_id=issued['attempt_id'],question_key=question['key'])
            assert response.status_code==200,response.text
            assert response.json()['is_correct'] is correct
            steps=[s['text'] for s in response.json()['evidence'] if s['kind']=='solution']
            assert steps==[s['body'] for s in submitted.json()['solution']]


def test_biology_lesson_and_daily_use_owned_issued_reviewed_questions(beta_api):
    from services import study_help
    study_help._requests.clear()
    client,_,account,_=beta_api
    outline=client.get(f"/beta/skills/{account['user_id']}/curriculum",params={'subject':'biologiya','grade':5}).json()
    lesson=outline['chapters'][0]['topics'][0]['lesson_ids'][0]
    issued=client.post(f'/beta/skills/lessons/{lesson}/start',json={'user_id':account['user_id'],'language':'uz'}).json()
    q=issued['questions'][0]
    context=dict(subject='biologiya',attempt_id=f"lesson:{issued['attempt_id']}",question_key=str(q['id']))
    before=ask(client,**context)
    assert before.status_code==200,before.text
    assert before.json()['grade']==5 and not before.json()['answered']
    for selected,correct in [(q['correct_answer'],True),(next(o for o in q['options'] if o!=q['correct_answer']),False)]:
        result=ask(client,**context,checked=True,selected_answer=selected)
        assert result.status_code==200,result.text
        assert result.json()['is_correct'] is correct
    assert ask(client,**dict(context,grade=7)).status_code==409
    result=ask(client,subject='biologiya',grade=5)
    assert result.status_code==200,result.text
    daily=client.get(f"/beta/skills/{account['user_id']}/daily-challenge").json()
    q=daily['questions'][0]
    result=ask(client,subject='biologiya',attempt_id=daily['attempt_id'],question_key=str(q['id']))
    assert result.status_code==200,result.text


def test_provider_output_is_only_whitelisted_evidence_and_no_environment_key(monkeypatch):
    from services.study_help import HelpRequest, respond, configure_provider
    from services import study_help
    context=dict(subject='kimyo',grade=7,source_refs=[{'book_id':'reviewed','printed_pages':[5]}],
        evidence=[{'id':'e1','kind':'feedback','text':'Verified explanation','source_refs':[{'printed_pages':[5]}]}])
    request=HelpRequest(subject='kimyo',grade=7)
    configure_provider()
    monkeypatch.setenv('OPENAI_API_KEY','must-not-be-used')
    assert respond(context,request)['provider_status']=='unconfigured'
    class FakeSelector:
        def select(self,context):
            return ['invented']
    monkeypatch.setattr(study_help,'_provider',FakeSelector())
    result=respond(context,request)
    assert result['provider_status']=='unavailable' and result['evidence']==context['evidence']
    assert 'api_key' not in json.dumps(result)


def test_request_bounds_and_private_configuration(tmp_path):
    from services.study_help import HelpRequest, configure_provider
    from pydantic import ValidationError
    for kwargs in [dict(subject='matematika',grade=7),dict(subject='kimyo',grade=4),
                   dict(subject='kimyo',question_key='q'),dict(subject='kimyo',grade=7,message='x'*1001)]:
        with pytest.raises(ValidationError): HelpRequest(**kwargs)
    configure_provider()
    with pytest.raises(ValueError): configure_provider(__file__)


@pytest.mark.parametrize('ids', [['missing'], ['e1', 'e1'], 'e1', [1], ['e1'] * 13, None])
def test_invalid_selected_ids_never_replace_reviewed_evidence(monkeypatch, ids):
    from services import study_help
    class Selector:
        def select(self, context):
            return ids
    monkeypatch.setattr(study_help, '_provider', Selector())
    evidence = [dict(id='e1', kind='feedback', text='Reviewed grader explanation', source_refs=[{'page': 5}])]
    selected, status = study_help.select_evidence(dict(evidence=evidence), 'private student message', 'uz')
    assert selected == evidence and status == 'unavailable'


def test_valid_selection_preserves_required_grader_feedback(monkeypatch):
    from services import study_help
    class Selector:
        def select(self, context):
            return ['e2']
    monkeypatch.setattr(study_help, '_provider', Selector())
    evidence = [dict(id='e1', kind='feedback', text='Reviewed feedback'),
                dict(id='e2', kind='cards', text='Reviewed teaching material')]
    selected, status = study_help.select_evidence(dict(evidence=evidence), 'ignored free-form text', 'uz')
    assert selected == evidence and status == 'selected'


def test_provider_wait_does_not_hold_the_request_database_connection(beta_api, monkeypatch):
    from services import study_help
    client, factory, _, _ = beta_api
    engine = factory.kw['bind']
    observed = []
    class Selector:
        def select(self, context):
            observed.append(engine.pool.checkedout())
            return [context['evidence'][0]['id']]
    monkeypatch.setattr(study_help, '_provider', Selector())
    result = ask(client, subject='kimyo', grade=7)
    assert result.status_code == 200, result.text
    assert result.json()['provider_status'] == 'selected'
    assert observed == [0]
