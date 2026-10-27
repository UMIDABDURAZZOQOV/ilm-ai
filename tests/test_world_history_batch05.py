"""Greek sources: region boundaries, finite aliases and once-only shared v2 XP."""
from copy import deepcopy
from uuid import uuid4

import pytest

from test_world_history_lesson import history, PREFIX, answer_for, send, finish  # noqa: F401
from services.world_history_lessons import load_lessons, validate_lesson
from services.world_history_validation import DIRECTORY, fingerprint, load_catalog, read_json
from services.chemistry_grading import grade_answer
from services.models import User
from services.world_history_models import WorldHistoryProgress


def test_batch05_reviewed_counts_scope_and_source_decisions():
    documents=load_lessons();assert len(documents)>=26
    batch=documents[21:26]
    assert [len(d['facts']) for d in batch]==[19,11,14,13,11]
    assert [len(d['content']['cards']) for d in batch]==[9,6,8,6,6]
    assert [len(d['assessments']) for d in batch]==[10,10,10,10,8]
    assert sum(q['response_kind']=='short_text' for d in batch for q in d['assessments'])==20
    for d,span in zip(batch,[(86,90),(91,93),(93,97),(98,101),(102,104)]):
        assert [r['pdf_pages'][0] for r in d['source_refs']]==list(range(span[0],span[1]+1))
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
    for n,identifier in [(0,'citizenship-scope'),(0,'spartan-model'),(1,'outsider-label'),(2,'reform-scope'),(3,'runner'),(3,'three-hundred'),(3,'ending'),(4,'rhetoric')]:
        assert not batch[n]['facts'][identifier]['automatic_assessment_allowed']
    assert 'hierarchy-review' not in batch[2]['facts']
    assert 'period-review' not in batch[1]['facts']
    assert batch[1]['source_refs'][-1]['regions']==['above_next_heading']
    assert batch[4]['source_refs'][-1]['regions']==['above_next_heading']


@pytest.mark.parametrize('number',[22,23,24,25,26])
def test_batch05_cannot_expand_opening_page_scope(number):
    d=deepcopy(load_lessons()[number-1]);r=read_json(DIRECTORY/f'grade6_paragraph{number:02d}_review.json')
    d['source_refs'][0]['regions']=['topic_body'];r['source_pages'][0]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


@pytest.mark.parametrize('number',[23,26])
def test_batch05_cannot_expand_shared_closing_page(number):
    d=deepcopy(load_lessons()[number-1]);r=read_json(DIRECTORY/f'grade6_paragraph{number:02d}_review.json')
    d['source_refs'][-1]['regions']=['topic_body'];r['source_pages'][-1]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_reviewed_periek_spellings_do_not_accept_another_social_group():
    d=load_lessons()[21];q=d['assessments'][-1]
    for alias in ['Periek','Periyek','Perieklar','Periyeklar']:
        assert grade_answer(q['grading_spec'],{'value':alias})=='correct'
    assert grade_answer(q['grading_spec'],{'value':'Ilotlar'})=='incorrect'
    d=deepcopy(d);r=read_json(DIRECTORY/'grade6_paragraph22_review.json')
    d['assessments'][-1]['grading_spec']['aliases'].append('Ilotlar')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_all_twenty_six_prerequisites_and520_xp_once(history):
    client,factory,_=history;documents=load_lessons()[:26]
    assert client.post(f"{PREFIX}/lessons/{documents[21]['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())}).status_code==403
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text
        attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q))
            assert response.status_code==200 and response.json()['is_correct']
        response=finish(client,attempt);assert response.status_code==200
        assert response.json()['xp_awarded']==20
        assert finish(client,attempt).json()==response.json()
    with factory() as db:
        assert db.get(User,1).xp_total==520
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==26
        assert db.get(User,42).xp_total==137
    catalog=client.get(PREFIX+'/catalog').json()
    assert catalog['implemented_sections']==sum(d['grade']==6 for d in load_lessons()) and catalog['source_sections']==46
    assert all(r['state']=='completed' for r in catalog['lessons'][:26])
    assert all(r['state']!='completed' for r in catalog['lessons'][26:])
    assert catalog['grade_content_complete'] and not catalog['course_complete']
