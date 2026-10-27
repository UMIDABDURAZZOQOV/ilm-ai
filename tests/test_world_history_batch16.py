"""Grade7 paragraphs31–35: cultural vocabulary, chronology and exact source scope."""
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
    return [d for d in load_lessons() if d['grade']==7 and 31<=d['sequence']<=35]


def test_batch16_counts_source_chapter_transition_and_ungraded_interpretations():
    documents=batch()
    assert [d['sequence'] for d in documents]==[31,32,33,34,35]
    assert [len(d['facts']) for d in documents]==[13,16,19,9,17]
    assert [len(d['content']['cards']) for d in documents]==[6,8,8,5,7]
    assert [len(d['assessments']) for d in documents]==[10,12,12,8,12]
    assert sum(q['response_kind']=='short_text' for d in documents for q in d['assessments'])==20
    assert all(ref['chapter_id']=='wh7-chapter04' for d in documents[:3] for ref in d['source_refs'])
    assert all(ref['chapter_id']=='wh7-chapter05' for d in documents[3:] for ref in d['source_refs'])
    for d in documents:
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
    for index,identifier in [(0,'growth'),(0,'periodization'),(1,'worldview'),(1,'belief'),(2,'education'),(2,'scenes'),(3,'economy'),(3,'ethnogenesis'),(4,'range'),(4,'coercion'),(4,'land')]:
        assert not documents[index]['facts'][identifier]['automatic_assessment_allowed']
    for index,page in [(1,117),(2,121)]:
        assert page not in [p for ref in documents[index]['source_refs'] for p in ref['pdf_pages']]
    assert 'bursa' not in documents[4]['facts']
    assert documents[4]['assessments'][7]['grading_spec']['verified_answer']=='Angara — Konstantinopolning olinishi'


@pytest.mark.parametrize('number,ending',[(31,False),(32,False),(33,False),(34,False),(35,False),(31,True),(34,True),(35,True)])
def test_batch16_exact_shared_source_regions(number,ending):
    d=deepcopy(batch()[number-31]);r=read_json(DIRECTORY/f'grade7_paragraph{number:02d}_review.json')
    index=-1 if ending else 0
    d['source_refs'][index]['regions']=['topic_body'];r['source_pages'][index]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_roles_ordinals_and_nickname_targets_are_finite():
    documents=batch()
    for n,index,wrong in [(0,7,'Dmitriy Ivanovich'),(1,10,'Kansler'),(2,9,'Miniatyura'),(3,6,'Roman III Diogen'),(4,9,'Mehmet I'),(4,10,'Boyazid')]:
        assert grade_answer(documents[n]['assessments'][index]['grading_spec'],{'value':wrong})=='incorrect'
    d=deepcopy(documents[1]);r=read_json(DIRECTORY/'grade7_paragraph32_review.json')
    d['assessments'][10]['grading_spec']['aliases'].append('Kansler')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_coercive_recruitment_context_cannot_become_an_automatic_fact_key():
    d=deepcopy(batch()[-1]);r=read_json(DIRECTORY/'grade7_paragraph35_review.json')
    d['assessments'][0]['fact_ids']=['coercion']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][0]['key']]['fact_ids']=['coercion']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_all81_units1620_xp_once_preserve_grade_history_and_old_user(history):
    client,factory,_=history;documents=load_lessons()[:81]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        response=finish(client,attempt);assert response.status_code==200 and response.json()['xp_awarded']==20
        assert finish(client,attempt).json()==response.json()
    with factory() as db:
        assert db.get(User,1).xp_total==1620
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==81
        assert db.get(User,42).xp_total==137
    six=client.get(PREFIX+'/catalog',params={'grade':6}).json()
    seven=client.get(PREFIX+'/catalog',params={'grade':7}).json()
    assert six['grade_content_complete']
    assert seven['grade_content_complete']==(seven['implemented_sections']==44)
    assert all(r['state']=='completed' for r in six['lessons'])
    assert all(r['state']=='completed' for r in seven['lessons'][:35])
    assert all(r['state']!='completed' for r in seven['lessons'][35:])
    assert seven['source_review_issue_count']==44-len(seven['lessons'])
    assert not six['course_complete'] and not seven['course_complete']
