"""Grade8 uses the same sourced learning contract and independent progression."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,readiness,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_grade8_first_five_source_order_complete_page_identity_and_kind_coverage():
    docs=load_lessons()[74:79]
    assert [d['topic_id'] for d in docs]==[f'ch8-paragraph{n:02}' for n in range(1,6)]
    assert [d['sequence'] for d in docs]==list(range(1,6))
    assert docs[0]['prerequisite_ids']==[]
    assert [d['prerequisite_ids'] for d in docs[1:]]==[[d['topic_id']] for d in docs[:-1]]
    assert sum(len(d['content']['cards']) for d in docs)==44
    assert sum(len(d['assessments']) for d in docs)==68
    assert {q['response_kind'] for d in docs for q in d['assessments']}=={'concept_selection','short_text','numeric_value','chemical_formula','chemical_equation'}
    for d in docs:
        assert d['grade']==8 and d['book_id']=='chemistry-8-uz-2019'
        for f in d['facts'].values():
            for r in f['source_refs']:
                assert r['pdf_pages']==r['printed_pages'] and r['regions']==['full']
    state=next(s for s in readiness(load_catalog(),load_lessons()) if s['grade']==8)
    assert state['implemented_lessons']>=5 and state['pending_source_review_ids'] and not state['course_ready']


@pytest.mark.parametrize('n',range(1,6))
def test_new_grade8_source_issues_cannot_be_silently_removed(n):
    c=deepcopy(load_catalog());next(r for r in c['books'][1]['records'] if r['id']==f'ch8-paragraph{n:02}').pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


@pytest.mark.parametrize('n,fid,value,error',[
 (1,'molar','1 mol = 98 g','unresolved_mol_mass_identity'),
 (2,'mass','43.25','unresolved_grade8_rounding'),
 (4,'water','2Na+O2=Na2O2','unresolved_alkali_oxygen'),
 (4,'water','4Na+O2=2Na2O2','unresolved_alkali_oxygen'),
 (5,'oxides','N2O5 valentligi IV','unresolved_nitrogen_valence'),
 (5,'oxides','N₂O₅ valentligi V','unresolved_nitrogen_valence')])
def test_held_source_premises_and_silent_corrections_are_rejected(n,fid,value,error):
    l=deepcopy(load_lessons()[73+n]);r=read_json(DIRECTORY/f'grade8_paragraph{n:02}_review.json')
    l['facts'][fid]['verified_answers'].append(value)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('n,qn,value,code',[
 (1,8,'H₂SO₄','correct'),(1,12,'0,5','correct'),
 (2,11,'AlCl3+3NaOH=Al(OH)3+3NaCl','correct'),
 (2,14,'2NaOH+H2SO4=Na2SO4+2H2O','incorrect_species'),
 (2,14,'NaOH+H2SO4=NaHSO4+H2O','correct'),
 (2,18,'60','correct'),(3,8,'Zn(OH)2+HCl=ZnCl2+H2O','atom_imbalance'),
 (3,9,'Zn(OH)2+2NaOH=Na2ZnO2+2H2O','correct'),
 (4,7,'HI','correct'),(4,8,'I₂','correct'),(4,13,'97,8','correct'),
 (5,5,'PROTONLAR','correct'),(5,8,'Cl₂O₇','correct'),(5,10,'18','correct')])
def test_existing_shared_grader_handles_grade8_without_a_new_mechanism(n,qn,value,code,reviewed_chemistry_documents):
    q=reviewed_chemistry_documents[73+n]['assessments'][qn-1]
    assert grade_answer(q['grading_spec'],{'value':value})==code


def test_grade8_progress_is_independent_preserves_grade7_and_awards_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons();old=docs[0]
    with factory.begin() as db:
        db.add(ChemistryProgress(user_id=1,lesson_key=old['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=20
    g7=client.get(PREFIX+'/catalog?grade=7').json()
    g8=client.get(PREFIX+'/catalog?grade=8').json()
    assert g7['grade']==7 and g8['grade']==8
    assert g7['available_grades']==g8['available_grades']==[7,8]
    assert len(g7['lessons'])==74 and len(g8['lessons'])>=5
    assert g7['lessons'][0]['state']=='completed' and g7['lessons'][2]['state']=='locked'
    assert g8['lessons'][0]['state']=='available' and g8['lessons'][1]['state']=='locked'
    assert not g8['grade_content_complete'] and g8['source_review_pending']
    locked=client.post(f"{PREFIX}/lessons/{docs[75]['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
    assert locked.status_code==403
    for l in docs[74:79]:
        a=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())}).json()
        assert a['lesson_key']==l['key'] and 'grading_spec' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        r=finish(client,a);assert r.status_code==200 and r.json()['xp_awarded']==20
        assert finish(client,a).json()==r.json()
    with factory() as db:
        assert db.get(User,1).xp_total==120
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==6
        p=db.query(ChemistryProgress).filter_by(user_id=1,lesson_key=old['key']).one()
        assert p.xp_earned==20 and p.attempts==1
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert client.get(PREFIX+'/catalog?grade=7').json()==g7
    assert all(r['state']=='completed' for r in client.get(PREFIX+'/catalog?grade=8').json()['lessons'][:5])
