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

TOPICS=[f'ch9-laboratory{n:02}' for n in range(12,18)]


def test_batch37_source_order_and_shared_types():
    lessons=load_lessons()[188:194]
    assert [l['topic_id'] for l in lessons]==TOPICS
    assert [l['sequence'] for l in lessons]==list(range(56,62))
    assert sum(len(l['content']['cards']) for l in lessons)==46
    assert Counter(q['response_kind'] for l in lessons for q in l['assessments'])=={
        'concept_selection':24,'short_text':12,'numeric_value':18,'chemical_formula':6,'chemical_equation':16}
    assert all(l['content']['examples'] for l in lessons)
    assert all(not b['course_ready'] for b in load_catalog()['books'])
    assert [l['topic_id'] for l in load_lessons() if l['grade']==9]==[r['id'] for r in load_catalog()['books'][2]['records'] if r['kind'] in {'paragraph','laboratory','practical'}]
    assert all(q['response_kind']=='concept_selection' for l in lessons for q in l['assessments'] if '[' in q['grading_spec']['verified_answer'])



@pytest.mark.parametrize('topic',TOPICS)
def test_batch37_review_cannot_disappear(topic):
    catalog=deepcopy(load_catalog())
    next(r for r in catalog['books'][2]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(catalog)


@pytest.mark.parametrize('n,fid,value,error',[
    (13,'volume','Zichliksiz aniq massa','missing_solution_densities'),
    (16,'blueform','Yagona haqiqiy faza','source_complex_notation'),
    (17,'rate','Teng massa doim teng tezlik','total_gas_amount')])
def test_batch37_held_or_unqualified_key_is_rejected(n,fid,value,error):
    l=deepcopy(read_json(DIRECTORY/f'grade9_laboratory{n:02}.json'))
    l['facts'][fid]['verified_answers'].append(value)
    with pytest.raises(ValueError,match=error):
        validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade9_laboratory{n:02}_review.json'))


@pytest.mark.parametrize('n,fid,expected,value,code',[
    (12,'formation','Cu(OH)2','Cu(OH)2','correct'),
    (12,'acid','Cu(OH)2+2HCl=CuCl2+2H2O','Cu(OH)2+2HCl=CuCl2+H2O','atom_imbalance'),
    (12,'volume','1.639','1,639','correct'),
    (12,'volume','1.639','1.639344','incorrect'),
    (12,'amount','0.005','5e-3','correct'),
    (13,'acid','Zn(OH)2+H2SO4=ZnSO4+2H2O','Zn(OH)2+H2SO4=ZnSO4+H2O','atom_imbalance'),
    (13,'ratio','0.04','0,04','correct'),(13,'base','4','4','correct'),
    (14,'redox','K2Cr2O7+3Na2SO3+4H2SO4=Cr2(SO4)3+3Na2SO4+K2SO4+4H2O','K2Cr2O7+3Na2SO3+4H2SO4=Cr2(SO4)3+3Na2SO4+K2SO4+4H2O','correct'),
    (14,'electrons','6','6','correct'),(14,'ratio','0.06','6e-2','correct'),
    (15,'ii','Fe(OH)2','Fe(OH)3','incorrect'),
    (15,'iii','Fe(OH)3','Fe(OH)3','correct'),
    (15,'air','4Fe(OH)2+2H2O+O2=4Fe(OH)3','4Fe(OH)2+2H2O+O2=4Fe(OH)3','correct'),
    (15,'ratio','0.04','0.04','correct'),(15,'ratio','0.06','0.06','correct'),
    (16,'bluecount','7','7','correct'),(16,'bluecount','18','18','correct'),
    (16,'sulfurcount','3','3','correct'),
    (17,'volumea','0.388','0,388','correct'),
    (17,'volumeb','0.396','3.96e-1','correct'),
    (17,'volumeb','0.008','8e-3','correct')])
def test_batch37_existing_grader(n,fid,expected,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch9-laboratory{n:02}')
    q=next(q for q in l['assessments'] if fid in q['fact_ids'] and q['grading_spec']['expected']==expected)
    assert grade_answer(q['grading_spec'],{'value':value})==code


def test_batch37_preserves188_and_awards120xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:188]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=3760
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8)}
    g9=client.get(PREFIX+'/catalog?grade=9').json()['lessons']
    assert g9[55]['state']=='available' and all(l['state']=='locked' for l in g9[56:])
    for l in docs[188:194]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==3880
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==194
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert all(l['state']=='completed' for l in client.get(PREFIX+'/catalog?grade=9').json()['lessons'][:61])
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
