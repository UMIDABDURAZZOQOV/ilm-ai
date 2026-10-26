"""Grade11 introduction uses the established Chemistry contracts and supplied scans."""
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

TOPICS=[f'ch11-paragraph{n:02}' for n in range(1,6)]

def test_batch46_five_source_ordered_grade11_lessons(reviewed_chemistry_documents):
    lessons=reviewed_chemistry_documents[235:240]
    assert [l['topic_id'] for l in lessons]==TOPICS
    assert [l['sequence'] for l in lessons]==[1,2,3,4,5]
    assert sum(len(l['content']['cards']) for l in lessons)==62
    assert Counter(q['response_kind'] for l in lessons for q in l['assessments'])==dict(concept_selection=20,short_text=13,numeric_value=39,chemical_formula=3,chemical_equation=1)
    assert all(l['content']['examples'] for l in lessons)
    assert all(not b['course_ready'] for b in load_catalog()['books'])

@pytest.mark.parametrize('topic',TOPICS)
def test_batch46_scope_cannot_disappear(topic):
    c=deepcopy(load_catalog());next(r for r in c['books'][4]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)

@pytest.mark.parametrize('n,value,error',[
    (1,'n² ta pog‘onacha','quantum_shell_n_squared_is_orbitals_not_subshells'),
    (2,'Barcha elementlarning eng yuqori oksidlanishi guruh raqamiga teng','periodic_group_is_not_universal_max_oxidation'),
    (3,'Cr51 jami 78 ta zarracha','isotope_cr51_wrong_particle_sum_withheld'),
    (4,'Suyuq simobda metall bog‘ yo‘q','bond_liquid_mercury_claim_withheld'),
    (5,'Ag atom massasi 1.79e-24 g','mole_silver_wrong_single_atom_exponent_withheld')])
def test_batch46_known_bad_literal_is_rejected(n,value,error):
    l=deepcopy(read_json(DIRECTORY/f'grade11_paragraph{n:02}.json'))
    next(iter(l['facts'].values()))['verified_answers'].append(value)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade11_paragraph{n:02}_review.json'))

@pytest.mark.parametrize('n,expected,value,code',[
    (1,'-0.5','-0,5','correct'),(1,'14','14','correct'),(1,'9','18','incorrect'),
    (2,'9','9e0','correct'),(3,'35.45','35,45','correct'),
    (3,'82','82','correct'),(3,'12','12','correct'),
    (4,'0.9','0,9','correct'),(4,'1.4','1,4','correct'),
    (5,'0.1','1e-1','correct'),(5,'3.82e-23','3,82e-23','correct'),
    (5,'1.06e-22','1.06e-24','incorrect'),
    (5,'Fe+S=FeS','2Fe+2S=2FeS','correct'),
    (5,'Na2SO4','Na2SO3','incorrect')])
def test_batch46_common_grader_models(n,expected,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch11-paragraph{n:02}')
    q=next(q for q in l['assessments'] if q['grading_spec']['expected']==expected and q['response_kind']!='concept_selection')
    assert grade_answer(q['grading_spec'],{'value':value})==code

def test_batch46_no_nuclear_or_configuration_formula_parser(reviewed_chemistry_documents):
    for l in (reviewed_chemistry_documents[235],reviewed_chemistry_documents[237]):
        assert all(q['response_kind'] not in {'chemical_formula','chemical_equation'} for q in l['assessments'])
    for l in reviewed_chemistry_documents[235:240]:
        assert all(r['file_name']=='umumiy_kimyo_11_uzb.pdf' for r in l['source_refs'] if r['book_id']==l['book_id'])
    rows={l['topic_id']:l for l in reviewed_chemistry_documents}
    refs=rows['ch11-paragraph04']['facts']['acetylene']['source_refs']
    assert any(r['topic_id']=='ch10-paragraph17' and r['printed_pages']==[68] and r['file_name']=='organik_kimyo_10_uzb.pdf' for r in refs)

def test_batch46_numeric_models_recomputed():
    assert (3**2,2*3**2,2*(2*3+1))==(9,18,14)
    assert Decimal('.775')*35+Decimal('.225')*37==Decimal('35.45')
    assert [136-54,138-56,139-57]==[82,82,82]
    assert 24+27+24==75 and 6*2==12
    assert Decimal('3.5')-Decimal('2.1')==Decimal('1.4')
    assert 2*23+32+4*16==142 and Decimal('14.2')/142==Decimal('.1')

def test_batch46_grade11_preserves235_and_adds100xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:235]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=4700
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8,9,10)}
    g11=client.get(PREFIX+'/catalog?grade=11').json()
    assert g11['available_grades']==[7,8,9,10,11]
    assert g11['lessons'][0]['state']=='available' and all(l['state']=='locked' for l in g11['lessons'][1:5])
    assert not g11['course_complete'] and not g11['grade_content_complete']
    for l in docs[235:240]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==4800
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==240
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    current=client.get(PREFIX+'/catalog?grade=11').json()['lessons']
    assert all(l['state']=='completed' for l in current[:5])
    if len(current)>5:assert current[5]['state']=='available'
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
