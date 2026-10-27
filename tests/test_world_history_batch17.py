"""Grade7 paragraphs36–40: regional terms, narrative scope and original page bounds."""
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
    return [d for d in load_lessons() if d['grade']==7 and 36<=d['sequence']<=40]


def test_batch17_counts_original_order_scoped_claims_and_legend_comprehension():
    documents=batch()
    assert [d['sequence'] for d in documents]==[36,37,38,39,40]
    assert [len(d['facts']) for d in documents]==[17,18,19,13,15]
    assert [len(d['content']['cards']) for d in documents]==[7,8,8,6,7]
    assert [len(d['assessments']) for d in documents]==[12,12,12,10,10]
    assert sum(q['response_kind']=='short_text' for d in documents for q in d['assessments'])==20
    assert all(ref['chapter_id']=='wh7-chapter05' for d in documents for ref in d['source_refs'])
    for d in documents:
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
    for index,identifier in [(0,'causes'),(0,'organization'),(1,'religion'),(1,'decline'),(2,'inflation'),(2,'recovery'),(3,'dual'),(3,'hardship'),(4,'unification'),(4,'contact'),(4,'invasion')]:
        assert not documents[index]['facts'][identifier]['automatic_assessment_allowed']
    assert 'afsonaviy' in documents[4]['facts']['tangun']['claim']
    assert 'afsonasida' in documents[4]['assessments'][0]['public']['prompt']
    assert documents[0]['facts']['kalka']['source_refs'][0]['pdf_pages']==[127]
    assert documents[3]['facts']['ports']['verified_answers']==['Sakai','Xyogo','Xakata']


@pytest.mark.parametrize('number,ending',[(n,ending) for n in range(36,41) for ending in [False,True]])
def test_batch17_exact_shared_source_regions(number,ending):
    d=deepcopy(batch()[number-36]);r=read_json(DIRECTORY/f'grade7_paragraph{number:02d}_review.json')
    index=-1 if ending else 0
    d['source_refs'][index]['regions']=['topic_body'];r['source_pages'][index]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_title_office_fullname_and_polity_targets_cannot_be_interchanged():
    documents=batch()
    for n,index,wrong in [(0,9,'Temuchin'),(1,8,'Ulusbegi'),(2,9,'Yuan Chjan'),(3,6,'Mikado'),(4,7,'Koguryo')]:
        assert grade_answer(documents[n]['assessments'][index]['grading_spec'],{'value':wrong})=='incorrect'
    d=deepcopy(documents[2]);r=read_json(DIRECTORY/'grade7_paragraph38_review.json')
    d['assessments'][9]['grading_spec']['aliases'].append('Yuan Chjan')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_uncertain_invasion_period_cannot_become_an_automatic_key():
    d=deepcopy(batch()[-1]);r=read_json(DIRECTORY/'grade7_paragraph40_review.json')
    d['assessments'][0]['fact_ids']=['invasion']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][0]['key']]['fact_ids']=['invasion']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_all86_units1720_xp_once_preserve_grade_history_and_old_user(history):
    client,factory,_=history;documents=load_lessons()[:86]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        response=finish(client,attempt);assert response.status_code==200 and response.json()['xp_awarded']==20
        assert finish(client,attempt).json()==response.json()
    with factory() as db:
        assert db.get(User,1).xp_total==1720
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==86
        assert db.get(User,42).xp_total==137
    six=client.get(PREFIX+'/catalog',params={'grade':6}).json()
    seven=client.get(PREFIX+'/catalog',params={'grade':7}).json()
    assert six['grade_content_complete']
    assert seven['grade_content_complete']==(seven['implemented_sections']==44)
    assert all(r['state']=='completed' for r in six['lessons'])
    assert all(r['state']=='completed' for r in seven['lessons'][:40])
    assert all(r['state']!='completed' for r in seven['lessons'][40:])
    assert seven['source_review_issue_count']==44-len(seven['lessons'])
    assert not six['course_complete'] and not seven['course_complete']
