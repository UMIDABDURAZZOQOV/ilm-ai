"""Grade7 paragraphs6–10: original regions, finite targets and separate progress."""
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
    return [d for d in load_lessons() if d['grade']==7 and 6<=d['sequence']<=10]


def test_batch11_exact_source_order_counts_and_ungraded_interpretations():
    documents=batch()
    assert [d['sequence'] for d in documents]==[6,7,8,9,10]
    assert [len(d['facts']) for d in documents]==[15,16,16,21,16]
    assert [len(d['content']['cards']) for d in documents]==[6,7,8,8,8]
    assert [len(d['assessments']) for d in documents]==[10,10,10,12,10]
    assert sum(q['response_kind']=='short_text' for d in documents for q in d['assessments'])==20
    assert all(d['book_id']=='world-history-7-uz-2017' for d in documents)
    assert documents[-1]['source_refs'][0]['chapter_id']=='wh7-chapter02'
    for d in documents:
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
    for index,identifier in [(0,'economy'),(0,'later'),(1,'beliefs'),(1,'piast'),(2,'chronicle'),(2,'law_source'),(3,'traditions'),(3,'technology'),(4,'revelation'),(4,'social'),(4,'unification')]:
        assert not documents[index]['facts'][identifier]['automatic_assessment_allowed']


@pytest.mark.parametrize('number,ending',[(6,False),(7,False),(8,False),(9,False),(10,False),(6,True),(8,True)])
def test_batch11_source_regions_cannot_expand(number,ending):
    d=deepcopy(batch()[number-6]);r=read_json(DIRECTORY/f'grade7_paragraph{number:02d}_review.json')
    index=-1 if ending else 0
    d['source_refs'][index]['regions']=['topic_body'];r['source_pages'][index]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_next_topic_whole_pages_are_excluded_and_city_names_not_rivers():
    documents=batch()
    for index,excluded in [(1,37),(3,47),(4,51)]:
        assert excluded not in [p for ref in documents[index]['source_refs'] for p in ref['pdf_pages']]
    fact=documents[2]['facts']['itil_city']
    assert 'Volga' not in fact['verified_answers']+fact['approved_aliases']
    assert 'Vladimir Monomax' not in documents[2]['facts']['vladimir']['approved_aliases']


def test_hijra_madina_and_mecca_have_question_specific_finite_targets():
    d=batch()[-1]
    for index,correct,wrong in [(6,'Hijrat','Madina'),(7,'Qur’on','Hijrat'),(8,'Makka','Madina'),(9,'Madina','Yasrib')]:
        spec=d['assessments'][index]['grading_spec']
        assert grade_answer(spec,{'value':correct})=='correct'
        assert grade_answer(spec,{'value':wrong})=='incorrect'
    d=deepcopy(d);r=read_json(DIRECTORY/'grade7_paragraph10_review.json')
    d['assessments'][-1]['grading_spec']['aliases'].append('Yasrib')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_religious_belief_cannot_replace_an_assessable_book_name():
    d=deepcopy(batch()[-1]);r=read_json(DIRECTORY/'grade7_paragraph10_review.json')
    d['assessments'][3]['fact_ids']=['revelation']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][3]['key']]['fact_ids']=['revelation']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_all56_units1120_xp_once_preserve_grade6_and_existing_users(history):
    client,factory,_=history;documents=load_lessons()[:56]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        response=finish(client,attempt);assert response.status_code==200 and response.json()['xp_awarded']==20
        assert finish(client,attempt).json()==response.json()
    with factory() as db:
        assert db.get(User,1).xp_total==1120
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==56
        assert db.get(User,42).xp_total==137
    six=client.get(PREFIX+'/catalog',params={'grade':6}).json()
    seven=client.get(PREFIX+'/catalog',params={'grade':7}).json()
    assert six['grade_content_complete'] and not seven['grade_content_complete']
    assert all(r['state']=='completed' for r in six['lessons'])
    assert all(r['state']=='completed' for r in seven['lessons'][:10])
    assert all(r['state']!='completed' for r in seven['lessons'][10:])
    assert seven['source_review_issue_count']==44-len(seven['lessons'])
    assert not six['course_complete'] and not seven['course_complete']
