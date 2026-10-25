"""Grade9 starts with the same bounded source/assessment/progress contract."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_grade9_first_five_source_order_and_common_contract():
    docs=load_lessons();new=docs[133:138]
    assert len(docs)>=138 and [l['topic_id'] for l in new]==[f'ch9-paragraph{n:02}' for n in range(1,6)]
    assert [l['sequence'] for l in new]==list(range(1,6))
    assert sum(len(l['content']['cards']) for l in new)==64
    assert sum(len(l['assessments']) for l in new)==97
    assert all(l['content']['examples'] for l in new)
    assert set(q['response_kind'] for l in new for q in l['assessments'])=={'concept_selection','short_text','chemical_formula','numeric_value'}
    assert all(l['grade']==9 and l['content']['xp_reward']==20 for l in new)
    assert all(r['book_id']==new[0]['book_id'] for l in new for r in l['source_refs'])
    assert ('ch9-paragraph03',[23]) in [(r['topic_id'],r['printed_pages']) for r in new[3]['facts']['acid']['source_refs']]
    assert ('ch9-paragraph05',[28]) in [(r['topic_id'],r['printed_pages']) for r in new[4]['facts']['weak']['source_refs']]
    assert all(not b['course_ready'] for b in load_catalog()['books'])


@pytest.mark.parametrize('n',range(1,6))
def test_grade9_scoped_source_issues_cannot_disappear(n):
    c=deepcopy(load_catalog());next(r for r in c['books'][2]['records'] if r['id']==f'ch9-paragraph{n:02}').pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


@pytest.mark.parametrize('n,fid,answer,error',[
 (1,'table','Mg radius0,269nm','unreviewed_magnesium_radius'),
 (1,'table','Barcha davrlarda ionlanish energiyasi qat’iy ortadi','unqualified_monotonic_ionization'),
 (1,'counts','Ar-Z','average_atomic_mass_neutron_rule'),
 (3,'acidmodels','H3PO3=3H+ vaPO3','unverified_phosphorous_acid_three_protons'),
 (5,'weak','Barcha organik kislotalar kuchsiz','unqualified_all_organic_weak'),
 (5,'degree','58','ambiguous_sulfate_dissociation_degree')])
def test_reviewed_errors_never_become_answer_keys(n,fid,answer,error):
    l=deepcopy(read_json(DIRECTORY/f'grade9_paragraph{n:02}.json'));l['facts'][fid]['verified_answers'].append(answer)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade9_paragraph{n:02}_review.json'))


@pytest.mark.parametrize('n,qn,value,code',[
 (1,10,'Na','correct'),(1,10,'na','invalid_answer'),(1,11,'Cl','correct'),
 (1,12,'33','correct'),(1,13,'31','correct'),(1,16,'7','correct'),
 (1,17,'1,66','correct'),(1,18,'18','correct'),(1,19,'32','correct'),
 (1,20,'10','correct'),(1,21,'14','correct'),(1,22,'9','correct'),
 (1,23,'15','correct'),(1,24,'4.557','correct'),
 (2,12,'H2','correct'),(2,13,'HF','correct'),(2,14,'NaCl','correct'),
 (2,15,'H2O','correct'),(2,16,'0','correct'),(2,17,'−1','correct'),
 (2,18,'-2','correct'),(2,19,'0','correct'),
 (3,6,'Katod','correct'),(3,7,'Anod','correct'),(3,8,'Gidroksoniy','correct'),
 (3,12,'Al2(SO4)3','correct'),(3,13,'10','correct'),(3,14,'18','correct'),
 (3,15,'0,2','correct'),(3,16,'0.3','correct'),(3,17,'0.5','correct'),
 (4,8,'HNO3','correct'),(4,9,'Ca(OH)2','correct'),(4,10,'K2SO4','correct'),
 (4,11,'Al2(SO4)3','correct'),(4,12,'NaHSO4','correct'),
 (4,15,'2','correct'),(4,16,'3','correct'),(4,17,'5','correct'),(4,18,'0','correct'),
 (5,8,'KNO3','correct'),(5,9,'H2CO3','correct'),(5,10,'CH3COOH','correct'),
 (5,11,'H3PO4','correct'),(5,12,'0,85','correct'),(5,13,'50','correct'),
 (5,14,'0.2','correct'),(5,15,'20','correct'),(5,16,'160','correct'),
 (5,19,'1e-5','correct'),(5,19,'0.00001','correct'),(5,19,'0.001','incorrect')])
def test_grade9_frq_uses_existing_deterministic_kinds(n,qn,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch9-paragraph{n:02}')
    assert grade_answer(l['assessments'][qn-1]['grading_spec'],{'value':value})==code


def test_new_grade_preserves_both_old_grades_and_once_only_xp(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:133]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=2660
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8)}
    g9=client.get(PREFIX+'/catalog?grade=9').json()
    assert {7,8,9} <= set(g9['available_grades']) and len(g9['lessons'])>=5
    assert g9['lessons'][0]['state']=='available' and all(l['state']=='locked' for l in g9['lessons'][1:])
    for l in docs[133:138]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==2760
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==138
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert all(l['state']=='completed' for l in client.get(PREFIX+'/catalog?grade=9').json()['lessons'][:5])
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
