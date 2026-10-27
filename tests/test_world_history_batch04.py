"""Reviewed China/Central Asia/Greece sources; unresolved claims stay ungraded."""
from copy import deepcopy
from uuid import uuid4

import pytest

from test_world_history_lesson import history, PREFIX, answer_for, send, finish  # noqa: F401
from services.world_history_lessons import load_lessons, validate_lesson
from services.world_history_validation import DIRECTORY, fingerprint, load_catalog, read_json
from services.chemistry_grading import grade_answer
from services.models import User
from services.world_history_models import WorldHistoryProgress


def test_batch04_exact_source_counts_and_unresolved_fact_exclusions():
    documents=load_lessons();assert len(documents)>=21
    batch=documents[16:21]
    assert [len(d['facts']) for d in batch]==[12,17,16,15,11]
    assert [len(d['content']['cards']) for d in batch]==[8,9,10,8,6]
    assert [len(d['assessments']) for d in batch]==[8,10,10,10,8]
    assert sum(q['response_kind']=='short_text' for d in batch for q in d['assessments'])==20
    for d,span in zip(batch,[(68,71),(72,75),(75,79),(80,83),(84,86)]):
        assert [r['pdf_pages'][0] for r in d['source_refs']]==list(range(span[0],span[1]+1))
        assert d['source_refs'][0]['regions']==['below_topic_heading']
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])
    for n,identifier in [(0,'date-discrepancy'),(0,'rice-origin'),(1,'qin-date'),(1,'seismo-prediction'),(2,'bactrian-state'),(3,'name-etymology'),(4,'mountain-fraction'),(4,'collapse')]:
        assert not batch[n]['facts'][identifier]['automatic_assessment_allowed']
    assert all('seismo-prediction' not in q['fact_ids'] for q in batch[1]['assessments'])
    assert 'oldindan' not in batch[1]['facts']['seismo']['claim']
    assert batch[1]['source_refs'][-1]['regions']==['above_next_heading']
    assert batch[4]['source_refs'][-1]['regions']==['above_next_heading']
    assert batch[2]['title']=='O‘zbekiston hududidagi ilk davlatlar'


@pytest.mark.parametrize('number',[17,18,19,20,21])
def test_batch04_cannot_expand_shared_opening_region(number):
    d=deepcopy(load_lessons()[number-1]);r=read_json(DIRECTORY/f'grade6_paragraph{number:02d}_review.json')
    d['source_refs'][0]['regions']=['topic_body'];r['source_pages'][0]['region']='topic_body'
    r['lesson_sha256']=fingerprint(d)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_olymp_mountain_is_not_an_olimpiya_alias():
    d=deepcopy(load_lessons()[20]);r=read_json(DIRECTORY/'grade6_paragraph21_review.json')
    q=d['assessments'][4];q['grading_spec']['aliases'].append('Olimpiya')
    r['lesson_sha256']=fingerprint(d);r['approved_assessments_sha256']=fingerprint(d['assessments'])
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_all_twentyone_prerequisites_and420_xp_once(history):
    client,factory,_=history;documents=load_lessons()[:21]
    assert client.post(f"{PREFIX}/lessons/{documents[16]['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())}).status_code==403
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
        assert db.get(User,1).xp_total==420
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==21
        assert db.get(User,42).xp_total==137
    catalog=client.get(PREFIX+'/catalog').json()
    assert catalog['implemented_sections']==len(load_lessons()) and catalog['source_sections']==46
    assert all(r['state']=='completed' for r in catalog['lessons'][:21])
    assert all(r['state']!='completed' for r in catalog['lessons'][21:])
    assert catalog['grade_content_complete'] and not catalog['course_complete']
