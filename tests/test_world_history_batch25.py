"""Grade8 conclusion and scanned grade9 opening: exact context and grade isolation."""
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
    return [d for d in load_lessons() if (d['grade']==8 and 31<=d['sequence']<=33) or (d['grade']==9 and d['sequence']<=2)]


def test_batch25_five_ordered_lessons_and_book_boundaries():
    ds=batch()
    assert [(d['grade'],d['sequence']) for d in ds]==[(8,31),(8,32),(8,33),(9,1),(9,2)]
    assert [len(d['facts']) for d in ds]==[15,11,8,17,12]
    assert [len(d['content']['cards']) for d in ds]==[10,7,7,9,7]
    assert [len(d['assessments']) for d in ds]==[14,10,7,14,10]
    assert sum(q['response_kind']=='short_text' for d in ds for q in d['assessments'])==23
    assert ds[2]['topic_id']=='wh8-conclusion'
    assert ds[3]['prerequisite_ids']==[] and ds[4]['prerequisite_ids']==['wh9-topic01']
    assert {r['book_id'] for d in ds[3:] for r in d['source_refs']}=={'world-history-9-uz-2019'}
    assert all(151 not in ref['pdf_pages'] for ref in ds[0]['source_refs'])
    assert all(156 not in ref['pdf_pages'] for ref in ds[1]['source_refs'])
    assert all(11 not in ref['pdf_pages'] for ref in ds[3]['source_refs'])
    assert all(16 not in ref['pdf_pages'] for ref in ds[4]['source_refs'])
    for d in ds:
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])


@pytest.mark.parametrize('index', [0,1,2,3,4])
def test_batch25_scan_and_conclusion_original_digest_cannot_be_replaced(index):
    d=batch()[index];r=read_json(DIRECTORY/f"grade{d['grade']}_paragraph{d['sequence']:02d}_review.json")
    r['source_pages'][0]['page_image_sha256']='0'*64
    with pytest.raises(ValueError,match='exact_original_page_digest_required'):
        validate_lesson(load_catalog(),d,r)


@pytest.mark.parametrize('change',['context_digest','binding','fact'])
def test_grade8_conclusion_cannot_invent_or_rebind_recap_facts(change):
    d=deepcopy(batch()[2]);r=read_json(DIRECTORY/'grade8_paragraph33_review.json')
    assert len(r['approved_context_fact_bindings'])==3
    assert set(r['approved_context_sha256'])=={'wh8-topic02','wh8-topic03','wh8-topic11'}
    for key in r['approved_context_fact_bindings']:
        assert all(156 not in ref['pdf_pages'] for ref in d['facts'][key]['source_refs'])
    if change=='context_digest':r['approved_context_sha256']['wh8-topic02']='0'*64
    if change=='binding':r['approved_context_fact_bindings'].pop('recap_manufacture')
    if change=='fact':
        d['facts']['recap_manufacture']['claim']+=' Qo‘shimcha tasdiqlanmagan da’vo.'
        r['approved_fact_sha256']['recap_manufacture']=fingerprint(d['facts']['recap_manufacture'])
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_migration_urbanization_and_person_targets_are_not_interchangeable():
    ds=batch()
    for n,index,wrong in [(0,9,'Hakim'),(0,11,'Muhammadxon'),(2,5,'Lyuter'),(2,6,'Deklaratsiya'),(3,11,'Morgan'),(4,7,'Migratsiya'),(4,8,'Urbanizatsiya'),(4,9,'Internatsional')]:
        assert grade_answer(ds[n]['assessments'][index]['grading_spec'],{'value':wrong})=='incorrect'
    d=deepcopy(ds[4]);r=read_json(DIRECTORY/'grade9_paragraph02_review.json')
    d['assessments'][7]['grading_spec']['aliases'].append('Migratsiya')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_political_models_and_labour_judgements_are_not_automatic_truths():
    ds=batch()
    for i,key in [(0,'causes'),(0,'conclusion'),(2,'politics'),(2,'ideas'),(3,'stage'),(3,'colonial'),(3,'effects'),(4,'workers'),(4,'rights'),(4,'middle')]:
        assert not ds[i]['facts'][key]['automatic_assessment_allowed']
    d=deepcopy(ds[3]);r=read_json(DIRECTORY/'grade9_paragraph01_review.json')
    d['assessments'][0]['fact_ids']=['stage']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][0]['key']]['fact_ids']=['stage']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_scanned_grade9_opening_uses_introduction_and_1914_legend_only():
    d=batch()[3]
    assert d['facts']['scope']['source_refs'][0]['topic_id']=='wh9-intro'
    assert d['facts']['scope']['claim_kind']=='textbook_periodization'
    assert {p for ref in d['facts']['map']['source_refs'] for p in ref['pdf_pages']}=={8,9}
    assert d['facts']['map']['verified_answers']==['1914-yil']
    assert d['facts']['map']['automatic_assessment_allowed']
    assert not d['facts']['colonial']['automatic_assessment_allowed']


def test_grade9_first_is_independent_and_second_requires_its_own_first(history):
    client,_,_=history;ds=batch()
    for grade in [8,9]:
        c=client.get(PREFIX+'/catalog',params={'grade':grade}).json()
        assert c['lessons'][0]['state']=='available'
    blocked=client.post(f"{PREFIX}/lessons/{ds[4]['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
    assert blocked.status_code==403
    first=client.post(f"{PREFIX}/lessons/{ds[3]['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
    assert first.status_code==200


def test_all125_units2500_xp_once_and_previous_grade_progress_preserved(history):
    client,factory,_=history;documents=load_lessons()[:125]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        result=finish(client,attempt);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==2500
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==125
        assert db.get(User,42).xp_total==137
    for grade in [6,7,8]:
        c=client.get(PREFIX+'/catalog',params={'grade':grade}).json()
        assert c['grade_content_complete'] and all(r['state']=='completed' for r in c['lessons'])
        assert not c['course_complete']
    nine=client.get(PREFIX+'/catalog',params={'grade':9}).json()
    assert all(r['state']=='completed' for r in nine['lessons'][:2])
    assert all(r['state']!='completed' for r in nine['lessons'][2:])
    assert nine['grade_content_complete']==(nine['implemented_sections']==41)
    assert not nine['course_complete']
