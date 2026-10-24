"""Source-bound acid teaching, earlier review reuse and digital practical6."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services.chemistry_models import ChemistryProgress
from services import chemistry_validation as validation
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,readiness,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import chemistry,PREFIX,send,finish,answer_for


def test_batch11_original_order_pages_and_source_review_reuse():
    docs=load_lessons()[46:51]
    assert [l['topic_id'] for l in docs]==['ch7-paragraph42','ch7-paragraph43','ch7-paragraph44','ch7-practical06','ch7-paragraph45']
    assert [l['sequence'] for l in docs]==list(range(47,52))
    assert sum(len(l['content']['cards']) for l in docs)==39
    assert sum(len(l['assessments']) for l in docs)==53
    practical=docs[3]
    assert practical['source_context_ids']==['ch7-1']
    assert not practical.get('source_activity_ids')
    ref=practical['facts']['copper']['source_refs'][0]
    assert ref['topic_id']=='ch7-1' and ref['paragraph'] is None and ref['printed_pages']==[50]
    assert 'Temir(III)-oksid' in practical['facts']['purpose']['verified_answers']
    assert len({i for l in load_lessons() for i in l.get('source_activity_ids',[])})==7
    state=readiness(load_catalog(),load_lessons()[:51])[0]
    assert state['implemented_lessons']==51 and len(state['remaining_ids'])==23 and not state['course_ready']


@pytest.mark.parametrize('n',[42,43,44,45])
def test_scoped_acid_reviews_cannot_be_removed(n):
    c=deepcopy(load_catalog());r=next(r for r in c['books'][0]['records'] if r['id']==f'ch7-paragraph{n}')
    r.pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


@pytest.mark.parametrize('value',['HJ','KJ'])
def test_unresolved_legacy_iodine_notation_cannot_be_a_key(value):
    l=deepcopy(load_lessons()[46]);r=read_json(DIRECTORY/'grade7_paragraph42_review.json')
    l['facts']['simple']['verified_answers'].append(value)
    with pytest.raises(ValueError,match='unresolved_legacy_iodine'):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('fact,claim',[('phosphorus','H3PO3 uch negizli'),('others','H3BO3 bir negizli')])
def test_neither_held_nor_invented_alternative_basicity_is_verified(fact,claim):
    l=deepcopy(load_lessons()[46]);r=read_json(DIRECTORY/'grade7_paragraph42_review.json')
    l['facts'][fact]['claim']=claim
    with pytest.raises(ValueError,match='unresolved_acid_basicity'):validate_lesson(load_catalog(),l,r)


def test_future_chapter_review_cannot_be_an_earlier_context():
    l=deepcopy(load_lessons()[49]);r=read_json(DIRECTORY/'grade7_practical06_review.json')
    l['source_context_ids']=['ch7-8']
    with pytest.raises(ValueError,match='source_context_must_precede'):validate_lesson(load_catalog(),l,r)


def test_review_context_requires_an_actually_earlier_integrated_manifest(monkeypatch):
    real=validation.read_json
    def read(path):
        result=real(path)
        if path.name=='chemistry_lessons.json':
            result['lessons']=[r for r in result['lessons'] if r['file']!='grade7_paragraph16.json']
        return result
    monkeypatch.setattr(validation,'read_json',read)
    with pytest.raises(ValueError,match='review_context_must_already_be_integrated'):validation.load_lessons()


@pytest.mark.parametrize('offset,qn,value,code',[
    (0,7,'H₄P₂O₇','correct'),(0,8,'H2CrO4','incorrect'),
    (1,6,'H4P2O7','correct'),(1,8,'3','correct'),
    (2,11,'H3PO4+KOH=KH2PO4+H2O','correct'),
    (2,11,'H3PO4+3KOH=K3PO4+3H2O','incorrect_species'),
    (2,12,'CaO+2HNO3=H2O+Ca(NO3)2','correct'),
    (2,13,'Cu+4HNO3=Cu(NO3)2+2NO2+2H2O','correct'),
    (2,13,'Cu+HNO3=Cu(NO3)2+NO2+H2O','atom_imbalance'),
    (3,6,'2CuO+2H2SO4=2CuSO4+2H2O','correct'),
    (3,7,'4,9','correct'),(3,8,'8','correct'),(3,9,'0,9','correct'),
    (4,8,'HNO2','incorrect')])
def test_specific_formulas_partial_products_concentrated_case_and_original_ratio(offset,qn,value,code):
    l=load_lessons()[46+offset]
    assert grade_answer(l['assessments'][qn-1]['grading_spec'],{'value':value})==code


def test_five_new_lessons_preserve46_completions_and_once_only_xp(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:46]:
            db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=920
    for lesson in docs[46:51]:
        path=f"{PREFIX}/lessons/{lesson['key']}/start";payload={'assessment_version':2,'request_id':str(uuid4())}
        response=client.post(path,json=payload);assert response.status_code==200,response.text
        a=response.json();assert a['lesson_key']==lesson['key']
        assert client.post(path,json=payload).json()['attempt_id']==a['attempt_id']
        for q in lesson['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        done=finish(client,a);assert done.status_code==200 and done.json()['xp_awarded']==20
        assert finish(client,a).json()==done.json()
    with factory() as db:
        assert db.get(User,1).xp_total==1020
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==51
        old=db.get(User,42);assert (old.xp_total,old.streak_days)==(137,3)
