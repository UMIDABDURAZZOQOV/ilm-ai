"""Source-bound digital grade9 activities never invent sample measurements."""
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

TOPICS=[f'ch9-practical{n:02}' for n in range(1,4)]+[f'ch9-laboratory{n:02}' for n in range(1,5)]


def test_batch35_source_order_and_shared_types():
    lessons=load_lessons()[174:181]
    assert [l['topic_id'] for l in lessons]==TOPICS
    assert [l['sequence'] for l in lessons]==list(range(42,49))
    assert sum(len(l['content']['cards']) for l in lessons)==61
    assert Counter(q['response_kind'] for l in lessons for q in l['assessments'])=={
        'concept_selection':28,'short_text':14,'numeric_value':16,'chemical_formula':7,'chemical_equation':20}
    assert all(l['content']['examples'] for l in lessons)
    assert all(not b['course_ready'] for b in load_catalog()['books'])
    l=lessons[4]
    assert any(r['topic_id']=='ch9-paragraph12' and r['printed_pages']==[61] for r in l['facts']['kaolin']['source_refs'])
    assert all(q['response_kind']=='concept_selection' for l in lessons for q in l['assessments'] if '·' in q['grading_spec']['verified_answer'])
    assert not any('Mohs' in a for f in l['facts'].values() for a in f['verified_answers'])


@pytest.mark.parametrize('topic',TOPICS)
def test_batch35_review_cannot_disappear(topic):
    catalog=deepcopy(load_catalog())
    next(r for r in catalog['books'][2]['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(catalog)


@pytest.mark.parametrize('slug,fid,value,error',[
    ('practical01','soil','Tuproqdagi oq cho‘kma doim AgCl','unknown_soil_precipitate'),
    ('practical02','elimination','Nitrat uchun universal sinov','closed_candidate_elimination'),
    ('laboratory02','conclusion','Mohs 7','missing_mineral_hardness')])
def test_unmeasured_or_unqualified_key_is_rejected(slug,fid,value,error):
    l=deepcopy(read_json(DIRECTORY/f'grade9_{slug}.json'))
    l['facts'][fid]['verified_answers'].append(value)
    with pytest.raises(ValueError,match=error):
        validate_lesson(load_catalog(),l,read_json(DIRECTORY/f'grade9_{slug}_review.json'))


@pytest.mark.parametrize('slug,fid,expected,value,code',[
    ('practical01','amount','0.448','0,448','correct'),
    ('practical01','amount','0.02','2e-2','correct'),
    ('practical01','water','H2CO3','H2CO3','correct'),
    ('practical02','elimination','NaNO3','NaNO3','correct'),
    ('practical02','forms','0','0','correct'),
    ('practical02','ratio','0.10','0,1','correct'),
    ('practical03','ratio','0.10','0.10','correct'),
    ('practical03','zinchydroxide','Zn(OH)2+2HCl=ZnCl2+2H2O','Zn(OH)2+2HCl=ZnCl2+H2O','atom_imbalance'),
    ('laboratory01','model','0.05','0.05','correct'),
    ('laboratory01','third','6','6','correct'),
    ('laboratory02','kaolin','9','9','correct'),
    ('laboratory02','feldspar','16','16','correct'),
    ('laboratory03','count','14','14','correct'),
    ('laboratory03','crystal','PbO','PbO','correct'),
    ('laboratory04','table','660.5','660,5','correct'),
    ('laboratory04','difference','422.5','422.5','correct'),
    ('laboratory04','difference','456','456','correct')])
def test_batch35_existing_grader(slug,fid,expected,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch9-{slug}')
    q=next(q for q in l['assessments'] if fid in q['fact_ids'] and q['grading_spec']['expected']==expected)
    assert grade_answer(q['grading_spec'],{'value':value})==code


def test_batch35_preserves174_and_awards140xp_once(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:174]:db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=3480
    old={g:client.get(PREFIX+f'/catalog?grade={g}').json() for g in (7,8)}
    g9=client.get(PREFIX+'/catalog?grade=9').json()['lessons']
    assert g9[41]['state']=='available' and all(l['state']=='locked' for l in g9[42:])
    for l in docs[174:181]:
        response=client.post(f"{PREFIX}/lessons/{l['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text;a=response.json()
        assert 'grading_spec' not in str(a) and 'verified_answers' not in str(a)
        for q in l['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        result=finish(client,a);assert result.status_code==200 and result.json()['xp_awarded']==20
        assert finish(client,a).json()==result.json()
    with factory() as db:
        assert db.get(User,1).xp_total==3620
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==181
        assert (db.get(User,42).xp_total,db.get(User,42).streak_days)==(137,3)
    assert all(l['state']=='completed' for l in client.get(PREFIX+'/catalog?grade=9').json()['lessons'][:48])
    for g,c in old.items():assert client.get(PREFIX+f'/catalog?grade={g}').json()==c
