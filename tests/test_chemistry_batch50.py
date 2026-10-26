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
TOPICS=[f'ch11-paragraph{n:02}' for n in range(21,26)]

def test_batch50_source_order_and_topic_appropriate_frq(reviewed_chemistry_documents):
    lessons=reviewed_chemistry_documents[255:260]
    assert [l['topic_id'] for l in lessons]==TOPICS
    assert [l['sequence'] for l in lessons]==[21,22,23,24,25]
    assert sum(len(l['content']['cards']) for l in lessons)==45
    assert Counter(q['response_kind'] for l in lessons for q in l['assessments'])==dict(concept_selection=15,short_text=8,numeric_value=25,chemical_equation=3)
    assert all(l['content']['examples'] for l in lessons)
    assert all(not b['course_ready'] for b in load_catalog()['books'])

@pytest.mark.parametrize('topic',TOPICS)
def test_batch50_scope_cannot_disappear(topic):
    c=deepcopy(load_catalog());next(r for r in c['books'][4]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)

@pytest.mark.parametrize('n,value,error',[(21, 'Normal konsentratsiya barcha reaksiyalarda molyarlikka teng', 'normality_percent_requires_reaction_factor'), (22, 'Tezlik har qanday tenglama koeffitsiyentidan aniqlanadi', 'kinetic_order_not_universal_stoichiometry'), (23, 'Barcha reaksiyalarda gamma har doim 2–4', 'gamma_not_universal_all_reactions'), (24, 'Tenglashtirilgan tenglamadan har doim haqiqiy kinetik daraja keladi', 'rate_order_requires_separate_model'), (25, 'Kc=2 bo‘lsa muvozanatda teskari tezlik ikki marta katta', 'equilibrium_rates_equal_despite_k2')])
def test_batch50_bad_literal_is_rejected(n,value,error):
    l=deepcopy(read_json(DIRECTORY/f'grade11_paragraph{n:02}.json'));next(iter(l['facts'].values()))['verified_answers'].append(value)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade11_paragraph{n:02}_review.json'))

@pytest.mark.parametrize('n,expected,value,code',[(21, '32.67', '32,67', 'correct'), (21, '3', '3', 'correct'), (22, '1.5', '1,5', 'correct'), (22, '2', '1', 'incorrect'), (22, '2.5', '25e-1', 'correct'), (22, '75', '75', 'correct'), (23, '27', '27', 'correct'), (23, '0.04', '4e-2', 'correct'), (24, '180', '180', 'correct'), (24, '0.125', '0,125', 'correct'), (25, '0.05', '5e-2', 'correct'), (25, '9.6', '9,6', 'correct')])
def test_batch50_common_grader(n,expected,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch11-paragraph{n:02}')
    q=next(q for q in l['assessments'] if q['grading_spec']['expected']==expected and q['response_kind']!='concept_selection')
    assert grade_answer(q['grading_spec'],{'value':value})==code

def test_batch50_independent_numeric_basis():
    d=Decimal
    assert (d(98)/3).quantize(d('.01'),rounding=ROUND_HALF_UP)==d('32.67')
    assert d(9)/(3*d('1.5'))==2
    assert d(75)/(5*6)==d('2.5')
    assert (d(7)-2)/4*60==75
    assert d(3)**2*3==27
    assert d(5)**-2==d('.04')
    assert d(45)/(6*d('2.5'))*60==180
    assert d(8)*d('.25')**3==d('.125')
    assert d('.25')*d('.8')/(d('.4')*d('.5')**2)==2
    assert d('.03')*d('.4')**2/(d('.1')**3*d('.5'))==d('9.6')

def test_batch50_prior_context_and_equal_rates(reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']=='ch11-paragraph23')
    assert any(r['topic_id']=='ch11-paragraph08' and r['printed_pages']==[46] for r in l['facts']['compression']['source_refs'])
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']=='ch11-paragraph25')
    assert l['facts']['equal']['verified_answers'][0]=='Teng'

def test_batch50_preserves255_and_adds100xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:255]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=5100
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8,9,10)}
    g11=client.get(PREFIX+'/catalog?grade=11').json()['lessons']
    assert all(l['state']=='completed' for l in g11[:20])
    assert g11[20]['state']=='available' and all(l['state']=='locked' for l in g11[21:25])
    for l in docs[255:260]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json();assert 'grading_spec' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==5200
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==260
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    current=client.get(PREFIX+'/catalog?grade=11').json()['lessons']
    assert all(l['state']=='completed' for l in current[:25])
    if len(current)>25:assert current[25]['state']=='available'
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
