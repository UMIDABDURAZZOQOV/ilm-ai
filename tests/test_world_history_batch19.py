"""Grade8 begins with its own 2019 source, prerequisites and original exercises."""
from copy import deepcopy
from uuid import uuid4

import pytest

from test_world_history_lesson import history, PREFIX, answer_for, send, finish  # noqa: F401
from services.world_history_lessons import load_lessons, validate_lesson
from services.world_history_validation import DIRECTORY, fingerprint, load_catalog, read_json
from services.chemistry_grading import grade_answer
from services.models import User
from services.world_history_models import WorldHistoryProgress


def batch():
    return [d for d in load_lessons() if d['grade']==8 and d['sequence']<=5]


def test_grade8_first_batch_original_order_bibliography_and_ungraded_interpretations():
    ds=batch()
    assert [d['sequence'] for d in ds]==[1,2,3,4,5]
    assert [len(d['facts']) for d in ds]==[23,14,12,17,19]
    assert [len(d['content']['cards']) for d in ds]==[11,8,8,9,9]
    assert [len(d['assessments']) for d in ds]==[14,12,12,14,14]
    assert ds[0]['prerequisite_ids']==[] and ds[0]['source_context_ids']==['wh8-intro']
    assert sum(q['response_kind']=='short_text' for d in ds for q in d['assessments'])==20
    for d in ds:
        assert d['book_id']=='world-history-8-uz-2019'
        assert all(ref['year']==2019 and ref['grade']==8 for ref in d['source_refs'])
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
    for n,identifier in [(0,'period'),(0,'motives'),(1,'classes'),(1,'change'),(2,'effects'),(2,'conflict'),(3,'bruno'),(3,'culture'),(4,'context'),(4,'results')]:
        assert not ds[n]['facts'][identifier]['automatic_assessment_allowed']
    assert 13 not in [p for ref in ds[0]['source_refs'] for p in ref['pdf_pages']]
    assert 18 not in [p for ref in ds[1]['source_refs'] for p in ref['pdf_pages']]
    assert 28 not in [p for ref in ds[3]['source_refs'] for p in ref['pdf_pages']]


@pytest.mark.parametrize('number,ending',[(1,False),(2,False),(3,False),(4,False),(5,False),(3,True),(5,True)])
def test_grade8_shared_original_page_regions_cannot_expand(number,ending):
    d=deepcopy(batch()[number-1]);r=read_json(DIRECTORY/f'grade8_paragraph{number:02d}_review.json')
    index=(4 if number==1 else -1) if ending else 0
    d['source_refs'][index]['regions']=['topic_body'];r['source_pages'][index]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_grade8_finite_names_and_regnal_numbers_are_not_fuzzy_aliases():
    ds=batch()
    for n,index,wrong in [(0,12,'Bartolomeu Diash'),(1,8,'Birja'),(2,8,'Jan Kalvin'),(3,10,'Tomas Myunser'),(4,11,'Karl I'),(4,12,'Jamoa palatasi')]:
        assert grade_answer(ds[n]['assessments'][index]['grading_spec'],{'value':wrong})=='incorrect'
    d=deepcopy(ds[4]);r=read_json(DIRECTORY/'grade8_paragraph05_review.json')
    d['assessments'][11]['grading_spec']['aliases'].append('Karl I')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_uncertain_cosmology_and_ideology_cannot_become_automatic_keys():
    d=deepcopy(batch()[3]);r=read_json(DIRECTORY/'grade8_paragraph04_review.json')
    d['assessments'][0]['fact_ids']=['bruno']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][0]['key']]['fact_ids']=['bruno']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_grade8_starts_independently_preserving_grade6_and_grade7_progress(history):
    client,factory,_=history;ds=batch()
    initial=client.get(PREFIX+'/catalog',params={'grade':8}).json()
    assert initial['source_sections']==33 and initial['implemented_sections']==sum(d['grade']==8 for d in load_lessons())
    assert initial['implemented_grades']==sorted({d['grade'] for d in load_lessons()})
    assert initial['lessons'][0]['state']=='available'
    assert all(r['state']=='locked' for r in initial['lessons'][1:])
    assert client.post(f"{PREFIX}/lessons/{ds[1]['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())}).status_code==403
    response=client.post(f"{PREFIX}/lessons/{ds[0]['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
    assert response.status_code==200;attempt=response.json()
    assert all(ref['grade']==8 and ref['year']==2019 for ref in attempt['content']['source_refs'])
    for q in ds[0]['assessments']:assert send(client,attempt,q,answer_for(q)).json()['is_correct']
    result=finish(client,attempt);assert result.json()['xp_awarded']==20
    assert finish(client,attempt).json()==result.json()
    for grade in [6,7]:
        catalog=client.get(PREFIX+'/catalog',params={'grade':grade}).json()
        assert catalog['lessons'][0]['state']=='available'
        assert all(row['state']!='completed' for row in catalog['lessons'])
    with factory() as db:
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==1
        assert db.get(User,1).xp_total==20 and db.get(User,42).xp_total==137


def test_all95_lessons1900_xp_once_preserve_completed_earlier_grades(history):
    client,factory,_=history;documents=load_lessons()[:95]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        result=finish(client,attempt);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==1900
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==95
        assert db.get(User,42).xp_total==137
    for grade in [6,7]:
        catalog=client.get(PREFIX+'/catalog',params={'grade':grade}).json()
        assert catalog['grade_content_complete'] and all(r['state']=='completed' for r in catalog['lessons'])
        assert not catalog['course_complete']
    eight=client.get(PREFIX+'/catalog',params={'grade':8}).json()
    assert all(r['state']=='completed' for r in eight['lessons'][:5])
    assert all(r['state']!='completed' for r in eight['lessons'][5:])
    assert eight['grade_content_complete']==(eight['implemented_sections']==33)
    assert not eight['course_complete']
