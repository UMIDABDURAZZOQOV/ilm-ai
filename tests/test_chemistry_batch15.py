"""All mapped grade7 entries exist;scientific holds still gate readiness."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,readiness,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_all74_grade7_teaching_entries_are_ordered_but_not_scientifically_ready():
    docs=load_lessons()[:74];tail=docs[69:74]
    assert [l['topic_id'] for l in tail]==[f'ch7-laboratory{n:02}' for n in range(12,17)]
    assert [l['sequence'] for l in docs]==list(range(1,75))
    assert sum(len(l['content']['cards']) for l in tail)==17
    assert sum(len(l['assessments']) for l in tail)==33
    assert all(l['content']['xp_reward']==20 for l in docs)
    c=load_catalog();records=[r for r in c['books'][0]['records'] if r['kind'] in {'paragraph','practical','laboratory'}]
    assert [l['topic_id'] for l in docs]==[r['id'] for r in records]
    assert len({i for l in docs for i in l.get('source_activity_ids',[])})==9
    state=readiness(c,docs)[0]
    assert state['implemented_lessons']==74 and state['remaining_ids']==[]
    assert state['pending_source_review_ids'] and not state['source_review_complete'] and not state['course_ready']


def test_lab15_acid_condition_scope_cannot_be_removed():
    c=deepcopy(load_catalog());next(r for r in c['books'][0]['records'] if r['id']=='ch7-laboratory15').pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


@pytest.mark.parametrize('text',['Cu+H2SO4=CuSO4+H2','H₂SO₄ + Cu = CuSO₄ + H₂'])
def test_unqualified_copper_sulfuric_equation_is_not_a_lab_premise(text):
    l=deepcopy(load_lessons()[72]);r=read_json(DIRECTORY/'grade7_laboratory15_review.json')
    l['facts']['task']['claim']=text
    with pytest.raises(ValueError,match='unresolved_lab_copper_acid_conditions'):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('offset,qn,value,code',[
    (0,4,'Cu(OH)2=CuO+H2O','correct'),(0,5,'H₂O','correct'),
    (1,4,'HCl+NaOH=H2O+NaCl','correct'),(1,6,'0,04','correct'),
    (2,5,'HCl','correct'),(2,6,'H2SO4','correct'),
    (3,5,'Zn+H2SO4=ZnSO4+H2','correct'),
    (3,6,'Fe+2HCl=FeCl2+H2','correct'),
    (4,4,'Fe2O3+6HCl=2FeCl3+3H2O','correct'),
    (4,5,'Fe2O3+H2SO4=Fe2(SO4)3+H2O','atom_imbalance'),
    (4,5,'Fe2O3+3H2SO4=Fe2(SO4)3+3H2O','correct'),
    (4,8,'Fe₂(SO₄)₃','correct'),(4,9,'6','correct')])
def test_final_laboratory_formula_equation_and_stated_ratio_models(offset,qn,value,code,reviewed_chemistry_documents):
    l=reviewed_chemistry_documents[69+offset]
    assert grade_answer(l['assessments'][qn-1]['grading_spec'],{'value':value})==code


def test_final_five_labs_preserve69_completions_and_once_only_xp(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:69]:
            db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=1380
    for lesson in docs[69:74]:
        path=f"{PREFIX}/lessons/{lesson['key']}/start";payload={'assessment_version':2,'request_id':str(uuid4())}
        response=client.post(path,json=payload);assert response.status_code==200,response.text
        a=response.json();assert a['lesson_key']==lesson['key']
        assert client.post(path,json=payload).json()['attempt_id']==a['attempt_id']
        for q in lesson['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        done=finish(client,a);assert done.status_code==200 and done.json()['xp_awarded']==20
        assert finish(client,a).json()==done.json()
    with factory() as db:
        assert db.get(User,1).xp_total==1480
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==74
        old=db.get(User,42);assert (old.xp_total,old.streak_days)==(137,3)
