"""Grade7 paragraphs11–15: book-scoped terminology, evidence and original activities."""
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
    return [d for d in load_lessons() if d['grade']==7 and 11<=d['sequence']<=15]


def test_batch12_counts_original_order_and_assessment_scope():
    documents=batch()
    assert [d['sequence'] for d in documents]==[11,12,13,14,15]
    assert [len(d['facts']) for d in documents]==[18,16,17,22,19]
    assert [len(d['content']['cards']) for d in documents]==[7,7,7,9,9]
    assert [len(d['assessments']) for d in documents]==[10,10,10,12,10]
    assert sum(q['response_kind']=='short_text' for d in documents for q in d['assessments'])==20
    assert documents[-1]['source_refs'][0]['chapter_id']=='wh7-chapter03'
    for d in documents:
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
    for index,identifier in [(0,'expansion'),(0,'fragmentation'),(1,'grant'),(1,'land'),(2,'coin'),(2,'campaigns'),(3,'gunpowder'),(3,'indian_science'),(4,'conditions'),(4,'inequality')]:
        assert not documents[index]['facts'][identifier]['automatic_assessment_allowed']


@pytest.mark.parametrize('number,ending',[(11,False),(12,False),(13,False),(14,False),(15,False),(11,True),(12,True),(13,True),(15,True)])
def test_batch12_exact_shared_source_region(number,ending):
    d=deepcopy(batch()[number-11]);r=read_json(DIRECTORY/f'grade7_paragraph{number:02d}_review.json')
    index=-1 if ending else 0
    d['source_refs'][index]['regions']=['topic_body'];r['source_pages'][index]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_finite_book_names_roles_and_diagram_targets():
    documents=batch()
    spec=documents[1]['assessments'][-1]['grading_spec']
    assert grade_answer(spec,{'value':'Chandragupta I'})=='correct'
    assert grade_answer(spec,{'value':'Chandragupta Maurya'})=='incorrect'
    assert 'Kalkutta' not in documents[1]['facts']['kalikut']['approved_aliases']
    assert 65 not in [p for ref in documents[3]['source_refs'] for p in ref['pdf_pages']]
    last=documents[-1]
    assert grade_answer(last['assessments'][-1]['grading_spec'],{'value':'Xalfa'})=='correct'
    assert grade_answer(last['assessments'][-1]['grading_spec'],{'value':'Shogird'})=='incorrect'
    assert last['assessments'][1]['grading_spec']['verified_answer']=='Bahorgi ekin — kuzgi ekin — shudgor'
    assert not any('grant' in q['fact_ids'] for q in documents[1]['assessments'])
    assert not any('gunpowder' in q['fact_ids'] for q in documents[3]['assessments'])


def test_uncertain_grant_word_cannot_become_an_automatic_answer():
    d=deepcopy(batch()[1]);r=read_json(DIRECTORY/'grade7_paragraph12_review.json')
    d['assessments'][3]['fact_ids']=['grant']
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    r['approved_answer_targets'][d['assessments'][3]['key']]['fact_ids']=['grant']
    with pytest.raises(ValueError,match='graded_question_must_use_taught_assessable_facts'):
        validate_lesson(load_catalog(),d,r)


def test_all61_units1220_xp_once_keep_separate_grade_progress_and_old_user(history):
    client,factory,_=history;documents=load_lessons()[:61]
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        response=finish(client,attempt);assert response.status_code==200 and response.json()['xp_awarded']==20
        assert finish(client,attempt).json()==response.json()
    with factory() as db:
        assert db.get(User,1).xp_total==1220
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==61
        assert db.get(User,42).xp_total==137
    six=client.get(PREFIX+'/catalog',params={'grade':6}).json()
    seven=client.get(PREFIX+'/catalog',params={'grade':7}).json()
    assert six['grade_content_complete'] and not seven['grade_content_complete']
    assert all(r['state']=='completed' for r in six['lessons'])
    assert all(r['state']=='completed' for r in seven['lessons'][:15])
    assert all(r['state']!='completed' for r in seven['lessons'][15:])
    assert seven['source_review_issue_count']==44-len(seven['lessons'])
    assert not six['course_complete'] and not seven['course_complete']
