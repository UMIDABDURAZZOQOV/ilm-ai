"""Gas/equivalent/ion lessons use declared textbook models and common grading."""
from collections import Counter
from copy import deepcopy
from decimal import Decimal
from uuid import uuid4
import pytest
from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for
TOPICS=[f'ch11-paragraph{n:02}' for n in range(6,11)]

def test_batch47_source_order_and_existing_inputs(reviewed_chemistry_documents):
    lessons=reviewed_chemistry_documents[240:245]
    assert [l['topic_id'] for l in lessons]==TOPICS
    assert [l['sequence'] for l in lessons]==[6,7,8,9,10]
    assert sum(len(l['content']['cards']) for l in lessons)==53
    assert Counter(q['response_kind'] for l in lessons for q in l['assessments'])==dict(concept_selection=21,short_text=11,numeric_value=29,chemical_equation=3)
    assert all(l['content']['examples'] for l in lessons)
    assert all(not b['course_ready'] for b in load_catalog()['books'])

@pytest.mark.parametrize('topic',TOPICS)
def test_batch47_scope_cannot_disappear(topic):
    c=deepcopy(load_catalog());next(r for r in c['books'][4]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)

@pytest.mark.parametrize('n,value,error',[
    (6,'Molyar hajm 22.4 mol/L','gas_molar_volume_reciprocal_unit_withheld'),
    (7,'Ekvivalent massa reaksiyaga hech qachon bog‘liq emas','equivalent_requires_reaction_context'),
    (8,'Birlik o‘zgarsa fizik R doimiysi o‘zgaradi','gas_R_physical_constant_not_changed_by_units'),
    (9,'H2SO4 kuchsiz elektrolit','electrolyte_sulfuric_weak_literal_withheld'),
    (10,'CaCl2 dan bitta xlorid ioni','dissociation_cacl2_chloride_count_withheld')])
def test_batch47_bad_literal_is_rejected(n,value,error):
    l=deepcopy(read_json(DIRECTORY/f'grade11_paragraph{n:02}.json'));next(iter(l['facts'].values()))['verified_answers'].append(value)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade11_paragraph{n:02}_review.json'))

@pytest.mark.parametrize('n,expected,value,code',[
    (6,'11.2','11,2','correct'),(6,'3.01e23','301e21','correct'),
    (6,'H2+Cl2=2HCl','2H2+2Cl2=4HCl','correct'),
    (7,'17','17','correct'),(7,'49','49','correct'),(7,'5.6','5,6','correct'),
    (8,'200','200','correct'),(8,'132.96','132,96','correct'),
    (8,'9.03e23','9.03e22','incorrect'),(9,'Anion','anion','correct'),
    (9,'2','2','correct'),(10,'0.005','5e-3','correct'),
    (10,'400','200','incorrect'),(10,'3.612e21','3,612e21','correct'),
    (10,'Na2CO3+2HCl=2NaCl+CO2+H2O','Na2CO3+HCl=NaCl+CO2+H2O','atom_imbalance')])
def test_batch47_common_grader(n,expected,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch11-paragraph{n:02}')
    q=next(q for q in l['assessments'] if q['grading_spec']['expected']==expected and q['response_kind']!='concept_selection')
    assert grade_answer(q['grading_spec'],{'value':value})==code

def test_batch47_recomputed_unit_models():
    assert Decimal('11.2')/Decimal('22.4')*Decimal('6.02e23')==Decimal('3.01e23')
    assert 102/(2*3)==17 and 98/2==49 and 342/6==57
    assert Decimal('.5')*Decimal('8.31')*320/10==Decimal('132.96')
    assert 50/Decimal('.2')*Decimal('.8')*2==400
    assert Decimal('.4')*3*Decimal('.005')*Decimal('6.02e23')==Decimal('3.612e21')
    assert Decimal(210)/3/Decimal('.7')*Decimal('.3')==30

def test_batch47_source_model_boundaries(reviewed_chemistry_documents):
    rows={l['topic_id']:l for l in reviewed_chemistry_documents}
    proof=rows['ch11-paragraph06']['facts']['particles']['source_refs']
    assert any(r['topic_id']=='ch11-paragraph05' and r['printed_pages']==[31] and r['file_name']=='umumiy_kimyo_11_uzb.pdf' for r in proof)
    assert all(q['response_kind'] not in {'chemical_formula','chemical_equation'} for q in rows['ch11-paragraph09']['assessments'])
    assert all('H+' not in q['grading_spec']['expected'] for q in rows['ch11-paragraph10']['assessments'] if q['response_kind']=='chemical_equation')

def test_batch47_preserves240_and_adds100xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:240]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=4800
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8,9,10)}
    g11=client.get(PREFIX+'/catalog?grade=11').json()['lessons']
    assert all(l['state']=='completed' for l in g11[:5])
    assert g11[5]['state']=='available' and all(l['state']=='locked' for l in g11[6:10])
    for l in docs[240:245]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json();assert 'grading_spec' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==4900
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==245
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    current=client.get(PREFIX+'/catalog?grade=11').json()['lessons']
    assert all(l['state']=='completed' for l in current[:10])
    if len(current)>10:assert current[10]['state']=='available'
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
