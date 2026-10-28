"""Grade9§18–22: exact scanned context, programmes and institutions."""
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
    return [d for d in load_lessons() if d['grade']==9 and 18<=d['sequence']<=22]


def test_batch29_original_order_scoped_counts_and_answer_targets():
    ds=batch()
    assert [d['sequence'] for d in ds]==list(range(18,23))
    assert [len(d['facts']) for d in ds]==[12,12,15,13,15]
    assert [len(d['content']['cards']) for d in ds]==[7,7,8,7,8]
    assert all(len(d['assessments'])==10 for d in ds)
    assert sum(q['response_kind']=='short_text' for d in ds for q in d['assessments'])==20
    for d in ds:
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])


@pytest.mark.parametrize('number,ending',[(n,e) for n in range(18,23) for e in [False,True]])
def test_batch29_exact_shared_page_scope_cannot_be_broadened(number,ending):
    d=deepcopy(batch()[number-18]);r=read_json(DIRECTORY/f'grade9_paragraph{number:02d}_review.json')
    index=(3 if number==18 else 4 if number==20 else -1) if ending else 0
    d['source_refs'][index]['regions']=['topic_body'];r['source_pages'][index]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_batch29_party_institution_and_term_answers_cannot_be_swapped_or_expanded():
    ds=batch()
    for i,index,wrong in [(0,6,'Izabel'),(0,8,'Viktoriya'),(1,6,'Produgol'),(1,7,'Prodmet'),(2,7,'Demobilizatsiya'),(3,7,'ASDP'),(3,8,'Lenin'),(4,6,'Davlat dumasi'),(4,7,'RSDRP')]:
        assert grade_answer(ds[i]['assessments'][index]['grading_spec'],{'value':wrong})=='incorrect'
    d=deepcopy(ds[1]);r=read_json(DIRECTORY/'grade9_paragraph19_review.json')
    d['assessments'][9]['grading_spec']['aliases'].append('P. A. Stolipin')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_batch29_programmes_discrimination_and_causal_interpretations_are_not_keys():
    ds=batch()
    for i,key in [(0,'slavery'),(0,'land'),(1,'politics'),(1,'internal'),(1,'resettlement'),(2,'empire'),(2,'east'),(2,'central_asia'),(3,'programme'),(3,'exploitation'),(4,'national'),(4,'antisemitism'),(4,'barricade')]:
        assert not ds[i]['facts'][key]['automatic_assessment_allowed']
    d=deepcopy(ds[3]);r=read_json(DIRECTORY/'grade9_paragraph21_review.json')
    d['assessments'][0]['fact_ids']=['programme']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][0]['key']]['fact_ids']=['programme']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_batch29_appendix154_and155_require_separate_linked_original_evidence():
    catalog=load_catalog();appendix=next(r for r in catalog['books'][3]['ancillary_records'] if r['id']=='wh9-appendix')
    assert appendix['fact_review']=='not_reviewed'
    for n,p in [(18,154),(20,155)]:
        d=batch()[n-18];refs=[r for r in d['source_refs'] if r['topic_id']=='wh9-appendix']
        assert len(refs)==1 and refs[0]['pdf_pages']==[p]
        assert all(156 not in r['pdf_pages'] for r in d['source_refs'])
        r=read_json(DIRECTORY/f'grade9_paragraph{n:02d}_review.json')
        next(row for row in r['source_pages'] if row['pdf_page']==p)['page_image_sha256']='0'*64
        with pytest.raises(ValueError,match='exact_original_page_digest_required'):
            validate_lesson(catalog,d,r)


def test_all145_units2900_xp_once_and_existing_progress_preserved(history):
    client,factory,_=history;documents=load_lessons()[:145]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        result=finish(client,attempt);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==2900
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==145
        assert db.get(User,42).xp_total==137
    for grade in [6,7,8]:
        c=client.get(PREFIX+'/catalog',params={'grade':grade}).json()
        assert c['grade_content_complete'] and all(r['state']=='completed' for r in c['lessons'])
        assert not c['course_complete']
    nine=client.get(PREFIX+'/catalog',params={'grade':9}).json()
    assert all(r['state']=='completed' for r in nine['lessons'][:22])
    assert all(r['state']!='completed' for r in nine['lessons'][22:])
    assert nine['grade_content_complete']==(nine['implemented_sections']==41)
    assert not nine['course_complete']
