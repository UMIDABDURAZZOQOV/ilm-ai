"""Grade7 paragraphs16–20: historical vocabulary, mixed causes and finite aliases."""
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
    return [d for d in load_lessons() if d['grade']==7 and 16<=d['sequence']<=20]


def test_batch13_counts_original_order_scoped_knowledge_and_activities():
    documents=batch()
    assert [d['sequence'] for d in documents]==[16,17,18,19,20]
    assert [len(d['facts']) for d in documents]==[17,17,16,12,15]
    assert [len(d['content']['cards']) for d in documents]==[7,7,7,6,7]
    assert [len(d['assessments']) for d in documents]==[10,10,10,10,12]
    assert sum(q['response_kind']=='short_text' for d in documents for q in d['assessments'])==20
    assert all(ref['chapter_id']=='wh7-chapter03' for d in documents for ref in d['source_refs'])
    for d in documents:
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
    for index,identifier in [(0,'exchange'),(0,'fair_life'),(1,'growth'),(1,'japan'),(2,'dissent'),(2,'repression'),(3,'promises'),(3,'merchants'),(4,'violence'),(4,'causes')]:
        assert not documents[index]['facts'][identifier]['automatic_assessment_allowed']


@pytest.mark.parametrize('number,ending',[(n,end) for n in range(16,21) for end in [False,True]])
def test_batch13_shared_source_regions_are_exact(number,ending):
    d=deepcopy(batch()[number-16]);r=read_json(DIRECTORY/f'grade7_paragraph{number:02d}_review.json')
    index=-1 if ending else 0
    d['source_refs'][index]['regions']=['topic_body'];r['source_pages'][index]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_historical_alternate_name_cannot_override_the_question_target():
    documents=batch();d=documents[-1];spec=d['assessments'][9]['grading_spec']
    assert grade_answer(spec,{'value':'Ioanniylar'})=='correct'
    assert grade_answer(spec,{'value':'Gospitalyerlar'})=='incorrect'
    assert grade_answer(d['assessments'][8]['grading_spec'],{'value':'Aleksey II'})=='incorrect'
    assert grade_answer(documents[0]['assessments'][8]['grading_spec'],{'value':'G‘azna'})=='incorrect'
    d=deepcopy(d);r=read_json(DIRECTORY/'grade7_paragraph20_review.json')
    d['assessments'][9]['grading_spec']['aliases'].append('Gospitalyerlar')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_attributed_promise_cannot_replace_a_historical_identity_key():
    d=deepcopy(batch()[3]);r=read_json(DIRECTORY/'grade7_paragraph19_review.json')
    d['assessments'][0]['fact_ids']=['promises']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][0]['key']]['fact_ids']=['promises']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_all66_units1320_xp_once_preserve_grades_and_existing_user(history):
    client,factory,_=history;documents=load_lessons()[:66]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        response=finish(client,attempt);assert response.status_code==200 and response.json()['xp_awarded']==20
        assert finish(client,attempt).json()==response.json()
    with factory() as db:
        assert db.get(User,1).xp_total==1320
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==66
        assert db.get(User,42).xp_total==137
    six=client.get(PREFIX+'/catalog',params={'grade':6}).json()
    seven=client.get(PREFIX+'/catalog',params={'grade':7}).json()
    assert six['grade_content_complete']
    assert seven['grade_content_complete']==(seven['implemented_sections']==44)
    assert all(r['state']=='completed' for r in six['lessons'])
    assert all(r['state']=='completed' for r in seven['lessons'][:20])
    assert all(r['state']!='completed' for r in seven['lessons'][20:])
    assert seven['source_review_issue_count']==44-len(seven['lessons'])
    assert not six['course_complete'] and not seven['course_complete']
