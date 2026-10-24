"""Genetic models,digital inquiry and separate sourced laboratory entries."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,readiness,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_batch13_first_labs_have_distinct_keys_prerequisites_and_real_sources():
    docs=load_lessons()[56:61]
    assert [l['topic_id'] for l in docs]==['ch7-paragraph51','ch7-practical07',*[f'ch7-laboratory{n:02}' for n in range(1,4)]]
    assert [l['sequence'] for l in docs]==list(range(57,62))
    assert sum(len(l['content']['cards']) for l in docs)==24
    assert sum(len(l['assessments']) for l in docs)==39
    assert [l['key'] for l in docs[2:]]==[f'chemistry-7-lab{n:02}-r1' for n in range(1,4)]
    assert docs[2]['prerequisite_ids']==['ch7-practical07']
    assert docs[3]['prerequisite_ids']==['ch7-laboratory01']
    assert docs[1]['source_activity_ids']==['ch7-9']
    assert 'ch7-8' in docs[1]['source_context_ids']
    assert len({i for l in load_lessons()[:61] for i in l.get('source_activity_ids',[])})==9
    assert not any(q['response_kind']=='numeric_value' for q in docs[2]['assessments'])
    c=load_catalog();records={r['id']:r for r in c['books'][0]['records']}
    for l in docs[2:]:assert records[l['topic_id']]['digital_activity_policy']['physical_execution_required'] is False
    state=readiness(c,load_lessons()[:61])[0]
    assert state['implemented_lessons']==61 and len(state['remaining_ids'])==13 and not state['course_ready']


@pytest.mark.parametrize('topic',['ch7-practical07','ch7-9'])
def test_practical_clinical_and_review_condition_holds_remain_visible(topic):
    c=deepcopy(load_catalog());next(r for r in c['books'][0]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


def test_medical_recipe_cannot_enter_practical_verified_teaching():
    l=deepcopy(load_lessons()[57]);r=read_json(DIRECTORY/'grade7_practical07_review.json')
    l['facts']['mass']['claim']+=' Regidron'
    with pytest.raises(ValueError,match='held_clinical_recipe'):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('unit,value',[('l','4.48'),('ml','8960')])
def test_unspecified_review_co2_product_does_not_get_a_unique_gas_key(unit,value):
    l=deepcopy(load_lessons()[57]);r=read_json(DIRECTORY/'grade7_practical07_review.json')
    q=l['assessments'][-1];q['public']['unit']=unit;q['grading_spec'].update(expected=value,verified_answer=value,unit=unit)
    l['facts']['conservation']['verified_answers'].append(value)
    with pytest.raises(ValueError,match='unresolved_review_co2_product'):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('offset,qn,value,code',[
    (0,7,'4P+5O2=2P2O5','correct'),
    (0,9,'FeCl2+KOH=Fe(OH)2+KCl','atom_imbalance'),
    (1,6,'CuCl2+2NaOH=Cu(OH)2+2NaCl','correct'),
    (1,9,'80','correct'),(1,10,'12,5','correct'),
    (1,11,'15,6','correct'),(1,11,'15.56','incorrect'),
    (1,12,'12,8','correct'),
    (2,4,'eruvchanlik','correct'),(3,5,'Hid','correct'),
    (4,5,'CuO','correct'),(4,5,'Cu2O','incorrect')])
def test_source_models_rounding_bounded_lab_text_and_notation(offset,qn,value,code,reviewed_chemistry_documents):
    l=reviewed_chemistry_documents[56+offset]
    assert grade_answer(l['assessments'][qn-1]['grading_spec'],{'value':value})==code


def test_five_new_lessons_preserve56_completions_and_once_only_xp(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:56]:
            db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=1120
    for lesson in docs[56:61]:
        path=f"{PREFIX}/lessons/{lesson['key']}/start";payload={'assessment_version':2,'request_id':str(uuid4())}
        response=client.post(path,json=payload);assert response.status_code==200,response.text
        a=response.json();assert a['lesson_key']==lesson['key']
        assert client.post(path,json=payload).json()['attempt_id']==a['attempt_id']
        for q in lesson['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        done=finish(client,a);assert done.status_code==200 and done.json()['xp_awarded']==20
        assert finish(client,a).json()==done.json()
    with factory() as db:
        assert db.get(User,1).xp_total==1220
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==61
        old=db.get(User,42);assert (old.xp_total,old.streak_days)==(137,3)
