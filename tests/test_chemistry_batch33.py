"""Source-reviewed Cr/Mn/Fe models retain strict copy, clinical and legacy holds."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_batch33_source_order_counts_and_common_types():
    lessons=load_lessons()[163:168]
    assert [l['topic_id'] for l in lessons]==[f'ch9-paragraph{n}' for n in range(31,36)]
    assert [l['sequence'] for l in lessons]==list(range(31,36))
    assert sum(len(l['content']['cards']) for l in lessons)==89
    assert sum(len(l['assessments']) for l in lessons)==189
    assert all(l['content']['examples'] for l in lessons)
    assert all(not b['course_ready'] for b in load_catalog()['books'])
    refs=lessons[-1]['facts']['chlorineatoms']['source_refs']
    source=next(r for r in refs if r['topic_id']=='ch7-paragraph10')
    assert source['printed_pages']==[34] and source['pdf_pages']==[18] and source['regions']==['left']
    assert source['file_name']=='kimyo_7_uzb.pdf'
    assert all(q['response_kind']=='concept_selection' for l in lessons for q in l['assessments'] if '[' in q['grading_spec']['verified_answer'])


@pytest.mark.parametrize('n',range(31,36))
def test_batch33_review_cannot_disappear(n):
    catalog=deepcopy(load_catalog())
    next(r for r in catalog['books'][2]['records'] if r['id']==f'ch9-paragraph{n}').pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(catalog)


@pytest.mark.parametrize('n,fid,value,error',[
    (31,'chloride','Ortiqcha HCl doim CrCl3 beradi','unreviewed_chromium_excess_acid'),
    (32,'missingcoefficient','K2Cr2O7+H2SO4=CrO3+K2SO4+H2O','unbalanced_chromium_trioxide_copy'),
    (33,'manganatebalance','K2MnO4 da Mn +7','unreviewed_manganate_oxidation_copy'),
    (33,'manganatebalance','K2MnO4 hosil bo‘lishida 3 elektron','unreviewed_manganate_oxidation_copy'),
    (34,'ores','Limonit FeO2·nH2O','unreviewed_limonite_formula'),
    (34,'configuration','6 juftlashmagan elektron','unreviewed_iron_orbital_diagram'),
    (35,'biology','200 mg','unreviewed_iron_clinical_dose')])
def test_batch33_held_copy_cannot_become_key(n,fid,value,error):
    lesson=deepcopy(read_json(DIRECTORY/f'grade9_paragraph{n}.json'))
    lesson['facts'][fid]['verified_answers'].append(value)
    with pytest.raises(ValueError,match=error):
        validate_lesson(load_catalog(),lesson,read_json(DIRECTORY/f'grade9_paragraph{n}_review.json'))


@pytest.mark.parametrize('n,fid,expected,value,code',[
    (31,'identity','24','24','correct'),
    (31,'table','51.996','51,996','correct'),
    (31,'configuration','1','1','correct'),
    (31,'aluminothermy','Cr2O3+2Al=Al2O3+2Cr','Cr2O3+2Al=Al2O3+2Cr','correct'),
    (31,'aluminothermy','Cr2O3+2Al=Al2O3+2Cr','Cr2O3+Al=Al2O3+Cr','atom_imbalance'),
    (31,'carbon','Fe(CrO2)2+4C=2Cr+Fe+4CO','Fe(CrO2)2+4C=2Cr+Fe+4CO','correct'),
    (31,'gasvolume','3.36','3,36','correct'),
    (31,'saltmass','19.6','19.6','correct'),
    (32,'oxideclasses','CrO','CrO','correct'),
    (32,'hydroxideiii','Cr(OH)3','Cr(OH)3','correct'),
    (32,'samplegas','0.448','4.48e-1','correct'),
    (32,'samplemass','18.24','18,24','correct'),
    (32,'samplemass','5.88','5.88','correct'),
    (32,'missingcoefficient','K2Cr2O7+H2SO4=2CrO3+K2SO4+H2O','K2Cr2O7+H2SO4=2CrO3+K2SO4+H2O','correct'),
    (32,'missingcoefficient','K2Cr2O7+H2SO4=2CrO3+K2SO4+H2O','K2Cr2O7+H2SO4=CrO3+K2SO4+H2O','atom_imbalance'),
    (32,'ironsulfate','6FeSO4+K2Cr2O7+7H2SO4=3Fe2(SO4)3+Cr2(SO4)3+K2SO4+7H2O','6FeSO4+K2Cr2O7+7H2SO4=3Fe2(SO4)3+Cr2(SO4)3+K2SO4+7H2O','correct'),
    (33,'identity','54.938','54,938','correct'),
    (33,'physical','14.88','14.88','correct'),
    (33,'oxygenfraction','50.5','50,5','correct'),
    (33,'manganatebalance','6','6','correct'),
    (33,'manganatebalance','6','7','incorrect'),
    (33,'manganatebalance','2','3','incorrect'),
    (33,'hclbalance','10','10','correct'),
    (33,'exercisemanganate','3K2MnO4+2H2O=2KMnO4+MnO2+4KOH','3K2MnO4+2H2O=2KMnO4+MnO2+4KOH','correct'),
    (34,'identity','55.847','55,847','correct'),
    (34,'configuration','6','6','correct'),
    (34,'physical','15.748','15,748','correct'),
    (34,'aluminothermy','9','9','correct'),
    (34,'steam','3Fe+4H2O=Fe3O4+4H2','3Fe+4H2O=Fe3O4+4H2','correct'),
    (34,'nitrate','5Fe+12HNO3=5Fe(NO3)2+N2+6H2O','5Fe+12HNO3=5Fe(NO3)2+N2+6H2O','correct'),
    (35,'blueii','6','6','correct'),
    (35,'blueiii','4','4','correct'),
    (35,'thiocyanate','KNCS','KNCS','correct'),
    (35,'ore','10.741','10,741','correct'),
    (35,'chlorineamount','0.375','0.375','correct'),
    (35,'chlorinevolume','8.4','8,4','correct'),
    (35,'chlorineatoms','4.515e23','4.515e23','correct'),
    (35,'chlorineatoms','4.515e23','4.515e22','incorrect')])
def test_declared_models_with_shared_grader(n,fid,expected,value,code,reviewed_chemistry_documents):
    lesson=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch9-paragraph{n}')
    q=next(q for q in lesson['assessments'] if fid in q['fact_ids'] and q['grading_spec']['expected']==expected)
    assert grade_answer(q['grading_spec'],{'value':value})==code


def test_batch33_preserves163_and_awards100xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for lesson in docs[:163]:db.add(ChemistryProgress(user_id=1,lesson_key=lesson['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=3260
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8)}
    g9=client.get(PREFIX+'/catalog?grade=9').json()['lessons']
    assert g9[30]['state']=='available' and all(l['state']=='locked' for l in g9[31:])
    for lesson in docs[163:168]:
        response=client.post(f"{PREFIX}/lessons/{lesson['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;attempt=response.json()
        assert 'grading_spec' not in str(attempt) and 'verified_answers' not in str(attempt)
        for q in lesson['assessments']:
            r=send(client,attempt,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,attempt);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,attempt).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==3360
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==168
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert all(l['state']=='completed' for l in client.get(PREFIX+'/catalog?grade=9').json()['lessons'][:35])
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
