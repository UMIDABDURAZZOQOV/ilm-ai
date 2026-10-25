"""Finite, digest-pinned textbook corrections; no automatic or user-payload override."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

DIRECTORY = Path(__file__).resolve().parents[1] / 'scripts/curriculum/chemistry'
MANIFEST_SHA256 = 'a7ebf833f3a98ddb3319522e1411a73e051939c371f1f237bc88c33931ffb8bc'
ERRATUM_ID = 'ch9-p40-page186-reviewed-configuration-erratum'
HOLD_ID = 'ch9-p40-page186-configuration-conflict'
TOPIC_ID = 'ch9-paragraph40'
EXPECTED_VALUES = {
    'be_group': ['Be', 'II', 'IIA', '2'],
    'be_outer_configuration': ['Be', '2s2', '1s2 2s2', '2', '4'],
    'ca_group': ['Ca', 'II', 'IIA', '2'],
    'ca_outer_configuration': ['Ca', '4s2', '1s2 2s2 2p6 3s2 3p6 4s2', '2', '20'],
    'cl_group': ['Cl', 'VII', 'VIIA', '7'],
    'cl_outer_configuration': ['Cl', '3s2 3p5', '1s2 2s2 2p6 3s2 3p5', '7', '17', '3', '5', '2'],
}
EXPECTED_EVIDENCE = {
    ('ch9-paragraph40', 186), ('ch9-paragraph01', 9), ('ch9-paragraph01', 11),
    ('ch9-paragraph23', 109), ('ch8-paragraph11', 49),
    ('ch8-paragraph12', 52), ('ch8-paragraph23', 96),
}


def _require(condition, code):
    if not condition:
        raise ValueError(code)


def _proof_location(proof):
    pages = proof.get('printed_pages')
    _require(type(pages) is list and len(pages) == 1 and type(pages[0]) is int,
             'reviewed_erratum_evidence_page_required')
    return proof.get('topic_id'), pages[0]


def reviewed_erratum(catalog, identifier=ERRATUM_ID):
    _require(identifier == ERRATUM_ID, 'unknown_reviewed_erratum')
    path = DIRECTORY / 'chemistry_reviewed_errata.json'
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise ValueError('reviewed_erratum_manifest_required') from error
    _require(hashlib.sha256(raw).hexdigest() == MANIFEST_SHA256,
             'reviewed_erratum_digest_mismatch')
    manifest = json.loads(raw)
    _require(manifest.get('schema_version') == 1 and manifest.get('subject') == 'kimyo'
             and type(manifest.get('errata')) is list and len(manifest['errata']) == 1,
             'reviewed_erratum_manifest_schema')
    item = manifest['errata'][0]
    _require(item.get('id') == ERRATUM_ID and item.get('status') == 'reviewed_erratum'
             and item.get('topic_id') == TOPIC_ID and item.get('resolves_hold_id') == HOLD_ID
             and item.get('affected_printed_pages') == [186]
             and item.get('affected_pdf_pages') == [186]
             and item.get('affected_regions') == ['full']
             and item.get('review_method') == 'original_page_images_and_independent_supplied_passage_comparison'
             and item.get('authorization', {}).get('kind') == 'explicit_user_erratum_instruction',
             'reviewed_erratum_scope_mismatch')
    rows = item.get('corrections', [])
    _require(len(rows) == len(EXPECTED_VALUES)
             and {r.get('id'): r.get('verified_values') for r in rows} == EXPECTED_VALUES,
             'reviewed_erratum_correction_mismatch')
    books = {r['id']: b for b in catalog['books'] for r in b['records']}
    records = {r['id']: r for b in catalog['books'] for r in b['records']}
    _require(item.get('source_sha256') == books[TOPIC_ID]['sha256'],
             'reviewed_erratum_source_digest_mismatch')
    evidence = item.get('evidence', [])
    _require(len(evidence) == len(EXPECTED_EVIDENCE)
             and {_proof_location(r) for r in evidence}
             == EXPECTED_EVIDENCE, 'reviewed_erratum_evidence_set_mismatch')
    for proof in evidence:
        record = records.get(proof.get('topic_id'));book = books.get(proof.get('topic_id'))
        page = proof.get('printed_pages', [None])[0]
        _require(book and record and record['kind'] == 'paragraph'
                 and (book['grade'] < 9 or record['id'] == TOPIC_ID or record['sequence'] < 40)
                 and proof.get('book_id') == book['id']
                 and proof.get('sha256') == book['sha256']
                 and proof.get('file_name') == book['file_name']
                 and proof.get('book_title') == book['title']
                 and proof.get('authors') == book['authors'] and proof.get('year') == book['year']
                 and proof.get('topic_title') == record['title']
                 and proof.get('paragraph') == record['number']
                 and record['printed_start'] <= page <= record['printed_end']
                 and proof.get('printed_pages') == [page] == proof.get('pdf_pages')
                 and proof.get('regions') == ['full']
                 and proof.get('verification') == 'page_image_reviewed'
                 and re.fullmatch(r'[0-9a-f]{64}', proof.get('page_image_sha256', '')),
                 'reviewed_erratum_original_evidence_required')
    for correction in rows:
        required = correction.get('required_evidence', [])
        _require(required and all((r.get('topic_id'), r.get('printed_page'))
                                  in EXPECTED_EVIDENCE - {(TOPIC_ID, 186)} for r in required),
                 'reviewed_erratum_corroboration_required')
    return item


def validate_resolution(catalog, record):
    """Keep the original issue; resolve only through this exact reviewed artifact."""
    _require(record.get('id') == TOPIC_ID
             and record.get('reviewed_erratum_ids') == [ERRATUM_ID]
             and record.get('source_review_hold', {}).get('id') == HOLD_ID
             and record.get('source_review_hold', {}).get('status') == 'resolved_by_reviewed_erratum'
             and record.get('source_review_hold', {}).get('resolution_id') == ERRATUM_ID
             and record.get('source_review_hold', {}).get('original_status') == 'open'
             and record.get('source_review_hold', {}).get('printed_pages') == [186]
             and record.get('source_review_hold', {}).get('pdf_pages') == [186]
             and record.get('source_review_hold', {}).get('region') == 'full'
             and record.get('source_review_hold', {}).get('kind') == 'internal_scientific_contradiction'
             and record.get('fact_review_status') == 'reviewed_with_erratum',
             'known_source_conflict_requires_reviewed_erratum')
    return reviewed_erratum(catalog)


def validate_fact_erratum(catalog, fact, reviewed_pages):
    refs = fact.get('source_refs', [])
    affected = any(r.get('topic_id') == TOPIC_ID and 186 in r.get('printed_pages', []) for r in refs)
    identifiers = fact.get('reviewed_erratum_ids', [])
    claims = fact.get('reviewed_erratum_claim_ids', [])
    if not affected:
        _require(not identifiers and not claims, 'erratum_cannot_override_unrelated_fact')
        return
    _require(identifiers == [ERRATUM_ID] and type(claims) is list and claims
             and len(claims) == len(set(claims)) and set(claims) <= EXPECTED_VALUES.keys(),
             'affected_fact_requires_reviewed_erratum')
    item = reviewed_erratum(catalog)
    record = next(r for b in catalog['books'] for r in b['records'] if r['id'] == TOPIC_ID)
    validate_resolution(catalog, record)
    rows = {r['id']: r for r in item['corrections']}
    required = {(TOPIC_ID, 186)} | {
        (r['topic_id'], r['printed_page']) for claim in claims for r in rows[claim]['required_evidence']
    }
    actual = {(r['topic_id'], r['printed_pages'][0]) for r in refs}
    _require(required <= actual, 'corrected_fact_requires_corroborating_pages')
    pinned_images = {(r['topic_id'], r['printed_pages'][0]): r['page_image_sha256']
                     for r in item['evidence']}
    for ref in refs:
        location = (ref['topic_id'], ref['printed_pages'][0])
        if location in required:
            proof = reviewed_pages.get(ref['review_id'], {})
            _require(proof.get('page_image_sha256') == pinned_images[location],
                     'corrected_fact_image_evidence_mismatch')
    values = {v for claim in claims for v in EXPECTED_VALUES[claim]}
    _require(set(fact.get('verified_answers', [])) <= values,
             'corrected_fact_outside_reviewed_values')
    if any(claim.startswith('cl_') for claim in claims):
        _require(not re.search(r'\bCl\s*(?:—|:|-)?\s*II(?:A)?\b', fact.get('claim', '')),
                 'erratum_cannot_reintroduce_original_error')


def validate_question_erratum(question, facts):
    """Bind a corrected answer to one claim, not the union of unrelated values."""
    linked = [facts[fid] for fid in question['fact_ids']
              if facts[fid].get('reviewed_erratum_ids')]
    claim = question.get('reviewed_erratum_claim_id')
    if not linked:
        _require(claim is None, 'erratum_cannot_override_unrelated_question')
        return
    claims = {identifier for fact in linked for identifier in fact['reviewed_erratum_claim_ids']}
    _require(claim in claims and claim in EXPECTED_VALUES,
             'corrected_question_requires_exact_erratum_claim')
    normalize = lambda value: re.sub(r'\s+', '', value).casefold()
    values = {normalize(value) for value in EXPECTED_VALUES[claim]}
    spec = question['grading_spec']
    _require(normalize(spec['verified_answer']) in values
             and all(normalize(value) in values for value in spec.get('aliases', [])),
             'corrected_question_outside_reviewed_values')
