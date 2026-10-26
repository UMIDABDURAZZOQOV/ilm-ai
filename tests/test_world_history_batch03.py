"""Reviewed grade6 paragraphs12–16: new facts cannot weaken prior source gates."""
from copy import deepcopy
from uuid import uuid4

import pytest

from test_world_history_lesson import history, PREFIX, answer_for, send, finish  # noqa: F401
from services.world_history_lessons import load_lessons, validate_lesson
from services.world_history_validation import DIRECTORY, fingerprint, load_catalog, read_json
from services.chemistry_grading import grade_answer
from services.models import User
from services.world_history_models import WorldHistoryProgress


def test_batch03_exact_coverage_aliases_and_interpretation_limits():
    documents=load_lessons();assert len(documents)==16
    batch=documents[11:16]
    assert [len(d['facts']) for d in batch]==[16,18,14,15,15]
    assert [len(d['content']['cards']) for d in batch]==[10,11,9,8,8]
    assert all(len(d['assessments'])==10 for d in batch)
    assert sum(q['response_kind']=='short_text' for d in batch for q in d['assessments'])==21
    for d,span in zip(batch,[(49,52),(53,57),(57,60),(61,64),(65,68)]):
        assert [r['pdf_pages'][0] for r in d['source_refs']]==list(range(span[0],span[1]+1))
        assert d['source_refs'][0]['regions']==['below_topic_heading']
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])
        assert not any(r['automatic_score'] for r in d['content']['reflections'])
    assert batch[1]['source_refs'][-1]['regions']==['above_next_heading']
    assert batch[-1]['source_refs'][-1]['regions']==['above_next_heading']
    assert not batch[0]['facts']['law-claims']['automatic_assessment_allowed']
    assert not batch[0]['facts']['conquest-scope']['automatic_assessment_allowed']
    assert not batch[2]['facts']['road']['automatic_assessment_allowed']
    assert not batch[3]['facts']['brahma-myth']['automatic_assessment_allowed']
    assert not batch[4]['facts']['religion-heading']['automatic_assessment_allowed']
    q=next(q for q in batch[1]['assessments'] if q['grading_spec'].get('expected')=='Xattusa')
    assert grade_answer(q['grading_spec'],{'value':'Xatusa'})=='correct'
    assert grade_answer(q['grading_spec'],{'value':'Tushpa'})=='incorrect'


@pytest.mark.parametrize('number',[12,13,14,15,16])
def test_batch03_cannot_relax_shared_opening_page_scope(number):
    d=deepcopy(load_lessons()[number-1]);r=read_json(DIRECTORY/f'grade6_paragraph{number:02d}_review.json')
    d['source_refs'][0]['regions']=['topic_body'];r['source_pages'][0]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_distinct_buddha_names_cannot_become_an_unreviewed_alias_for_every_question():
    d=deepcopy(load_lessons()[15]);r=read_json(DIRECTORY/'grade6_paragraph16_review.json')
    q=d['assessments'][-1];q['grading_spec']['aliases'].append('Sidhartha Gautama')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_all_sixteen_follow_prerequisites_and_award320_once(history):
    client,factory,_=history;documents=load_lessons()
    assert client.post(f"{PREFIX}/lessons/{documents[11]['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())}).status_code==403
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
        assert db.get(User,1).xp_total==320
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==16
        assert db.get(User,42).xp_total==137
    catalog=client.get(PREFIX+'/catalog').json()
    assert catalog['implemented_sections']==16 and catalog['source_sections']==46
    assert all(r['state']=='completed' for r in catalog['lessons'])
    assert not catalog['grade_content_complete'] and not catalog['course_complete']
