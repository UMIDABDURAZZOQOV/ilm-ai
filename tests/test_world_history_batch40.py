"""Grade11 topics6–15 exact source boundaries and question-specific targets."""
from copy import deepcopy
from uuid import uuid4

import pytest

from test_world_history_lesson import history, PREFIX, answer_for, send, finish  # noqa: F401
from services.world_history_lessons import load_lessons, validate_lesson
from services.world_history_validation import DIRECTORY, fingerprint, load_catalog, read_json
from services.chemistry_grading import grade_answer
from services.models import User
from services.world_history_models import WorldHistoryProgress


def batch():return load_lessons()[195:205]


def test_batch40_source_order_and_counts():
    ds=batch();book=load_catalog()['books'][5]
    assert [(d['grade'],d['sequence']) for d in ds]==[(11,n) for n in range(6,16)]
    assert [len(d['facts']) for d in ds]==[16,16,21,13,15,12,15,14,13,11]
    assert all(len(d['content']['cards'])==8 and len(d['assessments'])==10 for d in ds)
    assert sum(q['response_kind']=='short_text' for d in ds for q in d['assessments'])==40
    assert [next(row for row in book['records'] if row['id']==d['topic_id'])['source_numbers'] for d in ds]==[[n] for n in range(6,16)]
    for d in ds:
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])


@pytest.mark.parametrize('index,page',[(0,29),(0,33),(1,33),(1,38),(2,38),(3,44),(4,48),(4,52),(5,52),(5,55),(6,55),(6,60),(7,60),(7,64),(8,64),(8,68),(9,68),(9,72)])
def test_batch40_adjacent_topic_boundary_not_whole_page(index,page):
    d=deepcopy(batch()[index]);r=read_json(DIRECTORY/f"grade11_paragraph{d['sequence']:02d}_review.json")
    next(ref for ref in d['source_refs'] if ref['pdf_pages']==[page])['regions']=['topic_body']
    next(row for row in r['source_pages'] if row['pdf_page']==page)['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_batch40_question_targets_cannot_be_broadened():
    ds=batch()
    for d in ds:
        frq=[q for q in d['assessments'] if q['response_kind']=='short_text']
        for q,other in zip(frq,frq[1:]+frq[:1]):
            assert grade_answer(q['grading_spec'],{'value':other['grading_spec']['expected']})=='incorrect'
    d=deepcopy(ds[0]);r=read_json(DIRECTORY/'grade11_paragraph06_review.json')
    q=d['assessments'][6];q['grading_spec']['aliases'].append('Harakat')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):validate_lesson(load_catalog(),d,r)


def test_batch40_politics_religion_and_uncertain_claims_not_keys():
    ds=batch()
    for i,keys in [(0,['tigers','latviaeconomy','estoniarelations','portraits']),(1,['azerpolicy','map','georgiapolitics','armeniarelations']),(2,['region','kazpolicy','tajikwar','kyrgyzpolitics','visits','technology']),(3,['integration','rights','catalonia','relations']),(4,['economy','campaign','foreign']),(5,['reforms','economy','foreign','migration']),(6,['economy','reforms','foreign']),(7,['privatization','politics','postindustrial','social']),(8,['industry','services','parties','economy','neofascism']),(9,['regions','demography','asia','religion','latin','left'])]:
        assert all(not ds[i]['facts'][k]['automatic_assessment_allowed'] for k in keys)
    d=deepcopy(ds[9]);r=read_json(DIRECTORY/'grade11_paragraph15_review.json')
    q=d['assessments'][0];q['fact_ids']=['religion']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][q['key']]['fact_ids']=['religion']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):validate_lesson(load_catalog(),d,r)


def test_batch40_event_instruments_legend_and_exact_page_digest():
    ds=batch()
    assert ds[0]['facts']['latvia']['verified_answers']==['1990-yil 4-may']
    assert ds[0]['facts']['estonia']['verified_answers']==['1988-yil 16-noyabr']
    assert ds[1]['facts']['referendum']['verified_answers']==['1991-yil 21-sentabr']
    assert ds[2]['facts']['turkmenreferendum']['verified_answers']==['1991-yil 26-oktabr']
    assert ds[2]['facts']['rahmon']['approved_aliases']==['Imomali Rahmonov','Imomali Rahmon']
    assert ds[3]['facts']['maastricht']['verified_answers']==['1993-yil']
    assert ds[6]['facts']['referendum']['verified_answers']==['2016-yil iyun']
    assert ds[9]['facts']['sunni']['verified_answers']==['Sunniylar']
    assert ds[9]['facts']['shia']['verified_answers']==['Shialar']
    d=ds[2];r=read_json(DIRECTORY/'grade11_paragraph08_review.json')
    assert all(row['reviewed_on']=='2026-10-29' for row in r['source_pages'])
    next(row for row in r['source_pages'] if row['pdf_page']==40)['page_image_sha256']='0'*64
    with pytest.raises(ValueError,match='exact_original_page_digest_required'):validate_lesson(load_catalog(),d,r)


def test_all205_units4100_xp_once_and_existing_progress_preserved(history):
    client,factory,_=history
    for d in load_lessons()[:205]:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        result=finish(client,attempt);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==4100
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==205
        assert db.get(User,42).xp_total==137
    catalog=client.get(PREFIX+'/catalog',params={'grade':11}).json()
    assert all(r['state']=='completed' for r in catalog['lessons'][:15])
    assert all(r['state']!='completed' for r in catalog['lessons'][15:])
    assert catalog['grade_content_complete']==(catalog['implemented_sections']==29)
    assert not catalog['course_complete']
