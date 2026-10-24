"""Exact nonmetal/halogen/gas sources;state assumptions and common learning flow."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_five_exact_nonmetal_halogen_gas_lessons_and_real_context():
    docs=load_lessons()[94:99]
    assert [l['topic_id'] for l in docs]==[f'ch8-paragraph{n:02}' for n in range(21,26)]
    assert [l['sequence'] for l in docs]==list(range(21,26))
    assert sum(len(l['content']['cards']) for l in docs)==54
    assert sum(len(l['assessments']) for l in docs)==78
    assert docs[0]['source_refs'][0]['topic_id']=='ch8-paragraph21'
    assert not any(r['topic_id']=='ch8-chapter04' for l in docs for r in l['source_refs'])
    assert [r['printed_pages'][0] for r in docs[0]['facts']['trend']['source_refs']]==[89,90,92]
    salt=docs[2]['facts']['salt']['source_refs']
    assert [(r['paragraph'],r['printed_pages'][0]) for r in salt]==[(16,73),(17,74),(23,96)]
    assert all(r['pdf_pages']==r['printed_pages'] and r['regions']==['full'] for l in docs for r in l['source_refs'])
    assert '4°C' in docs[4]['facts']['liquid']['claim']
    assert 'n.sh.' in docs[4]['facts']['volume']['claim']
    assert 'Hajm' in docs[4]['facts']['mixture']['verified_answers']


@pytest.mark.parametrize('n',range(21,26))
def test_batch20_source_issues_cannot_disappear(n):
    c=deepcopy(load_catalog());next(r for r in c['books'][1]['records'] if r['id']==f'ch8-paragraph{n:02}').pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


@pytest.mark.parametrize('n,fid,text,error',[
 (21,'table','Barcha inert gazlar RO4 hosil qiladi','unreviewed_universal_noble_oxide'),
 (22,'names','1866','unresolved_halogen_history_date'),
 (23,'physical','0.63','unresolved_chlorine_solubility_state'),
 (24,'acid','500','unresolved_hcl_solubility_conditions'),
 (25,'volume','112','unresolved_water_vapour_state')])
def test_unresolved_universal_or_state_or_precision_key_is_held(n,fid,text,error):
    l=deepcopy(load_lessons()[73+n]);r=read_json(DIRECTORY/f'grade8_paragraph{n:02}_review.json')
    l['facts'][fid]['verified_answers'].append(text)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('n,qn,value,code',[
 (21,7,'XeF4','correct'),(21,8,'2Na+H2=2NaH','correct'),(21,12,'−1','correct'),
 (22,7,'KI','correct'),(22,8,'2KBr+Cl2=2KCl+Br2','correct'),
 (22,9,'2KI+Br2=2KBr+I2','correct'),(22,10,'2H2O+2F2=4HF+O2','correct'),
 (23,7,'2Fe+3Cl2=2FeCl3','correct'),(23,8,'Cl2+H2O=HCl+HClO','correct'),
 (23,9,'3Cl2+6KOH=KClO3+5KCl+3H2O','correct'),
 (23,9,'Cl2+2KOH=KClO+KCl+H2O','incorrect_species'),
 (23,10,'Cl2+2KOH=KClO+KCl+H2O','correct'),
 (24,6,'NaCl+H2SO4=NaHSO4+HCl','correct'),
 (24,7,'H2+Cl2=2HCl','correct'),(24,8,'2NaCl+2H2O=2NaOH+Cl2+H2','correct'),
 (24,9,'4HCl+MnO2=MnCl2+Cl2+2H2O','correct'),
 (24,11,'1,259','correct'),(24,12,'0.85','correct'),
 (25,13,'3.344e25','correct'),(25,14,'64','correct'),
 (25,16,'37.6','correct'),(25,17,'18.8','correct'),
 (25,20,'1.505e23','correct'),(25,21,'4.515e23','correct'),
 (25,23,'0.044','correct'),(25,24,'22400','correct'),
 (25,24,'22.4 L','invalid_answer')])
def test_shared_equation_and_scientific_decimal_inputs(n,qn,value,code,reviewed_chemistry_documents):
    q=reviewed_chemistry_documents[73+n]['assessments'][qn-1]
    assert grade_answer(q['grading_spec'],{'value':value})==code


def test_nonmetals_follow_completed94_without_touching_biology_or_prior_progress(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:94]:
            db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=1880
    old=client.get(PREFIX+'/catalog?grade=7').json()
    g8=client.get(PREFIX+'/catalog?grade=8').json()
    assert len(g8['lessons'])>=25 and g8['lessons'][20]['state']=='available'
    for l in docs[94:99]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            result=send(client,a,q,answer_for(q));assert result.status_code==200 and result.json()['is_correct'],result.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==1980
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==99
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert client.get(PREFIX+'/catalog?grade=7').json()==old
