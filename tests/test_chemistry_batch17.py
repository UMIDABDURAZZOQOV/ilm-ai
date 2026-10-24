"""Source-scoped nucleus,isotope,shell and subshell lessons reuse bounded grading."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,readiness,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_grade8_six_to_ten_source_order_counts_and_existing_response_kinds():
    docs=load_lessons()[79:84]
    assert [l['topic_id'] for l in docs]==[f'ch8-paragraph{n:02}' for n in range(6,11)]
    assert [l['sequence'] for l in docs]==list(range(6,11))
    assert sum(len(l['content']['cards']) for l in docs)==35
    assert sum(len(l['assessments']) for l in docs)==52
    assert {q['response_kind'] for l in docs for q in l['assessments']}=={'concept_selection','short_text','numeric_value'}
    for l in docs:
        assert l['grade']==8 and l['prerequisite_ids']==[f"ch8-paragraph{l['sequence']-1:02}"]
        assert all(r['pdf_pages']==r['printed_pages'] and r['regions']==['full'] for r in l['source_refs'])
    state=next(r for r in readiness(load_catalog(),load_lessons()) if r['grade']==8)
    assert state['implemented_lessons']>=10 and not state['course_ready']


@pytest.mark.parametrize('n',range(6,10))
def test_scoped_nucleus_and_electron_model_issues_cannot_be_removed(n):
    c=deepcopy(load_catalog());next(r for r in c['books'][1]['records'] if r['id']==f'ch8-paragraph{n:02}').pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


@pytest.mark.parametrize('n,fid,text,error',[
 (6,'groups','Geliy tashqi qavatida8 elektron;8','unresolved_helium_group_rule'),
 (7,'count','Ar=N+Z','unresolved_average_mass_identity'),
 (8,'boron','35.543','unresolved_isotope_chart_average'),
 (8,'boron','35,4846','unresolved_isotope_chart_average'),
 (8,'boron','Tabiiy kaliy93% va7%','unresolved_natural_potassium'),
 (9,'cloud','Elektron markazdan qochma kuch bilan barqaror','unresolved_classical_electron_force')])
def test_unresolved_source_generalisation_or_silent_repair_is_not_a_premise(n,fid,text,error):
    l=deepcopy(load_lessons()[73+n]);r=read_json(DIRECTORY/f'grade8_paragraph{n:02}_review.json')
    if n==6:l['facts'][fid]['claim']=text;l['facts'][fid]['verified_answers'].append('8')
    else:l['facts'][fid]['verified_answers'].append(text)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('n,qn,value,code',[
 (6,4,'DAVR','correct'),(6,10,'8','correct'),
 (7,6,'13','correct'),(7,7,'-1','correct'),(7,8,'27','correct'),(7,9,'14','correct'),
 (8,4,'izoton','correct'),(8,6,'0','correct'),(8,7,'20','correct'),
 (8,9,'19','correct'),(8,10,'81','correct'),(8,12,'33','correct'),
 (9,5,'18','correct'),(9,8,'1','correct'),(9,8,'18','incorrect'),
 (10,4,'F','correct'),(10,7,'10','correct'),(10,8,'14','correct'),(10,9,'3','correct')])
def test_scoped_counting_models_use_existing_text_and_numeric_grader(n,qn,value,code,reviewed_chemistry_documents):
    q=reviewed_chemistry_documents[73+n]['assessments'][qn-1]
    assert grade_answer(q['grading_spec'],{'value':value})==code


def test_five_new_atom_lessons_preserve79_completions_and_award100xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:79]:
            db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=1580
    before=client.get(PREFIX+'/catalog?grade=7').json()
    for l in docs[79:84]:
        path=f"{PREFIX}/lessons/{l['key']}/start";payload={'assessment_version':2,'request_id':str(uuid4())}
        response=client.post(path,json=payload);assert response.status_code==200,response.text
        a=response.json();assert a['lesson_key']==l['key']
        assert client.post(path,json=payload).json()['attempt_id']==a['attempt_id']
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        r=finish(client,a);assert r.status_code==200 and r.json()['xp_awarded']==20
        assert finish(client,a).json()==r.json()
    with factory() as db:
        assert db.get(User,1).xp_total==1680
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==84
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert client.get(PREFIX+'/catalog?grade=7').json()==before
    assert all(r['state']=='completed' for r in client.get(PREFIX+'/catalog?grade=8').json()['lessons'][:10])
