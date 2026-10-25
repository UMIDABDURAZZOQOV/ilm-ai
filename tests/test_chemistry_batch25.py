"""Fertilizer reporting,held medical claims and exact digital-lab source models."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_last_paragraphs_practical_and_first_lab_keep_exact_source_order():
    docs=load_lessons()[119:124]
    assert [l['topic_id'] for l in docs]==['ch8-paragraph42','ch8-paragraph43','ch8-paragraph44','ch8-practical05','ch8-laboratory01']
    assert [l['sequence'] for l in docs]==list(range(46,51))
    assert sum(len(l['content']['cards']) for l in docs)==59
    assert sum(len(l['assessments']) for l in docs)==68
    assert all(l['content']['examples'] for l in docs)
    assert all(r['topic_id']!='ch8-laboratory02' for l in docs for r in l['source_refs'])
    assert ('ch8-paragraph04',[21]) in [(r['topic_id'],r['printed_pages']) for r in docs[3]['facts']['watermatrix']['source_refs']]
    assert ('ch8-paragraph20',[83]) in [(r['topic_id'],r['printed_pages']) for r in docs[3]['facts']['acidmatrix']['source_refs']]
    assert ('ch8-paragraph02',[15]) in [(r['topic_id'],r['printed_pages']) for r in docs[3]['facts']['families']['source_refs']]
    assert 'KHSO3' not in str(docs[3]['facts']['families'])
    assert set(q['response_kind'] for q in docs[2]['assessments'])=={'concept_selection','short_text','chemical_formula'}
    assert all('parser' not in f['claim'] for f in docs[0]['facts'].values())


@pytest.mark.parametrize('topic',['ch8-paragraph42','ch8-paragraph43','ch8-paragraph44','ch8-practical05','ch8-laboratory01'])
def test_all_five_scoped_source_reviews_remain_visible(topic):
    c=deepcopy(load_catalog());next(r for r in c['books'][1]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


@pytest.mark.parametrize('file,fid,text,error',[
 ('paragraph43','nitrogenmass','16.4','unresolved_fertilizer_arithmetic'),
 ('paragraph43','phosphatemass','4.117','unresolved_fertilizer_arithmetic'),
 ('paragraph43','potassiummass','473.3','unresolved_fertilizer_arithmetic'),
 ('paragraph44','symbols','Askaltsiy','unreviewed_biogen_clinical_claim'),
 ('paragraph44','substances','C vitamini','unreviewed_biogen_clinical_claim'),
 ('paragraph44','examples','Barcha mikroelementlar zarur','unqualified_trace_element_essentiality'),
 ('laboratory01','copper','Barcha gidroksidlar ishqorda eriydi','unqualified_hydroxide_alkali_dissolution')])
def test_wrong_arithmetic_clinical_and_universal_claims_never_become_verified_answers(file,fid,text,error):
    l=deepcopy(read_json(DIRECTORY/f'grade8_{file}.json'));l['facts'][fid]['verified_answers'].append(text)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade8_{file}_review.json'))


@pytest.mark.parametrize('topic,qn,value,code',[
 ('ch8-paragraph42',7,'CO(NH2)2','correct'),
 ('ch8-paragraph42',8,'NH4H2PO4','correct'),
 ('ch8-paragraph42',11,'35','correct'),
 ('ch8-paragraph42',12,'21,21','correct'),
 ('ch8-paragraph43',7,'Ca(NO3)2','correct'),
 ('ch8-paragraph43',9,'Ca3(PO4)2+2H2SO4=Ca(H2PO4)2+2CaSO4','correct'),
 ('ch8-paragraph43',10,'Ca3(PO4)2+4H3PO4=3Ca(H2PO4)2','correct'),
 ('ch8-paragraph43',11,'CaCO3+H3PO4=CaHPO4+H2O+CO2','correct'),
 ('ch8-paragraph43',12,'16.47','correct'),
 ('ch8-paragraph43',12,'16.4','incorrect'),
 ('ch8-paragraph43',13,'4,120','correct'),
 ('ch8-paragraph43',13,'4.117','incorrect'),
 ('ch8-paragraph43',15,'473.2','correct'),
 ('ch8-paragraph43',15,'473.3','incorrect'),
 ('ch8-paragraph43',16,'31.5','correct'),
 ('ch8-paragraph43',17,'8.5','correct'),
 ('ch8-paragraph43',18,'11200','correct'),
 ('ch8-paragraph44',7,'Zn','correct'),
 ('ch8-paragraph44',7,'zn','invalid_answer'),
 ('ch8-paragraph44',8,'Mo','correct'),
 ('ch8-practical05',7,'KHSO4','correct'),
 ('ch8-practical05',8,'3CaO+2H3PO4=Ca3(PO4)2+3H2O','correct'),
 ('ch8-practical05',10,'Al(OH)3+3HCl=AlCl3+3H2O','correct'),
 ('ch8-practical05',11,'2Na+H2=2NaH','correct'),
 ('ch8-practical05',12,'CuCl2+2NaOH=Cu(OH)2+2NaCl','correct'),
 ('ch8-practical05',13,'5.486','correct'),
 ('ch8-practical05',15,'4.816e22','correct'),
 ('ch8-practical05',16,'44','correct'),
 ('ch8-practical05',17,'7,9744','correct'),
 ('ch8-practical05',18,'2.007','correct'),
 ('ch8-laboratory01',5,'Zn(OH)2','correct'),
 ('ch8-laboratory01',7,'ZnCl2+2NaOH=Zn(OH)2+2NaCl','correct'),
 ('ch8-laboratory01',8,'Zn(OH)2+2HCl=ZnCl2+2H2O','correct'),
 ('ch8-laboratory01',9,'Zn(OH)2+2NaOH=Na2ZnO2+2H2O','correct'),
 ('ch8-laboratory01',9,'Zn(OH)2+NaOH=Na2ZnO2+H2O','atom_imbalance'),
 ('ch8-laboratory01',10,'Cu(OH)2+2HCl=CuCl2+2H2O','correct')])
def test_bounded_grader_keeps_exact_given_model_and_rounding(topic,qn,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==topic)
    assert grade_answer(l['assessments'][qn-1]['grading_spec'],{'value':value})==code


def test_five_new_lessons_preserve119_and_award100_xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:119]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=2380
    old=client.get(PREFIX+'/catalog?grade=7').json()
    assert client.get(PREFIX+'/catalog?grade=8').json()['lessons'][45]['state']=='available'
    for l in docs[119:124]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==2480
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==124
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert client.get(PREFIX+'/catalog?grade=7').json()==old
