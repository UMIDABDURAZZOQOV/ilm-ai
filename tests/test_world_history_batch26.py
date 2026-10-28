"""Scanned grade9§3–7: exact chronology targets and ungraded political models."""
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
    return [d for d in load_lessons() if d['grade']==9 and 3<=d['sequence']<=7]


def test_batch26_original_order_taught_objective_targets_and_counts():
    ds=batch()
    assert [d['sequence'] for d in ds]==[3,4,5,6,7]
    assert [len(d['facts']) for d in ds]==[11,12,10,13,10]
    assert [len(d['content']['cards']) for d in ds]==[7,7,6,7,7]
    assert [len(d['assessments']) for d in ds]==[12,10,10,10,10]
    assert sum(q['response_kind']=='short_text' for d in ds for q in d['assessments'])==22
    for d in ds:
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])


@pytest.mark.parametrize('number,ending',[(3,False),(3,True),(4,False),(4,True),(5,False),(5,True),(6,False),(7,False)])
def test_batch26_exact_scanned_regions_cannot_be_broadened(number,ending):
    d=deepcopy(batch()[number-3]);r=read_json(DIRECTORY/f'grade9_paragraph{number:02d}_review.json')
    index=-1 if ending else 0
    d['source_refs'][index]['regions']=['topic_body'];r['source_pages'][index]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_ordinals_dispatch_and_full_institution_targets_are_distinct():
    ds=batch()
    for i,index,wrong in [(0,6,'Depesha'),(0,10,'Napoleon III'),(0,11,'Izabella'),(1,8,'Kommuna'),(2,6,'Majlis'),(2,9,'Palata'),(3,8,'Ishchi partiyasi'),(4,7,'Uchlar'),(4,8,'Italiya')]:
        assert grade_answer(ds[i]['assessments'][index]['grading_spec'],{'value':wrong})=='incorrect'
    d=deepcopy(ds[0]);r=read_json(DIRECTORY/'grade9_paragraph03_review.json')
    d['assessments'][10]['grading_spec']['aliases'].append('Napoleon III')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_disputed_dates_constitution_and_treaty_clauses_not_repaired_from_memory():
    ds=batch()
    assert ds[0]['facts']['outbreak']['verified_answers']==['Fransiya','Prussiya']
    assert ds[0]['facts']['sedan']['verified_answers']==['Sedan','1870-yil 2-sentabr']
    assert ds[1]['facts']['republic']['verified_answers']==['1870-yil 4-sentabr','Uchinchi Respublika']
    assert ds[2]['facts']['constitution']['verified_answers']==['1875-yil']
    assert ds[3]['facts']['unions']['verified_answers']==['1884-yil']
    assert ds[4]['facts']['britain']['verified_answers']==['Buyuk Britaniya','1904-yil']
    assert ds[4]['facts']['entente']['verified_answers']==['Antanta','Rossiya']
    assert all(30 not in ref['pdf_pages'] for ref in ds[4]['source_refs'])
    assert all(27 not in ref['pdf_pages'] for ref in ds[3]['source_refs'])


def test_racial_superiority_and_political_causes_cannot_be_graded_as_facts():
    ds=batch()
    for i,key in [(0,'causes'),(1,'measures'),(1,'defeat_causes'),(2,'rights'),(3,'racism'),(3,'politics'),(4,'situation'),(4,'russia')]:
        assert not ds[i]['facts'][key]['automatic_assessment_allowed']
    d=deepcopy(ds[3]);r=read_json(DIRECTORY/'grade9_paragraph06_review.json')
    d['assessments'][0]['fact_ids']=['racism']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][0]['key']]['fact_ids']=['racism']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_original_source_scan_digest_required_for_dreyfus_and_treaty_pages():
    for n,p in [(6,24),(7,28)]:
        d=batch()[n-3];r=read_json(DIRECTORY/f'grade9_paragraph{n:02d}_review.json')
        next(row for row in r['source_pages'] if row['pdf_page']==p)['page_image_sha256']='0'*64
        with pytest.raises(ValueError,match='exact_original_page_digest_required'):
            validate_lesson(load_catalog(),d,r)


def test_all130_units2600_xp_once_and_existing_progress_preserved(history):
    client,factory,_=history;documents=load_lessons()[:130]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        result=finish(client,attempt);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==2600
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==130
        assert db.get(User,42).xp_total==137
    for grade in [6,7,8]:
        c=client.get(PREFIX+'/catalog',params={'grade':grade}).json()
        assert c['grade_content_complete'] and all(r['state']=='completed' for r in c['lessons'])
        assert not c['course_complete']
    nine=client.get(PREFIX+'/catalog',params={'grade':9}).json()
    assert all(r['state']=='completed' for r in nine['lessons'][:7])
    assert all(r['state']!='completed' for r in nine['lessons'][7:])
    assert nine['grade_content_complete']==(nine['implemented_sections']==41)
    assert not nine['course_complete']
