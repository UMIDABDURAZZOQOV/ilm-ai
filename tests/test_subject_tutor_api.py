"""Owned database API integration; provider is synthetic, not live inference."""
import asyncio
from uuid import uuid4
import pytest
from services import study_help, subject_tutor
from tests.test_integrated_beta import beta_api  # noqa: F401


@pytest.mark.parametrize('subject,grade,question', [
    ('biologiya',6,'Botanika nimani o‘rganadi?'),
    ('fizika',6,'Fizika nimani o‘rganadi?'),
    ('kimyo',7,'Modda nima?'),
    ('jahon_tarixi',6,'Qadimgi tarix haqida tushuntir'),
    ('ozbekiston_tarixi',7,'Tarix haqida tushuntir'),
])
def test_real_catalogue_conversation_and_followup(beta_api,monkeypatch,subject,grade,question):  # noqa: F811
    client,factory,account,_=beta_api
    from services.models import User
    with factory() as db:
        user=db.get(User,account['user_id']);user.age=25;db.commit()
    calls=[]
    class Provider:
        requires_adult_profile=True
        def chat(self,context):
            calls.append(context)
            assert context['evidence'] and context['subject']==subject
            assert all('grading_spec' not in e for e in context['evidence'])
            return dict(status='answered',paragraphs=[dict(text=context['evidence'][0]['text'],evidence_ids=['e1'])])
    monkeypatch.setattr(study_help,'_provider',Provider())
    study_help._requests.clear()
    body=dict(subject=subject,grade=grade,message=question,
              conversation_id=str(uuid4()),request_id=str(uuid4()))
    before=client.get(f"/beta/skills/{account['user_id']}/profile").json()
    first=client.post('/beta/subject-chat',json=body)
    assert first.status_code==200,first.text
    assert first.json()['status']=='answered'
    assert client.post('/beta/subject-chat',json=body).json()==first.json()
    assert len(calls)==1
    body.update(message='Yana soddaroq tushuntir',request_id=str(uuid4()))
    followup=client.post('/beta/subject-chat',json=body)
    assert followup.status_code==200,followup.text
    assert calls[-1]['message']==body['message'] and len(calls[-1]['history'])==2
    after=client.get(f"/beta/skills/{account['user_id']}/profile").json()
    assert after['xp_total']==before['xp_total']
    subject_tutor._conversations.clear()


def test_slow_chat_retrieval_does_not_block_health(beta_api, monkeypatch):
    import anyio
    import httpx
    import threading
    client, _, _, _ = beta_api
    started, finished = threading.Event(), threading.Event()
    def slow_retrieve(*args):
        started.set()
        assert finished.wait(5), 'health could not run while retrieval was busy'
        return dict(subject='kimyo', grade=7, message='Modda nima?', question='Modda nima?',
                    history=[], external_ai_eligible=True, evidence=[])
    monkeypatch.setattr(subject_tutor, 'retrieve', slow_retrieve)
    monkeypatch.setattr(study_help, '_provider', None)
    study_help._requests.clear()
    async def scenario():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=client.app),
                base_url='http://127.0.0.1:8930', headers=dict(client.headers)) as api:
            async def chat():
                response = await api.post('/beta/subject-chat', json=dict(subject='kimyo', grade=7,
                    message='Modda nima?', conversation_id=str(uuid4()), request_id=str(uuid4())))
                assert response.status_code == 200
            async with anyio.create_task_group() as group:
                group.start_soon(chat)
                try:
                    with anyio.fail_after(3):
                        while not started.is_set():
                            await anyio.sleep(.01)
                        assert (await api.get('/health')).status_code == 200
                finally:
                    finished.set()
    anyio.run(scenario)


def test_subject_chat_report_reuses_server_answer_and_authenticates_owner(beta_api, monkeypatch):
    client, factory, account, _ = beta_api
    from services.ai_answer_report_models import AiAnswerReport
    from tests.test_ai_answer_reports import install_report_table

    install_report_table(factory.kw['bind'])

    class Provider:
        def chat(self, context):
            return dict(status='answered', model='synthetic-model', http_status=200,
                        paragraphs=[dict(text=context['evidence'][0]['text'], evidence_ids=['e1'])])

    def retrieve(*_):
        return dict(subject='kimyo', grade=7, message='PRIVATE synthetic question',
                    evidence=[{'id': 'e1', 'text': 'Synthetic reply'}], external_ai_eligible=True)

    monkeypatch.setattr(study_help, '_provider', Provider())
    monkeypatch.setattr(subject_tutor, 'retrieve', retrieve)
    study_help._requests.clear()
    body = dict(subject='kimyo', grade=7, message='Modda nima?',
                conversation_id=str(uuid4()), request_id=str(uuid4()))
    response = client.post('/beta/subject-chat', json=body, headers={'X-ILM-AI-Report': 'v1'})
    assert response.status_code == 200
    data = dict(receipt=response.json()['report_receipt'], paragraphs=['Synthetic reply'])
    response = client.post('/beta/ai-answer-report', json=data)
    assert response.status_code == 200 and response.json() == {'reported': True}
    with factory() as db:
        report = db.query(AiAnswerReport).filter_by(user_id=account['user_id']).one()
        assert report.paragraphs == ['Synthetic reply']


def test_cancelled_retrieval_releases_turn_for_retry(beta_api, monkeypatch):
    import anyio
    from routers.beta_mobile import beta_db, create_router

    client, factory, account, _ = beta_api
    payload = dict(subject='kimyo', grade=7, message='Modda nima?',
                   conversation_id=str(uuid4()), request_id=str(uuid4()))
    router = create_router('/beta', beta_db)
    endpoint = next(route.endpoint for route in router.routes
                    if getattr(route, 'path', None) == '/beta/subject-chat')

    def cancelled(*args):
        raise asyncio.CancelledError

    async def cancel_before_provider():
        # Exercise the handler itself. Starlette's TestClient removes task
        # cancellation details when the cancelled handler has no HTTP response.
        with factory() as db, pytest.raises(asyncio.CancelledError):
            await endpoint(subject_tutor.ChatRequest(**payload), None, db, account['user_id'])

    with monkeypatch.context() as patch:
        patch.setattr(subject_tutor, 'retrieve', cancelled)
        anyio.run(cancel_before_provider)

    monkeypatch.setattr(study_help, '_provider', None)
    response = client.post('/beta/subject-chat', json=payload)
    assert response.status_code == 200, response.text
    assert response.json()['status'] == 'unavailable'
