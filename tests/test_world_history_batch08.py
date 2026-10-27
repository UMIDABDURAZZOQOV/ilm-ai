"""Roman source terminology, legendary dates and unequal historical status."""
from copy import deepcopy
from uuid import uuid4

import pytest

from test_world_history_lesson import history, PREFIX, answer_for, send, finish  # noqa: F401
from services.world_history_lessons import load_lessons, validate_lesson
from services.world_history_validation import DIRECTORY, fingerprint, load_catalog, read_json
from services.chemistry_grading import grade_answer
from services.models import User
from services.world_history_models import WorldHistoryProgress


def test_batch08_exact_counts_and_scoped_source_claims():
    documents=load_lessons()[:41];assert len(documents)==41
    batch=documents[36:41]
    assert [len(d['facts']) for d in batch]==[12,14,15,14,12]
    assert [len(d['content']['cards']) for d in batch]==[6,7,7,6,6]
    assert [len(d['assessments']) for d in batch]==[10]*5
    assert sum(q['response_kind']=='short_text' for d in batch for q in d['assessments'])==20
    for d,span in zip(batch,[(145,147),(148,151),(152,155),(155,159),(160,164)]):
        assert [r['pdf_pages'][0] for r in d['source_refs']]==list(range(span[0],span[1]+1))
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
    for n,identifier in [(0,'climate'),(0,'foundation'),(0,'republic'),(1,'schema'),(1,'inequality'),(2,'city-life'),(2,'other-deities'),(3,'army'),(3,'division'),(4,'coercion'),(4,'spectacle'),(4,'ending')]:
        assert not batch[n]['facts'][identifier]['automatic_assessment_allowed']
    assert batch[3]['assessments'][4]['grading_spec']['verified_answer']=='Kann — Zama — Karfagen'
    assert all('grading_spec' not in str(d['content']) for d in batch)


@pytest.mark.parametrize('number',[37,38,39,40,41])
def test_batch08_cannot_expand_shared_opening_page(number):
    d=deepcopy(load_lessons()[number-1]);r=read_json(DIRECTORY/f'grade6_paragraph{number:02d}_review.json')
    d['source_refs'][0]['regions']=['topic_body'];r['source_pages'][0]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


@pytest.mark.parametrize('number',[39,41])
def test_batch08_cannot_expand_shared_closing_page(number):
    d=deepcopy(load_lessons()[number-1]);r=read_json(DIRECTORY/f'grade6_paragraph{number:02d}_review.json')
    d['source_refs'][-1]['regions']=['topic_body'];r['source_pages'][-1]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_tenants_are_not_gladiators_or_colonies():
    d=load_lessons()[40];q=d['assessments'][6]
    for alias in ['Kolon','Kolonlar']:
        assert grade_answer(q['grading_spec'],{'value':alias})=='correct'
    for wrong in ['Gladiatorlar','Koloniyalar','Konsullar']:
        assert grade_answer(q['grading_spec'],{'value':wrong})=='incorrect'
    d=deepcopy(d);r=read_json(DIRECTORY/'grade6_paragraph41_review.json')
    d['assessments'][6]['grading_spec']['aliases'].append('Koloniyalar')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_all_forty_one_prerequisites_and820_xp_once(history):
    client,factory,_=history;documents=load_lessons()[:41]
    assert client.post(f"{PREFIX}/lessons/{documents[36]['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())}).status_code==403
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text
        attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q))
            assert response.status_code==200 and response.json()['is_correct']
        response=finish(client,attempt);assert response.status_code==200
        assert response.json()['xp_awarded']==20
        assert finish(client,attempt).json()==response.json()
    with factory() as db:
        assert db.get(User,1).xp_total==820
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==41
        assert db.get(User,42).xp_total==137
    catalog=client.get(PREFIX+'/catalog').json()
    assert catalog['implemented_sections']==len(load_lessons()) and catalog['source_sections']==46
    assert all(r['state']=='completed' for r in catalog['lessons'][:41])
    assert all(r['state']!='completed' for r in catalog['lessons'][41:])
    assert catalog['grade_content_complete'] and not catalog['course_complete']
