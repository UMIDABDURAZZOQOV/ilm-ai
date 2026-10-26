"""Build a page-by-page locator inventory, never an automatic fact review.

Source text/OCR remains private. Public output is hashes, topic IDs, page numbers
and feature categories. Category candidates must be confirmed in original images
before a lesson relies on a map, table, question, chronology or interpretation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from services.world_history_validation import load_catalog

PATTERNS = {
    'map_or_map_reference': r'xarita|xaritadan|kartograf',
    'table_or_table_reference': r'jadval',
    'chronology_or_date_summary': r'xronolog|sanalar|tayanch konspekt',
    'question_group': r'savol\s*va\s*topshiriq|savollar|mustahkamlash uchun',
    'independent_or_practical_activity': r'mustaqil ish|ijodiy ish|amaliy|bahs uchun',
    'recall_activity': r'o[‘’\x27]zingizni sinang|esga oling|eslab qoling',
    'external_research_instruction': r'internet|http|www\.',
    'terminology': r'atamalar|lug[‘’\x27]at|tushunchalar',
}


def catalog_pages(cache, output):
    cache = cache.resolve()
    private = Path(__file__).resolve().parents[1] / '.local'
    if private.resolve() not in cache.parents:
        raise ValueError('private_cache_required')
    result = []
    for book in load_catalog()['books']:
        grade = book['grade']
        folder = cache / f'grade{grade}'
        pages = json.loads((folder/'extracted-pages.json').read_text(encoding='utf8'))
        records = book['records'] + book['ancillary_records']
        for page in pages:
            number = page['pdf_page']
            image = folder/f'pdf-{number:03}.png'
            if not image.exists():
                raise ValueError(f'original_render_missing:{grade}:{number}')
            if grade == 9:
                lines = json.loads((folder/f'pdf-{number:03}.lines.json').read_text(encoding='utf8'))
                text = '\n'.join(line['text'] for line in lines)
                method = 'windows_ocr_unverified_locator'
            else:
                text = page['text']
                method = 'embedded_text_locator'
            text = re.sub(r'\s+', ' ', text).casefold()
            # Encoding substitutions are for lookup only, never authored copy.
            text = text.translate(str.maketrans({'à':'a','î':'o','õ':'x','å':'e','ò':'t'}))
            result.append({
                'book_id': book['id'], 'grade': grade, 'sha256': book['sha256'],
                'pdf_page': number, 'printed_page_candidate': number if number <= (160 if grade == 7 else book['pdf_page_count']) else None,
                'page_image_sha256': hashlib.sha256(image.read_bytes()).hexdigest(),
                'topic_ids': [r['id'] for r in records if number in r['pdf_pages']],
                'feature_candidates': [name for name, pattern in PATTERNS.items() if re.search(pattern,text)],
                'locator_method': method, 'feature_review': 'pending_original_image_check',
                'fact_verification': 'not_approved_by_inventory',
            })
    document = {'schema_version': 1, 'subject': 'jahon_tarixi', 'pdf_pages': len(result),
                'warning': 'A map reference is not proof that a map is printed on this page. OCR and text searches are locators only.',
                'pages': result}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(document, ensure_ascii=False, indent=2)+'\n',encoding='utf8')
    print(f'{len(result)} original pages inventoried with private render hashes; no historical fact auto-approved', flush=True)
    return document


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    catalog_pages(args.cache, args.output)
