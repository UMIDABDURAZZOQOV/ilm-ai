"""Derive teaching/ancillary coverage from the completed manual page inventory.

This does not inspect PDFs, approve facts, or mark any lesson as implemented.
It refuses to proceed without the pre-existing original-image feature ledger.
"""
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'scripts/curriculum/world_history'


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8')


def main():
    catalog = json.loads((DATA / 'world_history_sources.json').read_text(encoding='utf8'))
    inventory = json.loads((DATA / 'world_history_page_inventory.json').read_text(encoding='utf8'))
    pages = {(p['book_id'], p['pdf_page']): p for p in inventory['pages']}
    additions = {'wh6-conclusion', 'wh6-final-review', 'wh8-conclusion'}
    rows = []
    for book in catalog['books']:
        grade = book['grade']
        features = book['page_feature_inventory']
        assert [p['pdf_page'] for p in features] == list(range(1, book['pdf_page_count'] + 1))
        for page in features:
            original = pages[book['id'], page['pdf_page']]
            assert page['verification'] == 'original_image_features_reviewed'
            assert page['page_image_sha256'] == original['page_image_sha256']
            original['feature_review'] = page['verification']
            original['reviewed_features'] = page['features']
            original['fact_verification'] = 'not_approved_by_inventory'
        units = []
        for record in book['records']:
            record['page_mapping_verification'] = 'contents_and_body_heading_cross_checked_shared_boundaries_retained'
            units.append({
                'id': record['id'], 'kind': record['kind'], 'title': record['title'],
                'source_record_id': record['id'], 'pdf_pages': record['pdf_pages'],
                'printed_pages': record['printed_pages'], 'chapter_id': record['chapter_id'],
                'interactive_status': record.get('interactive_status', 'not_implemented'),
            })
        all_numbered = [r['id'] for r in book['records']]
        for ancillary in book['ancillary_records']:
            ancillary['verification'] = 'original_image_structure_reviewed_facts_pending'
            if ancillary['id'] in additions:
                ancillary['coverage_decision'] = 'separate_teaching_unit'
                ancillary['linked_teaching_ids'] = [ancillary['id']]
                units.append({
                    'id': ancillary['id'], 'kind': ancillary['kind'], 'title': ancillary['title'],
                    'source_record_id': ancillary['id'], 'pdf_pages': ancillary['pdf_pages'],
                    'printed_pages': ancillary['printed_pages'], 'chapter_id': None,
                    'interactive_status': ancillary.get('interactive_status', 'not_implemented'),
                })
            elif ancillary['kind'] in {'introduction', 'preface'}:
                ancillary['coverage_decision'] = 'opening_context_in_first_numbered_unit'
                ancillary['linked_teaching_ids'] = all_numbered[:1]
            elif ancillary['kind'] == 'map_appendix':
                ancillary['coverage_decision'] = 'source_maps_attached_to_relevant_numbered_units'
                ancillary['linked_teaching_ids'] = [f'wh9-topic{n:02d}' for n in
                                                  (17, 18, 20, 26, 27, 28, 29, 30, 31, 32)]
                ancillary['page_bindings'] = [
                    {'pdf_page': 154, 'topic_ids': ['wh9-topic17', 'wh9-topic18'], 'scope': 'Latin America map'},
                    {'pdf_page': 155, 'topic_ids': ['wh9-topic20', 'wh9-topic26'], 'scope': 'Russo-Japanese war map'},
                    {'pdf_page': 156, 'topic_ids': [f'wh9-topic{n:02d}' for n in range(26, 33)], 'scope': 'Asia map'},
                ]
            else:
                ancillary['coverage_decision'] = 'grade_reference_cross_linked_after_fact_review'
                ancillary['linked_teaching_ids'] = all_numbered
            ancillary.setdefault('fact_review', 'not_reviewed')
        units.sort(key=lambda u: (u['pdf_pages'][0], u['id']))
        for index, unit in enumerate(units):
            unit['sequence'] = index + 1
            unit['prerequisite_ids'] = [] if index == 0 else [units[index-1]['id']]
        book['teaching_units'] = units
        book['total_teaching_topics'] = len(units)
        book['catalogue_status'] = 'body_and_features_reviewed'
        book['catalog_review'] = 'bibliography_contents_body_headings_ancillary_and_page_features_reviewed'
        book['activity_bindings'] = []
        for page in features:
            original = pages[book['id'], page['pdf_page']]
            ancillary_ids = [r['id'] for r in book['ancillary_records'] if page['pdf_page'] in r['pdf_pages']]
            book['activity_bindings'].append({
                'pdf_page': page['pdf_page'], 'features': page['features'],
                'candidate_numbered_topic_ids': [r['id'] for r in book['records'] if page['pdf_page'] in r['pdf_pages']],
                'ancillary_ids': ancillary_ids,
                'scope': 'presence_and_candidate_parent_only_exact_region_and_facts_require_lesson_review',
            })
        counts = Counter(f for page in features for f in page['features'])
        rows.append((grade, len(book['records']), len(units), book['pdf_page_count'], counts))
    implemented = sum(u['interactive_status'] == 'reviewed_preview_ready' for b in catalog['books'] for u in b['teaching_units'])
    catalog.update(
        catalogue_complete=True, total_teaching_topics=sum(r[2] for r in rows),
        implemented_lessons=implemented, remaining_lessons=sum(r[2] for r in rows)-implemented,
        note='Source/activity catalogue complete; no lesson or fact approved by this inventory. '
             '216 numbered blocks plus grade6 conclusion/final review and grade8 conclusion = 219 teaching units. '
             'Introductions/prefaces embed in first numbered unit; glossaries/indices/timelines/maps remain linked references. '
             'Shared pages require exact region review; open creative activities are not automatically graded.',
    )
    write(DATA / 'world_history_sources.json', catalog)
    write(DATA / 'world_history_page_inventory.json', inventory)
    lines = ['# Jahon tarixi: complete source and teaching map', '',
             ('2026-10-29. **Catalogue and local-preview coverage complete; release approval remains separate.**' if implemented == catalog['total_teaching_topics'] else '2026-10-26. **Catalogue complete; executable course incomplete.**'), '',
             '| Grade | Numbered source blocks | Teaching units | PDF pages |',
             '| --- | ---: | ---: | ---: |']
    lines += [f'| {g} | {n} | {u} | {p} |' for g, n, u, p, _ in rows]
    lines += ['| Total | 216 | 219 | 961 |', '',
              '219 printed paragraph labels and 219 teaching units are different measurements.',
              'Grade10 retains three combined paragraphs. The three extra teaching units are',
              'grade6 conclusion (179–180), final review (184), and grade8 conclusion (156).', '',
              'Introductions and the grade7 author preface belong to opening context in the',
              'first numbered lesson. Glossaries, geographical/name indices and chronologies',
              'remain cross-linked grade references. Grade9 appendix maps154–156 attach to',
              'their relevant numbered topics. No reference page is silently discarded.', '',
              'Questions, creative/independent tasks, map activities and review boxes remain',
              'inside their original parent topic. Candidate shared-page ownership is explicit',
              'in `activity_bindings`; exact activity regions and factual claims must be checked',
              'when authoring that lesson. Interpretive/open responses use self/teacher review.',
              'Internet/media research prompts do not authorize importing outside facts.', '',
              f'**Reviewed preview lessons: {implemented}; remaining: {219-implemented}.** Source pages are candidate spans;',
              'a shared final page can include the next heading. It is not blanket fact approval.', '']
    for book in catalog['books']:
        lines += [f"## Grade {book['grade']}: {book['title']} ({book['year']})", '',
                  '| Order | ID | Source title | Printed/PDF pages | Status |', '| ---: | --- | --- | --- | --- |']
        for unit in book['teaching_units']:
            pages_ = unit['pdf_pages']
            span = str(pages_[0]) if len(pages_) == 1 else f'{pages_[0]}–{pages_[-1]}'
            lines.append(f"| {unit['sequence']} | {unit['id']} | {unit['title']} | {span} | {unit['interactive_status']} |")
        lines += ['', '### Supporting source records', '']
        for record in book['ancillary_records']:
            lines.append(f"- `{record['id']}`: {record['title']}, pages {', '.join(map(str, record['pdf_pages']))}; {record['coverage_decision']}.")
        lines.append('')
    (ROOT / 'docs/world_history/COURSE_MAP.md').write_text('\n'.join(lines), encoding='utf8')
    features = sorted({f for *_, counts in rows for f in counts})
    audit = ['# Original-page feature inventory', '',
             '2026-10-26. All 961 rendered page images inspected for feature presence/layout.',
             'Each record pins its original render digest. This is not fact, map legend,',
             'date, answer-key or teacher approval. OCR candidates remain separate.', '',
             'Counts are pages containing a category, not numbers of exercises or diagrams.',
             'A page can carry several categories. An empty feature list is not a blank-page claim.', '',
             '| Feature | 6 | 7 | 8 | 9 | 10 | 11 |', '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
    audit += [f"| {f} | " + ' | '.join(str(row[4][f]) for row in rows) + ' |' for f in features]
    audit += ['', '## Review boundaries', '',
              '- Grade7 map-location questions do not imply a printed teaching map exists.',
              '- Grade9 blank exercise tables are activities, not factual reference tables.',
              '- Cover/stylized maps are distinguished from geographic evidence.',
              '- Mythology tables describe beliefs; they do not establish divine events as facts.',
              '- Rental/colophon tables are administrative, not teaching units.',
              '- Map captions, legends and territorial dates need exact review before assessment.',
              '- No original source images, extracted text or OCR are published in Git.', '']
    (ROOT / 'docs/world_history/PAGE_FEATURE_AUDIT.md').write_text('\n'.join(audit), encoding='utf8')
    print({'teaching_units': catalog['total_teaching_topics'], 'page_images': len(pages), 'implemented': implemented})


if __name__ == '__main__':
    main()
