"""Eight laboratory entries retain common learning and explicit source models."""
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import load_catalog,load_lessons,readiness
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_batch14_labs4_to11_have_distinct_ordered_source_keys_and_no_double_count():
    docs=load_lessons()[61:69]
    assert [l['topic_id'] for l in docs]==[f'ch7-laboratory{n:02}' for n in range(4,12)]
    assert [l['key'] for l in docs]==[f'chemistry-7-lab{n:02}-r1' for n in range(4,12)]
    assert [l['sequence'] for l in docs]==list(range(62,70))
    assert sum(len(l['content']['cards']) for l in docs)==28
    assert sum(len(l['assessments']) for l in docs)==51
    assert docs[0]['prerequisite_ids']==['ch7-laboratory03']
    for previous,l in zip(docs,docs[1:]):assert l['prerequisite_ids']==[previous['topic_id']]
    assert len({i for l in load_lessons()[:69] for i in l.get('source_activity_ids',[])})==9
    assert 'ch7-paragraph21' in docs[3]['source_context_ids']
    assert 'ch7-8' in docs[6]['source_context_ids']
    assert 'ch7-1' in docs[7]['source_context_ids']
    for l in [docs[2],docs[3]]:
        assert not any(q['public'].get('unit') in {'g/cm3','kJ','%'} for q in l['assessments'])
    state=readiness(load_catalog(),load_lessons()[:69])[0]
    assert state['implemented_lessons']==69 and len(state['remaining_ids'])==5 and not state['course_ready']


@pytest.mark.parametrize('offset,qn,value,code',[
    (0,5,'O₂','correct'),(0,6,'cu','invalid_answer'),
    (1,4,'o‘rin olish','correct'),(1,7,'Cu2(OH)2CO3=2CuO+CO2+H2O','correct'),
    (1,8,'2Fe+3CuCl2=2FeCl3+3Cu','incorrect_species'),
    (2,4,'Al₂O₃','correct'),(2,6,'2','correct'),
    (3,4,'Qattiq','correct'),(3,6,'H2','correct'),
    (4,4,'Zn+HCl=ZnCl2+H2','atom_imbalance'),(4,6,'0,25','correct'),
    (5,4,'H2+CuO=H2O+Cu','correct'),(5,6,'0,3','correct'),
    (6,6,'CaO+H2O=Ca(OH)2','correct'),
    (6,7,'P2O5+H2O=H3PO4','atom_imbalance'),
    (7,4,'Cu(OH)2+H2SO4=CuSO4+2H2O','correct'),
    (7,5,'Fe(OH)3+3HCl=FeCl3+3H2O','correct'),
    (7,5,'Fe(OH)3+2HCl=FeCl2+3H2O','incorrect_species')])
def test_sourced_laboratory_models_case_grouping_and_molar_ratios(offset,qn,value,code,reviewed_chemistry_documents):
    l=reviewed_chemistry_documents[61+offset]
    assert grade_answer(l['assessments'][qn-1]['grading_spec'],{'value':value})==code


def test_eight_labs_preserve61_completions_and_once_only_xp(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:61]:
            db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=1220
    for lesson in docs[61:69]:
        path=f"{PREFIX}/lessons/{lesson['key']}/start";payload={'assessment_version':2,'request_id':str(uuid4())}
        response=client.post(path,json=payload);assert response.status_code==200,response.text
        a=response.json();assert a['lesson_key']==lesson['key']
        assert client.post(path,json=payload).json()['attempt_id']==a['attempt_id']
        for q in lesson['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        done=finish(client,a);assert done.status_code==200 and done.json()['xp_awarded']==20
        assert finish(client,a).json()==done.json()
    with factory() as db:
        assert db.get(User,1).xp_total==1380
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==69
        old=db.get(User,42);assert (old.xp_total,old.streak_days)==(137,3)
