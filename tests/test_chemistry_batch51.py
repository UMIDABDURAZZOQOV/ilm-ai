"""Hydrolysis and solutions distinguish source models, phase and mass bases."""
from collections import Counter
from copy import deepcopy
from decimal import Decimal,ROUND_HALF_UP
from uuid import uuid4
import pytest
from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for
TOPICS=[f'ch11-paragraph{n:02}' for n in range(26,34)]

def test_batch51_source_order_and_topic_appropriate_frq(reviewed_chemistry_documents):
    lessons=reviewed_chemistry_documents[260:268]
    assert [l['topic_id'] for l in lessons]==TOPICS
    assert [l['sequence'] for l in lessons]==[26,27,28,29,30,31,32,33]
    assert sum(len(l['content']['cards']) for l in lessons)==66
    assert Counter(q['response_kind'] for l in lessons for q in l['assessments'])==dict(concept_selection=26,short_text=16,numeric_value=42,chemical_equation=8)
    assert all(l['content']['examples'] for l in lessons)
    assert all(not b['course_ready'] for b in load_catalog()['books'])

@pytest.mark.parametrize('topic',TOPICS)
def test_batch51_scope_cannot_disappear(topic):
    c=deepcopy(load_catalog());next(r for r in c['books'][4]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)

@pytest.mark.parametrize('n,value,error',[(26, 'Katalizator muvozanatni har doim o‘ngga siljitadi', 'catalyst_does_not_shift_equilibrium'), (27, '9×9=27', 'equilibrium_bad_product_27_withheld'), (28, 'Eritmada alohida N5+ ioni bor', 'formal_oxidation_state_not_isolated_ion'), (29, 'Kislotali berilgan molekulyar kartada suv koeffitsiyenti 8', 'redox_acid_bad_water_coefficient_withheld'), (30, 'MnSO4 har qanday reaksiyada oksidlovchi ekvivalenti 30,2', 'redox_product_equivalent_not_intrinsic'), (31, 'Barcha elektrokimyoviy elementlarda katod manfiy', 'electrolytic_polarity_not_all_cells'), (32, '96500 sekundli formulaga minutni o‘zgartirmasdan qo‘yish mumkin', 'faraday_seconds_require_time_conversion'), (33, 'Aralashmadagi har bir metallga bir xil jami zaryad to‘liq sarflanadi', 'mixed_metals_share_one_total_charge')])
def test_batch51_bad_literal_is_rejected(n,value,error):
    l=deepcopy(read_json(DIRECTORY/f'grade11_paragraph{n:02}.json'));next(iter(l['facts'].values()))['verified_answers'].append(value)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade11_paragraph{n:02}_review.json'))

@pytest.mark.parametrize('n,expected,value,code',[(26, '4', '4', 'correct'), (26, 'Katalizator', 'katalizator', 'correct'), (27, '2.77', '2,77', 'correct'), (27, '1.9', '19e-1', 'correct'), (27, '2.25', '2,25', 'correct'), (28, '84', '84', 'correct'), (28, '30', '30', 'correct'), (29, '5', '5', 'correct'), (29, '1', '1', 'correct'), (30, '31.6', '31,6', 'correct'), (30, '6.04', '604e-2', 'correct'), (31, 'Anod', 'anod', 'correct'), (31, '2', '2', 'correct'), (32, '38600', '38600', 'correct'), (32, '7.03', '7', 'incorrect'), (32, '5', '5', 'correct'), (33, '0.96', '96e-2', 'correct'), (33, '2.82', '2,82', 'correct')])
def test_batch51_common_grader(n,expected,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch11-paragraph{n:02}')
    q=next(q for q in l['assessments'] if q['grading_spec']['expected']==expected and q['response_kind']!='concept_selection')
    assert grade_answer(q['grading_spec'],{'value':value})==code

def test_batch51_independent_numeric_basis():
    d=Decimal
    assert (d(36)/13).quantize(d('.01'),rounding=ROUND_HALF_UP)==d('2.77')
    assert d(9)/4==d('2.25')
    assert d('.7')+3*d('.4')==d('1.9')
    assert d(158)/5==d('31.6')
    assert d('30.4')/152/5*151==d('6.04')
    assert d(160)/80*96500/5==38600
    assert d(270)*96500/(9*4825*60)==10
    assert (d('16.8')/d('239.05')*100).quantize(d('.01'),rounding=ROUND_HALF_UP)==d('7.03')
    assert (d('11.25')/18)/(d(20)/160)==5
    assert d('.04')*d('.25')*108+d('.04')*d('.75')*32==d('2.04')
    assert d('.015')*188==d('2.82')

def test_batch51_context_and_safe_ionic_display(reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']=='ch11-paragraph32')
    assert any(r['topic_id']=='ch11-paragraph05' and r['printed_pages']==[31] for r in l['facts']['hydrate']['source_refs'])
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']=='ch11-paragraph28')
    assert all('e−' not in q['grading_spec']['expected'] for q in l['assessments'] if q['response_kind']=='chemical_equation')

def test_batch51_preserves260_and_adds160xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:260]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=5200
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8,9,10)}
    g11=client.get(PREFIX+'/catalog?grade=11').json()['lessons']
    assert all(l['state']=='completed' for l in g11[:25])
    assert g11[25]['state']=='available' and all(l['state']=='locked' for l in g11[26:33])
    for l in docs[260:268]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json();assert 'grading_spec' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==5360
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==268
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    current=client.get(PREFIX+'/catalog?grade=11').json()['lessons']
    assert all(l['state']=='completed' for l in current[:33])
    assert len(current)==33
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
