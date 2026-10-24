"""Reviewed ions,lattices and redox;bounded signs and immutable sourced attempts."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import canonical_number,grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_five_sourced_ionic_lattice_redox_lessons_and_earlier_hydride_evidence():
    docs=load_lessons()[89:94]
    assert [l['topic_id'] for l in docs]==[f'ch8-paragraph{n:02}' for n in range(16,21)]
    assert [l['sequence'] for l in docs]==list(range(16,21))
    assert sum(len(l['content']['cards']) for l in docs)==44
    assert sum(len(l['assessments']) for l in docs)==66
    l=docs[3];assert l['source_context_ids']==['ch8-paragraph18']
    refs=l['facts']['hydrogenroles']['source_refs']
    assert [(r['paragraph'],r['printed_pages']) for r in refs]==[(19,[82]),(18,[78])]
    assert all(r['pdf_pages']==r['printed_pages'] and r['regions']==['full'] for r in refs)
    assert all(q['response_kind'] in {'concept_selection','short_text','numeric_value','chemical_formula','chemical_equation'} for l in docs for q in l['assessments'])


@pytest.mark.parametrize('n',range(16,21))
def test_new_scope_reviews_cannot_be_removed(n):
    c=deepcopy(load_catalog());next(r for r in c['books'][1]['records'] if r['id']==f'ch8-paragraph{n:02}').pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


@pytest.mark.parametrize('n,fid,text,error',[
 (18,'oxygen','Kislorod doimo -2','unresolved_universal_oxygen_state'),
 (19,'copper','Kislorod doimo −2','unresolved_universal_oxygen_state'),
 (19,'definition','Barcha metall ionlari qaytaruvchi','unresolved_universal_metal_ion_role'),
 (20,'nitric','N2O dagi har bir N +1','unreviewed_individual_nitrogen_site')])
def test_universal_state_or_role_or_individual_site_claim_is_held(n,fid,text,error):
    l=deepcopy(load_lessons()[73+n]);r=read_json(DIRECTORY/f'grade8_paragraph{n:02}_review.json')
    l['facts'][fid]['verified_answers'].append(text)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('value,expected',[('−2','-2'),(' −2,0 ','-2'),('−2e0','-2'),('−0','0'),('-2','-2')])
def test_math_minus_is_only_a_bounded_numeric_spelling(value,expected):
    assert canonical_number(value)==expected


@pytest.mark.parametrize('value',['−2+1','−2;print(1)','−2 mol','⁻2','–2','−'+'1'*80])
def test_numeric_sign_support_does_not_add_expressions_units_or_charge_syntax(value):
    with pytest.raises(ValueError):canonical_number(value)


@pytest.mark.parametrize('n,qn,value,code',[
 (16,7,'18','correct'),(16,9,'−1','correct'),(16,10,'+1','correct'),
 (17,7,'H₂O','correct'),(17,8,'6','correct'),(17,9,'4','correct'),
 (18,8,'−2','correct'),(18,9,'+5','correct'),(18,10,'-1','correct'),(18,11,'−1','correct'),
 (19,7,'2Na+Cl2=2NaCl','correct'),(19,9,'Fe2O3+3H2=2Fe+3H2O','correct'),
 (19,11,'8','correct'),(19,12,'6','correct'),(19,15,'2H2S+3O2=2SO2+2H2O','correct'),
 (20,6,'8Al+30HNO3=8Al(NO3)3+3N2O+15H2O','correct'),
 (20,7,'2KMnO4=K2MnO4+MnO2+O2','correct'),
 (20,8,'2H2O2+MnO2=2H2O+O2','incorrect_species'),
 (20,10,'3H2SO3+K2Cr2O7+H2SO4=K2SO4+Cr2(SO4)3+4H2O','correct'),
 (20,11,'10FeSO4+2KMnO4+8H2SO4=5Fe2(SO4)3+K2SO4+2MnSO4+8H2O','correct'),
 (20,12,'3Cu+8HNO3=3Cu(NO3)2+2NO+4H2O','correct'),(20,14,'5','correct')])
def test_shared_numeric_formula_equation_grader_remains_topic_scoped(n,qn,value,code,reviewed_chemistry_documents):
    q=reviewed_chemistry_documents[73+n]['assessments'][qn-1]
    assert grade_answer(q['grading_spec'],{'value':value})==code


def test_five_new_lessons_preserve89_and_math_minus_replays_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:89]:
            db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=1780
    before=client.get(PREFIX+'/catalog?grade=7').json()
    for l in docs[89:94]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        for q in l['assessments']:
            answer=answer_for(q)
            special=l['topic_id']=='ch8-paragraph18' and q['key'].endswith('-q08')
            if special:answer={'value':'−2'}
            result=send(client,a,q,answer);assert result.status_code==200 and result.json()['is_correct'],result.text
            if special:
                assert send(client,a,q,{'value':'-2'}).json()==result.json()
                assert send(client,a,q,{'value':'−3'}).status_code==409
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==1880
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==94
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert client.get(PREFIX+'/catalog?grade=7').json()==before
