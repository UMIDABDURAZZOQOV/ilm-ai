"""Given organic sourcegraphs and conditional amount models retain exact grading."""
from collections import Counter
from copy import deepcopy
from uuid import uuid4
import pytest
from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for

TOPICS=[f'ch10-paragraph{n:02}' for n in range(6,11)]
def test_batch39_source_order_graph_and_given_product_scope():
    lessons=load_lessons()[199:204]
    assert [l['topic_id'] for l in lessons]==TOPICS
    assert [l['sequence'] for l in lessons]==list(range(6,11))
    assert sum(len(l['content']['cards']) for l in lessons)==57
    assert Counter(q['response_kind'] for l in lessons for q in l['assessments'])=={
        'concept_selection':20,'short_text':11,'numeric_value':35,'chemical_formula':1,'chemical_equation':17}
    assert all(l['content']['examples'] for l in lessons)
    assert all(not b['course_ready'] for b in load_catalog()['books'])
    assert all(q['response_kind']!='chemical_formula' for q in lessons[0]['assessments'])
    assert all(r['printed_pages'][0]<=41 for r in lessons[4]['source_refs'] if r['book_id']==lessons[4]['book_id'])
    mismatch=next(q for q in lessons[4]['assessments'] if q['fact_ids']==['inconsistent'])
    assert mismatch['grading_spec']['verified_answer']=='Ma’lumotlar mos kelmaydi'
    assert grade_answer(mismatch['grading_spec'],{'choice_id':'d'})=='correct'

@pytest.mark.parametrize('topic',TOPICS)
def test_batch39_required_editorial_review_cannot_disappear(topic):
    catalog=deepcopy(load_catalog())
    next(r for r in catalog['books'][3]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(catalog)

@pytest.mark.parametrize('n,fid,value,error',[
    (6,'method','1,5-dimetilgeksan','copied_nonlongest_parent'),
    (7,'mixed','2,2,3,3-tetrametilgeksan','c8_dimer'),
    (8,'five','Pentanda C soni kamayadi','same_c5_isomer'),
    (9,'difference','Har qanday alkan o‘z-o‘zidan halqa','schematic_formula_difference'),
    (10,'inconsistent','198','inconsistent_combustion_data')])
def test_batch39_withheld_key_cannot_become_verified(n,fid,value,error):
    l=deepcopy(read_json(DIRECTORY/f'grade10_paragraph{n:02}.json'))
    l['facts'][fid]['verified_answers'].append(value)
    with pytest.raises(ValueError,match=error):
        validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade10_paragraph{n:02}_review.json'))

@pytest.mark.parametrize('n,fid,expected,value,code',[
    (6,'dimethyl','2','2','correct'),(6,'avogadro','Propan','propan','correct'),
    (6,'colored','8','8','correct'),(6,'dimethyl','0','0','correct'),
    (7,'small','6.72','6,72','correct'),(7,'large','234','234','correct'),
    (7,'large','50.4','5.04e1','correct'),(7,'acetatemass','11.2','11,2','correct'),
    (7,'carbide','Al4C3+12H2O=4Al(OH)3+3CH4','Al4C3+12H2O=4Al(OH)3+3CH4','correct'),
    (8,'watermass','216','216','correct'),(8,'butanemass','352','352','correct'),
    (8,'gasratio','268.8','268,8','correct'),
    (8,'pyrolysis','2CH4=C2H2+3H2','2CH4=C2H2+2H2','atom_imbalance'),
    (9,'gas_h','16.8','16,8','correct'),(9,'gas_c','72','72','correct'),
    (9,'table','C3H6','C3H6','correct'),
    (10,'water','50.4','50,4','correct'),(10,'consistent','120','120','correct'),
    (10,'reverse','5.6','5,6','correct'),(10,'pentanemass','14.4','1.44e1','correct')])
def test_batch39_existing_grader(n,fid,expected,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch10-paragraph{n:02}')
    q=next(q for q in l['assessments'] if fid in q['fact_ids'] and q['grading_spec']['expected']==expected)
    assert grade_answer(q['grading_spec'],{'value':value})==code

def test_batch39_preserves199_and_awards100xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:199]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=3980
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8,9)}
    g10=client.get(PREFIX+'/catalog?grade=10').json()
    assert g10['available_grades']==[7,8,9,10]
    assert all(l['state']=='completed' for l in g10['lessons'][:5])
    assert g10['lessons'][5]['state']=='available' and all(l['state']=='locked' for l in g10['lessons'][6:])
    for l in docs[199:204]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==4080
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==204
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    current=client.get(PREFIX+'/catalog?grade=10').json()['lessons']
    assert all(l['state']=='completed' for l in current[:10])
    if len(current)>10:assert current[10]['state']=='available'
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
