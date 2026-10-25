"""Original grade9 alloys/corrosion/electrolysis/alkali models, source order."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_batch30_preserves_order_and_source_models():
    lessons=load_lessons()[148:153]
    assert [l['topic_id'] for l in lessons]==[f'ch9-paragraph{n:02}' for n in range(16,21)]
    assert [l['sequence'] for l in lessons]==list(range(16,21))
    assert sum(len(l['content']['cards']) for l in lessons)==75
    assert sum(len(l['assessments']) for l in lessons)==111
    assert all(l['content']['examples'] for l in lessons)
    assert all(not b['course_ready'] for b in load_catalog()['books'])
    silver=lessons[1]['facts']['silvermass']['source_refs']
    assert ('ch8-paragraph13',[59]) in [(r['topic_id'],r['printed_pages']) for r in silver]
    current=lessons[3]['facts']['silvercurrent']['source_refs']
    assert ('ch9-paragraph19',[90]) in [(r['topic_id'],r['printed_pages']) for r in current]
    assert any(r['topic_id']=='ch7-paragraph09' and r['regions']==['right'] for r in lessons[2]['facts']['copper']['source_refs'])
    assert 'Cu + AgNO3 → Cu(NO3)2 + Ag' in lessons[1]['assessments'][9]['public']['prompt']


@pytest.mark.parametrize('n',range(16,21))
def test_batch30_editorial_holds_stay_visible(n):
    c=deepcopy(load_catalog());next(r for r in c['books'][2]['records'] if r['id']==f'ch9-paragraph{n:02}').pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


@pytest.mark.parametrize('n,fid,value,error',[
 (16,'properties','Barcha qotishmalar yuqori o‘tkazuvchan','unqualified_alloy_conductivity'),
 (17,'series','Har bir metall barcha o‘ng metallarni siqib chiqaradi','unqualified_aqueous_displacement'),
 (18,'inhibitors','Ingibitor 10^6 mol/L','unreviewed_inhibitor_concentration'),
 (18,'rustmodel','Barcha zang Fe(OH)3','unqualified_rust_identity'),
 (19,'inert','Barcha sulfidlar anodida H2S','unreviewed_sulfide_anode_product'),
 (19,'roles','2H++2e=H+','unbalanced_electrolysis_hydrogen_copy'),
 (20,'later','Fransiy tabiatda uchramaydi','unreviewed_francium_occurrence'),
 (20,'biological','Seziy zaharli emas','unqualified_alkali_toxicity')])
def test_unresolved_source_claims_cannot_become_keys(n,fid,value,error):
    l=deepcopy(read_json(DIRECTORY/f'grade9_paragraph{n:02}.json'));l['facts'][fid]['verified_answers'].append(value)
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade9_paragraph{n:02}_review.json'))


@pytest.mark.parametrize('n,qn,value,code',[
 (16,7,'Cu3Al','correct'),(16,8,'Cu5Zn8','correct'),
 (16,10,'9,9','correct'),(16,11,'0.1','correct'),(16,12,'13.4','correct'),
 (16,14,'0,2','correct'),(16,15,'36.5','correct'),
 (17,7,'Pb(NO3)2','correct'),(17,8,'Cu(NO3)2','correct'),
 (17,9,'Zn+Pb(NO3)2=Pb+Zn(NO3)2','correct'),
 (17,10,'Cu+2AgNO3=Cu(NO3)2+2Ag','correct'),
 (17,12,'6,769','correct'),(17,12,'4.3','incorrect'),(17,14,'3.2','correct'),
 (18,9,'4Fe+6H2O+3O2=4Fe(OH)3','correct'),
 (18,10,'4Fe(OH)2+2H2O+O2=4Fe(OH)3','correct'),
 (18,11,'2H3PO4+Fe=Fe(H2PO4)2+H2','correct'),
 (18,13,'2FeHPO4+Fe=Fe3(PO4)2+H2','correct'),
 (18,17,'0,672','correct'),(18,18,'53.5','correct'),
 (18,19,'8.4','correct'),(18,20,'2.24','correct'),(18,21,'16','correct'),
 (19,14,'2H2O=2H2+O2','correct'),
 (19,15,'2NaCl+2H2O=2NaOH+H2+Cl2','correct'),
 (19,16,'2NaI=2Na+I2','correct'),
 (19,17,'2CuSO4+2H2O=2Cu+2H2SO4+O2','correct'),
 (19,18,'4AgNO3+2H2O=4Ag+O2+4HNO3','correct'),
 (19,19,'2Cu(NO3)2+2H2O=2Cu+O2+4HNO3','correct'),
 (19,22,'5,6','correct'),(19,25,'0.64','correct'),(19,26,'3.76','correct'),
 (19,29,'0.2','correct'),(19,30,'1,88','correct'),(19,32,'12.195','correct'),
 (19,33,'33,5','correct'),(19,34,'12.087','correct'),(19,35,'162','correct'),
 (19,36,'3.01e23','correct'),
 (20,7,'Li','correct'),(20,10,'Fr','correct'),(20,12,'K2SO4','correct'),
 (20,18,'87','correct'),(20,20,'22,989','correct'),(20,21,'39.102','correct')])
def test_batch30_existing_grading(n,qn,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch9-paragraph{n:02}')
    assert grade_answer(l['assessments'][qn-1]['grading_spec'],{'value':value})==code


def test_batch30_preserves148_completions_and_adds100xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:148]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=2960
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8)}
    g9=client.get(PREFIX+'/catalog?grade=9').json()['lessons']
    assert g9[15]['state']=='available' and all(l['state']=='locked' for l in g9[16:])
    for l in docs[148:153]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==3060
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==153
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert all(l['state']=='completed' for l in client.get(PREFIX+'/catalog?grade=9').json()['lessons'][:20])
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
