"""Oxygen chapter close, safe practical and hydrogen opening, original source only."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,readiness,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import chemistry,PREFIX,send,finish,answer_for


def test_batch06_book_order_pages_and_original_review_anchor():
    docs=load_lessons()[21:26]
    assert [l['topic_id'] for l in docs]==['ch7-paragraph19','ch7-paragraph20','ch7-paragraph21','ch7-practical04','ch7-paragraph22']
    assert [l['sequence'] for l in docs]==list(range(22,27))
    assert sum(len(l['content']['cards']) for l in docs)==38
    assert sum(len(l['assessments']) for l in docs)==52
    assert docs[3]['source_activity_ids']==['ch7-3']
    assert docs[-1]['title']=='Vodorod'
    review=[r for r in docs[3]['source_refs'] if r['topic_id']=='ch7-3']
    assert len(review)==1 and review[0]['paragraph'] is None and review[0]['printed_pages']==[66]
    assert all(r['printed_pages']!=[69] for r in docs[-1]['source_refs'] if r['topic_id']==docs[-1]['topic_id'])
    state=readiness(load_catalog(),load_lessons()[:26])[0]
    assert state['implemented_lessons']==26 and len(state['remaining_ids'])==48
    assert len(state['pending_source_review_ids'])>=4 and not state['course_ready']


@pytest.mark.parametrize('topic',['ch7-paragraph19','ch7-paragraph20'])
def test_new_source_discrepancies_cannot_disappear(topic):
    catalog=deepcopy(load_catalog())
    row=next(r for r in catalog['books'][0]['records'] if r['id']==topic)
    row.pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(catalog)


@pytest.mark.parametrize('n,bad,error',[
    (19,'SiH4+2O2=SiO2+H2O','unresolved_silane_equation'),
    (19,'SiH₄+2O₂=SiO₂+2H₂O','unresolved_silane_equation'),
    (20,'6CO2+6H2O*=C6H12O6+6O2*','unresolved_photosynthesis_label')])
def test_held_reactions_are_not_reviewed_answers(n,bad,error):
    l=deepcopy(next(l for l in load_lessons() if l['topic_id']==f'ch7-paragraph{n}'))
    r=read_json(DIRECTORY/f'grade7_paragraph{n}_review.json')
    next(iter(l['facts'].values()))['verified_answers'].append(bad)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('n,qnumber,value',[
    (19,7,'4Mg+2O₂→4MgO'),
    (19,8,'2Al₂O₃=4Al+3O₂'),
    (20,9,'2,586'),
    (22,12,'5,88')])
def test_new_reviewed_input_variants_and_wrong_direction(n,qnumber,value):
    lesson=next(l for l in load_lessons() if l['topic_id']==f'ch7-paragraph{n}')
    q=lesson['assessments'][qnumber-1]
    result=grade_answer(q['grading_spec'],{'value':value})
    assert (result=='correct') is (value!='2Al₂O₃=4Al+3O₂')


def test_new_five_lessons_resume_replay_once_xp_and_preserve_prior_data(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:21]:
            db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=420
    first=None
    for lesson in docs[21:26]:
        request_id=str(uuid4());path=f"{PREFIX}/lessons/{lesson['key']}/start"
        payload={'assessment_version':2,'request_id':request_id}
        response=client.post(path,json=payload);assert response.status_code==200,response.text
        a=response.json();assert a['lesson_key']==lesson['key']
        assert client.post(path,json=payload).json()['attempt_id']==a['attempt_id']
        for q in lesson['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        done=finish(client,a);assert done.status_code==200 and done.json()['xp_awarded']==20
        assert finish(client,a).json()==done.json()
        if first is None:first=(a,lesson)
    with factory() as db:
        assert db.get(User,1).xp_total==520
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==26
        old=db.get(User,42);assert (old.xp_total,old.streak_days)==(137,3)
