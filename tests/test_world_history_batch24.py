"""Grade8 paragraphs26–30: scoped terms, historical claims and source guards."""
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
    return [d for d in load_lessons() if d['grade']==8 and 26<=d['sequence']<=30]


def test_batch24_original_order_counts_and_ungraded_interpretations():
    ds=batch()
    assert [d['sequence'] for d in ds]==[26,27,28,29,30]
    assert [len(d['facts']) for d in ds]==[10,10,10,9,10]
    assert [len(d['content']['cards']) for d in ds]==[7,7,8,6,7]
    assert [len(d['assessments']) for d in ds]==[10,10,10,8,10]
    assert sum(q['response_kind']=='short_text' for d in ds for q in d['assessments'])==20
    for d in ds:
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
    for n,key in [(0,'religion'),(0,'education'),(1,'programme'),(1,'causes'),(2,'ideology'),(3,'missionaries'),(3,'conclusion'),(4,'causes')]:
        assert not ds[n]['facts'][key]['automatic_assessment_allowed']
    assert all(142 not in ref['pdf_pages'] for ref in ds[3]['source_refs'])
    assert ds[1]['facts']['first_war']['claim_kind']=='textbook_periodization'
    assert ds[0]['facts']['sepoy']['claim'].startswith('Ushbu paragrafda sipohiy')


@pytest.mark.parametrize('number,ending',[(26,False),(27,False),(28,False),(29,False),(30,False),(26,True),(27,True),(28,True),(30,True)])
def test_batch24_exact_reviewed_original_regions(number,ending):
    d=deepcopy(batch()[number-26]);r=read_json(DIRECTORY/f'grade8_paragraph{number:02d}_review.json')
    index=-1 if ending else 0
    d['source_refs'][index]['regions']=['topic_body'];r['source_pages'][index]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_regent_king_other_name_and_office_targets_are_distinct():
    ds=batch()
    for n,index,wrong in [(0,8,'Bahodirshoh'),(1,7,'Xun'),(2,6,'Mutsuxito'),(2,9,'Huquq'),(3,4,'Kojon'),(3,5,'Li Xa In'),(4,7,'Ali'),(4,9,'Nikolay II')]:
        assert grade_answer(ds[n]['assessments'][index]['grading_spec'],{'value':wrong})=='incorrect'
    d=deepcopy(ds[2]);r=read_json(DIRECTORY/'grade8_paragraph28_review.json')
    d['assessments'][6]['grading_spec']['aliases'].append('Mutsuxito')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_imperial_superiority_and_divine_origin_are_not_automatic_truths():
    d=deepcopy(batch()[2]);r=read_json(DIRECTORY/'grade8_paragraph28_review.json')
    d['assessments'][0]['fact_ids']=['ideology']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][0]['key']]['fact_ids']=['ideology']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_taiping_map_requires_exact_original_image_digest():
    d=batch()[1];r=read_json(DIRECTORY/'grade8_paragraph27_review.json')
    next(p for p in r['source_pages'] if p['pdf_page']==132)['page_image_sha256']='0'*64
    with pytest.raises(ValueError,match='exact_original_page_digest_required'):
        validate_lesson(load_catalog(),d,r)


def test_all120_units2400_xp_once_and_existing_grade_progress_preserved(history):
    client,factory,_=history;documents=load_lessons()[:120]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        result=finish(client,attempt);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==2400
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==120
        assert db.get(User,42).xp_total==137
    for grade in [6,7]:
        catalog=client.get(PREFIX+'/catalog',params={'grade':grade}).json()
        assert catalog['grade_content_complete'] and all(r['state']=='completed' for r in catalog['lessons'])
        assert not catalog['course_complete']
    eight=client.get(PREFIX+'/catalog',params={'grade':8}).json()
    assert all(r['state']=='completed' for r in eight['lessons'][:30])
    assert all(r['state']!='completed' for r in eight['lessons'][30:])
    assert eight['grade_content_complete']==(eight['implemented_sections']==33)
    assert not eight['course_complete']
