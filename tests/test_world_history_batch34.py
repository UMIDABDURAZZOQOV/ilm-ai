"""Grade10 source-bound theory and finite assessment targets, topics2–6."""
from copy import deepcopy
from uuid import uuid4

import pytest

from test_world_history_lesson import history, PREFIX, answer_for, send, finish  # noqa: F401
from services.world_history_lessons import load_lessons, validate_lesson
from services.world_history_validation import DIRECTORY, fingerprint, load_catalog, read_json
from services.chemistry_grading import grade_answer
from services.models import User
from services.world_history_models import WorldHistoryProgress


def batch():return load_lessons()[165:170]


def test_batch34_source_order_and_taught_objective_targets():
    ds=batch()
    assert [(d['grade'],d['sequence']) for d in ds]==[(10,n) for n in range(2,7)]
    assert [len(d['facts']) for d in ds]==[11,15,12,14,17]
    assert [len(d['content']['cards']) for d in ds]==[7,7,6,7,8]
    assert all(len(d['assessments'])==10 for d in ds)
    assert sum(q['response_kind']=='short_text' for d in ds for q in d['assessments'])==20
    for d in ds:
        assert {ref['book_id'] for ref in d['source_refs']}=={'world-history-10-uz-2017'}
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])


@pytest.mark.parametrize('index,page',[(0,8),(1,12),(1,16),(2,16),(2,20),(3,20),(4,25)])
def test_batch34_shared_page_regions_cannot_be_broadened(index,page):
    d=deepcopy(batch()[index]);r=read_json(DIRECTORY/f"grade10_paragraph{d['sequence']:02d}_review.json")
    next(ref for ref in d['source_refs'] if ref['pdf_pages']==[page])['regions']=['topic_body']
    next(row for row in r['source_pages'] if row['pdf_page']==page)['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_batch34_per_question_targets_not_interchangeable():
    ds=batch()
    for d in ds:
        frq=[q for q in d['assessments'] if q['response_kind']=='short_text']
        for q,other in zip(frq,frq[1:]+frq[:1]):
            assert grade_answer(q['grading_spec'],{'value':other['grading_spec']['expected']})=='incorrect'
    d=deepcopy(ds[0]);r=read_json(DIRECTORY/'grade10_paragraph02_review.json')
    q=d['assessments'][6];q['grading_spec']['aliases'].append('Bi-bi-si')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):validate_lesson(load_catalog(),d,r)


def test_batch34_medical_priorities_maps_and_political_judgment_not_scored():
    ds=batch()
    for d in ds:
        assert any(not f['automatic_assessment_allowed'] for f in d['facts'].values())
    for i,keys in [(0,['development','nuclear','materials','home']),(1,['economy','maps','policy']),(2,['economy','social','politics','interpretation','glosses']),(3,['economy','map','hardship','outcomes','ideas']),(4,['nazism','power','militarization','map','totalitarian'])]:
        assert all(not ds[i]['facts'][key]['automatic_assessment_allowed'] for key in keys)
    d=deepcopy(ds[4]);r=read_json(DIRECTORY/'grade10_paragraph06_review.json')
    q=d['assessments'][0];q['fact_ids']=['nazism']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][q['key']]['fact_ids']=['nazism']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):validate_lesson(load_catalog(),d,r)


def test_batch34_source_images_and_paris_alias_have_exact_review():
    ds=batch();d=ds[2]
    assert d['facts']['occupation']['approved_aliases']==['Parij']
    r=read_json(DIRECTORY/'grade10_paragraph04_review.json')
    next(row for row in r['source_pages'] if row['pdf_page']==19)['page_image_sha256']='0'*64
    with pytest.raises(ValueError,match='exact_original_page_digest_required'):validate_lesson(load_catalog(),d,r)
    assert ds[4]['facts']['weimar']['verified_answers']==['Veymar','1919-yil 31-iyul']


def test_all170_units3400_xp_once_and_existing_progress_preserved(history):
    client,factory,_=history
    for d in load_lessons()[:170]:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        result=finish(client,attempt);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==3400
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==170
        assert db.get(User,42).xp_total==137
    ten=client.get(PREFIX+'/catalog',params={'grade':10}).json()
    assert all(r['state']=='completed' for r in ten['lessons'][:6])
    assert all(r['state']!='completed' for r in ten['lessons'][6:])
    assert ten['grade_content_complete']==(ten['implemented_sections']==26)
    assert not ten['course_complete']
