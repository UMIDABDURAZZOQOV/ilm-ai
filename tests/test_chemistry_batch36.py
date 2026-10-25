"""Activity conditions and known source contradictions remain visible and bounded."""
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

TOPICS=[f'ch9-laboratory{n:02}' for n in range(5,12)]


def test_batch36_source_order_and_shared_types():
    lessons=load_lessons()[181:188]
    assert [l['topic_id'] for l in lessons]==TOPICS
    assert [l['sequence'] for l in lessons]==list(range(49,56))
    assert sum(len(l['content']['cards']) for l in lessons)==53
    assert Counter(q['response_kind'] for l in lessons for q in l['assessments'])=={
        'concept_selection':28,'short_text':14,'numeric_value':18,'chemical_formula':5,'chemical_equation':9}
    assert all(l['content']['examples'] for l in lessons)
    assert all(not b['course_ready'] for b in load_catalog()['books'])
    anode=lessons[2]['facts']['soluble']['source_refs']
    assert any(r['topic_id']=='ch9-paragraph19' and r['printed_pages']==[86] for r in anode)
    assert not any(q['fact_ids']==['starch'] for q in lessons[2]['assessments'])
    assert all(q['response_kind']=='concept_selection' for l in lessons for q in l['assessments'] if '[' in q['grading_spec']['verified_answer'])


@pytest.mark.parametrize('topic',TOPICS)
def test_batch36_review_cannot_disappear(topic):
    catalog=deepcopy(load_catalog())
    next(r for r in catalog['books'][2]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(catalog)


@pytest.mark.parametrize('n,fid,value,error',[
    (7,'soluble','Cu anodda doim Cl2','unqualified_copper_anode_chlorine'),
    (8,'base','2Al+2NaOH+6H2O=2Na[Al(OH)4]+H2','unbalanced_aluminium_hydrogen_copy'),
    (10,'amounts','Barcha Al doim cho‘kadi','drop_counts_cannot_certify'),
    (11,'third','AlCl3 doim to‘liq gidrolizlanadi','formal_hydrolysis_is_not_unconditional')])
def test_batch36_held_or_unqualified_key_is_rejected(n,fid,value,error):
    l=deepcopy(read_json(DIRECTORY/f'grade9_laboratory{n:02}.json'))
    l['facts'][fid]['verified_answers'].append(value)
    with pytest.raises(ValueError,match=error):
        validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade9_laboratory{n:02}_review.json'))


@pytest.mark.parametrize('n,fid,expected,value,code',[
    (5,'mass','190','190','correct'),(5,'nickelin','32','32','correct'),
    (6,'lead','Siqib chiqarmaydi','Siqib chiqarmaydi','correct'),
    (6,'silver','Cu+2AgNO3=Cu(NO3)2+2Ag','Cu+AgNO3=Cu(NO3)2+Ag','atom_imbalance'),
    (6,'amount','0.10','0,1','correct'),
    (7,'cathode','2','2','correct'),(7,'ratio','0.05','5e-2','correct'),
    (7,'balance','2KI+2H2O=2KOH+H2+I2','2KI+2H2O=2KOH+H2+I2','correct'),
    (8,'hydrogen','14','14','correct'),(8,'ratio','0.30','3e-1','correct'),
    (8,'ratio','0.60','0,60','correct'),
    (9,'density','26.98','26,98','correct'),(9,'mass','47.5','47.5','correct'),
    (9,'mass','0.25','0,25','correct'),
    (10,'amounts','0.03','0.03','correct'),(10,'amounts','0.01','0.01','correct'),
    (10,'ioncount','0','0','correct'),
    (11,'first','AlCl3+H2O=Al(OH)Cl2+HCl','AlCl3+H2O=Al(OH)Cl2+HCl','correct'),
    (11,'third','Al(OH)2Cl+H2O=Al(OH)3+HCl','Al(OH)2Cl+H2O=Al(OH)3+HCl','correct'),
    (11,'second','2','2','correct'),(11,'count','3','3','correct')])
def test_batch36_existing_grader(n,fid,expected,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch9-laboratory{n:02}')
    q=next(q for q in l['assessments'] if fid in q['fact_ids'] and q['grading_spec']['expected']==expected)
    assert grade_answer(q['grading_spec'],{'value':value})==code


def test_batch36_preserves181_and_awards140xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:181]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=3620
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8)}
    g9=client.get(PREFIX+'/catalog?grade=9').json()['lessons']
    assert g9[48]['state']=='available' and all(l['state']=='locked' for l in g9[49:])
    for l in docs[181:188]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==3760
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==188
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert all(l['state']=='completed' for l in client.get(PREFIX+'/catalog?grade=9').json()['lessons'][:55])
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
