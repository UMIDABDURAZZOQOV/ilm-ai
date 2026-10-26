"""Original-image sourced aromatic/oxygen compound tasks preserve common contracts."""
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

TOPICS=[f'ch10-paragraph{n:02}' for n in range(16,26)]

def test_batch41_ten_source_ordered_lessons_and_shared_response_contract(reviewed_chemistry_documents):
    lessons=reviewed_chemistry_documents[209:219]
    assert [l['topic_id'] for l in lessons]==TOPICS
    assert [l['sequence'] for l in lessons]==list(range(16,26))
    assert sum(len(l['content']['cards']) for l in lessons)==123
    assert Counter(q['response_kind'] for l in lessons for q in l['assessments'])=={
        'concept_selection':40,'short_text':26,'numeric_value':58,'chemical_formula':7,'chemical_equation':34}
    assert all(l['content']['examples'] for l in lessons)
    assert all(not b['course_ready'] for b in load_catalog()['books'])
    assert all(q['response_kind']!='chemical_equation' for l in lessons for q in l['assessments'] if q['fact_ids'] in [['nitro'],['esterclass'],['nitrated']])

@pytest.mark.parametrize('topic',TOPICS)
def test_batch41_source_review_scopes_cannot_disappear(topic):
    c=deepcopy(load_catalog())
    next(r for r in c['books'][3]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)

@pytest.mark.parametrize('n,fid,value,error',[(16, 'oxidation', 'Toluol har doim faqat tribrommahsulot', 'arene_sole_product_without_conditions_is_withheld'), (17, 'tetrahedral', '109.28', 'decimal_angle_copy_requires_review'), (18, 'residue', 'Parafin va vazelin aynan bir modda', 'petroleum_product_synonym_error_is_withheld'), (19, 'worked', '22.4/67.2=3', 'reciprocal_volume_division_cannot_be_a_key'), (20, 'names', '3-metilpentanon-1', 'terminal_ketone_misprint_is_withheld'), (21, 'onewater', '140°C barcha spirtlar uchun aniq chegara', 'universal_dehydration_threshold_is_withheld'), (22, 'polyol', 'Bir C da ikki OH bo‘lishi mutlaqo mumkin emas', 'absolute_gemdiol_impossibility_is_withheld'), (23, 'violet', 'Fe(C6H5O)3 har doim yagona kompleks', 'phenol_complex_schematic_is_not_unique_speciation'), (24, 'branched', '2-metilpropan', 'aldehyde_wrong_alkane_suffix_is_withheld'), (25, 'secondamount', 'C6H12O yagona keton tuzilishi', 'ketone_amount_does_not_determine_unique_graph')])
def test_batch41_withheld_literal_or_universal_key_is_rejected(n,fid,value,error):
    l=deepcopy(read_json(DIRECTORY/f'grade10_paragraph{n:02}.json'))
    l['facts'][fid]['verified_answers'].append(value)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade10_paragraph{n:02}_review.json'))

@pytest.mark.parametrize('n,fid,expected,value,code',[
    (16,'yield','23.4','23,4','correct'),(16,'yield','80','80','correct'),
    (16,'trimer','3C2H2=C6H6','2C2H2=C6H6','atom_imbalance'),
    (17,'planar','120','120','correct'),(17,'linear','180','180','correct'),
    (17,'pentyne','12','12','correct'),(17,'hexene','17','17','correct'),
    (17,'diene','4','4','correct'),(17,'hexyne','34','34','correct'),
    (17,'dimethyl','36','36','correct'),
    (18,'cracking','16','16','correct'),
    (19,'oxygen','11','11','correct'),(19,'oxygen','18','18','correct'),
    (19,'amount','44.8','44,8','correct'),(19,'amount','39','39','correct'),
    (20,'hydrationmass','30','30','correct'),(20,'estermass','18.4','18,4','correct'),
    (21,'sodiumamount','3.36','3,36','correct'),(21,'air','537.6','5.376e2','correct'),
    (22,'bonds','9','9','correct'),(22,'bonds','13','13','correct'),
    (22,'amount','16.8','16,8','correct'),(22,'mass','127.2','127,2','correct'),
    (22,'glycerolsodium','2C3H8O3+6Na=2C3H5O3Na3+3H2','2C3H8O3+6Na=2C3H5O3Na3+2H2','atom_imbalance'),
    (23,'benzylbonds','16','16','correct'),(23,'benzylbonds','16','17','incorrect'),
    (23,'benzylbonds','19','19','correct'),(23,'benzylbonds','19','20','incorrect'),
    (24,'silveramount','0.3','3e-1','correct'),(24,'silveramount','44','44','correct'),
    (24,'copperamount','36.8','36,8','correct'),
    (25,'firstamount','72','72','correct'),(25,'secondamount','100','100','correct'),
    (25,'secondamount','C6H12O','C6H12O','correct')])
def test_batch41_exact_common_grader(n,fid,expected,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch10-paragraph{n:02}')
    q=next(q for q in l['assessments'] if fid in q['fact_ids'] and q['grading_spec']['expected']==expected)
    assert grade_answer(q['grading_spec'],{'value':value})==code

def test_batch41_critical_counts_and_decimal_math_are_independently_recomputed(reviewed_chemistry_documents):
    rows={l['topic_id']:l for l in reviewed_chemistry_documents}
    f=rows['ch10-paragraph23']['facts']['benzylbonds']
    sigma=6+1+1+8
    assert sigma==16 and sigma+3==19
    assert {'16','19'}<=set(f['verified_answers']) and not {'17','20'}&set(f['verified_answers'])
    oxygen=Decimal(92)*Decimal('0.8')/46*3*Decimal('22.4')
    assert oxygen/Decimal('0.20')==Decimal('537.6')
    assert Decimal('1.2')*(2*12+4+2*16+2*23)==Decimal('127.2')
    assert Decimal('115.2')/(2*64+16)*46==Decimal('36.8')

def test_batch41_mass_proofs_keep_original_books_and_pages(reviewed_chemistry_documents):
    rows={l['topic_id']:l for l in reviewed_chemistry_documents}
    for n,fid,topic,page in [(22,'mass','ch8-paragraph05',27),(24,'silveramount','ch8-paragraph13',59),(24,'copperamount','ch8-practical01',127),(25,'secondamount','ch8-paragraph26',114)]:
        refs=rows[f'ch10-paragraph{n:02}']['facts'][fid]['source_refs']
        proof=next(r for r in refs if r['topic_id']==topic and r['printed_pages']==[page])
        assert proof['file_name']=='kimyo_8_uzb.pdf' and proof['printed_pages']==proof['pdf_pages']
    assert all(r['printed_pages']!=[75] for r in rows['ch10-paragraph19']['facts']['worked']['source_refs'])

def test_batch41_preserves209_and_awards200xp_only_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:209]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=4180
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8,9)}
    g10=client.get(PREFIX+'/catalog?grade=10').json()['lessons']
    assert all(l['state']=='completed' for l in g10[:15])
    assert g10[15]['state']=='available' and all(l['state']=='locked' for l in g10[16:])
    for l in docs[209:219]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==4380
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==219
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    current=client.get(PREFIX+'/catalog?grade=10').json()['lessons']
    assert all(l['state']=='completed' for l in current[:25])
    if len(current)>25:assert current[25]['state']=='available'
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
