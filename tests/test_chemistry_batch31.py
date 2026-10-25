"""Grade9 sodium/soda/alkaline-earth/hardness/aluminium source adaptation."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_batch31_order_and_unchanged_response_contract():
    ls=load_lessons()[153:158]
    assert [l['topic_id'] for l in ls]==[f'ch9-paragraph{n:02}' for n in range(21,26)]
    assert [l['sequence'] for l in ls]==list(range(21,26))
    assert sum(len(l['content']['cards']) for l in ls)==80
    assert sum(len(l['assessments']) for l in ls)==133
    assert all(l['content']['examples'] for l in ls)
    assert all(not b['course_ready'] for b in load_catalog()['books'])
    assert ls[0]['assessments'][13]['grading_spec']['expected']=='4Li+O2=2Li2O'
    assert 'Li + O2 → Li2O' in ls[0]['assessments'][13]['public']['prompt']
    assert 'L i' not in str(ls)
    assert ('ch9-paragraph22',[108]) in [(r['topic_id'],r['printed_pages']) for r in ls[2]['facts']['hydridechain']['source_refs']]
    assert ('ch9-paragraph19',[91]) in [(r['topic_id'],r['printed_pages']) for r in ls[4]['facts']['cathode']['source_refs']]
    assert ('ch8-paragraph05',[30]) in [(r['topic_id'],r['printed_pages']) for r in ls[0]['facts']['sulfate']['source_refs']]


@pytest.mark.parametrize('n',range(21,26))
def test_batch31_issues_remain_visible(n):
    c=deepcopy(load_catalog());next(r for r in c['books'][2]['records'] if r['id']==f'ch9-paragraph{n:02}').pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


@pytest.mark.parametrize('n,fid,value,error',[
 (21,'hydroxides','NaON','unreviewed_sodium_hydroxide_label'),
 (21,'oxygen','KO2 peroksid','unreviewed_potassium_oxygen_category'),
 (22,'hydride','Har qanday gidrid KH','unqualified_hydride_identity'),
 (23,'minerals','Olivin MgSiO3','unreviewed_olivine_formula'),
 (23,'biological','Askalsiy davolaydi','unreviewed_alkaline_earth_clinical_claim'),
 (24,'proportion','165','unresolved_milk_arithmetic_copy'),
 (25,'cathode','Katod musbat','unreviewed_aluminium_electrode_sign'),
 (25,'anode','O2+2C=CO','unbalanced_aluminium_carbon_copy')])
def test_unreviewed_source_errors_cannot_enter_keys(n,fid,value,error):
    l=deepcopy(read_json(DIRECTORY/f'grade9_paragraph{n:02}.json'));l['facts'][fid]['verified_answers'].append(value)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade9_paragraph{n:02}_review.json'))


@pytest.mark.parametrize('n,qn,value,code',[
 (21,14,'4Li+O2=2Li2O','correct'),(21,14,'Li+O2=Li2O','atom_imbalance'),
 (21,15,'Na2O2+2Na=2Na2O','correct'),
 (21,23,'2NaCl+2H2O=2NaOH+Cl2+H2','correct'),
 (21,24,'2Na2O2+2CO2=2Na2CO3+O2','correct'),
 (21,25,'Na2O2+H2SO4=Na2SO4+H2O2','correct'),
 (21,28,'22,4','correct'),(21,29,'39','correct'),(21,30,'22.4','correct'),
 (21,31,'19.6','correct'),(21,32,'98','correct'),
 (22,12,'Na2S+CaCO3=Na2CO3+CaS','correct'),
 (22,17,'KH+H2O=KOH+H2','correct'),
 (22,18,'103,3','correct'),(22,20,'0.058','correct'),(22,21,'5.808','correct'),
 (22,22,'0.56','correct'),(22,23,'16.557','correct'),(22,24,'4.811','correct'),
 (22,25,'12.453','correct'),(22,26,'2,910','correct'),
 (23,7,'Mg3N2','correct'),(23,8,'Ca3P2','correct'),
 (23,16,'2Mg+CO2=2MgO+C','correct'),
 (23,23,'Ca+2C=CaC2','correct'),
 (23,30,'2Ca(OH)2+2Cl2=Ca(OCl)2+CaCl2+2H2O','correct'),
 (23,31,'CaH2+2H2O=Ca(OH)2+2H2','correct'),
 (23,36,'400','correct'),(23,37,'336,336','correct'),
 (24,15,'3MgSO4+2Na3PO4=Mg3(PO4)2+3Na2SO4','correct'),
 (24,18,'50','correct'),(24,19,'450','correct'),
 (24,20,'615,385','correct'),(24,20,'6.15385e2','correct'),(24,20,'165','incorrect'),
 (24,21,'2.8','correct'),(24,22,'1.084','correct'),
 (25,7,'Al','correct'),(25,8,'Al2O3','correct'),(25,9,'Al(OH)3','correct'),
 (25,10,'Na3AlF6','correct'),(25,13,'26,9815','correct'),(25,14,'3','correct'),
 (25,15,'26','correct'),(25,16,'34','correct')])
def test_existing_grading_on_original_models(n,qn,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch9-paragraph{n:02}')
    assert grade_answer(l['assessments'][qn-1]['grading_spec'],{'value':value})==code


def test_batch31_preserves153_and_awards100xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:153]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=3060
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8)}
    g9=client.get(PREFIX+'/catalog?grade=9').json()['lessons']
    assert g9[20]['state']=='available' and all(l['state']=='locked' for l in g9[21:])
    for l in docs[153:158]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==3160
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==158
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert all(l['state']=='completed' for l in client.get(PREFIX+'/catalog?grade=9').json()['lessons'][:25])
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
