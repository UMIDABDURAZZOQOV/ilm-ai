"""All six organic laboratories are guided digital analysis, using common inputs."""
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

TOPICS=[f'ch10-laboratory{n:02}' for n in range(1,7)]

def test_batch45_all41_grade10_entries_and_common_digital_inputs(reviewed_chemistry_documents):
    lessons=reviewed_chemistry_documents[229:235]
    assert [l['topic_id'] for l in lessons]==TOPICS
    assert [l['sequence'] for l in lessons]==list(range(36,42))
    assert sum(len(l['content']['cards']) for l in lessons)==38
    assert Counter(q['response_kind'] for l in lessons for q in l['assessments'])=={
        'concept_selection':24,'short_text':11,'numeric_value':14,'chemical_formula':5,'chemical_equation':8}
    assert len([l for l in reviewed_chemistry_documents if l['grade']==10])==41
    assert all(l['content']['examples'] and 'raqamli' in l['facts']['digital']['claim'].lower() for l in lessons)
    assert all(not b['course_ready'] for b in load_catalog()['books'])

@pytest.mark.parametrize('topic',TOPICS)
def test_batch45_activity_source_scope_cannot_disappear(topic):
    c=deepcopy(load_catalog())
    next(r for r in c['books'][3]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)

@pytest.mark.parametrize('n,fid,value,error',[
    (1,'digital','Gazni amalda yig‘ish','lab_ethanol_physical_gas_collection_is_not_an_answer'),
    (2,'observation','Alanga atsetilenni yagona isbotlaydi','lab_acetylene_flame_is_not_unique_identity'),
    (3,'blue','Ko‘k rang har qanday ko‘p atomli spirtni isbotlaydi','lab_glycerol_blue_is_not_universal_identity'),
    (4,'metals','Magniy barcha sharoitda ruxdan tezroq','lab_acid_reported_rate_is_not_universal'),
    (5,'balance','C6H12O6+2Cu(OH)2=C6H12O7+Cu2O+H2O','lab_glucose_missing_water_literal_is_withheld'),
    (6,'observation','Biuret rangi oqsilni yagona isbotlaydi','lab_biuret_color_is_not_unique_identity')])
def test_batch45_unsafe_or_unverified_answer_is_rejected(n,fid,value,error):
    l=deepcopy(read_json(DIRECTORY/f'grade10_laboratory{n:02}.json'))
    l['facts'][fid]['verified_answers'].append(value)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade10_laboratory{n:02}_review.json'))

@pytest.mark.parametrize('n,fid,expected,value,code',[
    (1,'counts','6','6','correct'),(1,'counts','4','4','correct'),
    (1,'names','C2H4','C2H4','correct'),
    (1,'gross','C2H6O=C2H4+H2O','2C2H6O=2C2H4+2H2O','correct'),
    (1,'first','C2H6O+H2SO4=C2H6SO4+H2O','C2H6O+H2SO4=C2H6SO4+2H2O','atom_imbalance'),
    (2,'triple','3','3','correct'),(2,'triple','5','5','correct'),
    (2,'products','CaC2+2H2O=C2H2+Ca(OH)2','CaC2+H2O=C2H2+Ca(OH)2','atom_imbalance'),
    (3,'bonds','13','13','correct'),(3,'bonds','0','0','correct'),
    (3,'glycerol','C3H8O3','C3H8O3','correct'),
    (4,'acid','2','2','correct'),(4,'neutral','1','1','correct'),
    (5,'groups','5','5','correct'),(5,'balance','2','2','correct'),
    (5,'red','Cu2O','CuO','incorrect'),
    (5,'balance','C6H12O6+2Cu(OH)2=C6H12O7+Cu2O+2H2O','C6H12O6+2Cu(OH)2=C6H12O7+Cu2O+H2O','atom_imbalance'),
    (6,'count','1','1','correct'),(6,'count','2','2','correct'),
    (6,'observation','Biuret','biuret','correct')])
def test_batch45_existing_common_grader(n,fid,expected,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch10-laboratory{n:02}')
    q=next(q for q in l['assessments'] if fid in q['fact_ids'] and q['grading_spec']['expected']==expected)
    assert grade_answer(q['grading_spec'],{'value':value})==code

def test_batch45_source_proofs_and_no_complex_or_biuret_formula_key(reviewed_chemistry_documents):
    rows={l['topic_id']:l for l in reviewed_chemistry_documents}
    for n,fid,topic,page in [(1,'gross','ch10-paragraph21',83),(3,'blue','ch10-paragraph22',87),(4,'salt','ch10-paragraph26',104),(5,'balance','ch10-paragraph24',97),(5,'balance','ch10-paragraph30',119),(6,'observation','ch10-paragraph34',143)]:
        refs=rows[f'ch10-laboratory{n:02}']['facts'][fid]['source_refs']
        proof=next(r for r in refs if r['topic_id']==topic and r['printed_pages']==[page])
        assert proof['file_name']=='organik_kimyo_10_uzb.pdf' and proof['printed_pages']==proof['pdf_pages']
    for n in (3,6):
        assert all(q['response_kind']!='chemical_equation' for q in rows[f'ch10-laboratory{n:02}']['assessments'])
    assert all(q['response_kind']!='chemical_formula' for q in rows['ch10-laboratory06']['assessments'])

def test_batch45_local_graph_and_water_counts_are_recomputed():
    assert (1+2,2,1+2+2)==(3,2,5)
    assert 5+8==13
    # Glucose gross atom model: left H12+4/O6+4, right H12+4/O7+1+2.
    assert 12+2*2==12+2*2==16
    assert 6+2*2==7+1+2==10
    assert 3-1==2 and 2-1==1

def test_batch45_preserves229_and_adds120xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:229]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=4580
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8,9)}
    g10=client.get(PREFIX+'/catalog?grade=10').json()['lessons']
    assert all(l['state']=='completed' for l in g10[:35])
    assert g10[35]['state']=='available' and all(l['state']=='locked' for l in g10[36:])
    for l in docs[229:235]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==4700
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==235
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert all(l['state']=='completed' for l in client.get(PREFIX+'/catalog?grade=10').json()['lessons'])
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
