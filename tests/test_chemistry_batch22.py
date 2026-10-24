"""Sulfide/sulfate and rate/equilibrium models keep source conditions explicit."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_five_source_order_lessons_have_exact_prior_evidence_and_topic_appropriate_frq():
    docs=load_lessons()[104:109]
    assert [l['topic_id'] for l in docs]==[f'ch8-paragraph{n}' for n in range(30,35)]
    assert [l['sequence'] for l in docs]==list(range(31,36))
    assert sum(len(l['content']['cards']) for l in docs)==56
    assert sum(len(l['assessments']) for l in docs)==74
    assert set(q['response_kind'] for q in docs[3]['assessments'])=={'concept_selection','short_text','numeric_value'}
    assert 'ch8-paragraph33' not in docs[0]['source_context_ids']
    assert {(r['paragraph'],r['printed_pages'][0]) for r in docs[0]['facts']['mass']['source_refs']}=={(30,134),(30,135),(1,7),(25,106),(25,110)}
    assert (32,[139]) in [(r['paragraph'],r['printed_pages']) for r in docs[4]['facts']['oneway']['source_refs']]
    assert all(r['pdf_pages']==r['printed_pages'] and r['regions']==['full'] for l in docs for r in l['source_refs'])
    assert all('ch8-paragraph35'!=r['topic_id'] for l in docs for r in l['source_refs'])


@pytest.mark.parametrize('n',range(30,35))
def test_new_source_issue_stays_visible(n):
    c=deepcopy(load_catalog());next(r for r in c['books'][1]['records'] if r['id']==f'ch8-paragraph{n}').pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


@pytest.mark.parametrize('n,fid,text,error',[
 (30,'identity','H2S 0.01 ml/l xavfsiz','unverified_sulfide_exposure_threshold'),
 (31,'uses','0.03','unverified_sulfur_oxide_exposure_limit'),
 (32,'salts','CaSO4·1/4H2O','unresolved_gypsum_hydrate_quantity'),
 (32,'salts','CaSO4·¼H2O','unresolved_gypsum_hydrate_quantity'),
 (32,'conditions','Ag kislota bilan ta’sir etmaydi','unresolved_silver_acid_nonreaction'),
 (33,'coefficient','Barcha reaksiyalarda koeffitsiyent reaksiya tartibini beradi','unreviewed_universal_reaction_order'),
 (34,'heat','Harorat pasaysa reaksiya tezlashadi','unresolved_equilibrium_shift_rate_confusion')])
def test_held_exposure_formula_or_universal_claim_cannot_enter_verified_answers(n,fid,text,error):
    l=deepcopy(next(l for l in load_lessons() if l['topic_id']==f'ch8-paragraph{n}'))
    review=read_json(DIRECTORY/f'grade8_paragraph{n}_review.json')
    l['facts'][fid]['verified_answers'].append(text)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,review)


@pytest.mark.parametrize('n,qn,value,code',[
 (30,6,'H2S','correct'),(30,7,'2H2S+3O2=2SO2+2H2O','correct'),
 (30,8,'2H2S+O2=2S+2H2O','correct'),(30,8,'2H2S+3O2=2SO2+2H2O','incorrect_species'),
 (30,9,'2FeCl3+H2S=2FeCl2+2HCl+S','correct'),
 (30,10,'2H2S+H2SO3=3S+3H2O','correct'),
 (30,11,'Na2S+Pb(NO3)2=PbS+2NaNO3','correct'),
 (30,12,'CuSO4+H2S=CuS+H2SO4','correct'),(30,15,'1.172','correct'),(30,17,'56','correct'),
 (31,7,'4FeS2+11O2=2Fe2O3+8SO2','correct'),
 (31,9,'2SO2+O2=2SO3','correct'),(31,9,'2SO2+O2⇌2SO3','invalid_answer'),
 (31,10,'2H2S+SO2=3S+2H2O','correct'),(31,13,'2,207','correct'),(31,16,'15','correct'),
 (32,7,'2Al+3H2SO4=Al2(SO4)3+3H2','correct'),
 (32,9,'3H2SO4+Ca3(PO4)2=3CaSO4+2H3PO4','correct'),
 (32,10,'Cu+2H2SO4=CuSO4+SO2+2H2O','correct'),
 (32,11,'Na2SO4+BaCl2=BaSO4+2NaCl','correct'),(32,16,'147','correct'),
 (33,8,'0.6','correct'),(33,9,'0,06','correct'),(33,10,'16','correct'),
 (33,11,'32','correct'),(33,12,'128','correct'),
 (34,11,'CO2+H2=H2O+CO','correct'),(34,12,'3','correct'),(34,13,'2','correct')])
def test_existing_grader_checks_only_supplied_model(n,qn,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch8-paragraph{n}')
    assert grade_answer(l['assessments'][qn-1]['grading_spec'],{'value':value})==code


def test_no_future_air_fraction_context_can_replace_missing_earlier_evidence():
    l=deepcopy(next(l for l in load_lessons() if l['topic_id']=='ch8-paragraph30'))
    r=read_json(DIRECTORY/'grade8_paragraph30_review.json')
    l['source_context_ids'].append('ch8-paragraph33')
    with pytest.raises(ValueError,match='source_context_must_precede_lesson'):validate_lesson(load_catalog(),l,r)


def test_five_lessons_preserve104_and_award_only_new_once_only_xp(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:104]:
            db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=2080
    old=client.get(PREFIX+'/catalog?grade=7').json()
    g8=client.get(PREFIX+'/catalog?grade=8').json();assert g8['lessons'][30]['state']=='available'
    for l in docs[104:109]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            result=send(client,a,q,answer_for(q));assert result.status_code==200 and result.json()['is_correct'],result.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==2180
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==109
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert client.get(PREFIX+'/catalog?grade=7').json()==old
