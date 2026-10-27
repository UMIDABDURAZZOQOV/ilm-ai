"""Grade7 paragraphs26–30: bounded images, identities, source claims and saved progress."""
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
    return [d for d in load_lessons() if d['grade']==7 and 26<=d['sequence']<=30]


def test_batch15_counts_source_order_and_ungraded_interpretations():
    documents=batch()
    assert [d['sequence'] for d in documents]==[26,27,28,29,30]
    assert [len(d['facts']) for d in documents]==[16,15,16,12,13]
    assert [len(d['content']['cards']) for d in documents]==[7,7,7,6,6]
    assert [len(d['assessments']) for d in documents]==[10,12,10,10,10]
    assert sum(q['response_kind']=='short_text' for d in documents for q in d['assessments'])==20
    assert all(ref['chapter_id']=='wh7-chapter04' for d in documents for ref in d['source_refs'])
    for d in documents:
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
    for index,identifier in [(0,'land'),(0,'charter_scope'),(1,'demands'),(1,'aftermath'),(2,'economy'),(2,'roncal'),(3,'fragmentation'),(3,'unification'),(4,'tribute'),(4,'consequences'),(4,'baltic')]:
        assert not documents[index]['facts'][identifier]['automatic_assessment_allowed']
    assert documents[0]['facts']['robin']['claim'].startswith('Robin Gud xalq og‘zaki ijodi')
    for index,page in [(0,102),(2,108)]:
        assert page not in [p for ref in documents[index]['source_refs'] for p in ref['pdf_pages']]


@pytest.mark.parametrize('number,ending',[(26,False),(27,False),(28,False),(29,False),(30,False),(27,True),(29,True),(30,True)])
def test_batch15_exact_shared_source_regions(number,ending):
    d=deepcopy(batch()[number-26]);r=read_json(DIRECTORY/f'grade7_paragraph{number:02d}_review.json')
    index=-1 if ending else 0
    d['source_refs'][index]['regions']=['topic_body'];r['source_pages'][index]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_names_ordinals_and_nickname_targets_cannot_be_interchanged():
    documents=batch()
    for n,index,wrong in [(0,6,'Graf'),(1,11,'Genrix II'),(2,6,'Fridrix II'),(2,8,'Neapol universiteti'),(3,7,'Vladimir'),(4,7,'Aleksandr Yaroslavich'),(4,9,'Nevskiy')]:
        assert grade_answer(documents[n]['assessments'][index]['grading_spec'],{'value':wrong})=='incorrect'
    d=deepcopy(documents[4]);r=read_json(DIRECTORY/'grade7_paragraph30_review.json')
    d['assessments'][7]['grading_spec']['aliases'].append('Aleksandr Yaroslavich')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_unresolved_yaroslav_identity_cannot_be_a_scored_fact():
    d=deepcopy(batch()[-1]);r=read_json(DIRECTORY/'grade7_paragraph30_review.json')
    d['assessments'][0]['fact_ids']=['tribute']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][0]['key']]['fact_ids']=['tribute']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_all76_units1520_xp_once_preserve_grade_history_and_old_user(history):
    client,factory,_=history;documents=load_lessons()[:76]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        response=finish(client,attempt);assert response.status_code==200 and response.json()['xp_awarded']==20
        assert finish(client,attempt).json()==response.json()
    with factory() as db:
        assert db.get(User,1).xp_total==1520
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==76
        assert db.get(User,42).xp_total==137
    six=client.get(PREFIX+'/catalog',params={'grade':6}).json()
    seven=client.get(PREFIX+'/catalog',params={'grade':7}).json()
    assert six['grade_content_complete']
    assert seven['grade_content_complete']==(seven['implemented_sections']==44)
    assert all(r['state']=='completed' for r in six['lessons'])
    assert all(r['state']=='completed' for r in seven['lessons'][:30])
    assert all(r['state']!='completed' for r in seven['lessons'][30:])
    assert seven['source_review_issue_count']==44-len(seven['lessons'])
    assert not six['course_complete'] and not seven['course_complete']
