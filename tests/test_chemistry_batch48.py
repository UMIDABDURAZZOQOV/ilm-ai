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
TOPICS=[f'ch11-paragraph{n:02}' for n in range(11,16)]

def test_batch48_source_order_and_topic_appropriate_frq(reviewed_chemistry_documents):
    lessons=reviewed_chemistry_documents[245:250]
    assert [l['topic_id'] for l in lessons]==TOPICS
    assert [l['sequence'] for l in lessons]==[11,12,13,14,15]
    assert sum(len(l['content']['cards']) for l in lessons)==43
    assert Counter(q['response_kind'] for l in lessons for q in l['assessments'])==dict(concept_selection=20,short_text=11,numeric_value=21)
    assert all(l['content']['examples'] for l in lessons)
    assert all(q['response_kind'] in {'concept_selection','short_text'} for q in lessons[1]['assessments'])
    assert all(not b['course_ready'] for b in load_catalog()['books'])

@pytest.mark.parametrize('topic',TOPICS)
def test_batch48_scope_cannot_disappear(topic):
    c=deepcopy(load_catalog());next(r for r in c['books'][4]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)

@pytest.mark.parametrize('n,value,error',[
    (11,'Barcha cho‘kmalar hech qachon gidrolizlanmaydi','hydrolysis_precipitate_absolute_withheld'),
    (12,'Yomg‘ir suvi doimo kimyoviy sof','solution_rainwater_purity_absolute_withheld'),
    (13,'Barcha qattiq moddalar eruvchanligi haroratga to‘g‘ri proporsional','solubility_temperature_universal_proportion_withheld'),
    (14,'Kristall massasi eritma massasiga har doim kiradi','solubility_separate_crystal_not_dissolved_solution'),
    (15,'Foiz konsentratsiyada maxraj faqat suv massasi','mass_percentage_requires_total_solution_mass')])
def test_batch48_bad_literal_is_rejected(n,value,error):
    l=deepcopy(read_json(DIRECTORY/f'grade11_paragraph{n:02}.json'));next(iter(l['facts'].values()))['verified_answers'].append(value)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade11_paragraph{n:02}_review.json'))

@pytest.mark.parametrize('n,expected,value,code',[
    (11,'7','7','correct'),(11,'Gidroliz','gidroliz','correct'),
    (12,'Gomogen','gomogen','correct'),(12,'Gidratlanish','gidratlanish','correct'),
    (13,'2.2','2,2','correct'),(13,'137.2','141.4','incorrect'),
    (13,'4.2','4.2e0','correct'),(14,'74','74','correct'),
    (14,'59.75','59,75','correct'),(14,'276.25','276,25','correct'),
    (15,'23.08','23.08','correct'),(15,'35.33','35,33','correct')])
def test_batch48_common_grader(n,expected,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch11-paragraph{n:02}')
    q=next(q for q in l['assessments'] if q['grading_spec']['expected']==expected and q['response_kind']!='concept_selection')
    assert grade_answer(q['grading_spec'],{'value':value})==code

def test_batch48_mass_phase_and_rounding_recomputed():
    assert Decimal('41.4')-Decimal('37.2')==Decimal('4.2')
    water=Decimal(336)/Decimal('134.4')*100
    initial=water*Decimal('.344');remaining=water*Decimal('.105')
    assert (water,initial,remaining)==(250,86,Decimal('26.25'))
    assert initial-remaining==Decimal('59.75')
    assert water+remaining==Decimal('276.25')
    assert water+remaining+initial-remaining==336
    assert (Decimal(30)/130*100).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)==Decimal('23.08')
    assert (Decimal(53)/150*100).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)==Decimal('35.33')

def test_batch48_prior_solvent_basis_proof(reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']=='ch11-paragraph14')
    assert any(r['topic_id']=='ch11-paragraph13' and r['printed_pages']==[65] for r in l['facts']['rule']['source_refs'])
    assert '100 g erituvchi' in reviewed_chemistry_documents[247]['facts']['definition']['claim']
    assert 'eritma' in reviewed_chemistry_documents[249]['facts']['meaning']['claim'].lower()

def test_batch48_preserves245_and_adds100xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:245]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=4900
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8,9,10)}
    g11=client.get(PREFIX+'/catalog?grade=11').json()['lessons']
    assert all(l['state']=='completed' for l in g11[:10])
    assert g11[10]['state']=='available' and all(l['state']=='locked' for l in g11[11:15])
    for l in docs[245:250]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json();assert 'grading_spec' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==5000
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==250
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    current=client.get(PREFIX+'/catalog?grade=11').json()['lessons']
    assert all(l['state']=='completed' for l in current[:15])
    if len(current)>15:assert current[15]['state']=='available'
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
