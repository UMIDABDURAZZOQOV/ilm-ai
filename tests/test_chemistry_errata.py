"""A finite source-backed erratum is required; no blanket source-hold bypass."""
from copy import deepcopy
import hashlib
import json

import pytest

from services import chemistry_errata as errata
from services.chemistry_validation import load_catalog,validate_catalog,source_is_blocked


def resolved_catalog():
    catalog=deepcopy(load_catalog())
    row=next(r for r in catalog['books'][2]['records'] if r['id']==errata.TOPIC_ID)
    row['source_review_hold'].update(status='resolved_by_reviewed_erratum',original_status='open',resolution_id=errata.ERRATUM_ID)
    row['reviewed_erratum_ids']=[errata.ERRATUM_ID]
    row['fact_review_status']='reviewed_with_erratum'
    return catalog,row


def fact_fixture():
    catalog,row=resolved_catalog();item=errata.reviewed_erratum(catalog)
    proofs=[r for r in item['evidence'] if (r['topic_id'],r['printed_pages'][0]) in {
        (errata.TOPIC_ID,186),('ch9-paragraph01',11),('ch8-paragraph23',96)}]
    fact=dict(claim='Cl — VIIA bosh guruhcha. Tashqi konfiguratsiya 3s2 3p5.',
              verified_answers=['VIIA','3s2 3p5'],source_refs=deepcopy(proofs),
              reviewed_erratum_ids=[errata.ERRATUM_ID],
              reviewed_erratum_claim_ids=['cl_group','cl_outer_configuration'])
    return catalog,row,fact,{r['review_id']:deepcopy(r) for r in proofs}


def test_original_hold_can_resolve_only_with_pinned_independent_evidence():
    catalog,row=resolved_catalog()
    validate_catalog(catalog)
    assert not source_is_blocked(catalog,row)
    item=errata.validate_resolution(catalog,row)
    assert item['resolves_hold_id']==row['source_review_hold']['id']
    assert {(r['topic_id'],r['printed_pages'][0]) for r in item['evidence']}==errata.EXPECTED_EVIDENCE
    assert all(not book['course_ready'] for book in catalog['books'])


@pytest.mark.parametrize('mutation',['drop_history','unknown_id','wrong_status','drop_resolution','unreviewed_status','no_link','wrong_history','wrong_page'])
def test_forged_or_partial_resolution_is_rejected(mutation):
    catalog,row=resolved_catalog()
    if mutation=='drop_history':row.pop('source_review_hold')
    if mutation=='unknown_id':row['reviewed_erratum_ids']=['invented']
    if mutation=='wrong_status':row['source_review_hold']['status']='approved'
    if mutation=='drop_resolution':row['source_review_hold'].pop('resolution_id')
    if mutation=='unreviewed_status':row['fact_review_status']='reviewed'
    if mutation=='no_link':row.pop('reviewed_erratum_ids')
    if mutation=='wrong_history':row['source_review_hold']['original_status']='reviewed'
    if mutation=='wrong_page':row['source_review_hold']['printed_pages']=[187]
    with pytest.raises(ValueError,match='known_source_conflict'):validate_catalog(catalog)


def test_unknown_topic_cannot_acquire_an_erratum_override():
    catalog=deepcopy(load_catalog())
    next(r for r in catalog['books'][2]['records'] if r['id']=='ch9-paragraph39')['reviewed_erratum_ids']=[errata.ERRATUM_ID]
    with pytest.raises(ValueError,match='unsupported_source_erratum'):validate_catalog(catalog)


@pytest.mark.parametrize('mutation',['digest','source_identity','page','ocr','future','correction','empty_corroboration'])
def test_erratum_manifest_is_pinned_and_structurally_checked(tmp_path,monkeypatch,mutation):
    catalog=load_catalog();data=json.loads((errata.DIRECTORY/'chemistry_reviewed_errata.json').read_text(encoding='utf8'))
    item=data['errata'][0]
    if mutation=='source_identity':item['evidence'][1]['file_name']='kimyo_9_uzb.pdf-unknown'
    if mutation=='page':item['evidence'][1]['regions']=['left']
    if mutation=='ocr':item['evidence'][1]['verification']='ocr_candidate'
    if mutation=='future':item['evidence'][1]['topic_id']='ch9-paragraph41'
    if mutation=='correction':item['corrections'][-1]['verified_values']=['3s2']
    if mutation=='empty_corroboration':item['corrections'][-1]['required_evidence']=[]
    raw=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf8')
    if mutation=='digest':raw+=b' '
    (tmp_path/'chemistry_reviewed_errata.json').write_bytes(raw)
    monkeypatch.setattr(errata,'DIRECTORY',tmp_path)
    # A changed digest always fails in production. Other mutations are checked
    # behind that boundary too; only this test temporarily re-pins its fixture.
    if mutation!='digest':monkeypatch.setattr(errata,'MANIFEST_SHA256',hashlib.sha256(raw).hexdigest())
    with pytest.raises(ValueError,match='reviewed_erratum'):errata.reviewed_erratum(catalog)


def test_corrected_fact_retains_original_and_earlier_book_proofs():
    catalog,_,fact,pages=fact_fixture()
    errata.validate_fact_erratum(catalog,fact,pages)
    assert any(r['file_name']=='kimyo_8_uzb.pdf' for r in fact['source_refs'])


@pytest.mark.parametrize('mutation',['no_id','unknown_claim','no_claim','missing_proof','wrong_value','image_hash','original_error','unrelated','open_hold'])
def test_fact_cannot_use_erratum_as_a_generic_override(mutation):
    catalog,row,fact,pages=fact_fixture()
    if mutation=='no_id':fact.pop('reviewed_erratum_ids')
    if mutation=='unknown_claim':fact['reviewed_erratum_claim_ids']=['all-science']
    if mutation=='no_claim':fact['reviewed_erratum_claim_ids']=[]
    if mutation=='missing_proof':fact['source_refs']=fact['source_refs'][:1]
    if mutation=='wrong_value':fact['verified_answers'].append('II')
    if mutation=='image_hash':next(iter(pages.values()))['page_image_sha256']='0'*64
    if mutation=='original_error':fact['claim']='Cl — II guruh.'
    if mutation=='unrelated':fact['source_refs']=fact['source_refs'][1:]
    if mutation=='open_hold':row['source_review_hold']['status']='open'
    with pytest.raises(ValueError):errata.validate_fact_erratum(catalog,fact,pages)


@pytest.mark.parametrize('answer',['VIIA','VII'])
def test_corrected_question_uses_one_finite_claim(answer):
    _,_,fact,_=fact_fixture()
    question=dict(fact_ids=['cl'],reviewed_erratum_claim_id='cl_group',
                  grading_spec=dict(verified_answer=answer,aliases=['VIIA','VII']))
    errata.validate_question_erratum(question,{'cl':fact})


@pytest.mark.parametrize('mutation',['missing','foreign','mixed_answer','wrong_alias','unrelated'])
def test_question_cannot_borrow_other_corrected_fact_values(mutation):
    _,_,fact,_=fact_fixture()
    question=dict(fact_ids=['cl'],reviewed_erratum_claim_id='cl_group',
                  grading_spec=dict(verified_answer='VIIA',aliases=['VIIA']))
    if mutation=='missing':question.pop('reviewed_erratum_claim_id')
    if mutation=='foreign':question['reviewed_erratum_claim_id']='ca_group'
    if mutation=='mixed_answer':question['grading_spec']['verified_answer']='2'
    if mutation=='wrong_alias':question['grading_spec']['aliases'].append('II')
    if mutation=='unrelated':fact.pop('reviewed_erratum_ids')
    with pytest.raises(ValueError):errata.validate_question_erratum(question,{'cl':fact})
