"""Grade9 completion and independent grade10 entry with reviewed science history."""
from copy import deepcopy
from uuid import uuid4

import pytest

from test_world_history_lesson import history, PREFIX, answer_for, send, finish  # noqa: F401
from services.world_history_lessons import load_lessons, validate_lesson
from services.world_history_validation import DIRECTORY, fingerprint, load_catalog, read_json
from services.chemistry_grading import grade_answer
from services.models import User
from services.world_history_models import WorldHistoryProgress


def batch():return load_lessons()[160:165]


def test_batch33_source_order_counts_and_independent_grade10():
    ds=batch()
    assert [(d['grade'],d['sequence']) for d in ds]==[(9,38),(9,39),(9,40),(9,41),(10,1)]
    assert [len(d['facts']) for d in ds]==[13,17,15,20,20]
    assert [len(d['content']['cards']) for d in ds]==[8,8,8,9,9]
    assert [len(d['assessments']) for d in ds]==[10,10,10,14,10]
    assert sum(q['response_kind']=='short_text' for d in ds for q in d['assessments'])==22
    assert ds[4]['prerequisite_ids']==[]
    assert {ref['book_id'] for ref in ds[4]['source_refs']}=={'world-history-10-uz-2017'}
    for d in ds:
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])


@pytest.mark.parametrize('index,page',[(0,137),(0,141),(1,141),(1,146),(2,146),(2,150),(3,150),(4,4),(4,8)])
def test_batch33_shared_boundaries_cannot_be_broadened(index,page):
    d=deepcopy(batch()[index]);r=read_json(DIRECTORY/f"grade{d['grade']}_paragraph{d['sequence']:02d}_review.json")
    next(ref for ref in d['source_refs'] if ref['pdf_pages']==[page])['regions']=['topic_body']
    next(row for row in r['source_pages'] if row['pdf_page']==page)['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_batch33_finite_person_device_and_book_targets():
    ds=batch()
    for i,index,wrong in [(0,9,'Edison'),(0,8,'Jozef Mari Jakkard'),(1,7,'Darvin'),(1,8,'Paster'),(2,6,'Psixoanaliz'),(2,7,'Freyd'),(3,8,'Marten Iden'),(3,11,'Kapitan Grant bolalari'),(4,6,'Konferensiya'),(4,7,'Millatlar Ligasi')]:
        assert grade_answer(ds[i]['assessments'][index]['grading_spec'],{'value':wrong})=='incorrect'
    d=deepcopy(ds[0]);r=read_json(DIRECTORY/'grade9_paragraph38_review.json')
    d['assessments'][9]['grading_spec']['aliases'].append('Edison')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):validate_lesson(load_catalog(),d,r)


def test_batch33_unverified_priorities_medical_and_ideological_claims_not_keys():
    ds=batch()
    for i,key in [(0,'industry'),(0,'materials'),(0,'military'),(1,'disciplines'),(1,'models'),(1,'glossary'),(2,'education'),(2,'segregation'),(2,'humanities'),(2,'ideology'),(3,'movements'),(3,'japan'),(3,'decadence'),(4,'civilization'),(4,'aftermath'),(4,'poster'),(4,'map'),(4,'fascism'),(4,'crisis')]:
        assert not ds[i]['facts'][key]['automatic_assessment_allowed']
    assert ds[1]['facts']['pasteur']['verified_answers']==['Lui Paster']
    assert ds[2]['facts']['freud']['verified_answers']==['Freyd','Psixoanaliz']
    d=deepcopy(ds[1]);r=read_json(DIRECTORY/'grade9_paragraph39_review.json')
    d['assessments'][0]['fact_ids']=['glossary']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][0]['key']]['fact_ids']=['glossary']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):validate_lesson(load_catalog(),d,r)


def test_batch33_grade10_introduction_exact_digest_not_whole_approval():
    d=batch()[4];c=load_catalog();intro=c['books'][4]['ancillary_records'][0]
    assert intro['id']=='wh10-intro' and intro['fact_review']=='not_reviewed'
    assert d['facts']['period']['source_refs'][0]['topic_id']=='wh10-intro'
    assert d['facts']['period']['claim_kind']=='textbook_periodization'
    assert d['facts']['period']['verified_answers']==['Eng yangi tarix']
    assert d['facts']['three']['approved_aliases']==['Katta uchlik','Devid Lloyd Jorj','Jorj Klemanso','Vudro Vilson']
    r=read_json(DIRECTORY/'grade10_paragraph01_review.json')
    next(row for row in r['source_pages'] if row['pdf_page']==3)['page_image_sha256']='0'*64
    with pytest.raises(ValueError,match='exact_original_page_digest_required'):validate_lesson(c,d,r)


def test_batch33_grade10_starts_without_grade9_progress(history):
    client,factory,_=history;d=batch()[4]
    c=client.get(PREFIX+'/catalog',params={'grade':10}).json()
    assert c['implemented_sections']>=1 and c['lessons'][0]['state']=='available'
    assert not c['course_complete']
    attempt=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
    assert attempt.status_code==200
    with factory() as db:
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).filter(WorldHistoryProgress.lesson_key.like('world-history-9-%')).count()==0


def test_all165_units3300_xp_once_and_existing_progress_preserved(history):
    client,factory,_=history
    for d in load_lessons()[:165]:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        result=finish(client,attempt);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==3300
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==165
        assert db.get(User,42).xp_total==137
    for grade in [6,7,8,9]:
        c=client.get(PREFIX+'/catalog',params={'grade':grade}).json()
        assert c['grade_content_complete'] and all(r['state']=='completed' for r in c['lessons'])
        assert not c['course_complete']
    ten=client.get(PREFIX+'/catalog',params={'grade':10}).json()
    assert ten['lessons'][0]['state']=='completed'
    assert all(r['state']!='completed' for r in ten['lessons'][1:])
    assert ten['grade_content_complete']==(ten['implemented_sections']==26)
    assert not ten['course_complete']
