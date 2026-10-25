"""Final grade9 paragraphs preserve source scope and exact reviewed corrections."""
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


def test_batch34_source_order_counts_and_common_types():
    lessons=load_lessons()[168:174]
    assert [l['topic_id'] for l in lessons]==[f'ch9-paragraph{n}' for n in range(36,42)]
    assert [l['sequence'] for l in lessons]==list(range(36,42))
    assert sum(len(l['content']['cards']) for l in lessons)==90
    assert sum(len(l['assessments']) for l in lessons)==115
    assert Counter(q['response_kind'] for l in lessons for q in l['assessments'])=={
        'concept_selection':28,'short_text':15,'numeric_value':35,'chemical_formula':11,'chemical_equation':26}
    assert all(l['content']['examples'] for l in lessons)
    assert all(not b['course_ready'] for b in load_catalog()['books'])
    air=lessons[3]['facts']['air']['source_refs']
    source=next(r for r in air if r['topic_id']=='ch7-paragraph20')
    assert source['printed_pages']==[61] and source['pdf_pages']==[31] and source['regions']==['right']
    assert source['file_name']=='kimyo_7_uzb.pdf'
    assert all(q['response_kind']=='concept_selection' for q in lessons[4]['assessments'] if 's2' in q['grading_spec']['verified_answer'])


@pytest.mark.parametrize('n',range(36,42))
def test_batch34_review_cannot_disappear(n):
    catalog=deepcopy(load_catalog())
    next(r for r in catalog['books'][2]['records'] if r['id']==f'ch9-paragraph{n}').pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(catalog)


@pytest.mark.parametrize('n,fid,value,error',[
    (37,'ironoxygen','2Al+3O2=2Al2O3','unbalanced_steel_worked_copy'),
    (37,'ironoxygen','MeO+2HCl=MeCl2+H2','unbalanced_steel_worked_copy'),
    (38,'gas','Etan element','unreviewed_ethane_element_copy'),
    (39,'classes','Akaritsid kapalak','unreviewed_acaricide_taxonomy_copy')])
def test_batch34_held_copy_cannot_become_key(n,fid,value,error):
    lesson=deepcopy(read_json(DIRECTORY/f'grade9_paragraph{n}.json'))
    lesson['facts'][fid]['verified_answers'].append(value)
    with pytest.raises(ValueError,match=error):
        validate_lesson(load_catalog(),lesson,read_json(DIRECTORY/f'grade9_paragraph{n}_review.json'))


@pytest.mark.parametrize('n,fid,expected,value,code',[
    (36,'carbonmass','6','6','correct'),(36,'carbonmass','194','194','correct'),
    (36,'layers','3','3','correct'),(36,'density','15','15','correct'),
    (36,'stages','Fe3O4+CO=3FeO+CO2','Fe3O4+CO=FeO+CO2','atom_imbalance'),
    (37,'hydrate','5','5','correct'),(37,'bicarbonate','25.2','25,2','correct'),
    (37,'bicarbonate','58','58','correct'),(37,'copper','3.2','3,2','correct'),
    (37,'calcium','40','40','correct'),
    (38,'matrix','Matritsa','matritsa','correct'),
    (38,'filler','To‘ldirgich','Toldirgich','correct'),
    (39,'coal','2986.667','2986,667','correct'),
    (39,'air','14228.998','14228.998','correct'),
    (39,'air','14228.998','14228.997935524852','incorrect'),
    (39,'air','14228.998','14222.222','incorrect'),
    (40,'cl_group','VIIA','VIIA','correct'),(40,'cl_group','VIIA','IIA','incorrect'),
    (40,'cl_group','VIIA','17','invalid_answer'),
    (40,'be_group','IIA','IIA','correct'),(40,'ca_group','IIA','IIA','correct'),
    (40,'cl_outer','7','7','correct'),(40,'cl_outer','17','17','correct'),
    (40,'boron','10.804','10,804','correct'),
    (41,'gamma2','512','512','correct'),(41,'gamma3','41.918','41,918','correct'),
    (41,'gamma3','41.918','41.91806548578769','incorrect'),
    (41,'root','4.129','4,129','correct'),(41,'root','4.129','4.128917917333368','incorrect'),
    (41,'root','4.129','4','incorrect'),
    (41,'rate','0.06','0,06','correct'),(41,'volumetwo','0.111','0.111','correct'),
    (41,'volumethree','0.037','0.037','correct'),(41,'ethylene','27','27','correct')])
def test_batch34_declared_models_shared_grader(n,fid,expected,value,code,reviewed_chemistry_documents):
    lesson=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch9-paragraph{n}')
    q=next(q for q in lesson['assessments'] if fid in q['fact_ids'] and q['grading_spec']['expected']==expected)
    assert grade_answer(q['grading_spec'],{'value':value})==code


def test_authored_corrected_group_cannot_borrow_another_claim_value():
    l=deepcopy(read_json(DIRECTORY/'grade9_paragraph40.json'))
    q=next(q for q in l['assessments'] if q['response_kind']=='short_text' and 'cl_group' in q['fact_ids'])
    q['grading_spec']['verified_answer']='IIA'
    with pytest.raises(ValueError,match='corrected_question_outside_reviewed_values'):
        validate_lesson(load_catalog(),l,read_json(DIRECTORY/'grade9_paragraph40_review.json'))


def test_batch34_preserves168_and_awards120xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:168]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=3360
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8)}
    g9=client.get(PREFIX+'/catalog?grade=9').json()['lessons']
    assert g9[35]['state']=='available' and all(l['state']=='locked' for l in g9[36:])
    for l in docs[168:174]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==3480
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==174
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert all(l['state']=='completed' for l in client.get(PREFIX+'/catalog?grade=9').json()['lessons'][:41])
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
