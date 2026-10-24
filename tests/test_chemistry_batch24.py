"""Nitrate/phosphate models preserve source ambiguity and prior immutable progress."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_five_later_lessons_keep_exact_source_order_and_original_worked_models():
    docs=load_lessons()[114:119]
    assert [l['topic_id'] for l in docs]==['ch8-paragraph39','ch8-practical03','ch8-paragraph40','ch8-paragraph41','ch8-practical04']
    assert [l['sequence'] for l in docs]==list(range(41,46))
    assert sum(len(l['content']['cards']) for l in docs)==68
    assert sum(len(l['assessments']) for l in docs)==86
    assert all(l['content']['examples'] for l in docs)
    assert all(r['topic_id']!='ch8-paragraph42' for l in docs for r in l['source_refs'])
    assert {(r['topic_id'],r['printed_pages'][0]) for r in docs[4]['facts']['acids']['source_refs']} >= {('ch8-practical04',184),('ch8-paragraph27',116),('ch8-paragraph41',179)}
    assert 'P4O10' in docs[3]['content']['cards'][0]['body']
    assert 'M2(HPO4)3' in docs[3]['content']['cards'][7]['body']
    assert '2AgNO3=2Ag+2NO2+O2' in docs[0]['content']['cards'][11]['body']
    assert any('H/O' in c['body'] and 'review' in c['body'] for c in docs[3]['content']['cards'])


@pytest.mark.parametrize('topic',['ch8-paragraph39','ch8-practical03','ch8-paragraph40','ch8-paragraph41','ch8-practical04'])
def test_next_five_source_scopes_cannot_be_removed(topic):
    c=deepcopy(load_catalog());next(r for r in c['books'][1]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


@pytest.mark.parametrize('file,fid,text,error',[
 ('practical03','composition','Ca(CN)2','unresolved_cyanamide_formula_identity'),
 ('practical03','product','NH3+NH3=NH4NO3','unresolved_ammonia_reagent_copy'),
 ('paragraph40','phosphine','2P+3H2=2PH3','unreviewed_direct_phosphine_formation'),
 ('paragraph40','table','Qizil fosfor zaharsiz','unqualified_phosphorus_safety_claim'),
 ('paragraph41','potassium','P2O5+6KOH=2K3PO4+H2O','unbalanced_phosphate_water_copy'),
 ('paragraph41','solubility','Barcha fosfatlar erimaydi','unqualified_phosphate_solubility')])
def test_known_wrong_copy_and_unqualified_source_claims_cannot_be_keyed(file,fid,text,error):
    l=deepcopy(read_json(DIRECTORY/f'grade8_{file}.json'));l['facts'][fid]['verified_answers'].append(text)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade8_{file}_review.json'))


def test_misplaced_hcl_citation_is_rejected_instead_of_accepting_a_page_number():
    l=deepcopy(read_json(DIRECTORY/'grade8_practical04.json'))
    r=next(r for r in l['source_refs'] if r['topic_id']=='ch8-paragraph27' and r['printed_pages']==[116])
    r.update(printed_pages=[98],pdf_pages=[98])
    with pytest.raises(ValueError,match='claim_outside_topic'):
        validate_lesson(load_catalog(),l,read_json(DIRECTORY/'grade8_practical04_review.json'))


@pytest.mark.parametrize('topic,qn,value,code',[
 ('ch8-paragraph39',7,'HNO₃','correct'),
 ('ch8-paragraph39',9,'NaNO3+H2SO4=NaHSO4+HNO3','correct'),
 ('ch8-paragraph39',10,'4NO2+2H2O+O2=4HNO3','correct'),
 ('ch8-paragraph39',11,'4HNO3=4NO2+O2+2H2O','correct'),
 ('ch8-paragraph39',12,'Fe(OH)3+3HNO3=Fe(NO3)3+3H2O','correct'),
 ('ch8-paragraph39',14,'4Fe+10HNO3=4Fe(NO3)2+NH4NO3+3H2O','correct'),
 ('ch8-paragraph39',15,'2Cu(NO3)2=2CuO+4NO2+O2','correct'),
 ('ch8-paragraph39',16,'2AgNO3=2Ag+2NO2+O2','correct'),
 ('ch8-paragraph39',19,'0,747','correct'),
 ('ch8-practical03',5,'2NH4Cl+Ca(OH)2=CaCl2+2H2O+2NH3','correct'),
 ('ch8-practical03',6,'4NH3+5O2=4NO+6H2O','incorrect_species'),
 ('ch8-practical03',9,'2NaNO3=2NaNO2+O2','correct'),
 ('ch8-practical03',12,'560','correct'),
 ('ch8-practical03',13,'8,82','correct'),
 ('ch8-practical03',14,'0.833','correct'),
 ('ch8-practical03',14,'0.81','incorrect'),
 ('ch8-practical03',15,'44.8','correct'),
 ('ch8-practical03',17,'44,8','correct'),
 ('ch8-paragraph40',6,'P4','correct'),
 ('ch8-paragraph40',9,'Ca3(PO4)2+5C+3SiO2=3CaSiO3+2P+5CO','correct'),
 ('ch8-paragraph40',10,'4P+5O2=2P2O5','correct'),
 ('ch8-paragraph40',12,'2P+3Ca=Ca3P2','correct'),
 ('ch8-paragraph40',14,'−3','correct'),
 ('ch8-paragraph41',7,'H₄P₂O₇','correct'),
 ('ch8-paragraph41',8,'Ca(H2PO4)2','correct'),
 ('ch8-paragraph41',9,'(NH4)2HPO4','correct'),
 ('ch8-paragraph41',11,'2H3PO4=H4P2O7+H2O','correct'),
 ('ch8-paragraph41',12,'Ca3(PO4)2+3H2SO4=3CaSO4+2H3PO4','correct'),
 ('ch8-paragraph41',13,'3NaOH+H3PO4=Na3PO4+3H2O','correct'),
 ('ch8-paragraph41',14,'Ca3(PO4)2+4HNO3=Ca(H2PO4)2+2Ca(NO3)2','correct'),
 ('ch8-paragraph41',15,'P+5HNO3=H3PO4+5NO2+H2O','correct'),
 ('ch8-paragraph41',18,'29,4','correct'),
 ('ch8-paragraph41',20,'58.8','correct'),
 ('ch8-paragraph41',21,'147','correct'),
 ('ch8-paragraph41',22,'0.1','correct'),
 ('ch8-practical04',7,'Cu(OH)2+2HNO3=Cu(NO3)2+2H2O','correct'),
 ('ch8-practical04',8,'(CuOH)2CO3+4HNO3=2Cu(NO3)2+CO2+3H2O','correct'),
 ('ch8-practical04',8,'(CuOH)2CO3+4HNO3=2Cu(NO3)2+CO2+H2O','atom_imbalance'),
 ('ch8-practical04',10,'5','correct')])
def test_existing_grader_accepts_only_the_given_products_and_explicit_number_model(topic,qn,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==topic)
    assert grade_answer(l['assessments'][qn-1]['grading_spec'],{'value':value})==code


def test_five_new_lessons_preserve114_and_once_only_xp(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:114]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=2280
    old=client.get(PREFIX+'/catalog?grade=7').json()
    assert client.get(PREFIX+'/catalog?grade=8').json()['lessons'][40]['state']=='available'
    for l in docs[114:119]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==2380
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==119
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert client.get(PREFIX+'/catalog?grade=7').json()==old
