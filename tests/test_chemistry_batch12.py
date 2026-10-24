"""Salt formula groups,book review contexts and reaction-scoped equivalents."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,readiness,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_batch12_order_review_identity_and_no_new_input_engine():
    docs=load_lessons()[51:56]
    assert [l['topic_id'] for l in docs]==[f'ch7-paragraph{n}' for n in range(46,51)]
    assert [l['sequence'] for l in docs]==list(range(52,57))
    assert sum(len(l['content']['cards']) for l in docs)==42
    assert sum(len(l['assessments']) for l in docs)==59
    assert docs[3]['source_activity_ids']==['ch7-8']
    assert docs[3]['source_context_ids']==['ch7-6']
    refs=docs[3]['facts']['review']['source_refs']
    assert {r['topic_id'] for r in refs}=={'ch7-6','ch7-8'}
    assert {r['printed_pages'][0] for r in refs}=={96,135}
    assert all(r['paragraph'] is None for r in refs)
    assert len({i for l in load_lessons()[:56] for i in l.get('source_activity_ids',[])})==8
    for l in docs:
        for q in l['assessments']:
            if q['response_kind'] in {'chemical_formula','chemical_equation'}:
                assert '·' not in q['grading_spec']['expected'] and '[' not in q['grading_spec']['expected']
    state=readiness(load_catalog(),load_lessons()[:56])[0]
    assert state['implemented_lessons']==56 and len(state['remaining_ids'])==18 and not state['course_ready']


@pytest.mark.parametrize('n',[46,48,49,50])
def test_new_salt_source_reviews_cannot_be_removed(n):
    c=deepcopy(load_catalog());next(r for r in c['books'][0]['records'] if r['id']==f'ch7-paragraph{n}').pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


@pytest.mark.parametrize('text',['KJ','NaJ','AgJ','J₂'])
def test_legacy_iodine_species_cannot_enter_salt_keys(text):
    l=deepcopy(load_lessons()[53]);r=read_json(DIRECTORY/'grade7_paragraph48_review.json')
    l['facts']['metal']['verified_answers'].append(text)
    with pytest.raises(ValueError,match='unresolved_legacy_iodine'):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('text',[
    'CuCl2+2NaOH=(OH)2+2NaCl',
    'CuCl₂ + 2NaOH = Cu(OH)₂ + 2NaCl'])
def test_missing_copper_is_not_silently_fixed_into_a_new_verified_premise(text):
    l=deepcopy(load_lessons()[53]);r=read_json(DIRECTORY/'grade7_paragraph48_review.json')
    l['facts']['basesalt']['claim']=text
    with pytest.raises(ValueError,match='unresolved_missing_copper'):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('text',['32.66','32,67','oltingugurt oksidi CO₂'])
def test_unresolved_decimal_and_sulfur_carbon_typo_are_not_premises(text):
    l=deepcopy(load_lessons()[55]);r=read_json(DIRECTORY/'grade7_paragraph50_review.json')
    l['facts']['acid']['verified_answers'].append(text)
    with pytest.raises(ValueError,match='unresolved_equivalent_gas_or_precision'):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('offset,qn,value,code',[
    (0,7,'CH3COONa','correct'),(0,9,'Mg(OH)Br','correct'),
    (1,6,'Al₂(SO₄)₃','correct'),(1,8,'Ca(H2PO4)2','correct'),
    (1,9,'(MgOH)3PO4','correct'),(1,9,'MgOH3PO4','incorrect'),
    (2,9,'Zn+2NaOH=Na2ZnO2+H2','correct'),
    (2,10,'MgCl2+2NaOH=Mg(OH)2+2NaCl','incorrect_species'),
    (2,12,'Ca3(PO4)2+H2SO4=Ca(H2PO4)2+CaSO4','atom_imbalance'),
    (2,14,'H2O+CO2+CaCO3=Ca(HCO3)2','correct'),
    (3,10,'0,025','correct'),(3,11,'0.05','correct'),
    (4,10,'67,5','correct'),(4,10,'135','incorrect')])
def test_reviewed_condensed_grouped_salts_partial_equations_and_ratio_answers(offset,qn,value,code,reviewed_chemistry_documents):
    l=reviewed_chemistry_documents[51+offset]
    assert grade_answer(l['assessments'][qn-1]['grading_spec'],{'value':value})==code


def test_five_new_lessons_preserve51_completions_and_once_only_xp(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:51]:
            db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=1020
    for lesson in docs[51:56]:
        path=f"{PREFIX}/lessons/{lesson['key']}/start";payload={'assessment_version':2,'request_id':str(uuid4())}
        response=client.post(path,json=payload);assert response.status_code==200,response.text
        a=response.json();assert a['lesson_key']==lesson['key']
        assert client.post(path,json=payload).json()['attempt_id']==a['attempt_id']
        for q in lesson['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        done=finish(client,a);assert done.status_code==200 and done.json()['xp_awarded']==20
        assert finish(client,a).json()==done.json()
    with factory() as db:
        assert db.get(User,1).xp_total==1120
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==56
        old=db.get(User,42);assert (old.xp_total,old.streak_days)==(137,3)
