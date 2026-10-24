"""Equivalent-law/halogen practical/source-order tests;no new science engine."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_exact_book_order_includes_practical_before_paragraph29_and_all_six_categories():
    docs=load_lessons()[99:104]
    assert [l['topic_id'] for l in docs]==['ch8-paragraph26','ch8-paragraph27','ch8-paragraph28','ch8-practical01','ch8-paragraph29']
    assert [l['sequence'] for l in docs]==list(range(26,31))
    assert sum(len(l['content']['cards']) for l in docs)==59
    assert sum(len(l['assessments']) for l in docs)==72
    p=docs[3];assert p['facts']['tasks']['verified_answers']==['6','4']
    assert {(r['paragraph'],r['printed_pages'][0]) for r in p['facts']['fourth']['source_refs']}=={(1,124),(17,75),(23,97),(27,116)}
    assert {(r['paragraph'],r['printed_pages'][0]) for r in p['facts']['chloridecount']['source_refs']}=={(1,129),(1,126),(1,127),(26,112),(25,104)}
    assert [(r['paragraph'],r['printed_pages'][0]) for r in p['facts']['calcium']['source_refs']]==[(1,125)]
    assert not any(r['topic_id']=='ch8-paragraph30' for l in docs for r in l['source_refs'])
    assert all(r['pdf_pages']==r['printed_pages'] and r['regions']==['full'] for l in docs for r in l['source_refs'])


@pytest.mark.parametrize('topic',['ch8-paragraph26','ch8-paragraph27','ch8-paragraph28','ch8-practical01','ch8-paragraph29'])
def test_batch21_issue_is_required_even_after_scoped_teaching_is_authored(topic):
    c=deepcopy(load_catalog());next(r for r in c['books'][1]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


@pytest.mark.parametrize('file,fid,text,error',[
 ('paragraph26','calcium','9','unresolved_equivalent_target_mismatch'),
 ('paragraph27','chlorides','HgCl2 erimaydi','unreviewed_mercury_chloride_solubility'),
 ('paragraph28','industry','Uyqusizlik uchun brom','unverified_halogen_clinical_treatment'),
 ('practical01','calcium','Ca(OH)2+2HCl=2CaCl2+2H2O','unbalanced_calcium_hydroxide_copy'),
 ('practical01','acidmass','2.45*0.75=3.27','incorrect_solution_fraction_operation'),
 ('paragraph29','electrons','79','unreviewed_selenium_isotope_label')])
def test_copy_conflict_or_unverified_medical_is_not_a_ready_answer(file,fid,text,error):
    lesson=next(l for l in load_lessons() if l['topic_id']==f'ch8-{file}')
    l=deepcopy(lesson);review=read_json(DIRECTORY/f'grade8_{file}_review.json')
    l['facts'][fid]['verified_answers'].append(text)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,review)


@pytest.mark.parametrize('tag,qn,value,code',[
 ('p26',6,'CaO','correct'),('p26',8,'28','correct'),('p26',10,'18,67','correct'),('p26',14,'49','correct'),
 ('p27',7,'HClO3','correct'),('p27',8,'Fe+2HCl=FeCl2+H2','correct'),
 ('p27',8,'2Fe+6HCl=2FeCl3+3H2','incorrect_species'),
 ('p27',10,'Cu(OH)2+2HCl=CuCl2+2H2O','correct'),
 ('p27',11,'CaCO3+2HCl=CaCl2+CO2+H2O','correct'),
 ('p27',12,'2KMnO4+16HCl=2KCl+2MnCl2+5Cl2+8H2O','correct'),
 ('p27',15,'18.25','correct'),('p27',16,'58.5','correct'),
 ('p28',6,'XeF2','correct'),('p28',7,'SiO2+2F2=SiF4+O2','correct'),
 ('p28',8,'H2+I2=2HI','correct'),('p28',9,'AgNO3+NaBr=AgBr+NaNO3','correct'),
 ('practical01',5,'Zn+2HCl=ZnCl2+H2','correct'),
 ('practical01',6,'Zn(OH)2+2HCl=ZnCl2+2H2O','correct'),
 ('practical01',7,'Zn+Cl2=ZnCl2','correct'),
 ('practical01',8,'Ca(OH)2+2HCl=CaCl2+2H2O','correct'),
 ('practical01',8,'Ca(OH)2+2HCl=2CaCl2+2H2O','atom_imbalance'),
 ('practical01',13,'3.27','correct'),('practical01',14,'2.408e23','correct'),('practical01',15,'35','correct'),
 ('p29',7,'S8','correct'),('p29',8,'2Al+3S=Al2S3','correct'),
 ('p29',9,'S+3F2=SF6','correct'),('p29',10,'C+2S=CS2','correct'),
 ('p29',12,'+2','correct'),('p29',13,'−1','correct'),('p29',14,'0','correct')])
def test_scoped_existing_formula_equation_and_decimal_grading(tag,qn,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['key']==f'chemistry-8-{tag}-r1')
    assert grade_answer(l['assessments'][qn-1]['grading_spec'],{'value':value})==code


def test_fourth_model_cannot_lose_earlier_verified_product_evidence():
    l=deepcopy(next(l for l in load_lessons() if l['topic_id']=='ch8-practical01'))
    r=read_json(DIRECTORY/'grade8_practical01_review.json')
    l['source_context_ids'].remove('ch8-paragraph23')
    with pytest.raises(ValueError,match='source'):validate_lesson(load_catalog(),l,r)


def test_batch21_preserves99_completions_and_shared_once_only_xp(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:99]:
            db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=1980
    old=client.get(PREFIX+'/catalog?grade=7').json()
    g8=client.get(PREFIX+'/catalog?grade=8').json();assert g8['lessons'][25]['state']=='available'
    for l in docs[99:104]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            result=send(client,a,q,answer_for(q));assert result.status_code==200 and result.json()['is_correct'],result.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==2080
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==104
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert client.get(PREFIX+'/catalog?grade=7').json()==old
