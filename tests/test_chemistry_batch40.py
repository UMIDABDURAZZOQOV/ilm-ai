"""Sourced alkene,diene and alkyne tasks reuse finite common response kinds."""
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
TOPICS=[f'ch10-paragraph{n:02}' for n in range(11,16)]

def test_batch40_source_order_and_bounded_organic_scope():
    lessons=load_lessons()[204:209]
    assert [l['topic_id'] for l in lessons]==TOPICS
    assert [l['sequence'] for l in lessons]==list(range(11,16))
    assert sum(len(l['content']['cards']) for l in lessons)==59
    assert Counter(q['response_kind'] for l in lessons for q in l['assessments'])=={
        'concept_selection':20,'short_text':11,'numeric_value':27,'chemical_formula':4,'chemical_equation':17}
    assert all(l['content']['examples'] for l in lessons)
    assert all(not b['course_ready'] for b in load_catalog()['books'])
    assert lessons[1]['facts']['ez']['source_refs'][0]['printed_pages']==[48]
    assert all(q['response_kind'] in {'concept_selection','short_text'} for q in lessons[1]['assessments'] if q['fact_ids']==['ez'])
    assert any(r['printed_pages']==[54] for r in lessons[3]['facts']['dehydrogenation']['source_refs'])
    assert all(r['printed_pages'][0]<=61 for r in lessons[4]['source_refs'] if r['book_id']==lessons[4]['book_id'])

@pytest.mark.parametrize('topic',TOPICS)
def test_batch40_required_source_scope_cannot_disappear(topic):
    catalog=deepcopy(load_catalog())
    next(r for r in catalog['books'][3]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(catalog)

@pytest.mark.parametrize('n,fid,value,error',[
    (11,'family','CnH2n doim faqat alken','family_composition'),
    (12,'ez','E/Z ustunligi faqat molekulyar massa bilan','unreviewed_mass_only_ez'),
    (13,'physical','Barcha buten izomerlari n.sh.da gaz','unqualified_all_butene'),
    (14,'dehydrogenation','H2C–CH–CH=CH2','missing_diene_bond'),
    (15,'worked','Pentin yagona tuzilish','alkyne_gas_ratio')])
def test_batch40_withheld_key_is_rejected(n,fid,value,error):
    l=deepcopy(read_json(DIRECTORY/f'grade10_paragraph{n:02}.json'))
    l['facts'][fid]['verified_answers'].append(value)
    with pytest.raises(ValueError,match=error):
        validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade10_paragraph{n:02}_review.json'))

@pytest.mark.parametrize('n,fid,expected,value,code',[
    (11,'dimethyl','7','7','correct'),(11,'halogen','9','9','correct'),(11,'mass','6','6','correct'),
    (12,'ez','E','e','correct'),(12,'worked','28','28','correct'),
    (12,'newmass','84','84','correct'),(12,'gas','63','63','correct'),
    (13,'repeat','100','100','correct'),(13,'repeat','200','200','correct'),
    (13,'gain_propen','17.6','17,6','correct'),(13,'gain_butene','29','29','correct'),
    (13,'oxidation','3C2H4+2KMnO4+4H2O=3C2H6O2+2MnO2+2KOH','3C2H4+2KMnO4+4H2O=3C2H6O2+2MnO2+2KOH','correct'),
    (14,'butanemass','31.9','31,9','correct'),
    (14,'isoprene','57.6','5.76e1','correct'),(14,'isoprene','21.6','21,6','correct'),
    (14,'two_bromine','C4H6+2Br2=C4H6Br4','C4H6+Br2=C4H6Br4','atom_imbalance'),
    (15,'mass','52','52','correct'),(15,'chainmass','0.44','0,44','correct'),
    (15,'yield','1560','1.56e3','correct'),
    (15,'newratio','C6H10','C6H10','correct'),(15,'worked','3','3','correct'),
    (15,'hydration','C2H2+H2O=CH3CHO','C2H2+H2O=CH3CHO','correct')])
def test_batch40_existing_grader(n,fid,expected,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch10-paragraph{n:02}')
    q=next(q for q in l['assessments'] if fid in q['fact_ids'] and q['grading_spec']['expected']==expected)
    assert grade_answer(q['grading_spec'],{'value':value})==code

def test_batch40_preserves204_and_awards100xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:204]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=4080
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8,9)}
    g10=client.get(PREFIX+'/catalog?grade=10').json()
    assert all(l['state']=='completed' for l in g10['lessons'][:10])
    assert g10['lessons'][10]['state']=='available' and all(l['state']=='locked' for l in g10['lessons'][11:])
    for l in docs[204:209]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==4180
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==209
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert all(l['state']=='completed' for l in client.get(PREFIX+'/catalog?grade=10').json()['lessons'][:15])
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
