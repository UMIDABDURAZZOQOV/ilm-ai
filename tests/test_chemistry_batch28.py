"""Grade9 ion exchange/carbon with exact reviewed earlier-book evidence."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_next_five_keep_source_order_and_existing_assessment_kinds():
    new=load_lessons()[138:143]
    assert [l['topic_id'] for l in new]==[f'ch9-paragraph{n:02}' for n in range(6,11)]
    assert [l['sequence'] for l in new]==list(range(6,11))
    assert sum(len(l['content']['cards']) for l in new)==72
    assert sum(len(l['assessments']) for l in new)==124
    assert all(l['content']['examples'] for l in new)
    assert set(q['response_kind'] for l in new for q in l['assessments'])=={'concept_selection','short_text','numeric_value','chemical_formula','chemical_equation'}
    assert all(not b['course_ready'] for b in load_catalog()['books'])
    assert ('ch8-paragraph25',[110]) in [(r['topic_id'],r['printed_pages']) for r in new[2]['facts']['density']['source_refs']]
    assert ('ch8-paragraph05',[27]) in [(r['topic_id'],r['printed_pages']) for r in new[2]['facts']['density']['source_refs']]
    assert ('ch8-practical01',[127]) in [(r['topic_id'],r['printed_pages']) for r in new[3]['facts']['copper']['source_refs']]
    assert ('ch9-paragraph10',[52]) in [(r['topic_id'],r['printed_pages']) for r in new[4]['facts']['review']['source_refs']]
    assert all('grade8' not in l['key'] for l in new)


@pytest.mark.parametrize('n',range(6,11))
def test_source_issues_remain_visible(n):
    c=deepcopy(load_catalog());next(r for r in c['books'][2]['records'] if r['id']==f'ch9-paragraph{n:02}').pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


@pytest.mark.parametrize('n,fid,answer,error',[
 (6,'gas','H2S suvda erimaydi','unqualified_hydrogen_sulfide_insolubility'),
 (7,'sulfide','Barcha kuchsiz asos va kuchsiz kislota tuzlari to‘liq gidrolizlanadi','unqualified_complete_weak_salt'),
 (7,'ferriccarbonate','FeCl3+K2CO3=Fe(OH)2+CO2','unreviewed_ferric_carbonate'),
 (8,'configuration','1s2 2s2 2p6','unreviewed_carbon_configuration'),
 (8,'cage','Fulleren 80 dan ortiq atom','unreviewed_fullerene_atom_count'),
 (9,'surface','Qonni tozalash','unreviewed_adsorption_clinical_claim'),
 (10,'exception','CO2 barcha yong‘in uchun xavfsiz','unqualified_carbon_dioxide_fire_safety')])
def test_reviewed_source_errors_cannot_become_scientific_keys(n,fid,answer,error):
    l=deepcopy(read_json(DIRECTORY/f'grade9_paragraph{n:02}.json'));l['facts'][fid]['verified_answers'].append(answer)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade9_paragraph{n:02}_review.json'))


@pytest.mark.parametrize('n,qn,value,code',[
 (6,8,'BaSO4','correct'),(6,12,'HCl+KOH=KCl+H2O','correct'),
 (6,14,'Na2S+2HCl=2NaCl+H2S','correct'),
 (6,15,'NH4Cl+NaOH=NaCl+H2O+NH3','correct'),
 (6,16,'Ba(NO3)2+K2SO4=BaSO4+2KNO3','correct'),
 (6,17,'Pb(NO3)2+2NaCl=PbCl2+2NaNO3','correct'),
 (7,11,'Al2S3+6H2O=2Al(OH)3+3H2S','correct'),
 (7,13,'Fe(OH)Cl2+H2O=Fe(OH)2Cl+HCl','correct'),
 (7,16,'2FeCl3+3K2CO3+3H2O=2Fe(OH)3+3CO2+6KCl','correct'),
 (7,16,'2FeCl3+3K2CO3+H2O=2Fe(OH)3+3CO2+6KCl','atom_imbalance'),
 (7,21,'5,825','correct'),(7,25,'1.12','correct'),
 (8,8,'C','correct'),(8,12,'SiH4','correct'),(8,12,'SIH4','incorrect'),
 (8,15,'2','correct'),(8,16,'−4','correct'),(8,18,'32','correct'),
 (9,12,'6CO2+6H2O=C6H12O6+6O2','correct'),
 (9,17,'2Al2O3+9C=Al4C3+6CO','correct'),
 (9,19,'CaC2+2H2O=Ca(OH)2+C2H2','correct'),
 (9,22,'SiO2+3C=SiC+2CO','correct'),
 (9,26,'171666,667','correct'),(9,27,'0.25','correct'),
 (9,28,'3','correct'),(9,29,'16','correct'),
 (10,7,'CO','correct'),(10,7,'Co','incorrect'),(10,8,'CO2','correct'),
 (10,9,'COCl2','correct'),(10,10,'NaHCO3','correct'),
 (10,13,'SnO2+2CO=Sn+2CO2','correct'),
 (10,20,'2Mg+CO2=2MgO+C','correct'),
 (10,23,'Na2CO3+H2O+CO2=2NaHCO3','correct'),
 (10,25,'71,5','correct'),(10,25,'71.5','correct'),
 (10,25,'143','incorrect'),(10,26,'1.52','correct'),(10,27,'14','correct')])
def test_existing_formula_equation_numeric_contract(n,qn,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch9-paragraph{n:02}')
    assert grade_answer(l['assessments'][qn-1]['grading_spec'],{'value':value})==code


def test_new_five_preserve138_and_add100_xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:138]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=2760
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8)}
    g9=client.get(PREFIX+'/catalog?grade=9').json()['lessons']
    assert g9[5]['state']=='available' and all(l['state']=='locked' for l in g9[6:])
    for l in docs[138:143]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==2860
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==143
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert all(l['state']=='completed' for l in client.get(PREFIX+'/catalog?grade=9').json()['lessons'][:10])
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
