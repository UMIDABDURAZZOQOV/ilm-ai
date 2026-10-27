"""Grades6 paragraphs1–6: reviewed source coverage and real sequential v2 flow."""
from copy import deepcopy
from uuid import uuid4

import pytest

from test_world_history_lesson import history, PREFIX, answer_for, send, finish  # noqa: F401
from services.world_history_lessons import load_lessons, validate_lesson
from services.world_history_validation import load_catalog, read_json, DIRECTORY, fingerprint
from services.models import User
from services.world_history_models import WorldHistoryProgress


def test_first_batch_preserves_every_source_paragraph_and_taught_objective_keys():
    documents=load_lessons()[:6]
    assert len(documents)==6
    assert [d['sequence'] for d in documents]==list(range(1,7))
    assert [len(d['content']['cards']) for d in documents]==[13,8,9,8,8,9]
    assert sum(len(d['facts']) for d in documents)==92
    assert sum(len(d['assessments']) for d in documents)==58
    assert sum(q['response_kind']=='short_text' for d in documents for q in d['assessments'])==19
    for d in documents:
        assert all(d['facts'][i]['automatic_assessment_allowed'] for q in d['assessments'] for i in q['fact_ids'])
        assert all(r['automatic_score'] is False for r in d['content']['reflections'])
    assert {p for r in documents[1]['source_refs'] for p in r['pdf_pages']}==set(range(13,18))
    assert {p for r in documents[2]['source_refs'] for p in r['pdf_pages']}==set(range(18,22))
    assert documents[3]['source_refs'][-1]['regions']==['above_next_heading']
    assert documents[5]['facts']['map-key']['source_refs'][0]['pdf_pages']==[29]


def test_six_real_lessons_follow_prerequisites_and_award120_once(history):
    client,factory,_=history
    documents=load_lessons()[:6]
    request={'assessment_version':2,'request_id':str(uuid4())}
    assert client.post(f"{PREFIX}/lessons/{documents[1]['key']}/start",json=request).status_code==403
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text
        attempt=response.json()
        for q in d['assessments']:
            result=send(client,attempt,q,answer_for(q))
            assert result.status_code==200,result.text
            assert result.json()['is_correct']
        result=finish(client,attempt)
        assert result.status_code==200,result.text
        assert result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==120
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==6
        assert db.get(User,42).xp_total==137
    catalog=client.get(PREFIX+'/catalog').json()
    assert catalog['implemented_sections']==sum(d['grade']==6 for d in load_lessons()) and catalog['source_sections']==46
    assert all(r['state']=='completed' for r in catalog['lessons'][:6])
    assert all(r['state']!='completed' for r in catalog['lessons'][6:])
    assert catalog['grade_content_complete'] is True and catalog['course_complete'] is False


@pytest.mark.parametrize('number',[2,3,4,5,6])
def test_adjacent_paragraph_content_cannot_be_cited_as_full_shared_page(number):
    d=deepcopy(load_lessons()[number-1])
    review=read_json(DIRECTORY/f'grade6_paragraph{number:02d}_review.json')
    d['source_refs'][0]['regions']=['topic_body']
    review['source_pages'][0]['region']='topic_body'
    review['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):
        validate_lesson(load_catalog(),d,review)


def test_frq_cannot_accept_a_different_concept_from_the_same_fact():
    d=deepcopy(load_lessons()[5])
    review=read_json(DIRECTORY/'grade6_paragraph06_review.json')
    q=next(q for q in d['assessments'] if q['response_kind']=='short_text' and q['grading_spec']['expected']=='Nom')
    # Nomarx is a real word in the same source fact, but not an alias for Nom.
    q['grading_spec']['aliases'].append('Nomarx')
    review['lesson_sha256']=fingerprint(d)
    review['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,review)


def test_source_activity_cannot_claim_an_unimplemented_target():
    d=load_lessons()[1]
    review=read_json(DIRECTORY/'grade6_paragraph02_review.json')
    review['source_activity_coverage'][0]['covered_by']=['invented-activity']
    with pytest.raises(ValueError,match='source_activity_must_resolve'):
        validate_lesson(load_catalog(),d,review)
