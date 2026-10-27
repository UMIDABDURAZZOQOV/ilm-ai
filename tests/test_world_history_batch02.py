"""Source-reviewed grade6 paragraphs7–11; common objective assessment contract."""
from copy import deepcopy
from uuid import uuid4

import pytest

from test_world_history_lesson import history, PREFIX, answer_for, send, finish  # noqa: F401
from services.world_history_lessons import load_lessons, validate_lesson
from services.world_history_validation import DIRECTORY, fingerprint, load_catalog, read_json
from services.chemistry_grading import grade_answer
from services.models import User
from services.world_history_models import WorldHistoryProgress


def test_batch02_complete_exact_page_and_taught_content_coverage():
    lessons=load_lessons();assert len(lessons)>=11
    batch=lessons[6:11]
    assert [d['sequence'] for d in batch]==list(range(7,12))
    assert [len(d['facts']) for d in batch]==[12,13,13,14,20]
    assert [len(d['content']['cards']) for d in batch]==[7,8,9,8,12]
    assert [len(d['assessments']) for d in batch]==[8,10,8,9,11]
    assert sum(q['response_kind']=='short_text' for d in batch for q in d['assessments'])==17
    for d,span in zip(batch,[(32,34),(35,37),(37,39),(40,42),(43,48)]):
        assert [r['pdf_pages'][0] for r in d['source_refs']]==list(range(span[0],span[1]+1))
        assert d['source_refs'][0]['regions']==['below_topic_heading']
        assert all(d['facts'][i]['automatic_assessment_allowed'] for q in d['assessments'] for i in q['fact_ids'])
        assert len(d['content']['reflections'])==1 and not d['content']['reflections'][0]['automatic_score']
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
    assert batch[1]['source_refs'][-1]['regions']==['above_next_heading']
    assert not batch[-1]['facts']['legend']['automatic_assessment_allowed']
    assert not batch[-1]['facts']['army']['automatic_assessment_allowed']
    assert not batch[-2]['facts']['calendar']['automatic_assessment_allowed']
    assert not batch[-2]['facts']['sign-count']['automatic_assessment_allowed']


@pytest.mark.parametrize('number',[7,8,9,10,11])
def test_new_topic_opening_cannot_include_previous_paragraph(number):
    d=deepcopy(load_lessons()[number-1]);r=read_json(DIRECTORY/f'grade6_paragraph{number:02d}_review.json')
    d['source_refs'][0]['regions']=['topic_body'];r['source_pages'][0]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_shumer_and_akkad_are_not_interchangeable_aliases():
    d=deepcopy(load_lessons()[10]);r=read_json(DIRECTORY/'grade6_paragraph11_review.json')
    q=d['assessments'][1];q['grading_spec']['verified_answer']='Akkad'
    q['grading_spec']['expected']='a'
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_all_eleven_real_lessons_unlock_in_order_and_award220_once(history):
    client,factory,_=history;lessons=load_lessons()[:11]
    blocked=client.post(f"{PREFIX}/lessons/{lessons[6]['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
    assert blocked.status_code==403
    for d in lessons:
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
        assert db.get(User,1).xp_total==220
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==11
        assert db.get(User,42).xp_total==137
    catalog=client.get(PREFIX+'/catalog').json()
    assert catalog['implemented_sections']==len(load_lessons()) and catalog['source_sections']==46
    assert all(row['state']=='completed' for row in catalog['lessons'][:11])
    assert all(row['state']!='completed' for row in catalog['lessons'][11:])
    assert not catalog['course_complete'] and catalog['grade_content_complete']
