"""Grade9 Al/Cu/Ag/Au/Zn source models, preserving legacy gem/KOH holds."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,KNOWN_EDITORIAL_ISSUES,load_catalog,load_lessons,read_json,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_batch32_order_and_existing_response_types():
    ls=load_lessons()[158:163]
    assert [l['topic_id'] for l in ls]==[f'ch9-paragraph{n:02}' for n in range(26,31)]
    assert [l['sequence'] for l in ls]==list(range(26,31))
    assert sum(len(l['content']['cards']) for l in ls)==78
    assert sum(len(l['assessments']) for l in ls)==151
    assert all(l['content']['examples'] for l in ls)
    assert all(not b['course_ready'] for b in load_catalog()['books'])
    assert ('ch9-paragraph15',[72]) in [(r['topic_id'],r['printed_pages']) for r in ls[0]['facts']['chromiumratio']['source_refs']]
    assert ('ch8-practical01',[127]) in [(r['topic_id'],r['printed_pages']) for r in ls[2]['facts']['mixture']['source_refs']]
    assert ('ch8-paragraph28',[122]) in [(r['topic_id'],r['printed_pages']) for r in ls[3]['facts']['halides']['source_refs']]
    assert all(q['response_kind']=='concept_selection' for l in ls for q in l['assessments'] if '[' in q['grading_spec']['verified_answer'])


def test_existing_gem_and_koh_review_is_retained():
    r=next(r for r in load_catalog()['books'][2]['records'] if r['id']=='ch9-paragraph27')
    assert KNOWN_EDITORIAL_ISSUES[r['id']]=='ch9-p27-gem-and-equation-review'
    issue=next(i for i in r['editorial_review_issues'] if i['id']=='ch9-p27-gem-and-equation-review')
    assert issue['status']=='open_review' and issue['printed_pages']==[129,130,131]
    assert {'gem_hosts','koh_coefficient'}<={x['id'] for x in issue['withheld_claims']}
    assert issue['cross_source_evidence'][0]['topic_id']=='ch7-paragraph37'
    assert issue['cross_source_evidence'][0]['printed_pages']==[108]
    assert issue['cross_source_evidence'][0]['pdf_pages']==[55]
    assert issue['cross_source_evidence'][0]['regions']==['left']
    lesson=read_json(DIRECTORY/'grade9_paragraph27.json')
    assert all('KOH' not in q['grading_spec']['verified_answer'] for q in lesson['assessments'])
    assert not any(name in str(lesson['facts']).casefold() for name in ['rubin','sapfir','ametist'])


@pytest.mark.parametrize('n',range(26,31))
def test_batch32_review_cannot_disappear(n):
    c=deepcopy(load_catalog());next(r for r in c['books'][2]['records'] if r['id']==f'ch9-paragraph{n:02}').pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


@pytest.mark.parametrize('n,fid,value,error',[
 (26,'complex','2Al+2NaOH+6H2O=2Na[Al(OH)4]+H2','unbalanced_aluminium_hydrogen_copy'),
 (27,'hydroxidebase','Al(OH)3+2KOH=KAlO2+2H2O','unresolved_aluminium_koh_equation'),
 (27,'hydroxidebase','Al(OH)3+KOH=KAlO2+2H2O','unresolved_aluminium_koh_equation'),
 (27,'gems','Rubin','unresolved_gem_host'),
 (28,'physical','Cu hech qachon oksidlanmaydi','unqualified_copper_nonoxidation'),
 (29,'gold','Oltin0,0002 nm','unreviewed_gold_leaf_unit'),
 (29,'silver','Kumushli suv doim xavfsiz','unreviewed_silver_water_safety'),
 (30,'hydroxideacid','Zn(OH)2+H2SO4=ZnSO4+H2O','unbalanced_zinc_hydroxide_water_copy')])
def test_unresolved_copies_cannot_become_premises_or_keys(n,fid,value,error):
    l=deepcopy(read_json(DIRECTORY/f'grade9_paragraph{n:02}.json'));l['facts'][fid]['verified_answers'].append(value)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade9_paragraph{n:02}_review.json'))


@pytest.mark.parametrize('n,qn,value,code',[
 (26,8,'Al4C3','correct'),(26,10,'Al2(SO4)3','correct'),
 (26,12,'2Al+6H2O=2Al(OH)3+3H2','correct'),
 (26,14,'8Al+30HNO3=8Al(NO3)3+3NH4NO3+9H2O','correct'),
 (26,20,'8Al+3Fe3O4=4Al2O3+9Fe','correct'),
 (26,25,'2NaAlO2+4H2SO4=Na2SO4+Al2(SO4)3+4H2O','correct'),
 (26,26,'0,5','correct'),(26,27,'54','correct'),(26,28,'46','correct'),
 (26,29,'23.4','correct'),(26,32,'268,8','correct'),(26,33,'18','correct'),
 (26,34,'20.930','correct'),
 (27,9,'KAlO2','correct'),(27,14,'2Al(OH)3+3H2SO4=Al2(SO4)3+6H2O','correct'),
 (27,15,'0','correct'),(27,16,'19','correct'),(27,17,'0,8','correct'),(27,20,'12','correct'),
 (28,8,'CuFeS2','correct'),(28,11,'2Cu2S+3O2=2Cu2O+2SO2','correct'),
 (28,16,'2Cu+O2+H2O+CO2=(CuOH)2CO3','correct'),
 (28,19,'3Cu+8HNO3=3Cu(NO3)2+2NO+4H2O','correct'),
 (28,20,'(CuOH)2CO3=2CuO+CO2+H2O','correct'),
 (28,25,'CuSO4+2NaOH=Cu(OH)2+Na2SO4','correct'),
 (28,31,'63,546','correct'),(28,33,'5.9','correct'),
 (28,35,'8','correct'),(28,36,'20','correct'),
 (29,7,'AgNO3','correct'),(29,8,'AgBr','correct'),
 (29,10,'Ag+2HNO3=AgNO3+NO2+H2O','correct'),
 (29,11,'AgNO3+NaCl=AgCl+NaNO3','correct'),
 (29,12,'2Au+3Cl2=2AuCl3','correct'),
 (29,15,'38.64','correct'),(29,18,'58,3','correct'),
 (29,19,'11.66','correct'),(29,20,'8.34','correct'),
 (30,7,'HgS','correct'),(30,10,'Hg2O','correct'),
 (30,12,'2ZnS+3O2=2ZnO+2SO2','correct'),
 (30,23,'4Zn+10HNO3=4Zn(NO3)2+NH4NO3+3H2O','correct'),
 (30,30,'Zn(OH)2+H2SO4=ZnSO4+2H2O','correct'),
 (30,30,'Zn(OH)2+H2SO4=ZnSO4+H2O','atom_imbalance'),
 (30,32,'Hg(NO3)2=Hg+2NO2+O2','correct'),
 (30,33,'Hg(NO3)2+2NaOH=HgO+2NaNO3+H2O','correct'),
 (30,37,'65.39','correct'),(30,40,'3,270','correct'),
 (30,40,'3.25','incorrect'),(30,41,'18.25','correct')])
def test_existing_grader_handles_declared_source_models(n,qn,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch9-paragraph{n:02}')
    assert grade_answer(l['assessments'][qn-1]['grading_spec'],{'value':value})==code


def test_batch32_preserves158_and_adds100xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:158]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=3160
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8)}
    g9=client.get(PREFIX+'/catalog?grade=9').json()['lessons']
    assert g9[25]['state']=='available' and all(l['state']=='locked' for l in g9[26:])
    for l in docs[158:163]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==3260
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==163
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert all(l['state']=='completed' for l in client.get(PREFIX+'/catalog?grade=9').json()['lessons'][:30])
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
