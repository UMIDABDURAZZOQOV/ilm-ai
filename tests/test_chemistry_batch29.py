"""Grade9 carbonate/silicon/industry/metals: verified models and prior progress."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_batch29_order_source_coverage_and_common_assessments():
    lessons=load_lessons()[143:148]
    assert [l['topic_id'] for l in lessons]==[f'ch9-paragraph{n:02}' for n in range(11,16)]
    assert [l['sequence'] for l in lessons]==list(range(11,16))
    assert sum(len(l['content']['cards']) for l in lessons)==80
    assert sum(len(l['assessments']) for l in lessons)==125
    assert all(l['content']['examples'] for l in lessons)
    assert set(q['response_kind'] for l in lessons for q in l['assessments'])=={'concept_selection','short_text','numeric_value','chemical_formula','chemical_equation'}
    assert all(not b['course_ready'] for b in load_catalog()['books'])
    assert ('ch8-practical01',[125]) in [(r['topic_id'],r['printed_pages']) for r in lessons[3]['facts']['permanganate']['source_refs']]
    assert ('ch8-paragraph20',[85]) in [(r['topic_id'],r['printed_pages']) for r in lessons[3]['facts']['permanganate']['source_refs']]
    assert all(l['topic_id'] not in l.get('source_context_ids',[]) for l in lessons)
    assert 'suvsiz tuz' in lessons[0]['facts']['solution']['claim']
    assert 'SiO2 + Mg → MgO + Si' in lessons[1]['assessments'][16]['public']['prompt']


@pytest.mark.parametrize('n',range(11,16))
def test_source_review_issue_cannot_disappear(n):
    c=deepcopy(load_catalog());next(r for r in c['books'][2]['records'] if r['id']==f'ch9-paragraph{n:02}').pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


@pytest.mark.parametrize('n,fid,answer,error',[
 (11,'stages','HCO3²−','unbalanced_bicarbonate_charge'),
 (11,'stages','HCO3²⁻','unbalanced_bicarbonate_charge'),
 (11,'solution','2.74','unresolved_carbonate_arithmetic'),
 (11,'yield','20.4','unresolved_carbonate_arithmetic'),
 (12,'mass','3.3','unreviewed_silicon_phase_density'),
 (12,'mass','2,33','unreviewed_silicon_phase_density'),
 (13,'silane','Barcha silan uchun n<8','unqualified_silane_chain_limit'),
 (14,'cement','Klinker uchun 450 C','unreviewed_cement_temperature'),
 (14,'fraction','0.953','unresolved_limestone_fraction'),
 (15,'ferrous','Zichlik chegarasi 500 kg/m3','unreviewed_metal_density_threshold')])
def test_unreviewed_copy_cannot_enter_facts_or_keys(n,fid,answer,error):
    l=deepcopy(read_json(DIRECTORY/f'grade9_paragraph{n:02}.json'));l['facts'][fid]['verified_answers'].append(answer)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade9_paragraph{n:02}_review.json'))


@pytest.mark.parametrize('n,qn,value,code',[
 (11,6,'H2CO3','correct'),(11,8,'Ca(HCO3)2','correct'),
 (11,9,'H2CO3+2NaOH=Na2CO3+2H2O','correct'),
 (11,11,'Ca(HCO3)2+2HCl=CaCl2+2CO2+2H2O','correct'),
 (11,11,'Ca(HCO3)2+2HCl=CaCl2+CO2+2H2O','atom_imbalance'),
 (11,16,'2Pb(NO3)2=2PbO+4NO2+O2','correct'),
 (11,18,'200','correct'),(11,19,'400','correct'),(11,20,'11,2','correct'),
 (11,21,'90.909','correct'),(11,23,'10','correct'),(11,26,'2,467','correct'),
 (11,26,'2.74','incorrect'),(11,27,'75','correct'),
 (12,10,'−4','correct'),(12,11,'28,086','correct'),
 (12,13,'7','correct'),(12,15,'SiH4','correct'),(12,15,'SIH4','incorrect'),
 (12,17,'SiO2+2Mg=2MgO+Si','correct'),
 (12,18,'SiO2+2C=2CO+Si','correct'),
 (13,11,'H2SiO3','correct'),(13,16,'SiCl4+2H2O=SiO2+4HCl','correct'),
 (13,20,'Mg2Si+4HCl=2MgCl2+SiH4','correct'),
 (13,22,'Si+2NaOH+H2O=Na2SiO3+2H2','correct'),
 (13,26,'SiO2+4HF=SiF4+2H2O','correct'),
 (13,30,'356,8','correct'),(13,30,'3.568e2','correct'),
 (14,11,'2KMnO4=K2MnO4+MnO2+O2','correct'),
 (14,14,'78,57','correct'),(14,15,'20.014','correct'),
 (14,16,'146,140','correct'),(14,16,'146','incorrect'),
 (14,17,'75','correct'),(14,18,'6.72','correct'),
 (14,19,'0,952','correct'),(14,19,'0.953','incorrect'),
 (14,20,'0.127','correct'),(14,21,'4.051','correct'),(14,22,'80','correct'),
 (15,8,'Au','correct'),(15,8,'AU','incorrect'),
 (15,11,'Ca3(PO4)2','correct'),(15,15,'Cr2O3+2Al=Al2O3+2Cr','correct'),
 (15,16,'Fe3O4+4CO=3Fe+4CO2','correct'),
 (15,18,'2HgO=2Hg+O2','correct'),(15,20,'CuSO4+Fe=FeSO4+Cu','correct'),
 (15,23,'1','correct'),(15,24,'2','correct'),(15,25,'3','correct')])
def test_existing_grading_contract(n,qn,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch9-paragraph{n:02}')
    assert grade_answer(l['assessments'][qn-1]['grading_spec'],{'value':value})==code


def test_batch29_preserves143_and_awards100_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:143]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=2860
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8)}
    g9=client.get(PREFIX+'/catalog?grade=9').json()['lessons']
    assert g9[10]['state']=='available' and all(l['state']=='locked' for l in g9[11:])
    for l in docs[143:148]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==2960
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==148
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert all(l['state']=='completed' for l in client.get(PREFIX+'/catalog?grade=9').json()['lessons'][:15])
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
