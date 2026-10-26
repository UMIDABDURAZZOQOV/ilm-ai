from copy import deepcopy
import hashlib

import pytest

from services.world_history_validation import (
    DIRECTORY, ROOT, load_catalog, read_json, require_complete_catalog,
    validate_catalog, validate_inventory,
)
from services.world_history_chronology import century, elapsed_years, year_index


def test_all_six_supplied_originals_and_every_page_are_registered():
    report = validate_inventory(read_json(DIRECTORY / 'world_history_inventory.json'))
    assert sum(len(b['pages']) for b in report['books']) == 961
    assert report['books'][3]['pages_with_text_layer_over_60_characters'] == 0


def test_combined_topics_and_central_asian_content_are_not_dropped():
    catalog = load_catalog()
    assert len(catalog['books'][4]['records']) == 26
    assert catalog['numbered_source_labels'] == 219
    assert any(r['title'] == 'O‘zbekiston hududidagi ilk davlatlar'
               for r in catalog['books'][0]['records'])
    assert catalog['books'][3]['ancillary_records'][-1]['kind'] == 'map_appendix'


@pytest.mark.parametrize('change', ['sha', 'pages', 'grade', 'numbers', 'order', 'prerequisite', 'bibliography', 'image', 'ready'])
def test_catalog_mutations_fail_closed(change):
    document = deepcopy(load_catalog())
    book = document['books'][0]
    if change == 'sha': book['sha256'] = '0'*64
    if change == 'pages': book['records'][0]['pdf_pages'] = [999]
    if change == 'grade': book['grade'] = 5
    if change == 'numbers': document['books'][4]['records'][6]['source_numbers'] = [7]
    if change == 'order': book['records'][0]['sequence'] = 2
    if change == 'prerequisite': book['records'][1]['prerequisite_ids'] = []
    if change == 'bibliography': book['isbn'] = ''
    if change == 'image': book['catalog_image_evidence'][0]['verification'] = 'ocr_candidate'
    if change == 'ready': book['course_ready'] = True
    with pytest.raises(ValueError): validate_catalog(document)


def test_incomplete_inventory_cannot_be_used_to_publish_a_lesson():
    with pytest.raises(ValueError, match='complete_source_and_activity_catalog'):
        require_complete_catalog(load_catalog())


def test_readiness_booleans_cannot_substitute_for_page_evidence():
    document = deepcopy(load_catalog())
    document.update(catalogue_complete=True, total_teaching_topics=216)
    for book in document['books']:
        book['catalogue_status'] = 'body_and_features_reviewed'
    with pytest.raises(ValueError, match='complete_original_page_feature_inventory'):
        require_complete_catalog(document)


def test_all_original_page_render_hashes_are_inventoried_without_fact_approval():
    document = read_json(DIRECTORY / 'world_history_page_inventory.json')
    assert document['pdf_pages'] == len(document['pages']) == 961
    assert len({(p['book_id'],p['pdf_page']) for p in document['pages']}) == 961
    for page in document['pages']:
        assert len(page['page_image_sha256']) == 64
        assert page['fact_verification'] == 'not_approved_by_inventory'
        assert 'text' not in page


def test_all_674_existing_biology_and_chemistry_lessons_and_runtime_are_unchanged():
    document = read_json(DIRECTORY / 'protected_baseline.json')
    assert document['biology_lessons'] == 406
    assert document['chemistry_lessons'] == 268
    assert len(document['files']) == 687
    for name, digest in document['files'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name


@pytest.mark.parametrize('year,era,expected', [(1,'CE',1),(100,'CE',1),(101,'CE',2),(1,'BCE',1),(100,'BCE',1),(101,'BCE',2)])
def test_century_boundaries(year, era, expected):
    assert century(year, era) == expected


def test_bce_order_and_era_boundary_have_no_extra_year_zero():
    assert year_index(101,'BCE') < year_index(100,'BCE') < year_index(1,'BCE') < year_index(1,'CE')
    assert elapsed_years(1,'BCE',1,'CE') == 1
    assert elapsed_years(2,'BCE',2,'CE') == 3
    assert elapsed_years(10,'BCE',5,'BCE') == 5


@pytest.mark.parametrize('year,era', [(0,'CE'),(-1,'CE'),(True,'CE'),(1,'unknown'),(10_000_001,'BCE'),('100','CE'),(1,[])])
def test_invalid_dates_are_rejected(year, era):
    with pytest.raises(ValueError): year_index(year, era)


def test_reversed_duration_is_not_silently_absolute():
    with pytest.raises(ValueError): elapsed_years(2,'CE',1,'CE')
