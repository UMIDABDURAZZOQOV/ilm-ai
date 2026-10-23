"""Source identity, full catalogue coverage and spread mapping regressions."""
from copy import deepcopy

import pytest

from services.chemistry_validation import load_catalog, page_locator, validate_catalog, readiness


def test_all_five_books_are_mapped_but_not_claimed_as_complete_courses():
    catalog = load_catalog()
    assert sum(b['pdf_page_count'] for b in catalog['books']) == 817
    assert sum(b['chapter_count'] for b in catalog['books']) == 29
    assert sum(b['paragraph_count'] for b in catalog['books']) == 204
    assert sum(b['laboratory_count'] for b in catalog['books']) == 49
    assert sum(b['practical_count'] for b in catalog['books']) == 15
    assert sum(len(b['records']) for b in catalog['books']) == 327
    assert sum(p['source_teaching_entries'] for p in readiness(catalog)) == 268
    assert not any(p['course_ready'] for p in readiness(catalog))


@pytest.mark.parametrize('printed,pdf,region', [(1,1,'full'),(2,2,'left'),
    (3,2,'right'),(4,3,'left'),(9,5,'right'),(147,74,'right'),
    (156,79,'left'),(157,79,'right'),(159,80,'right'),(160,81,'full')])
def test_grade7_spreads_do_not_lose_left_right_or_singleton_frontmatter(printed,pdf,region):
    assert page_locator(7,printed) == {'pdf_page':pdf,'region':region}


def test_contents_discrepancies_preserve_original_pointer_and_verified_body_start():
    book = load_catalog()['books'][1]
    for n,toc,body in [(6,30,31),(7,32,34),(8,36,37),(9,39,41),
                       (10,42,44),(11,46,48),(12,49,51),(13,51,53)]:
        record = next(r for r in book['records'] if r['id']==f'ch8-paragraph{n:02}')
        assert (record['toc_printed_start'], record['printed_start']) == (toc,body)
        assert record['start_locator']=={'pdf_page':body,'region':'full'}


@pytest.mark.parametrize('mutation', ['digest','missing','duplicate','region',
    'ocr_only','prerequisite','range','physical','container','grade'])
def test_validator_rejects_source_or_coverage_tampering(mutation):
    c=deepcopy(load_catalog()); b=c['books'][0]
    r=next(r for r in b['records'] if r['kind']=='paragraph')
    if mutation=='digest': b['sha256']='0'*64
    if mutation=='missing': b['records'].remove(r)
    if mutation=='duplicate': b['records'].append(deepcopy(r))
    if mutation=='region': r['start_locator']['region']='left'
    if mutation=='ocr_only': c['books'][3]['records'][0]['heading_review']['status']='ocr_candidate'
    if mutation=='prerequisite': r['prerequisite_ids']=['unread']
    if mutation=='range': r['printed_end']=999
    if mutation=='physical': next(x for x in b['records'] if x['kind']=='laboratory')['digital_activity_policy']['physical_execution_required']=True
    if mutation=='container': r['chapter_id']='missing'
    if mutation=='grade': c['books'][-1]['grade']=10
    with pytest.raises(ValueError): validate_catalog(c)
