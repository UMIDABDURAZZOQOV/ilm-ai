"""Source-reviewed solution amounts: solvent is not solution, ml is not l."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,readiness,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_batch08_order_source_boundaries_and_solvent_units():
    docs=load_lessons()[31:36]
    assert [l['topic_id'] for l in docs]==[f'ch7-paragraph{n}' for n in range(28,33)]
    assert [l['sequence'] for l in docs]==list(range(32,37))
    assert sum(len(l['content']['cards']) for l in docs)==35
    assert sum(len(l['assessments']) for l in docs)==42
    assert docs[-1]['source_context_ids']==['ch7-paragraph10']
    assert docs[-1]['facts']['mass']['source_refs'][0]['printed_pages']==[34]
    assert docs[-1]['facts']['mass']['source_refs'][0]['paragraph']==10
    assert not any(r['printed_pages']==[93] for r in docs[-1]['source_refs'])
    assert not any(q['response_kind']=='numeric_value' for q in docs[1]['assessments'])
    state=readiness(load_catalog(),load_lessons()[:36])[0]
    assert state['implemented_lessons']==36 and len(state['remaining_ids'])==38
    assert not state['course_ready']


@pytest.mark.parametrize('answer',['1350000','1.35e6','1400000000','1.4e9'])
def test_conflicting_ocean_volume_does_not_become_an_answer(answer):
    l=deepcopy(load_lessons()[31]);r=read_json(DIRECTORY/'grade7_paragraph28_review.json')
    l['facts']['distribution']['verified_answers'].append(answer)
    with pytest.raises(ValueError,match='unresolved_ocean_volume'):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('n,qn,value,code',[
    (28,7,'39','correct'),(28,7,'65','incorrect'),
    (30,7,'190','correct'),(30,8,'31,6','correct'),(30,8,'24','incorrect'),
    (32,5,'0,2','correct'),(32,5,'20','incorrect'),
    (32,6,'20','correct'),(32,6,'0.2','incorrect'),
    (32,9,'0,4','correct'),(32,9,'400','incorrect'),
    (32,11,'0.400','correct'),(32,11,'0.0004','incorrect'),
    (32,11,'0.4 mol/l','invalid_answer')])
def test_solvent_fraction_percent_and_millilitre_answers(n,qn,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch7-paragraph{n}')
    assert grade_answer(l['assessments'][qn-1]['grading_spec'],{'value':value})==code


def test_five_new_lessons_preserve31_completions_and_once_only_xp(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:31]:
            db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=620
    for lesson in docs[31:36]:
        path=f"{PREFIX}/lessons/{lesson['key']}/start";payload={'assessment_version':2,'request_id':str(uuid4())}
        response=client.post(path,json=payload);assert response.status_code==200,response.text
        a=response.json();assert a['lesson_key']==lesson['key']
        assert client.post(path,json=payload).json()['attempt_id']==a['attempt_id']
        for q in lesson['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        done=finish(client,a);assert done.status_code==200 and done.json()['xp_awarded']==20
        assert finish(client,a).json()==done.json()
    with factory() as db:
        assert db.get(User,1).xp_total==720
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==36
        old=db.get(User,42);assert (old.xp_total,old.streak_days)==(137,3)
