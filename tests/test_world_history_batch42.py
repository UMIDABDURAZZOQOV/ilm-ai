"""Final four grade11 units and whole six-book local-preview coverage."""
from copy import deepcopy
from uuid import uuid4

import pytest

from test_world_history_lesson import history, PREFIX, answer_for, send, finish  # noqa: F401
from services.world_history_lessons import load_lessons, validate_lesson
from services.world_history_validation import DIRECTORY, fingerprint, load_catalog, read_json
from services.chemistry_grading import grade_answer
from services.models import User
from services.world_history_models import WorldHistoryProgress


def batch():return load_lessons()[215:219]


def test_batch42_all_six_books_and_final_source_order():
    all_ds=load_lessons();ds=all_ds[215:219];catalog=load_catalog()
    assert len(all_ds)==219 and catalog['implemented_lessons']==219 and catalog['remaining_lessons']==0
    assert [sum(d['grade']==g for d in all_ds) for g in range(6,12)]==[46,44,33,41,26,29]
    assert [(d['grade'],d['sequence']) for d in ds]==[(11,n) for n in range(26,30)]
    assert [len(d['facts']) for d in ds]==[14,11,13,12]
    assert [len(d['content']['cards']) for d in ds]==[8,8,8,10]
    assert all(len(d['assessments'])==10 and len(d['content']['reflections'])==1 for d in ds)
    for book in catalog['books']:
        rows=[d for d in all_ds if d['grade']==book['grade']]
        assert [d['topic_id'] for d in rows]==[u['id'] for u in book['teaching_units']]
        assert [d['sequence'] for d in rows]==list(range(1,len(rows)+1))
        assert all(u['interactive_status']=='reviewed_preview_ready' for u in book['teaching_units'])
        assert book['course_ready'] is False
    for d in ds:
        assert d['publication']=='local_test_preview_only' and d['content']['formulas']==[]
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])


@pytest.mark.parametrize('index,page',[(0,118),(1,124),(2,130),(2,135),(3,135)])
def test_batch42_shared_source_boundaries(index,page):
    d=deepcopy(batch()[index]);r=read_json(DIRECTORY/f"grade11_paragraph{d['sequence']:02d}_review.json")
    next(ref for ref in d['source_refs'] if ref['pdf_pages']==[page])['regions']=['topic_body']
    next(row for row in r['source_pages'] if row['pdf_page']==page)['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_batch42_question_specific_targets_and_fiction_not_author_alias():
    ds=batch()
    for d in ds:
        frq=[q for q in d['assessments'] if q['response_kind']=='short_text']
        for q,other in zip(frq,frq[1:]+frq[:1]):
            assert grade_answer(q['grading_spec'],{'value':other['grading_spec']['expected']})=='incorrect'
    d=deepcopy(ds[3]);r=read_json(DIRECTORY/'grade11_paragraph29_review.json')
    q=d['assessments'][7];assert q['grading_spec']['expected']=='Paulo Koelyo'
    q['grading_spec']['aliases'].append('Alkimyogar')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):validate_lesson(load_catalog(),d,r)


def test_batch42_uncertain_science_and_value_judgments_not_automatic_keys():
    ds=batch()
    for i,keys in [(0,['regions','egypt','sudanlibya','map','conflicts','society','legend','demography']),(1,['culture','military','extremism','environment','information','cooperation']),(2,['environment','discrimination','ethnosocial','uzbekistan','postsssr','racism']),(3,['information','science','medicine','values','literature','art','philosophy'])]:
        assert all(not ds[i]['facts'][k]['automatic_assessment_allowed'] for k in keys)
    d=deepcopy(ds[1]);r=read_json(DIRECTORY/'grade11_paragraph27_review.json')
    q=d['assessments'][0];q['fact_ids']=['environment']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][q['key']]['fact_ids']=['environment']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):validate_lesson(load_catalog(),d,r)


def test_batch42_distinct_names_events_and_exact_page_digest():
    ds=batch()
    assert '2011' in ds[0]['facts']['mubarak']['claim'] and '2014' in ds[0]['facts']['sisi']['claim']
    assert ds[0]['facts']['mursi']['verified_answers']==['Muhammad Mursi']
    assert ds[1]['facts']['aral']['verified_answers']==['Orol dengizi','O‘zbekiston']
    assert ds[2]['facts']['rio']['verified_answers']==['Rio-de-Janeyro']
    assert ds[2]['facts']['conferenceyear']['verified_answers']==['1992-yil']
    assert ds[3]['facts']['iti']['verified_answers']==['ITI','Ilmiy-texnik inqilob']
    assert ds[3]['facts']['rowling']['verified_answers']==['Joan Rouling','Garri Potter']
    assert not any(ref['pdf_pages'][0]>140 for d in ds for ref in d['source_refs'])
    d=ds[2];r=read_json(DIRECTORY/'grade11_paragraph28_review.json')
    assert all(row['reviewed_on']=='2026-10-29' for row in r['source_pages'])
    next(row for row in r['source_pages'] if row['pdf_page']==134)['page_image_sha256']='0'*64
    with pytest.raises(ValueError,match='exact_original_page_digest_required'):validate_lesson(load_catalog(),d,r)


def test_all219_units4380_xp_once_and_all_grade_catalogues_complete(history):
    client,factory,_=history
    for d in load_lessons():
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        result=finish(client,attempt);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==4380
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==219
        assert db.get(User,42).xp_total==137
    for grade,expected in zip(range(6,12),[46,44,33,41,26,29]):
        catalog=client.get(PREFIX+'/catalog',params={'grade':grade}).json()
        assert catalog['implemented_sections']==expected
        assert all(r['state']=='completed' for r in catalog['lessons'])
        assert catalog['grade_content_complete'] is True
        assert not catalog['course_complete']
