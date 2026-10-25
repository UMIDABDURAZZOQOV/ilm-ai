"""Earlier textbook citations retain digest, order, bibliography and spread checks."""
from copy import deepcopy
from pathlib import Path

import pytest

import services.chemistry_validation as validation
from services.chemistry_validation import DIRECTORY,load_catalog,load_lessons,read_json,validate_lesson


def linked_context(grade=8,page=7):
    lesson=deepcopy(read_json(DIRECTORY/'grade9_paragraph01.json'))
    review=deepcopy(read_json(DIRECTORY/'grade9_paragraph01_review.json'))
    old=read_json(DIRECTORY/f'grade{grade}_paragraph01.json')
    oldreview=read_json(DIRECTORY/f'grade{grade}_paragraph01_review.json')
    ref=deepcopy(next(r for r in old['source_refs'] if r['printed_pages']==[page]))
    evidence=deepcopy(next(r for r in oldreview['source_pages'] if r['review_id']==ref['review_id']))
    lesson.setdefault('source_context_ids',[]).append(ref['topic_id'])
    # This fixture adds a structural source anchor; no new science or indexed data.
    lesson['source_refs'].append(ref);lesson['content']['source_refs']=deepcopy(lesson['source_refs'])
    review['source_pages'].append(evidence)
    return lesson,review


def test_earlier_grade_link_validates_its_own_book_not_current_grade():
    l,r=linked_context();b,t=validate_lesson(load_catalog(),l,r)
    assert b['grade']==9 and t['id']=='ch9-paragraph01'
    assert l['source_refs'][-1]['book_id']!=l['book_id']


@pytest.mark.parametrize('page,region,pdf',[(3,'right',2),(4,'left',3),(7,'right',4),(8,'left',5)])
def test_grade7_spread_mapping_remains_exact_in_grade9_context(page,region,pdf):
    l,r=linked_context(7,page);validate_lesson(load_catalog(),l,r)
    assert l['source_refs'][-1]['regions']==[region] and l['source_refs'][-1]['pdf_pages']==[pdf]
    l['source_refs'][-1]['regions']=['full']
    with pytest.raises(ValueError,match='claim_pdf_printed_region_mismatch'):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('field,value,error',[
 ('sha256','0'*64,'claim_source_identity_mismatch'),
 ('book_id','forged-book','claim_source_identity_mismatch'),
 ('file_name','kimyo_9_uzb.pdf','claim_source_identity_mismatch'),
 ('book_title','other edition','claim_bibliography_mismatch'),
 ('authors',['unreviewed author'],'claim_bibliography_mismatch'),
 ('year',2026,'claim_bibliography_mismatch'),
 ('topic_title','wrong paragraph','claim_bibliography_mismatch'),
 ('paragraph',2,'claim_source_identity_mismatch'),
 ('pdf_pages',[8],'claim_pdf_printed_region_mismatch')])
def test_cross_grade_bibliography_and_page_forgery_rejected(field,value,error):
    l,r=linked_context();l['source_refs'][-1][field]=value
    with pytest.raises(ValueError,match=error):validate_lesson(load_catalog(),l,r)


@pytest.mark.parametrize('identifier,error',[
 ('ch10-paragraph01','source_context_grade_must_precede'),
 ('ch8-chapter01','earlier_grade_teaching_context_only'),
 ('ch8-laboratory99','unknown_or_blocked_linked_source'),
 ('ch9-paragraph40','unknown_or_blocked_linked_source')])
def test_future_unreviewed_container_and_blocked_sources_cannot_be_context(identifier,error):
    l=deepcopy(read_json(DIRECTORY/'grade9_paragraph01.json'));r=read_json(DIRECTORY/'grade9_paragraph01_review.json')
    l['source_context_ids']=[identifier]
    catalog=deepcopy(load_catalog())
    if identifier=='ch9-paragraph40':
        source=next(s for s in catalog['books'][2]['records'] if s['id']==identifier)
        source['source_review_hold']['status']='open'
        source['fact_review_status']='blocked_source_conflict'
        source.pop('reviewed_erratum_ids',None)
    with pytest.raises(ValueError,match=error):validate_lesson(catalog,l,r)


def test_context_must_exist_in_validated_manifest_prefix():
    l,r=linked_context()
    with pytest.raises(ValueError,match='earlier_grade_context_must_already_be_validated'):
        validate_lesson(load_catalog(),l,r,reviewed_context_topics=set())


@pytest.mark.parametrize('mode',['missing','changed_digest'])
def test_standalone_cross_context_requires_immutable_index_review(monkeypatch,mode):
    l,r=linked_context();read=validation.read_json
    def altered(path):
        v=read(path)
        if Path(path).name=='chemistry_lessons.json':
            if mode=='missing':v['lessons']=[i for i in v['lessons'] if i['file']!='grade8_paragraph01.json']
            else:next(i for i in v['lessons'] if i['file']=='grade8_paragraph01.json')['sha256']='0'*64
        return v
    monkeypatch.setattr(validation,'read_json',altered)
    with pytest.raises(ValueError,match='earlier_grade_context_must_be_reviewed_and_indexed|changed_context_requires_new_review'):
        validate_lesson(load_catalog(),l,r)


def test_all_current_immutable_lessons_keep_original_source_contract():
    assert len(load_lessons())>=138
