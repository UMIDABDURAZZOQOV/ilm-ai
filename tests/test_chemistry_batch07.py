"""Acids, hydrogen material equations, original chapter problems and water."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,readiness,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import chemistry,PREFIX,send,finish,answer_for


def test_batch07_original_order_review_anchors_and_hydrate_recognition():
    docs=load_lessons()[26:31]
    assert [l['topic_id'] for l in docs]==[f'ch7-paragraph{n}' for n in range(23,28)]
    assert [l['sequence'] for l in docs]==list(range(27,32))
    assert sum(len(l['content']['cards']) for l in docs)==40
    assert sum(len(l['assessments']) for l in docs)==55
    assert set(docs[3]['source_activity_ids'])=={'ch7-4','ch7-5'}
    assert {'ch7-paragraph17','ch7-paragraph24','ch7-paragraph25'}<=set(docs[3]['source_context_ids'])
    refs=[r for r in docs[3]['source_refs'] if r['topic_id'] in docs[3]['source_activity_ids']]
    assert all(r['paragraph'] is None for r in refs)
    assert {p for r in refs for p in r['printed_pages']}=={75,76,79}
    assert not any('·' in q['grading_spec']['expected'] for q in docs[-1]['assessments'] if q['response_kind']=='chemical_formula')
    state=readiness(load_catalog(),load_lessons()[:31])[0]
    assert state['implemented_lessons']==31 and len(state['remaining_ids'])==43
    assert len(state['pending_source_review_ids'])>=9 and not state['course_ready']


@pytest.mark.parametrize('topic',['ch7-paragraph24','ch7-paragraph26','ch7-4','ch7-paragraph27','ch7-paragraph28'])
def test_contextual_source_review_cannot_be_deleted(topic):
    c=deepcopy(load_catalog());next(r for r in c['books'][0]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


def test_source_heat_signs_are_not_silently_gradeable():
    l=deepcopy(load_lessons()[27]);r=read_json(DIRECTORY/'grade7_paragraph24_review.json')
    q=next(q for q in l['assessments'] if q['response_kind']=='numeric_value')
    q['public']['unit']='kJ'
    with pytest.raises(ValueError,match='unresolved_heat_sign'):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('bad',['S8','S₈','0.89','0,89'])
def test_source_review_phase_assumptions_are_not_verified_answers(bad):
    l=deepcopy(load_lessons()[29]);r=read_json(DIRECTORY/'grade7_paragraph26_review.json')
    l['facts']['density']['verified_answers'].append(bad)
    with pytest.raises(ValueError,match='unresolved_gas_phase'):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('n,qn,value,expected',[
    (23,5,'INDIKATOR','correct'),(23,8,'H₂SO₄','correct'),
    (24,7,'2CH4+2H2O=2CO+6H2','correct'),
    (25,7,'2NH3=N2+3H2','incorrect_species'),
    (26,7,'1,43','correct'),(26,12,'0,672','correct'),
    (27,6,'Ca(OH)₂','correct'),(27,9,'3Fe+4H2O=Fe3O4+4H2','correct')])
def test_new_finite_input_variants(n,qn,value,expected):
    l=next(l for l in load_lessons() if l['topic_id']==f'ch7-paragraph{n}')
    q=l['assessments'][qn-1]
    assert grade_answer(q['grading_spec'],{'value':value})==expected


def test_five_new_lessons_preserve26_completions_and_once_only_xp(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:26]:
            db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=520
    for lesson in docs[26:31]:
        path=f"{PREFIX}/lessons/{lesson['key']}/start";request_id=str(uuid4())
        payload={'assessment_version':2,'request_id':request_id}
        response=client.post(path,json=payload);assert response.status_code==200,response.text
        a=response.json();assert a['lesson_key']==lesson['key']
        assert client.post(path,json=payload).json()['attempt_id']==a['attempt_id']
        for q in lesson['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        done=finish(client,a);assert done.status_code==200 and done.json()['xp_awarded']==20
        assert finish(client,a).json()==done.json()
    with factory() as db:
        assert db.get(User,1).xp_total==620
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==31
        old=db.get(User,42);assert (old.xp_total,old.streak_days)==(137,3)
