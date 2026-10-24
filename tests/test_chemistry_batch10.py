"""Reviewed oxide applications/bases and retained source contradictions."""
from copy import deepcopy
from uuid import uuid4

import pytest

from services.chemistry_grading import grade_answer
from services import chemistry_curriculum as importer
from services.chemistry_models import ChemistryProgress
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,readiness,validate_catalog,validate_lesson
from services.models import User
from services.study import utcnow
from test_chemistry_lesson import reviewed_chemistry_documents,chemistry,PREFIX,send,finish,answer_for


def test_batch10_original_order_exact_boundaries_and_context():
    docs=load_lessons()[41:46]
    assert [l['topic_id'] for l in docs]==[f'ch7-paragraph{n}' for n in range(37,42)]
    assert [l['sequence'] for l in docs]==list(range(42,47))
    assert sum(len(l['content']['cards']) for l in docs)==29
    assert sum(len(l['assessments']) for l in docs)==43
    assert docs[0]['source_context_ids']==['ch7-paragraph20']
    ref=docs[0]['facts']['photosynthesis']['source_refs'][0]
    assert ref['paragraph']==20 and ref['printed_pages']==[60]
    expected=[{107,108,60},{109},{110},{111,112},{113,114}]
    for l,pages in zip(docs,expected):
        n=int(l['topic_id'].removeprefix('ch7-paragraph'))
        r=read_json(DIRECTORY/f"grade7_paragraph{n:02d}_review.json")
        assert {p['printed_page'] for p in r['source_pages']}==pages
        assert all(p['pdf_page']==p['printed_page']//2+1 for p in r['source_pages'])
    state=readiness(load_catalog(),load_lessons()[:46])[0]
    assert state['implemented_lessons']==46 and len(state['remaining_ids'])==28
    assert not state['course_ready']


@pytest.mark.parametrize('grade,topic',[(7,'ch7-paragraph37'),(9,'ch9-paragraph27')])
def test_cross_book_editorial_holds_cannot_be_removed(grade,topic):
    c=deepcopy(load_catalog())
    book=next(b for b in c['books'] if b['grade']==grade)
    next(r for r in book['records'] if r['id']==topic).pop('editorial_review_issues')
    with pytest.raises(ValueError,match='known_editorial_issue'):validate_catalog(c)


@pytest.mark.parametrize('name',['ametist','sapfir','yoqut','rubin'])
def test_disputed_gem_host_cannot_become_a_teaching_premise(name):
    l=deepcopy(load_lessons()[41]);r=read_json(DIRECTORY/'grade7_paragraph37_review.json')
    l['facts']['silicon']['claim']+=' '+name
    with pytest.raises(ValueError,match='unresolved_gem_host'):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('n,qn,value,code',[
    (38,5,'Al(OH)₃','correct'),(38,5,'AlOH3','incorrect'),
    (38,7,'2','correct'),(38,8,'2','incorrect'),
    (39,6,'Zn(OH)2','correct'),(39,8,'Fe(OH)2','incorrect'),
    (40,6,'2NiSO4+4NaOH=2Ni(OH)2+2Na2SO4','correct'),
    (40,6,'NiSO4+NaOH=Ni(OH)2+Na2SO4','atom_imbalance'),
    (40,8,'HCl+Mg(OH)2=H2O+Mg(OH)Cl','correct'),
    (40,8,'Mg(OH)2+2HCl=MgCl2+2H2O','incorrect_species'),
    (40,10,'CuCl2+NaOH=Cu(OH)Cl+NaCl','correct'),
    (41,8,'0,78','correct'),(41,8,'1.56','incorrect')])
def test_formula_grouping_partial_products_and_fixed_unit_ratio(n,qn,value,code,reviewed_chemistry_documents):
    l=next(l for l in reviewed_chemistry_documents if l['topic_id']==f'ch7-paragraph{n}')
    assert grade_answer(l['assessments'][qn-1]['grading_spec'],{'value':value})==code


def test_five_new_lessons_preserve41_completions_and_once_only_xp(chemistry):
    client,factory,_=chemistry;docs=load_lessons()
    with factory.begin() as db:
        for l in docs[:41]:
            db.add(ChemistryProgress(user_id=1,lesson_key=l['key'],best_score_pct=100,attempts=1,xp_earned=20,completed_at=utcnow()))
        db.get(User,1).xp_total=820
    for lesson in docs[41:46]:
        path=f"{PREFIX}/lessons/{lesson['key']}/start";payload={'assessment_version':2,'request_id':str(uuid4())}
        response=client.post(path,json=payload);assert response.status_code==200,response.text
        a=response.json();assert a['lesson_key']==lesson['key']
        assert client.post(path,json=payload).json()['attempt_id']==a['attempt_id']
        for q in lesson['assessments']:
            r=send(client,a,q,answer_for(q));assert r.status_code==200 and r.json()['is_correct'],r.text
        done=finish(client,a);assert done.status_code==200 and done.json()['xp_awarded']==20
        assert finish(client,a).json()==done.json()
    with factory() as db:
        assert db.get(User,1).xp_total==920
        assert db.query(ChemistryProgress).filter_by(user_id=1).count()==46
        old=db.get(User,42);assert (old.xp_total,old.streak_days)==(137,3)


def test_batch_import_revalidates_once_per_call_and_preserves_immutable_rows(chemistry,monkeypatch):
    _,factory,_=chemistry;original=importer.load_lessons;calls=[]
    def checked():
        calls.append(True)
        return original()
    monkeypatch.setattr(importer,'load_lessons',checked)
    with factory.begin() as db:
        rows=importer.import_reviewed_lessons(db)
        assert rows and all(not r['created'] for r in rows)
        assert len(calls)==1
        row=db.get(importer.ChemistryLesson,rows[0]['key']);row.title='Tampered QA row';db.flush()
        with pytest.raises(ValueError,match='published_chemistry_lesson_is_immutable'):
            importer.import_reviewed_lessons(db)
        assert len(calls)==2


def test_batch_import_validates_all_evidence_before_any_write(chemistry,monkeypatch):
    _,factory,_=chemistry;writes=[]
    def invalid():raise ValueError('changed_content_requires_new_review')
    monkeypatch.setattr(importer,'load_lessons',invalid)
    monkeypatch.setattr(importer,'_store_reviewed_lesson',lambda *args:writes.append(args))
    with factory.begin() as db:
        with pytest.raises(ValueError,match='changed_content_requires_new_review'):
            importer.import_reviewed_lessons(db)
    assert not writes
