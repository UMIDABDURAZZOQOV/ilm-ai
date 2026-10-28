"""Grade9 paragraphs33-37: colonial map dates and wartime source distinctions."""
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
    return [d for d in load_lessons() if d['grade']==9 and 33<=d['sequence']<=37]


def test_batch32_source_order_counts_and_finite_keys():
    ds=batch()
    assert [d['sequence'] for d in ds]==list(range(33,38))
    assert [len(d['facts']) for d in ds]==[14,15,16,10,15]
    assert [len(d['content']['cards']) for d in ds]==[7,7,8,6,7]
    assert all(len(d['assessments'])==10 for d in ds)
    assert sum(q['response_kind']=='short_text' for d in ds for q in d['assessments'])==20
    for d in ds:
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])


@pytest.mark.parametrize('number,page',[(33,116),(34,120),(35,125),(36,130),(36,132),(37,132)])
def test_batch32_shared_page_regions_cannot_include_adjacent_topics(number,page):
    d=deepcopy(batch()[number-33]);r=read_json(DIRECTORY/f'grade9_paragraph{number:02d}_review.json')
    next(ref for ref in d['source_refs'] if ref['pdf_pages']==[page])['regions']=['topic_body']
    next(row for row in r['source_pages'] if row['pdf_page']==page)['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_batch32_names_places_and_aliases_are_question_specific():
    ds=batch()
    for i,index,wrong in [(0,7,'Muhammad Ahmad'),(0,8,'Ahmad Orabey'),(1,8,'Xendrik Vitboy'),(1,9,'Samuil Magarero'),(2,7,'Gindenburg'),(2,8,'Somma'),(3,7,'Marna'),(3,8,'Fosh'),(4,6,'Versal'),(4,7,'Brest'),(4,9,'Separatizm')]:
        assert grade_answer(ds[i]['assessments'][index]['grading_spec'],{'value':wrong})=='incorrect'
    d=deepcopy(ds[4]);r=read_json(DIRECTORY/'grade9_paragraph37_review.json')
    d['assessments'][9]['grading_spec']['aliases'].append('Separatizm')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):validate_lesson(load_catalog(),d,r)


def test_batch32_religious_political_causal_and_casualty_claims_are_not_keys():
    ds=batch()
    for i,key in [(0,'colonial'),(0,'programme'),(0,'conflict'),(0,'morocco_libya'),(1,'rivalry'),(1,'map'),(1,'congo'),(1,'violence'),(2,'causes'),(2,'ypres'),(2,'china'),(3,'losses'),(3,'plans'),(4,'homefront'),(4,'other_fronts'),(4,'consequences')]:
        assert not ds[i]['facts'][key]['automatic_assessment_allowed']
    assert ds[0]['facts']['mahdi']['verified_answers']==['Muhammad Ahmad']
    assert ds[1]['facts']['feodor']['verified_answers']==['Feodor II']
    assert ds[4]['facts']['wilson']['approved_aliases']==['Vilson']
    d=deepcopy(ds[2]);r=read_json(DIRECTORY/'grade9_paragraph35_review.json')
    d['assessments'][0]['fact_ids']=['ypres']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][0]['key']]['fact_ids']=['ypres']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):validate_lesson(load_catalog(),d,r)


def test_batch32_held_date_conflict_and_map_layers_do_not_become_answer_keys():
    ds=batch()
    for d,page in [(ds[0],120),(ds[1],125),(ds[2],130),(ds[4],137)]:
        assert all(page not in ref['pdf_pages'] for ref in d['source_refs'])
    assert ds[2]['facts']['sarajevo']['verified_answers']==['Sarayevo','Frans Ferdinand','G. Prinsip','1914-yil']
    assert ds[2]['facts']['austria']['verified_answers']==['1914-yil 28-iyul','Serbiya']
    for d in [ds[2],ds[3],ds[4]]:
        r=read_json(DIRECTORY/f"grade9_paragraph{d['sequence']:02d}_review.json")
        assert any('held' in s for s in r['historical_review_notes'])
    assert any(ref['pdf_pages']==[121] for ref in ds[1]['facts']['map']['source_refs'])
    assert all(ref['topic_id']==ds[1]['topic_id'] for ref in ds[1]['facts']['map']['source_refs'])


def test_all160_units3200_xp_once_and_existing_progress_preserved(history):
    client,factory,_=history;documents=load_lessons()[:160]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        result=finish(client,attempt);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==3200
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==160
        assert db.get(User,42).xp_total==137
    for grade in [6,7,8]:
        c=client.get(PREFIX+'/catalog',params={'grade':grade}).json()
        assert c['grade_content_complete'] and all(r['state']=='completed' for r in c['lessons'])
        assert not c['course_complete']
    nine=client.get(PREFIX+'/catalog',params={'grade':9}).json()
    assert all(r['state']=='completed' for r in nine['lessons'][:37])
    assert all(r['state']!='completed' for r in nine['lessons'][37:])
    assert nine['grade_content_complete']==(nine['implemented_sections']==41)
    assert not nine['course_complete']
