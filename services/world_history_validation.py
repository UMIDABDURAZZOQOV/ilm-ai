"""Pure source inventory checks. Catalogue inspection is not lesson approval.

No DB/application, network or AI imports. Original images remain private.
Unreviewed OCR, uncertain interpretations and pending sections fail closed.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / 'scripts/curriculum/world_history'
PINNED = {
    6: ('qadimgi_dunyo_tarixi_6_uzb.pdf', 'aae8c182fb084bd58f98d06bd46542d5f33aeda9787dc6ba2946323257036b6d', 192, 2017, 44),
    7: ('jahon_tarixi_7_uzb.pdf', '4d057e61fa891875aeaad991adc5d77c6b8bdad7b9abe9a5eebf55bcf6efec11', 161, 2017, 44),
    8: ('jahon_tarixi_8_uzb.pdf', 'bb3b3f91bd01f239a626768d1b7e4f279374e63275eca41b7858765ee987e806', 160, 2019, 32),
    9: ('jahon_tarixi_9_uzb.pdf', '4f20684716e02748d1f6d54b3f5c00f7d3320f36d216dcbd4d807a8bbc6983b5', 160, 2019, 41),
    10: ('jahon_tarixi_10_uzb.pdf', 'c94cef41c7f9b46efca1a5d8c331a7bb8bcf1e686efe06a8daf812d1aae0aa76', 144, 2017, 26),
    11: ('jahon_tarixi_11_uzb.pdf', 'b446f17734e59c3fbb3caf94a80fc02f53a2f7c71525d5dfaf0525078527d33c', 144, 2018, 29),
}


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':')).encode('utf8')).hexdigest()


def require(condition, code):
    if not condition:
        raise ValueError(code)


def validate_inventory(document):
    require(document.get('subject') == 'jahon_tarixi', 'history_subject_required')
    books = document.get('books', [])
    require([b.get('grade') for b in books] == list(PINNED), 'six_original_grades_required')
    require(document.get('pdf_pages') == 961, 'original_pdf_total_required')
    for book in books:
        name, digest, count, _, _ = PINNED[book['grade']]
        require((book.get('file_name'), book.get('sha256'), book.get('pdf_page_count'))
                == (name, digest, count), 'original_book_identity_mismatch')
        require(book.get('decoded_pages') == count, 'every_page_must_decode')
        pages = book.get('pages', [])
        require([p.get('pdf_page') for p in pages] == list(range(1, count+1)),
                'every_original_page_required_once')
        require(all(p.get('decoded') is True and p.get('text_characters', -1) >= 0
                    and len(p.get('size_points', [])) == 2
                    and all(v > 0 for v in p['size_points']) for p in pages),
                'decoded_page_metrics_required')
        require(book.get('course_ready') is False, 'inventory_is_not_release_approval')
        require(not any('text' in p for p in pages), 'raw_extraction_must_stay_private')
    require(document.get('implemented_lessons') == 0, 'inventory_is_not_executable_content')
    return document


def validate_catalog(document):
    require(document.get('subject') == 'jahon_tarixi'
            and document.get('source_policy') == 'supplied_textbooks_only',
            'supplied_history_sources_only')
    books = document.get('books', [])
    require([b.get('grade') for b in books] == list(PINNED), 'six_original_grades_required')
    all_ids = set()
    for book in books:
        grade = book['grade']
        name, digest, count, year, units = PINNED[grade]
        require((book.get('file_name'), book.get('sha256'), book.get('pdf_page_count'),
                 book.get('year')) == (name, digest, count, year), 'original_book_identity_mismatch')
        require(book.get('id') == f'world-history-{grade}-uz-{year}', 'stable_book_id_required')
        require(book.get('title') and book.get('authors') and book.get('publisher')
                and book.get('edition') and re.fullmatch(r'[0-9-]{17}', book.get('isbn', '')),
                'reviewed_bibliography_required')
        records = book.get('records', [])
        require(len(records) == units, 'original_numbered_topic_units_required')
        require([r.get('sequence') for r in records] == list(range(1, units+1)), 'source_order_required')
        flattened = [n for r in records for n in r.get('source_numbers', [])]
        require(flattened == list(range(1, (29 if grade == 10 else units)+1)),
                'source_number_coverage_required')
        if grade == 10:
            require([r['source_numbers'] for r in records if len(r['source_numbers']) > 1]
                    == [[7, 8], [15, 16], [19, 20]], 'preserve_combined_source_topics')
        chapters = {c['id'] for c in book['chapters']}
        for index, record in enumerate(records):
            require(record.get('id') not in all_ids and record.get('title'), 'unique_named_source_topic_required')
            all_ids.add(record['id'])
            expected = [] if index == 0 else [records[index-1]['id']]
            require(record.get('prerequisite_ids') == expected, 'source_prerequisite_chain_required')
            require(record.get('chapter_id') in chapters or (grade == 10 and record.get('chapter_id') is None),
                    'original_chapter_membership_required')
            printed, pdf = record.get('printed_pages', []), record.get('pdf_pages', [])
            require(printed and printed == sorted(set(printed)) and printed == pdf
                    and all(type(n) is int and 1 <= n <= min(count, 160 if grade == 7 else count) for n in pdf),
                    'explicit_candidate_page_mapping_required')
            require(record.get('toc_printed_start') == printed[0], 'contents_start_page_required')
        evidence = book.get('catalog_image_evidence', [])
        require(evidence and {1, 2, *book['contents_pdf_pages']}
                <= {e.get('pdf_page') for e in evidence}, 'original_bibliography_and_contents_images_required')
        require(all(e.get('verification') == 'original_page_image_reviewed'
                    and e.get('scope') == 'bibliography_or_contents_only'
                    and re.fullmatch(r'[0-9a-f]{64}', e.get('page_image_sha256', '')) for e in evidence),
                'image_evidence_is_not_ocr_approval')
        require(book.get('course_ready') is False, 'catalog_is_not_release_approval')
    require(document.get('numbered_topic_units') == 216
            and document.get('numbered_source_labels') == 219
            and document.get('chapter_count') == 26, 'measured_catalog_totals_required')
    return document


def load_catalog():
    return validate_catalog(read_json(DIRECTORY / 'world_history_sources.json'))


def require_complete_catalog(document):
    validate_catalog(document)
    require(document.get('catalogue_complete') is True
            and type(document.get('total_teaching_topics')) is int
            and document['total_teaching_topics'] == 219,
            'complete_source_and_activity_catalog_required_before_lesson_import')
    original_pages = read_json(DIRECTORY / 'world_history_page_inventory.json')['pages']
    hashes = {(p['book_id'], p['pdf_page']): p['page_image_sha256'] for p in original_pages}
    feature_types = {
        'question_group', 'chronology_or_concept_summary', 'recall_activity',
        'printed_map', 'diagram', 'introduction', 'glossary', 'bibliography',
        'contents', 'printed_table', 'conclusion', 'reference_index',
        'study_instructions', 'final_review', 'colophon', 'administrative_rental_tables',
        'reflection_activity', 'authors_preface', 'creative_activity',
        'external_research_activity', 'map_activity', 'media_activity', 'cover_map',
        'independent_activity', 'activity_table', 'appendix_maps',
        'abbreviations_reference', 'illustrative_map',
    }
    for book in document['books']:
        require(book.get('catalogue_status') == 'body_and_features_reviewed',
                'body_and_page_feature_review_required')
        features = book.get('page_feature_inventory', [])
        require([p.get('pdf_page') for p in features]
                == list(range(1, book['pdf_page_count']+1))
                and all(type(p.get('pdf_page')) is int
                        and p.get('verification') == 'original_image_features_reviewed'
                        and re.fullmatch(r'[0-9a-f]{64}', p.get('page_image_sha256', ''))
                        for p in features),
                'complete_original_page_feature_inventory_required')
        for page in features:
            require(page['page_image_sha256'] == hashes.get((book['id'], page['pdf_page'])),
                    'original_page_render_digest_mismatch')
            values = page.get('features')
            require(type(values) is list and all(type(v) is str for v in values)
                    and len(set(values)) == len(values) and set(values) <= feature_types,
                    'reviewed_feature_categories_required')
        require(all(r.get('heading_verification') == (
                    'contents_and_original_body_image_heading_checked' if book['grade'] == 9
                    else 'contents_image_and_body_text_heading_checked')
                    for r in book['records']), 'every_numbered_body_heading_required')
        ancillary = book.get('ancillary_records', [])
        expected_ancillary = {
            6: ['wh6-intro', 'wh6-conclusion', 'wh6-glossary', 'wh6-final-review',
                'wh6-geographic-index', 'wh6-names-index', 'wh6-chronology'],
            7: ['wh7-authors', 'wh7-intro', 'wh7-chronology'],
            8: ['wh8-intro', 'wh8-conclusion'],
            9: ['wh9-intro', 'wh9-appendix'], 10: ['wh10-intro'], 11: ['wh11-intro'],
        }[book['grade']]
        require([r.get('id') for r in ancillary] == expected_ancillary,
                'every_original_ancillary_source_required')
        require(ancillary and all(r.get('verification') == 'original_image_structure_reviewed_facts_pending'
                    and r.get('coverage_decision') in {
                        'separate_teaching_unit', 'opening_context_in_first_numbered_unit',
                        'source_maps_attached_to_relevant_numbered_units',
                        'grade_reference_cross_linked_after_fact_review'}
                    and r.get('linked_teaching_ids') for r in ancillary),
                'all_ancillary_sources_need_explicit_coverage')
        units = book.get('teaching_units', [])
        extras = {6: ['wh6-conclusion', 'wh6-final-review'], 8: ['wh8-conclusion']}.get(book['grade'], [])
        expected_ids = [r['id'] for r in book['records']] + extras
        require([u.get('id') for u in units] == expected_ids
                and book.get('total_teaching_topics') == len(expected_ids),
                'complete_ordered_teaching_unit_map_required')
        source_records = {r['id']: r for r in book['records'] + ancillary}
        for index, unit in enumerate(units):
            source = source_records[unit['id']]
            require(unit.get('sequence') == index+1
                    and unit.get('prerequisite_ids') == ([] if index == 0 else [units[index-1]['id']])
                    and unit.get('source_record_id') == source['id']
                    and unit.get('pdf_pages') == source['pdf_pages']
                    and unit.get('printed_pages') == source['printed_pages']
                    and unit.get('title') == source['title'],
                    'teaching_units_must_preserve_source_order_and_location')
        require(all(set(r['linked_teaching_ids']) <= set(expected_ids) for r in ancillary),
                'ancillary_links_must_resolve')
        bindings = book.get('activity_bindings', [])
        require([p.get('pdf_page') for p in bindings] == list(range(1, book['pdf_page_count']+1)),
                'every_page_activity_binding_required')
        for binding, page in zip(bindings, features):
            number = page['pdf_page']
            require(binding.get('features') == page['features']
                    and binding.get('candidate_numbered_topic_ids') == [r['id'] for r in book['records'] if number in r['pdf_pages']]
                    and binding.get('ancillary_ids') == [r['id'] for r in ancillary if number in r['pdf_pages']],
                    'activity_bindings_must_match_original_page_catalog')
    return document
