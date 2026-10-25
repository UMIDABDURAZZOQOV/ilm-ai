"""First scan-reviewed organic lessons preserve the common assessment contract."""
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

TOPICS=[f'ch10-paragraph{n:02}' for n in range(1,6)]

def test_batch38_scan_sources_and_organic_response_scope():
    lessons=load_lessons()[194:199]
    assert [l['topic_id'] for l in lessons]==TOPICS
    assert [l['sequence'] for l in lessons]==list(range(1,6))
    assert sum(len(l['content']['cards']) for l in lessons)==58
    assert Counter(q['response_kind'] for l in lessons for q in l['assessments'])=={
        'concept_selection':22,'short_text':15,'numeric_value':23,'chemical_formula':5,'chemical_equation':3}
    assert all(l['content']['examples'] for l in lessons)
    assert all(not b['course_ready'] for b in load_catalog()['books'])
    for l in lessons:
        review=read_json(DIRECTORY/f"grade10_paragraph{l['sequence']:02}_review.json")
        assert review['review_method']=='original_page_images'
        assert all(r['verification']=='page_image_reviewed' and r['page_image_sha256'] for r in review['source_pages'])
    # Connectivity is assessed by the shown structure,never molecular equivalence.
    p2=lessons[1]
    assert [q['response_kind'] for q in p2['assessments'] if q['fact_ids']==['sodium']]==['concept_selection']
    assert all(q['response_kind'] in {'concept_selection','short_text','numeric_value'} for q in lessons[2]['assessments'])
    p5=lessons[4]
    assert any(r['topic_id']=='ch8-paragraph01' and r['file_name']=='kimyo_8_uzb.pdf' and r['printed_pages']==[7] for r in p5['facts']['fraction']['source_refs'])
    assert all(r['printed_pages'][0]<=25 for r in p5['source_refs'] if r['book_id']==p5['book_id'])

@pytest.mark.parametrize('topic',TOPICS)
def test_batch38_editorial_scope_cannot_disappear(topic):
    catalog=deepcopy(load_catalog())
    next(r for r in catalog['books'][3]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(catalog)

@pytest.mark.parametrize('n,fid,value,error',[
    (1,'scope','Barcha organik moddalar noelektrolit','organic_generalizations'),
    (2,'oxidation','HCOOH — sirka kislotasi','misprinted_formic'),
    (3,'positiongroup','CH3CHClCH2CH2','missing_terminal_hydrogen'),
    (4,'addition','Faqat organik moddalar polimerlanadi','polymerization_universality'),
    (5,'forward','82.75','copied_percentage_precision')])
def test_batch38_withheld_copied_key_is_rejected(n,fid,value,error):
    l=deepcopy(read_json(DIRECTORY/f'grade10_paragraph{n:02}.json'))
    l['facts'][fid]['verified_answers'].append(value)
    with pytest.raises(ValueError,match=error):
        validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade10_paragraph{n:02}_review.json'))

@pytest.mark.parametrize('n,fid,expected,value,code',[
    (1,'ratio','0.60','0,6','correct'),(1,'ratio','0.30','3e-1','correct'),
    (1,'combustion','CH4+2O2=CO2+2H2O','CH4+O2=CO2+H2O','atom_imbalance'),
    (1,'butane','C4H10','C4H10','correct'),
    (2,'sodiumratio','0.20','0,2','correct'),
    (2,'oxidation','-2','-2','correct'),(2,'oxidation','0','0','correct'),
    (2,'count','18','18','correct'),(2,'sum','0','0','correct'),
    (3,'pentane','3','3','correct'),(3,'counts','5','5','correct'),
    (3,'cis','Trans','trans','correct'),
    (4,'nitration','3','3','correct'),
    (4,'substitution','C6H6+Cl2=C6H5Cl+HCl','C6H6+Cl2=C6H5Cl+HCl','correct'),
    (4,'addition','C2H4+H2=C2H6','C2H4+H2=C2H6','correct'),
    (5,'triethyl','7','7','correct'),(5,'bonds','22','22','correct'),
    (5,'bonds','25','25','correct'),
    (5,'fraction','81.818','81,818','correct'),
    (5,'fraction','81.818','81.818181','incorrect'),
    (5,'forward','82.759','8.2759e1','correct'),
    (5,'forward','82.759','82.75','incorrect')])
def test_batch38_existing_grader(n,fid,expected,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch10-paragraph{n:02}')
    q=next(q for q in l['assessments'] if fid in q['fact_ids'] and q['grading_spec']['expected']==expected)
    assert grade_answer(q['grading_spec'],{'value':value})==code

def test_batch38_preserves194_and_awards100xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:194]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=3880
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8,9)}
    g10=client.get(PREFIX+'/catalog?grade=10').json()
    assert g10['available_grades']==[7,8,9,10]
    assert g10['lessons'][0]['state']=='available' and all(l['state']=='locked' for l in g10['lessons'][1:])
    for l in docs[194:199]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==3980
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==199
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    current=client.get(PREFIX+'/catalog?grade=10').json()['lessons']
    assert all(l['state']=='completed' for l in current[:5])
    if len(current)>5:assert current[5]['state']=='available'
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
