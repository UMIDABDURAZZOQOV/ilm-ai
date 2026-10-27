"""Grade8 paragraphs6–10 keep chronology, institutions and ordinals scoped."""
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
    return [d for d in load_lessons() if d['grade']==8 and 6<=d['sequence']<=10]


def test_batch20_original_order_counts_and_ungraded_interpretations():
    ds=batch()
    assert [d['sequence'] for d in ds]==[6,7,8,9,10]
    assert [len(d['facts']) for d in ds]==[10,14,10,10,17]
    assert [len(d['content']['cards']) for d in ds]==[7,7,7,6,9]
    assert [len(d['assessments']) for d in ds]==[12,12,12,12,14]
    assert sum(q['response_kind']=='short_text' for d in ds for q in d['assessments'])==20
    for d in ds:
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
    for n,key in [(0,'context'),(0,'consequences'),(1,'republic'),(1,'results'),(2,'meaning'),(3,'economy'),(4,'centralization'),(4,'science'),(4,'culture')]:
        assert not ds[n]['facts'][key]['automatic_assessment_allowed']
    assert 49 not in [p for ref in ds[3]['source_refs'] for p in ref['pdf_pages']]
    assert 54 not in [p for ref in ds[4]['source_refs'] for p in ref['pdf_pages']]


@pytest.mark.parametrize('number,ending',[(6,False),(7,False),(8,False),(9,False),(10,False),(6,True),(7,True),(8,True)])
def test_batch20_exact_shared_page_regions(number,ending):
    d=deepcopy(batch()[number-6]);r=read_json(DIRECTORY/f'grade8_paragraph{number:02d}_review.json')
    index=-1 if ending else 0
    d['source_refs'][index]['regions']=['topic_body'];r['source_pages'][index]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_singular_office_regnal_ordinals_and_places_are_not_aliases():
    ds=batch()
    for n,index,wrong in [(0,9,'Yetti yillik urush'),(1,8,'Kommuna'),(2,10,'Konsullik'),(3,8,'Fridrix II'),(3,9,'Fridrix I'),(4,11,'Ivan III'),(4,12,'Ivan IV')]:
        assert grade_answer(ds[n]['assessments'][index]['grading_spec'],{'value':wrong})=='incorrect'
    d=deepcopy(ds[2]);r=read_json(DIRECTORY/'grade8_paragraph08_review.json')
    d['assessments'][10]['grading_spec']['aliases'].append('Konsullik')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_held_french_chronology_cannot_become_an_automatic_key():
    d=deepcopy(batch()[1]);r=read_json(DIRECTORY/'grade8_paragraph07_review.json')
    d['assessments'][0]['fact_ids']=['republic']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][0]['key']]['fact_ids']=['republic']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_review_requires_exact_original_map_image_digest():
    d=batch()[4];r=read_json(DIRECTORY/'grade8_paragraph10_review.json')
    page=next(p for p in r['source_pages'] if p['pdf_page']==52)
    page['page_image_sha256']='0'*64
    with pytest.raises(ValueError,match='exact_original_page_digest_required'):
        validate_lesson(load_catalog(),d,r)


def test_all100_units2000_xp_once_and_independent_grade_progress(history):
    client,factory,_=history;documents=load_lessons()[:100]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        result=finish(client,attempt);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==2000
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==100
        assert db.get(User,42).xp_total==137
    for grade in [6,7]:
        catalog=client.get(PREFIX+'/catalog',params={'grade':grade}).json()
        assert catalog['grade_content_complete'] and all(r['state']=='completed' for r in catalog['lessons'])
        assert not catalog['course_complete']
    eight=client.get(PREFIX+'/catalog',params={'grade':8}).json()
    assert all(r['state']=='completed' for r in eight['lessons'][:10])
    assert all(r['state']!='completed' for r in eight['lessons'][10:])
    assert eight['grade_content_complete']==(eight['implemented_sections']==33)
    assert not eight['course_complete']
