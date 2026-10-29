"""Grade11 topics16–25: exact sources, historical instruments and finite targets."""
from copy import deepcopy
from uuid import uuid4

import pytest

from test_world_history_lesson import history, PREFIX, answer_for, send, finish  # noqa: F401
from services.world_history_lessons import load_lessons, validate_lesson
from services.world_history_validation import DIRECTORY, fingerprint, load_catalog, read_json
from services.chemistry_grading import grade_answer
from services.models import User
from services.world_history_models import WorldHistoryProgress


def batch():return load_lessons()[205:215]


def test_batch41_source_order_and_counts():
    ds=batch();book=load_catalog()['books'][5]
    assert [(d['grade'],d['sequence']) for d in ds]==[(11,n) for n in range(16,26)]
    assert [len(d['facts']) for d in ds]==[12,14,14,12,13,14,14,12,14,12]
    assert all(len(d['content']['cards'])==8 and len(d['assessments'])==10 for d in ds)
    assert sum(q['response_kind']=='short_text' for d in ds for q in d['assessments'])==40
    assert [next(row for row in book['records'] if row['id']==d['topic_id'])['source_numbers'] for d in ds]==[[n] for n in range(16,26)]
    for d in ds:
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])


@pytest.mark.parametrize('index,page',[(0,72),(1,77),(2,81),(2,85),(3,85),(3,90),(4,90),(4,94),(5,94),(5,98),(6,98),(6,104),(7,104),(8,109),(8,113),(9,113),(9,118)])
def test_batch41_adjacent_topic_boundary_not_whole_page(index,page):
    d=deepcopy(batch()[index]);r=read_json(DIRECTORY/f"grade11_paragraph{d['sequence']:02d}_review.json")
    next(ref for ref in d['source_refs'] if ref['pdf_pages']==[page])['regions']=['topic_body']
    next(row for row in r['source_pages'] if row['pdf_page']==page)['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_batch41_question_targets_cannot_be_broadened():
    ds=batch()
    for d in ds:
        frq=[q for q in d['assessments'] if q['response_kind']=='short_text']
        for q,other in zip(frq,frq[1:]+frq[:1]):
            assert grade_answer(q['grading_spec'],{'value':other['grading_spec']['expected']})=='incorrect'
    d=deepcopy(ds[0]);r=read_json(DIRECTORY/'grade11_paragraph16_review.json')
    q=next(q for q in d['assessments'] if q['response_kind']=='short_text' and q['grading_spec']['expected']=='JST')
    q['grading_spec']['aliases'].append('Jahon savdo tashkiloti')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):validate_lesson(load_catalog(),d,r)


def test_batch41_complex_claims_and_contested_politics_not_keys():
    ds=batch()
    for i,keys in [(0,['reforms','dream','social','foreign']),(1,['economy','earthquake','foreign','sect']),(2,['vietnam','malaysia','indonesia','philippines','tigers']),(3,['economy','government','forecast','social','foreign']),(4,['politics','economy','conflicts']),(5,['society','international','protests','development','ultra','agreement']),(6,['pakpolitics','afghanconflict','constitution','rebuilding']),(7,['syrianeconomy','syrianwar','iraqwars','iraqpolitics','interpretation']),(8,['economy','map','organizations','conflict','status']),(9,['models','protests','indigenous','political','ambitions','populism'])]:
        assert all(not ds[i]['facts'][k]['automatic_assessment_allowed'] for k in keys)
    d=deepcopy(ds[8]);r=read_json(DIRECTORY/'grade11_paragraph24_review.json')
    q=d['assessments'][0];q['fact_ids']=['conflict']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][q['key']]['fact_ids']=['conflict']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):validate_lesson(load_catalog(),d,r)


def test_batch41_distinct_events_and_exact_source_digest():
    ds=batch()
    assert ds[0]['facts']['wto']['verified_answers']==['JST','Jahon savdo tashkiloti','2001-yil']
    assert '2003' in ds[4]['facts']['erdoganpm']['claim'] and '2014' in ds[4]['facts']['erdoganpres']['claim']
    assert '2016' in ds[6]['facts']['tashkent']['claim']
    assert '2004' in ds[6]['facts']['karzai']['claim']
    assert ds[8]['facts']['madrid']['verified_answers']==['Madrid','1991-yil oktabr']
    assert ds[8]['facts']['oslo']['verified_answers']==['Oslo']
    assert ds[8]['facts']['washington']['verified_answers']==['Vashington','1993-yil']
    assert ds[9]['facts']['peso']['verified_answers']==['Peso']
    d=ds[8];r=read_json(DIRECTORY/'grade11_paragraph24_review.json')
    assert all(row['reviewed_on']=='2026-10-29' for row in r['source_pages'])
    next(row for row in r['source_pages'] if row['pdf_page']==111)['page_image_sha256']='0'*64
    with pytest.raises(ValueError,match='exact_original_page_digest_required'):validate_lesson(load_catalog(),d,r)


def test_all215_units4300_xp_once_and_existing_progress_preserved(history):
    client,factory,_=history
    for d in load_lessons()[:215]:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        result=finish(client,attempt);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==4300
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==215
        assert db.get(User,42).xp_total==137
    catalog=client.get(PREFIX+'/catalog',params={'grade':11}).json()
    assert all(r['state']=='completed' for r in catalog['lessons'][:25])
    assert all(r['state']!='completed' for r in catalog['lessons'][25:])
    assert catalog['grade_content_complete']==(catalog['implemented_sections']==29)
    assert not catalog['course_complete']
