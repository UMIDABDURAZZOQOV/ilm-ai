"""Two practical components, source-review arithmetic and finite oxide notation."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,readiness,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import chemistry,PREFIX,send,finish,answer_for


def test_batch09_original_order_both_practical_parts_and_exact_source_pointer():
    docs=load_lessons()[36:41]
    assert [l['topic_id'] for l in docs]==['ch7-practical05',*[f'ch7-paragraph{n}' for n in range(33,37)]]
    assert [l['sequence'] for l in docs]==list(range(37,42))
    assert sum(len(l['content']['cards']) for l in docs)==37
    assert sum(len(l['assessments']) for l in docs)==51
    assert {'soil','litmus','mass','label'}<=docs[0]['facts'].keys()
    assert set(docs[0]['source_activity_ids'])=={'ch7-6','ch7-7'}
    assert docs[1]['source_context_ids']==['ch7-paragraph07']
    ref=docs[1]['facts']['simple']['source_refs'][0]
    assert ref['paragraph']==7 and ref['printed_pages']==[26]
    assert docs[2]['source_context_ids']==['ch7-paragraph09']
    state=readiness(load_catalog(),load_lessons()[:41])[0]
    assert state['implemented_lessons']==41 and len(state['remaining_ids'])==33
    assert len(state['pending_source_review_ids'])>=13 and not state['course_ready']


@pytest.mark.parametrize('topic',['ch7-practical05','ch7-7','ch7-paragraph33','ch7-paragraph34'])
def test_new_source_review_holds_cannot_be_removed(topic):
    c=deepcopy(load_catalog());next(r for r in c['books'][0]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


def test_unverified_universal_colour_cannot_be_graded():
    l=deepcopy(load_lessons()[36]);r=read_json(DIRECTORY/'grade7_practical05_review.json')
    l['facts']['litmus']['verified_answers'].append('Pushti')
    with pytest.raises(ValueError,match='unresolved_soil_universal_colour'):validate_lesson(load_catalog(),l,r)


def test_unstated_hot_vapour_state_cannot_be_replaced_by_normal_volume():
    l=deepcopy(load_lessons()[36]);r=read_json(DIRECTORY/'grade7_practical05_review.json')
    q=next(q for q in l['assessments'] if q['fact_ids']==['test'])
    q['public']['unit']='ml';q['grading_spec'].update(expected='22400',verified_answer='22400',unit='ml')
    l['facts']['test']['verified_answers'].append('22400')
    with pytest.raises(ValueError,match='unresolved_water_vapour_state'):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('premise',['72.2% Fe','27,8% O'])
def test_imprecise_iron_percentages_cannot_become_a_fact_premise(premise):
    l=deepcopy(load_lessons()[38]);r=read_json(DIRECTORY/'grade7_paragraph34_review.json')
    l['facts']['examples']['claim']+=' '+premise
    with pytest.raises(ValueError,match='unresolved_iron_percentage'):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('n,qn,value,code',[
    (5,10,'11,1','correct'),(5,11,'16','correct'),(5,11,'15','incorrect'),
    (34,6,'Al₂O₃','correct'),(34,6,'AlO','incorrect'),
    (35,8,'N₂O','correct'),(35,8,'NO','incorrect'),
    (36,6,'2Cu2(OH)2CO3=4CuO+2CO2+2H2O','correct'),
    (36,8,'P2O5+H2O=2H3PO4','atom_imbalance'),
    (36,10,'H2O+Na2SO3=2NaOH+SO2','incorrect_species')])
def test_reviewed_original_numeric_and_parenthesized_equation_inputs(n,qn,value,code):
    topic='ch7-practical05' if n==5 else f'ch7-paragraph{n}'
    l=next(l for l in load_lessons() if l['topic_id']==topic)
    assert grade_answer(l['assessments'][qn-1]['grading_spec'],{'value':value})==code


def test_five_new_lessons_preserve36_completions_and_once_only_xp(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:36]:
            db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=720
    for lesson in docs[36:41]:
        path=f"{PREFIX}/lessons/{lesson['key']}/start";payload={'assessment_version':2,'request_id':str(uuid4())}
        response=client.post(path,json=payload);assert response.status_code==200,response.text
        a=response.json();assert a['lesson_key']==lesson['key']
        assert client.post(path,json=payload).json()['attempt_id']==a['attempt_id']
        for q in lesson['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        done=finish(client,a);assert done.status_code==200 and done.json()['xp_awarded']==20
        assert finish(client,a).json()==done.json()
    with factory() as db:
        assert db.get(User,1).xp_total==820
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==41
        old=db.get(User,42);assert (old.xp_total,old.streak_days)==(137,3)
