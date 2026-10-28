"""Scanned grade9§8–12: institution names, scoped policies and separate chronology."""
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
    return [d for d in load_lessons() if d['grade']==9 and 8<=d['sequence']<=12]


def test_batch27_original_order_scoped_knowledge_counts():
    ds=batch()
    assert [d['sequence'] for d in ds]==[8,9,10,11,12]
    assert [len(d['facts']) for d in ds]==[9,11,10,9,11]
    assert [len(d['content']['cards']) for d in ds]==[6,6,6,6,7]
    assert all(len(d['assessments'])==10 for d in ds)
    assert sum(q['response_kind']=='short_text' for d in ds for q in d['assessments'])==20
    for d in ds:
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])


@pytest.mark.parametrize('number,ending',[(8,False),(9,False),(9,True),(10,False),(10,True),(11,False),(11,True),(12,False),(12,True)])
def test_batch27_exact_scanned_regions_cannot_be_broadened(number,ending):
    d=deepcopy(batch()[number-8]);r=read_json(DIRECTORY/f'grade9_paragraph{number:02d}_review.json')
    index=-1 if ending else 0
    d['source_refs'][index]['regions']=['topic_body'];r['source_pages'][index]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_person_nickname_ordinal_and_institution_targets_are_distinct():
    ds=batch()
    for i,index,wrong in [(0,6,'Bismark'),(0,7,'Otto fon Bismark'),(0,8,'Reyxstag'),(1,9,'Vilgelm I'),(2,6,'Ekspansiya'),(2,8,'Bag‘dod'),(3,8,'Sterling'),(4,9,'Jamoa palatasi')]:
        assert grade_answer(ds[i]['assessments'][index]['grading_spec'],{'value':wrong})=='incorrect'
    d=deepcopy(ds[0]);r=read_json(DIRECTORY/'grade9_paragraph08_review.json')
    d['assessments'][7]['grading_spec']['aliases'].append('Otto fon Bismark')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_source_holds_not_silently_replaced_with_external_science_law_or_dates():
    ds=batch()
    for i,key in [(0,'vote'),(0,'resources'),(1,'labour'),(2,'ottomans'),(2,'colonial'),(3,'decline'),(4,'social'),(4,'autonomy_process')]:
        assert not ds[i]['facts'][key]['automatic_assessment_allowed']
    assert ds[2]['facts']['railway']['verified_answers']==['Bag‘dod temiryo‘li','Fors qo‘ltig‘i']
    assert 'Reja' in ds[2]['content']['cards'][3]['body']
    assert ds[4]['facts']['home_rule']['verified_answers']==['Gomrul']
    assert ds[4]['facts']['labour_party']['verified_answers']==['Leyboristlar partiyasi','1906-yil']
    assert all(46 not in ref['pdf_pages'] for ref in ds[4]['source_refs'])


def test_political_only_correct_path_cannot_be_an_automatic_truth():
    d=deepcopy(batch()[1]);r=read_json(DIRECTORY/'grade9_paragraph09_review.json')
    d['assessments'][0]['fact_ids']=['labour']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][0]['key']]['fact_ids']=['labour']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_source_scan_not_ocr_required_for_imperial_and_irish_context():
    for n,p in [(8,31),(12,43)]:
        d=batch()[n-8];r=read_json(DIRECTORY/f'grade9_paragraph{n:02d}_review.json')
        next(row for row in r['source_pages'] if row['pdf_page']==p)['page_image_sha256']='0'*64
        with pytest.raises(ValueError,match='exact_original_page_digest_required'):
            validate_lesson(load_catalog(),d,r)


def test_all135_units2700_xp_once_and_existing_progress_preserved(history):
    client,factory,_=history;documents=load_lessons()[:135]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        result=finish(client,attempt);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==2700
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==135
        assert db.get(User,42).xp_total==137
    for grade in [6,7,8]:
        c=client.get(PREFIX+'/catalog',params={'grade':grade}).json()
        assert c['grade_content_complete'] and all(r['state']=='completed' for r in c['lessons'])
        assert not c['course_complete']
    nine=client.get(PREFIX+'/catalog',params={'grade':9}).json()
    assert all(r['state']=='completed' for r in nine['lessons'][:12])
    assert all(r['state']!='completed' for r in nine['lessons'][12:])
    assert nine['grade_content_complete']==(nine['implemented_sections']==41)
    assert not nine['course_complete']
