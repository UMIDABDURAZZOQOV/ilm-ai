"""Final organic paragraphs retain source/model boundaries and common learning."""
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

TOPICS=[f'ch10-paragraph{n:02}' for n in range(31,36)]

def test_batch44_five_source_ordered_lessons_with_common_contract(reviewed_chemistry_documents):
    lessons=reviewed_chemistry_documents[224:229]
    assert [l['topic_id'] for l in lessons]==TOPICS
    assert [l['sequence'] for l in lessons]==list(range(31,36))
    assert sum(len(l['content']['cards']) for l in lessons)==57
    assert Counter(q['response_kind'] for l in lessons for q in l['assessments'])=={
        'concept_selection':20,'short_text':14,'numeric_value':26,'chemical_formula':4,'chemical_equation':10}
    assert all(l['content']['examples'] for l in lessons)
    assert all(not b['course_ready'] for b in load_catalog()['books'])
    assert all(q['response_kind'] not in {'chemical_formula','chemical_equation'} for q in lessons[1]['assessments'])

@pytest.mark.parametrize('topic',TOPICS)
def test_batch44_scoped_source_review_cannot_disappear(topic):
    c=deepcopy(load_catalog())
    next(r for r in c['books'][3]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)

@pytest.mark.parametrize('n,fid,value,error',[
    (31,'repeat','Bir molekula kraxmaldan 200 mol glukoza','polymer_particle_count_is_not_moles'),
    (32,'term','Nitrolash har doim bitta sof mahsulot','unconditional_nitration_product_claim_is_withheld'),
    (33,'isomers','C4H11N jami faqat 4 ta izomer','primary_amine_examples_are_not_all_amine_isomers'),
    (34,'biuret','Har qanday dipeptid musbat biuret beradi','universal_dipeptide_biuret_claim_is_withheld'),
    (35,'pvc','PVC hech qachon suyuqlanmaydi va yonmaydi','absolute_pvc_thermal_claim_is_withheld')])
def test_batch44_withheld_key_is_rejected(n,fid,value,error):
    l=deepcopy(read_json(DIRECTORY/f'grade10_paragraph{n:02}.json'))
    l['facts'][fid]['verified_answers'].append(value)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade10_paragraph{n:02}_review.json'))

@pytest.mark.parametrize('n,fid,expected,value,code',[
    (31,'repeat','200','200','correct'),(31,'fermentation','460','460','correct'),
    (31,'mixture','1.5','1,5','correct'),(31,'variant','2','2','correct'),
    (32,'primary','1','1','correct'),(32,'tertiary','3','3','correct'),
    (32,'complex','8','8','correct'),(32,'aromatic','1','1','correct'),
    (33,'triphenyl','36','36','correct'),(33,'triphenyl','9','9','correct'),
    (33,'triphenyl','45','45','correct'),(33,'mass','245','245','correct'),
    (34,'first','75','75','correct'),(34,'second','89','89','correct'),
    (34,'bonds','13','13','correct'),(34,'bonds','14','14','correct'),
    (34,'trigly','3C2H5NO2=C6H11N3O4+2H2O','3C2H5NO2=C6H11N3O4+H2O','atom_imbalance'),
    (35,'isobutylene','1005','1.005e3','correct'),
    (35,'chloridemass','1000','1000','correct'),(35,'chloridemass','61250','61250','correct')])
def test_batch44_exact_common_grader(n,fid,expected,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch10-paragraph{n:02}')
    q=next(q for q in l['assessments'] if fid in q['fact_ids'] and q['grading_spec']['expected']==expected)
    assert grade_answer(q['grading_spec'],{'value':value})==code

def test_batch44_model_arithmetic_and_graph_counts_are_recomputed():
    assert 32400/162==200
    assert Decimal('2.5')*2*2*46==460
    assert Decimal(720)/180-Decimal('2.5')==Decimal('1.5')
    sigma=3*(6+5+1);pi=3*3
    assert (sigma,pi,sigma+pi)==(36,9,45)
    assert 18*12+15+14==245
    assert Decimal('37.5')/(Decimal(9)/18)==75
    assert Decimal('26.7')/(Decimal('5.4')/18)==89
    assert 6+7==13 and 6+7+1==14
    assert 56280/56==1005 and 550*56==30800
    assert 13500/54==250 and 1020*54==55080
    assert Decimal(62500)/Decimal('62.5')==1000
    assert 980*Decimal('62.5')==61250

def test_batch44_prior_mass_proofs_and_explicit_model_scope(reviewed_chemistry_documents):
    rows={l['topic_id']:l for l in reviewed_chemistry_documents}
    for n,fid,topic,page in [(31,'repeat','ch8-paragraph01',7),(33,'mass','ch8-paragraph05',29),(34,'first','ch8-paragraph01',7),(35,'chloridemass','ch8-paragraph05',27)]:
        proof=next(r for r in rows[f'ch10-paragraph{n:02}']['facts'][fid]['source_refs'] if r['topic_id']==topic and r['printed_pages']==[page])
        assert proof['file_name']=='kimyo_8_uzb.pdf' and proof['printed_pages']==proof['pdf_pages']
    assert 'ch8-chapter06' not in rows['ch10-paragraph33'].get('source_context_ids',[])
    assert 'ideal' in rows['ch10-paragraph35']['facts']['chloridemass']['claim'].lower()
    assert 'yagona' in rows['ch10-paragraph34']['facts']['second']['claim']

def test_batch44_preserves224_and_adds100xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:224]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=4480
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8,9)}
    g10=client.get(PREFIX+'/catalog?grade=10').json()['lessons']
    assert all(l['state']=='completed' for l in g10[:30])
    assert g10[30]['state']=='available' and all(l['state']=='locked' for l in g10[31:])
    for l in docs[224:229]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==4580
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==229
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    current=client.get(PREFIX+'/catalog?grade=10').json()['lessons']
    assert all(l['state']=='completed' for l in current[:35])
    if len(current)>35:assert current[35]['state']=='available'
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
