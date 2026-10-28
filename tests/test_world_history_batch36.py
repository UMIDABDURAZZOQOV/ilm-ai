"""Grade10 units12–16 retain combined source numbering and finite source targets."""
from copy import deepcopy
from uuid import uuid4

import pytest

from test_world_history_lesson import history, PREFIX, answer_for, send, finish  # noqa: F401
from services.world_history_lessons import load_lessons, validate_lesson
from services.world_history_validation import DIRECTORY, fingerprint, load_catalog, read_json
from services.chemistry_grading import grade_answer
from services.models import User
from services.world_history_models import WorldHistoryProgress


def batch():return load_lessons()[175:180]


def test_batch36_source_order_combined_numbering_and_counts():
    ds=batch();c=load_catalog();book=c['books'][4]
    assert [(d['grade'],d['sequence']) for d in ds]==[(10,n) for n in range(12,17)]
    assert [len(d['facts']) for d in ds]==[18,17,24,16,16]
    assert [len(d['content']['cards']) for d in ds]==[8,8,11,8,8]
    assert [len(d['assessments']) for d in ds]==[10,10,16,10,10]
    assert sum(q['response_kind']=='short_text' for d in ds for q in d['assessments'])==22
    assert next(row for row in book['records'] if row['id']==ds[2]['topic_id'])['source_numbers']==[15,16]
    assert all(d['source_refs'][0]['chapter_id'] is None for d in ds)
    for d in ds:
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])


@pytest.mark.parametrize('index,page',[(0,57),(0,62),(1,62),(1,67),(2,67),(2,76),(3,76),(3,81),(4,81)])
def test_batch36_adjacent_topic_boundary_not_whole_page(index,page):
    d=deepcopy(batch()[index]);r=read_json(DIRECTORY/f"grade10_paragraph{d['sequence']:02d}_review.json")
    next(ref for ref in d['source_refs'] if ref['pdf_pages']==[page])['regions']=['topic_body']
    next(row for row in r['source_pages'] if row['pdf_page']==page)['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_batch36_question_targets_cannot_be_broadened():
    ds=batch()
    for d in ds:
        frq=[q for q in d['assessments'] if q['response_kind']=='short_text']
        for q,other in zip(frq,frq[1:]+frq[:1]):
            assert grade_answer(q['grading_spec'],{'value':other['grading_spec']['expected']})=='incorrect'
    d=deepcopy(ds[1]);r=read_json(DIRECTORY/'grade10_paragraph13_review.json')
    q=d['assessments'][6];q['grading_spec']['aliases'].append('AMK')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):validate_lesson(load_catalog(),d,r)


def test_batch36_interpretation_maps_religion_and_unverified_dates_not_keys():
    ds=batch()
    for i,keys in [(0,['turkishreforms','map','turkishforeign','iranreforms','iranforeign','terms']),(1,['regions','egypt','north','maps','infrastructure','society','pan','war','terms']),(2,['prewar','map','polandfinland','coalition','fronts','uzbekistan','consequences','terms']),(3,['tensions','cartoon','decolonization','map','warming']),(4,['postwar','crises','map','politics','relations','terms'])]:
        assert all(not ds[i]['facts'][k]['automatic_assessment_allowed'] for k in keys)
    d=deepcopy(ds[2]);r=read_json(DIRECTORY/'grade10_paragraph14_review.json')
    q=d['assessments'][0];q['fact_ids']=['prewar']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][q['key']]['fact_ids']=['prewar']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):validate_lesson(load_catalog(),d,r)


def test_batch36_historical_dates_specific_document_not_all_charters():
    ds=batch();d=ds[2]
    assert d['facts']['surrender']['verified_answers']==['1945-yil 8-may','9-may']
    assert d['facts']['atlantic']['verified_answers']==['Atlantik xartiya','1941-yil avgust']
    assert ds[0]['facts']['sultan']['verified_answers']==['1922-yil 1-noyabr']
    r=read_json(DIRECTORY/'grade10_paragraph14_review.json')
    next(row for row in r['source_pages'] if row['pdf_page']==71)['page_image_sha256']='0'*64
    with pytest.raises(ValueError,match='exact_original_page_digest_required'):validate_lesson(load_catalog(),d,r)


def test_all180_units3600_xp_once_and_existing_progress_preserved(history):
    client,factory,_=history
    for d in load_lessons()[:180]:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        result=finish(client,attempt);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==3600
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==180
        assert db.get(User,42).xp_total==137
    ten=client.get(PREFIX+'/catalog',params={'grade':10}).json()
    assert all(r['state']=='completed' for r in ten['lessons'][:16])
    assert all(r['state']!='completed' for r in ten['lessons'][16:])
    assert ten['grade_content_complete']==(ten['implemented_sections']==26)
    assert not ten['course_complete']
