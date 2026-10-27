"""Central Asia: distinct site names, dated networks and withheld source discrepancies."""
from copy import deepcopy
from uuid import uuid4

import pytest

from test_world_history_lesson import history, PREFIX, answer_for, send, finish  # noqa: F401
from services.world_history_lessons import load_lessons, validate_lesson
from services.world_history_validation import DIRECTORY, fingerprint, load_catalog, read_json
from services.chemistry_grading import grade_answer
from services.models import User
from services.world_history_models import WorldHistoryProgress


def test_batch07_exact_counts_and_source_scope():
    documents=load_lessons();assert len(documents)>=36
    batch=documents[31:36]
    assert [len(d['facts']) for d in batch]==[17,13,16,16,13]
    assert [len(d['content']['cards']) for d in batch]==[8,7,8,7,7]
    assert [len(d['assessments']) for d in batch]==[10]*5
    assert sum(q['response_kind']=='short_text' for d in batch for q in d['assessments'])==20
    for d,span in zip(batch,[(123,128),(129,132),(133,137),(137,141),(142,144)]):
        assert [r['pdf_pages'][0] for r in d['source_refs']]==list(range(span[0],span[1]+1))
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
    for n,identifier in [(0,'resistance'),(0,'consequences'),(1,'partition'),(1,'decline'),(2,'calendar'),(2,'capitals'),(3,'coins'),(3,'writing-evidence'),(4,'distance'),(4,'period')]:
        assert not batch[n]['facts'][identifier]['automatic_assessment_allowed']
    assert batch[2]['source_refs'][-1]['regions']==['above_next_heading']
    assert 'chess' not in batch[3]['facts']
    assert batch[4]['assessments'][7]['grading_spec']['aliases']==['F. Rixtgofen','Rixtgofen']


@pytest.mark.parametrize('number',[32,33,34,35,36])
def test_batch07_cannot_expand_shared_opening_page(number):
    d=deepcopy(load_lessons()[number-1]);r=read_json(DIRECTORY/f'grade6_paragraph{number:02d}_review.json')
    d['source_refs'][0]['regions']=['topic_body'];r['source_pages'][0]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_batch07_cannot_expand_shared_closing_page():
    d=deepcopy(load_lessons()[33]);r=read_json(DIRECTORY/'grade6_paragraph34_review.json')
    d['source_refs'][-1]['regions']=['topic_body'];r['source_pages'][-1]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_state_name_is_not_an_alias_for_every_capital_and_site():
    d=load_lessons()[33];q=d['assessments'][7]
    assert grade_answer(q['grading_spec'],{'value':'Qang‘yuy'})=='correct'
    for wrong in ['Qang‘dez','Bityan','Qang‘xa']:
        assert grade_answer(q['grading_spec'],{'value':wrong})=='incorrect'
    d=deepcopy(d);r=read_json(DIRECTORY/'grade6_paragraph34_review.json')
    d['assessments'][7]['grading_spec']['aliases'].append('Bityan')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError,match='question_specific_answer_target_review'):
        validate_lesson(load_catalog(),d,r)


def test_all_thirty_six_prerequisites_and720_xp_once(history):
    client,factory,_=history;documents=load_lessons()[:36]
    assert client.post(f"{PREFIX}/lessons/{documents[31]['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())}).status_code==403
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
        assert db.get(User,1).xp_total==720
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==36
        assert db.get(User,42).xp_total==137
    catalog=client.get(PREFIX+'/catalog').json()
    assert catalog['implemented_sections']==sum(d['grade']==6 for d in load_lessons()) and catalog['source_sections']==46
    assert all(r['state']=='completed' for r in catalog['lessons'][:36])
    assert all(r['state']!='completed' for r in catalog['lessons'][36:])
    assert catalog['grade_content_complete'] and not catalog['course_complete']
