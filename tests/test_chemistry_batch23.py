"""Sulfur practical/nitrogen use exact prior evidence and scoped source models."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_five_lessons_preserve_source_order_and_explicit_earlier_context():
    docs=load_lessons()[109:114]
    assert [l['topic_id'] for l in docs]==['ch8-paragraph35','ch8-practical02','ch8-paragraph36','ch8-paragraph37','ch8-paragraph38']
    assert [l['sequence'] for l in docs]==list(range(36,41))
    assert sum(len(l['content']['cards']) for l in docs)==60
    assert sum(len(l['assessments']) for l in docs)==86
    assert all(l['content']['examples'] for l in docs)
    assert all(r['pdf_pages']==r['printed_pages'] and r['regions']==['full'] for l in docs for r in l['source_refs'])
    assert 'ch8-paragraph33' in docs[1]['source_context_ids']
    assert {r['topic_id'] for r in docs[1]['facts']['earlierair']['source_refs']} >= {'ch8-paragraph30','ch8-paragraph33','ch8-practical02'}
    assert ('ch8-paragraph11',[50]) in [(r['topic_id'],r['printed_pages']) for r in docs[2]['facts']['configuration']['source_refs']]
    assert all(r['topic_id']!='ch8-paragraph39' for l in docs for r in l['source_refs'])


def test_nitrogen_table_retains_actual_chapter_identity_and_scoped_image_evidence():
    l=next(l for l in load_lessons() if l['topic_id']=='ch8-paragraph36')
    refs=[r for r in l['source_refs'] if r['topic_id']=='ch8-chapter06' and r['printed_pages']==[157]]
    assert refs and all(r['paragraph'] is None and r['page_scope']=='before_first_teaching_heading' for r in refs)
    review=read_json(DIRECTORY/'grade8_paragraph36_review.json')
    assert all(e['page_scope']=='before_first_teaching_heading' for e in review['source_pages'] if e['topic_id']=='ch8-chapter06' and e['printed_page']==157)
    bad=deepcopy(review)
    for e in bad['source_pages']:
        if e['topic_id']=='ch8-chapter06' and e['printed_page']==157:e.pop('page_scope')
    with pytest.raises(ValueError):validate_lesson(load_catalog(),l,bad)


@pytest.mark.parametrize('topic',['ch8-paragraph35','ch8-practical02','ch8-chapter06','ch8-paragraph36','ch8-paragraph37','ch8-paragraph38'])
def test_all_six_source_reviews_remain_visible(topic):
    c=deepcopy(load_catalog());next(r for r in c['books'][1]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


@pytest.mark.parametrize('topic,fid,text,error',[
 ('ch8-paragraph35','contact','99.2','unqualified_production_yield'),
 ('ch8-paragraph35','contact','73','unqualified_production_yield'),
 ('ch8-practical02','heat','3O2=2O3+192.46','unresolved_ozone_formation_heat'),
 ('ch8-paragraph36','table','5p10','unresolved_bismuth_p_capacity_copy'),
 ('ch8-paragraph36','nitrides','Barcha metallar azot bilan kirishmaydi','unqualified_nitrogen_metal_nonreaction'),
 ('ch8-paragraph37','equilibrium','Harorat pasaysa unum kamayadi','unresolved_ammonia_yield_rate_confusion'),
 ('ch8-paragraph38','oxidation','N2O5 valentligi5','unresolved_nitrogen_pentoxide_valence')])
def test_held_source_claims_never_become_verified_answers(topic,fid,text,error):
    l=deepcopy(next(l for l in load_lessons() if l['topic_id']==topic))
    file='grade8_practical02_review.json' if topic=='ch8-practical02' else f'grade8_paragraph{l["source_refs"][0]["paragraph"]}_review.json'
    l['facts'][fid]['verified_answers'].append(text)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,read_json(DIRECTORY/file))


def test_conflicting_solution_fraction_is_distinct_from_clear_pure_acid_mass():
    l=deepcopy(next(l for l in load_lessons() if l['topic_id']=='ch8-practical02'))
    assert l['facts']['puremass']['verified_answers'][1]=='4.9'
    l['facts']['puremass']['claim']+=' Eritmaning massa ulushi.'
    l['facts']['puremass']['verified_answers'].append('2.45')
    with pytest.raises(ValueError,match='unresolved_solution_total_mass'):
        validate_lesson(load_catalog(),l,read_json(DIRECTORY/'grade8_practical02_review.json'))


@pytest.mark.parametrize('topic,qn,value,code',[
 ('ch8-paragraph35',8,'Cu2S+2O2=2CuO+SO2','correct'),
 ('ch8-paragraph35',8,'CuS+O2=CuO+SO2','incorrect_species'),
 ('ch8-paragraph35',9,'4SO2+2O2=4SO3','correct'),
 ('ch8-paragraph35',9,'2SO2+O2⇌2SO3','invalid_answer'),
 ('ch8-paragraph35',14,'2','correct'),
 ('ch8-practical02',5,'Al2(SO4)3+3BaCl2=2AlCl3+3BaSO4','correct'),
 ('ch8-practical02',9,'27','correct'),
 ('ch8-practical02',10,'1','correct'),
 ('ch8-practical02',13,'4,9','correct'),
 ('ch8-practical02',14,'53.33','correct'),
 ('ch8-practical02',15,'266,67','correct'),
 ('ch8-practical02',16,'36','correct'),
 ('ch8-practical02',18,'122.5','correct'),
 ('ch8-paragraph36',7,'N₂','correct'),
 ('ch8-paragraph36',8,'Mg3N2','correct'),
 ('ch8-paragraph36',9,'2NH3+3CuO=3H2O+N2+3Cu','correct'),
 ('ch8-paragraph36',11,'N2+3H2=2NH3','correct'),
 ('ch8-paragraph36',12,'6Li+N2=2Li3N','correct'),
 ('ch8-paragraph36',17,'1,25','correct'),
 ('ch8-paragraph36',18,'14','correct'),
 ('ch8-paragraph37',8,'NH4HSO4','correct'),
 ('ch8-paragraph37',8,'(NH4)2SO4','incorrect'),
 ('ch8-paragraph37',10,'2NH4Cl+Ca(OH)2=CaCl2+2H2O+2NH3','correct'),
 ('ch8-paragraph37',11,'2NH3+H2SO4=(NH4)2SO4','correct'),
 ('ch8-paragraph37',14,'4NH3+3O2=2N2+6H2O','incorrect_species'),
 ('ch8-paragraph37',15,'(NH4)2CO3=2NH3+H2O+CO2','correct'),
 ('ch8-paragraph37',16,'(NH4)2SO4+2NaOH=Na2SO4+2NH3+2H2O','correct'),
 ('ch8-paragraph37',18,'−3','correct'),
 ('ch8-paragraph37',20,'7','correct'),
 ('ch8-paragraph37',21,'5,6','correct'),
 ('ch8-paragraph38',6,'N2O3','correct'),
 ('ch8-paragraph38',8,'3Cu+8HNO3=3Cu(NO3)2+2NO+4H2O','correct'),
 ('ch8-paragraph38',10,'Cu+4HNO3=Cu(NO3)2+2NO2+2H2O','correct'),
 ('ch8-paragraph38',11,'2NO2+H2O=HNO3+HNO2','correct'),
 ('ch8-paragraph38',13,'5','correct'),
 ('ch8-paragraph38',15,'1,59','correct')])
def test_existing_bounded_grader_preserves_supplied_conditions(topic,qn,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==topic)
    assert grade_answer(l['assessments'][qn-1]['grading_spec'],{'value':value})==code


def test_new_five_lessons_preserve109_and_grant_only100_xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:109]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=2180
    old=client.get(PREFIX+'/catalog?grade=7').json()
    g8=client.get(PREFIX+'/catalog?grade=8').json();assert g8['lessons'][35]['state']=='available'
    for l in docs[109:114]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==2280
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==114
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert client.get(PREFIX+'/catalog?grade=7').json()==old
