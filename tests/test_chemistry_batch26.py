"""Final grade8 labs: source-bounded models, no invented field observations."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_all_grade8_entries_and_nine_final_labs_keep_source_order():
    docs=load_lessons();labs=docs[124:133]
    assert len(docs)==133
    assert sum(l['grade']==7 for l in docs)==74
    assert sum(l['grade']==8 for l in docs)==59
    assert [l['topic_id'] for l in labs]==[f'ch8-laboratory{n:02}' for n in range(2,11)]
    assert [l['sequence'] for l in labs]==list(range(51,60))
    assert sum(len(l['content']['cards']) for l in labs)==55
    assert sum(len(l['assessments']) for l in labs)==93
    assert all(l['content']['examples'] for l in labs)
    assert all({'concept_selection','chemical_formula'} <= {q['response_kind'] for q in l['assessments']} for l in labs)
    assert all(not b['course_ready'] for b in load_catalog()['books'])
    assert ('ch8-paragraph37',[161]) in [(r['topic_id'],r['printed_pages']) for r in labs[7]['facts']['chloride']['source_refs']]
    assert all('blue' not in a.casefold() and 'ko‘k' not in a.casefold()
               for f in labs[1]['facts'].values() for a in f['verified_answers'])
    assert all('kuzatuv' not in q['grading_spec']['verified_answer'].casefold() for q in labs[2]['assessments'])


@pytest.mark.parametrize('n',range(2,11))
def test_nine_laboratory_evidence_scopes_cannot_be_removed(n):
    c=deepcopy(load_catalog());next(r for r in c['books'][1]['records'] if r['id']==f'ch8-laboratory{n:02}').pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


@pytest.mark.parametrize('n,fid,answer,error',[
 (3,'observation','Kraxmal ko‘k rang beradi','unprovided_starch_color'),
 (4,'purpose','Barcha tuproq xlorid tutadi','unprovided_soil_chloride'),
 (6,'layers','Benzol qatlami binafsha','unprovided_iodine_layer_color'),
 (9,'formation','1,5:1 aniq stexiometrik nisbat','recipe_is_not_exact')])
def test_unprovided_colors_field_results_and_recipe_keys_rejected(n,fid,answer,error):
    l=deepcopy(read_json(DIRECTORY/f'grade8_laboratory{n:02}.json'));l['facts'][fid]['verified_answers'].append(answer)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade8_laboratory{n:02}_review.json'))


@pytest.mark.parametrize('n,qn,value,code',[
 (2,5,'KCl','correct'),(2,5,'KCl6','incorrect'),(2,6,'S8','correct'),
 (2,8,'6','correct'),(2,9,'8','correct'),(2,10,'2','correct'),
 (3,5,'AgCl','correct'),(3,6,'AgBr','correct'),(3,7,'AgI','correct'),
 (3,8,'AgNO3+NaCl=AgCl+NaNO3','correct'),
 (3,9,'AgNO3+NaBr=AgBr+NaNO3','correct'),
 (3,10,'AgNO3+NaI=AgI+NaNO3','correct'),
 (3,11,'HCl+AgNO3=AgCl+HNO3','correct'),
 (4,5,'AgNO3','correct'),(4,6,'AgCl','correct'),(4,8,'3','correct'),
 (5,4,'Br2','correct'),(5,4,'br2','invalid_answer'),
 (5,5,'2NaBr+Cl2=2NaCl+Br2','correct'),
 (5,6,'2NaI+Cl2=2NaCl+I2','correct'),
 (5,7,'2NaI+Br2=2NaBr+I2','correct'),
 (5,7,'NaI+Br2=NaBr+I2','atom_imbalance'),
 (6,6,'I2','correct'),(6,7,'2','correct'),
 (7,5,'FeS2','correct'),(7,6,'ZnS','correct'),(7,8,'120','correct'),
 (7,9,'97','correct'),(7,10,'172','correct'),(7,11,'6','correct'),(7,12,'256','correct'),
 (8,5,'BaSO4','correct'),(8,6,'Al2(SO4)3','correct'),
 (8,10,'Al2(SO4)3+3BaCl2=3BaSO4+2AlCl3','correct'),
 (8,10,'Al2(SO4)3+BaCl2=BaSO4+AlCl3','atom_imbalance'),
 (9,5,'NH3','correct'),(9,6,'NH4Cl','correct'),
 (9,7,'2NH4Cl+Ca(OH)2=CaCl2+2H2O+2NH3','correct'),
 (9,8,'NH3+HCl=NH4Cl','correct'),(9,9,'4','correct'),
 (10,7,'(NH4)2SO4','correct'),(10,10,'85','correct'),(10,11,'80','correct'),
 (10,12,'132','correct'),(10,13,'74,5','correct'),(10,13,'74.5','correct'),(10,14,'101','correct')])
def test_exact_digital_models_use_existing_bounded_grader(n,qn,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch8-laboratory{n:02}')
    assert grade_answer(l['assessments'][qn-1]['grading_spec'],{'value':value})==code


def test_nine_labs_preserve124_and_award180_xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:124]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=2480
    old=client.get(PREFIX+'/catalog?grade=7').json()
    g8=client.get(PREFIX+'/catalog?grade=8').json()['lessons']
    assert g8[50]['state']=='available' and all(l['state']=='locked' for l in g8[51:])
    for l in docs[124:133]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==2660
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==133
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert all(l['state']=='completed' for l in client.get(PREFIX+'/catalog?grade=8').json()['lessons'])
    assert client.get(PREFIX+'/catalog?grade=7').json()==old
