"""Grade7 paragraphs21–25: original chapter transition, ordinals and scoped chronology."""
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
    return [d for d in load_lessons() if d['grade']==7 and 21<=d['sequence']<=25]


def test_batch14_counts_original_chapter_order_and_scoped_assessments():
    documents=batch()
    assert [d['sequence'] for d in documents]==[21,22,23,24,25]
    assert [len(d['facts']) for d in documents]==[12,15,11,12,18]
    assert [len(d['content']['cards']) for d in documents]==[6,6,5,6,8]
    assert [len(d['assessments']) for d in documents]==[10,10,10,10,12]
    assert sum(q['response_kind']=='short_text' for d in documents for q in d['assessments'])==20
    assert documents[0]['source_refs'][0]['chapter_id']=='wh7-chapter03'
    assert all(ref['chapter_id']=='wh7-chapter04' for d in documents[1:] for ref in d['source_refs'])
    for d in documents:
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
    for index,identifier in [(0,'venice'),(0,'ending'),(1,'support'),(1,'land_change'),(2,'templars'),(2,'dispute'),(3,'succession'),(3,'organization'),(4,'treaty'),(4,'centralization')]:
        assert not documents[index]['facts'][identifier]['automatic_assessment_allowed']
    for index,page in [(0,89),(4,98)]:
        assert page not in [p for ref in documents[index]['source_refs'] for p in ref['pdf_pages']]


@pytest.mark.parametrize('number,ending',[(21,False),(22,False),(23,False),(24,False),(25,False),(22,True),(23,True),(24,True)])
def test_batch14_exact_shared_source_regions(number,ending):
    d=deepcopy(batch()[number-21]);r=read_json(DIRECTORY/f'grade7_paragraph{number:02d}_review.json')
    index=-1 if ending else 0
    d['source_refs'][index]['regions']=['topic_body'];r['source_pages'][index]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_ordinals_places_and_chronology_are_question_specific():
    documents=batch()
    for n,index,wrong in [(0,8,'Mixail VII Paleolog'),(1,8,'Lyudovik IX'),(2,7,'Filipp II'),(3,7,'Kresi'),(4,11,'Lyudovik IX')]:
        assert grade_answer(documents[n]['assessments'][index]['grading_spec'],{'value':wrong})=='incorrect'
    assert documents[3]['assessments'][5]['grading_spec']['verified_answer']=='Kresi — Puate — Jakeriya'
    assert not any('treaty' in q['fact_ids'] for q in documents[4]['assessments'])
    d=deepcopy(documents[2]);r=read_json(DIRECTORY/'grade7_paragraph23_review.json')
    d['assessments'][7]['grading_spec']['aliases'].append('Filipp II')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_uncorroborated_treaty_wording_cannot_be_a_scored_fact():
    d=deepcopy(batch()[-1]);r=read_json(DIRECTORY/'grade7_paragraph25_review.json')
    d['assessments'][2]['fact_ids']=['treaty']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][2]['key']]['fact_ids']=['treaty']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_all71_units1420_xp_once_preserve_grade_history_and_old_user(history):
    client,factory,_=history;documents=load_lessons()[:71]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        response=finish(client,attempt);assert response.status_code==200 and response.json()['xp_awarded']==20
        assert finish(client,attempt).json()==response.json()
    with factory() as db:
        assert db.get(User,1).xp_total==1420
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==71
        assert db.get(User,42).xp_total==137
    six=client.get(PREFIX+'/catalog',params={'grade':6}).json()
    seven=client.get(PREFIX+'/catalog',params={'grade':7}).json()
    assert six['grade_content_complete']
    assert seven['grade_content_complete']==(seven['implemented_sections']==44)
    assert all(r['state']=='completed' for r in six['lessons'])
    assert all(r['state']=='completed' for r in seven['lessons'][:25])
    assert all(r['state']!='completed' for r in seven['lessons'][25:])
    assert seven['source_review_issue_count']==44-len(seven['lessons'])
    assert not six['course_complete'] and not seven['course_complete']
