"""Grade8 paragraphs11–15: exact source models, map labels and answer targets."""
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
    return [d for d in load_lessons() if d['grade']==8 and 11<=d['sequence']<=15]


def test_batch21_original_order_counts_and_ungraded_interpretations():
    ds=batch()
    assert [d['sequence'] for d in ds]==[11,12,13,14,15]
    assert [len(d['facts']) for d in ds]==[12,12,12,12,15]
    assert [len(d['content']['cards']) for d in ds]==[7,8,7,7,8]
    assert [len(d['assessments']) for d in ds]==[12,12,8,12,14]
    assert sum(q['response_kind']=='short_text' for d in ds for q in d['assessments'])==19
    for d in ds:
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
    for n,key in [(0,'principles'),(1,'ideas'),(2,'models'),(2,'comparison'),(2,'islam'),(3,'contacts'),(3,'conquest'),(4,'reforms'),(4,'crisis')]:
        assert not ds[n]['facts'][key]['automatic_assessment_allowed']
    assert {i for q in ds[2]['assessments'] for i in q['fact_ids']}=={'map_sw','map_s','map_se','map_e','extensive'}
    assert 65 not in [p for ref in ds[1]['source_refs'] for p in ref['pdf_pages']]


@pytest.mark.parametrize('number,ending',[(11,False),(12,False),(13,False),(14,False),(15,False),(11,True),(13,True),(14,True),(15,True)])
def test_batch21_exact_shared_original_regions(number,ending):
    d=deepcopy(batch()[number-11]);r=read_json(DIRECTORY/f'grade8_paragraph{number:02d}_review.json')
    index=-1 if ending else 0
    d['source_refs'][index]['regions']=['topic_body'];r['source_pages'][index]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_full_names_map_regions_and_patron_dedicatee_are_not_aliases():
    ds=batch()
    for n,index,wrong in [(0,8,'Jorj Vashington'),(1,10,'Gyote'),(2,5,'Sharqiy Osiyo'),(3,8,'Shunchji'),(3,9,'Abaxay'),(4,12,'Mumtoz Mahal')]:
        assert grade_answer(ds[n]['assessments'][index]['grading_spec'],{'value':wrong})=='incorrect'
    d=deepcopy(ds[4]);r=read_json(DIRECTORY/'grade8_paragraph15_review.json')
    d['assessments'][12]['grading_spec']['aliases'].append('Mumtoz Mahal')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_civilizational_model_and_religious_views_cannot_be_automatic_keys():
    d=deepcopy(batch()[2]);r=read_json(DIRECTORY/'grade8_paragraph13_review.json')
    d['assessments'][0]['fact_ids']=['islam']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][0]['key']]['fact_ids']=['islam']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_regional_map_legend_requires_exact_original_image_digest():
    d=batch()[2];r=read_json(DIRECTORY/'grade8_paragraph13_review.json')
    next(p for p in r['source_pages'] if p['pdf_page']==67)['page_image_sha256']='0'*64
    with pytest.raises(ValueError,match='exact_original_page_digest_required'):
        validate_lesson(load_catalog(),d,r)


def test_all105_units2100_xp_once_and_existing_grade_progress_preserved(history):
    client,factory,_=history;documents=load_lessons()[:105]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        result=finish(client,attempt);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==2100
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==105
        assert db.get(User,42).xp_total==137
    for grade in [6,7]:
        catalog=client.get(PREFIX+'/catalog',params={'grade':grade}).json()
        assert catalog['grade_content_complete'] and all(r['state']=='completed' for r in catalog['lessons'])
        assert not catalog['course_complete']
    eight=client.get(PREFIX+'/catalog',params={'grade':8}).json()
    assert all(r['state']=='completed' for r in eight['lessons'][:15])
    assert all(r['state']!='completed' for r in eight['lessons'][15:])
    assert eight['grade_content_complete']==(eight['implemented_sections']==33)
    assert not eight['course_complete']
