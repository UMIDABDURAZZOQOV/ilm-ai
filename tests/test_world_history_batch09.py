"""Grade6 completion and exact, reviewed predecessor facts in the final review."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
from uuid import uuid4

import pytest

from test_world_history_lesson import history, PREFIX, answer_for, send, finish  # noqa: F401
from services import world_history_lessons as lessons_module
from services.world_history_lessons import load_lessons, validate_lesson
from services.world_history_validation import DIRECTORY, fingerprint, load_catalog, read_json
from services.chemistry_grading import grade_answer
from services.models import User
from services.world_history_models import WorldHistoryProgress


def pair(number=46):
    return deepcopy(load_lessons()[number-1]),read_json(DIRECTORY/f'grade6_paragraph{number:02d}_review.json')


def refresh(d,r):
    r.update(lesson_sha256=fingerprint(d),approved_content_sha256=fingerprint(d['content']),
             approved_assessments_sha256=fingerprint(d['assessments']),
             approved_fact_sha256={i:fingerprint(f) for i,f in d['facts'].items()},
             approved_answer_targets={q['key']:{'fact_ids':q['fact_ids'],'verified_answer':q['grading_spec']['verified_answer'],
                                               'aliases':q['grading_spec'].get('aliases',[])} for q in d['assessments']})


def test_grade6_complete_exact_counts_and_ancillary_source_identity():
    documents=load_lessons();assert len(documents)==46
    batch=documents[41:46]
    assert [len(d['facts']) for d in batch]==[14,12,20,10,14]
    assert [len(d['content']['cards']) for d in batch]==[6,6,8,5,7]
    assert [len(d['assessments']) for d in batch]==[10,10,10,6,12]
    assert sum(q['response_kind']=='short_text' for d in batch for q in d['assessments'])==18
    assert sum(len(d['assessments']) for d in documents)==446
    assert [d['topic_id'] for d in batch[-2:]]==['wh6-conclusion','wh6-final-review']
    assert all(ref['paragraph'] is None for ref in batch[-2]['source_refs'])
    assert batch[-1]['source_refs'][0]['paragraph'] is None
    assert batch[-1]['source_refs'][0]['pdf_pages']==[184]
    assert len(batch[-1]['source_context_ids'])==9
    for d in batch:
        for q in d['assessments']:
            assert grade_answer(q['grading_spec'],answer_for(q))=='correct'
            assert all(d['facts'][i]['automatic_assessment_allowed'] for i in q['fact_ids'])
        assert all(not r['automatic_score'] for r in d['content']['reflections'])
    assert not batch[-1]['facts']['review-participation']['automatic_assessment_allowed']
    assert not batch[0]['facts']['caesar_power']['automatic_assessment_allowed']
    assert not batch[1]['facts']['outsider_label']['automatic_assessment_allowed']
    assert not batch[2]['facts']['narratives']['automatic_assessment_allowed']
    assert not batch[3]['facts']['publication']['automatic_assessment_allowed']


def test_review_borrows_exact_prior_facts_and_original_regions():
    documents=load_lessons();d,r=pair();prior={p['topic_id']:p for p in documents[:44]}
    assert validate_lesson(load_catalog(),d,r)==d
    for local,binding in r['approved_context_fact_bindings'].items():
        p=prior[binding['topic_id']];f=p['facts'][binding['fact_id']]
        assert r['approved_context_sha256'][p['topic_id']]==fingerprint(p)
        assert dict(d['facts'][local],fact_id=f['fact_id'])==f
        assert all(ref['pdf_pages']!=[184] for ref in d['facts'][local]['source_refs'])
    assert len(r['approved_context_fact_bindings'])==12


@pytest.mark.parametrize('change',['lesson_digest','binding','claim','alias','assessability','origin','future','cross_book'])
def test_review_context_cannot_expand_approved_knowledge(change):
    d,r=pair()
    if change=='lesson_digest':r['approved_context_sha256']['wh6-topic01']='0'*64
    if change=='binding':r['approved_context_fact_bindings'].pop('review-stylus')
    if change=='claim':d['facts']['review-mosaic']['claim']='Unreviewed meaning imported from memory.'
    if change=='alias':d['facts']['review-coloni']['approved_aliases'].append('Koloniyalar')
    if change=='assessability':d['facts']['review-participation']['automatic_assessment_allowed']=True
    if change=='origin':d['facts']['review-stylus']['source_refs']=[d['source_refs'][0]]
    if change=='future':d['source_context_ids'].append('wh6-final-review')
    if change=='cross_book':d['source_context_ids'].append('wh7-topic01')
    refresh(d,r)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_predecessor_must_be_in_explicit_digest_pinned_index(monkeypatch):
    d,r=pair();original=lessons_module.read_json
    def without_predecessor(path):
        value=original(path)
        if Path(path).name=='world_history_lessons.json':
            value['lessons']=[i for i in value['lessons'] if i['file']!='grade6_paragraph24.json']
        return value
    monkeypatch.setattr(lessons_module,'read_json',without_predecessor)
    with pytest.raises(ValueError,match='context_requires_unique_indexed_predecessor'):
        validate_lesson(load_catalog(),d,r)


def test_regular_numbered_lesson_cannot_borrow_arbitrary_prior_topic():
    d,r=pair(44);d['source_context_ids']=['wh6-topic01'];refresh(d,r)
    with pytest.raises(ValueError,match='only_ancillary_review'):
        validate_lesson(load_catalog(),d,r)


@pytest.mark.parametrize('number',[42,43,44])
def test_final_numbered_topic_requires_its_exact_opening_region(number):
    d,r=pair(number);d['source_refs'][0]['regions']=['topic_body'];r['source_pages'][0]['region']='topic_body';refresh(d,r)
    with pytest.raises(ValueError):validate_lesson(load_catalog(),d,r)


def test_catalog_finalizer_preserves_only_explicit_ancillary_readiness(tmp_path,monkeypatch):
    spec=importlib.util.spec_from_file_location('history_finalize',DIRECTORY.parents[1]/'finalize_world_history_catalog.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    data=tmp_path/'data';data.mkdir();docs=tmp_path/'docs/world_history';docs.mkdir(parents=True)
    catalog=load_catalog()
    for name,value in [('world_history_sources.json',catalog),('world_history_page_inventory.json',read_json(DIRECTORY/'world_history_page_inventory.json'))]:
        (data/name).write_text(json.dumps(value),encoding='utf8')
    monkeypatch.setattr(module,'DATA',data);monkeypatch.setattr(module,'ROOT',tmp_path)
    module.main();result=read_json(data/'world_history_sources.json')
    assert result['implemented_lessons']==46 and result['remaining_lessons']==173
    assert all(u['interactive_status']=='reviewed_preview_ready' for u in result['books'][0]['teaching_units'])
    ancillary={a['id']:a for a in result['books'][0]['ancillary_records']}
    for identifier in ['wh6-conclusion','wh6-final-review']:
        assert ancillary[identifier]['fact_review']=='reviewed_with_scope_limits'
    grade8=next(a for a in result['books'][2]['ancillary_records'] if a['id']=='wh8-conclusion')
    assert grade8['fact_review']=='not_reviewed' and 'interactive_status' not in grade8
    assert all(not b['course_ready'] and not b['content_reviewed'] for b in result['books'])


def test_all_forty_six_ordered_units_and920_xp_once_preserve_old_accounts(history):
    client,factory,_=history;documents=load_lessons()
    initial=client.get(PREFIX+'/catalog').json()
    assert initial['grade_content_complete'] and not initial['course_complete']
    assert not initial['source_review_pending']
    assert client.post(f"{PREFIX}/lessons/{documents[44]['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())}).status_code==403
    for d in documents:
        response=client.post(f"{PREFIX}/lessons/{d['key']}/start",json={'assessment_version':2,'request_id':str(uuid4())})
        assert response.status_code==200,response.text
        attempt=response.json()
        for q in d['assessments']:
            response=send(client,attempt,q,answer_for(q));assert response.status_code==200 and response.json()['is_correct']
        response=finish(client,attempt);assert response.status_code==200 and response.json()['xp_awarded']==20
        assert finish(client,attempt).json()==response.json()
    with factory() as db:
        assert db.get(User,1).xp_total==920
        assert db.query(WorldHistoryProgress).filter_by(user_id=1).count()==46
        assert db.get(User,42).xp_total==137
    completed=client.get(PREFIX+'/catalog').json()
    assert completed['implemented_sections']==completed['source_sections']==46
    assert all(r['state']=='completed' for r in completed['lessons'])
    next_grade=client.get(PREFIX+'/catalog',params={'grade':7}).json()
    assert next_grade['grade']==7 and next_grade['implemented_sections']==0 and next_grade['source_sections']==44
    assert not next_grade['grade_content_complete'] and not next_grade['course_complete']
    assert len(next_grade['source_units'])==44 and next_grade['bibliography']['year']==2017
