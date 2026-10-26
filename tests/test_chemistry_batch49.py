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
TOPICS=[f'ch11-paragraph{n:02}' for n in range(16,21)]

def test_batch49_source_order_and_topic_appropriate_frq(reviewed_chemistry_documents):
    lessons=reviewed_chemistry_documents[250:255]
    assert [l['topic_id'] for l in lessons]==TOPICS
    assert [l['sequence'] for l in lessons]==[16,17,18,19,20]
    assert sum(len(l['content']['cards']) for l in lessons)==40
    assert Counter(q['response_kind'] for l in lessons for q in l['assessments'])==dict(concept_selection=15,short_text=6,numeric_value=27,chemical_equation=2)
    assert all(l['content']['examples'] for l in lessons)
    assert all(not b['course_ready'] for b in load_catalog()['books'])

@pytest.mark.parametrize('topic',TOPICS)
def test_batch49_scope_cannot_disappear(topic):
    c=deepcopy(load_catalog());next(r for r in c['books'][4]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)

@pytest.mark.parametrize('n,value,error',[(16, 'Cho‘kma har doim suyuq eritma massasiga kiradi', 'reaction_separate_solid_not_solution_mass'), (17, 'Barcha suvli eritmalarning zichligi aynan 1 g/mL', 'solution_density_universal_water_value_withheld'), (18, 'Molyarlik maxraji har doim boshlang‘ich suv hajmi', 'molarity_requires_final_solution_volume'), (19, 'Normal konsentratsiya har doim molyar konsentratsiyaga teng', 'normality_requires_reaction_factor'), (20, 'Molyar massa 56 bo‘lsa modda har doim KOH', 'molar_mass_not_unique_identity')])
def test_batch49_bad_literal_is_rejected(n,value,error):
    l=deepcopy(read_json(DIRECTORY/f'grade11_paragraph{n:02}.json'));next(iter(l['facts'].values()))['verified_answers'].append(value)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade11_paragraph{n:02}_review.json'))

@pytest.mark.parametrize('n,expected,value,code',[(16, '15.71', '15,71', 'correct'), (16, '890.8', '984', 'incorrect'), (16, '93.2', '932e-1', 'correct'), (17, '224', '224', 'correct'), (17, '85.2', '85,2', 'correct'), (18, '0.25', '25e-2', 'correct'), (18, '124.8', '124,8', 'correct'), (19, '85.5', '85,5', 'correct'), (19, '4000.32', '4000', 'incorrect'), (20, '4.46', '4,46', 'correct'), (20, '1.25', '125e-2', 'correct'), (20, '56', '56', 'correct')])
def test_batch49_common_grader(n,expected,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch11-paragraph{n:02}')
    q=next(q for q in l['assessments'] if q['grading_spec']['expected']==expected and q['response_kind']!='concept_selection')
    assert grade_answer(q['grading_spec'],{'value':value})==code

def test_batch49_independent_numeric_basis():
    d=Decimal
    assert (d('46.8')/d('890.8')*100).quantize(d('.01'),rounding=ROUND_HALF_UP)==d('5.25')
    assert (d(110)/700*100).quantize(d('.01'),rounding=ROUND_HALF_UP)==d('15.71')
    assert d(200)*d('1.12')==224
    assert d('177.5')*d('1.2')*d('.4')==d('85.2')
    assert d('.6')*208==d('124.8')
    assert (d('5068.4')/d('1.267')).quantize(d('.01'),rounding=ROUND_HALF_UP)==d('4000.32')
    assert d(10)*d('1.26')*5/63==1
    assert d('2.5')*101/(10*d('20.2'))==d('1.25')

def test_batch49_reaction_factor_context(reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']=='ch11-paragraph19')
    assert any(r['topic_id']=='ch11-paragraph07' and r['printed_pages']==[42] for r in l['facts']['amount']['source_refs'])
    assert 'to‘liq' in l['facts']['reaction']['claim']

def test_batch49_preserves250_and_adds100xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:250]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=5000
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8,9,10)}
    g11=client.get(PREFIX+'/catalog?grade=11').json()['lessons']
    assert all(l['state']=='completed' for l in g11[:15])
    assert g11[15]['state']=='available' and all(l['state']=='locked' for l in g11[16:20])
    for l in docs[250:255]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json();assert 'grading_spec' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==5100
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==255
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    current=client.get(PREFIX+'/catalog?grade=11').json()['lessons']
    assert all(l['state']=='completed' for l in current[:20])
    if len(current)>20:assert current[20]['state']=='available'
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
