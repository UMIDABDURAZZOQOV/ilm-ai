"""Read supplied history PDFs into a private cache; never approves OCR as fact.

No application/ORM, network or AI imports. Public output contains bibliography,
page metrics and hashes only. Full extraction and page images stay in the cache.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

FILES = {
    6: 'qadimgi_dunyo_tarixi_6_uzb.pdf',
    7: 'jahon_tarixi_7_uzb.pdf',
    8: 'jahon_tarixi_8_uzb.pdf',
    9: 'jahon_tarixi_9_uzb.pdf',
    10: 'jahon_tarixi_10_uzb.pdf',
    11: 'jahon_tarixi_11_uzb.pdf',
}
EXPECTED_COUNTS = {6: 192, 7: 161, 8: 160, 9: 160, 10: 144, 11: 144}


def audit(source_dir: Path, cache: Path, output: Path):
    import pypdfium2 as pdfium
    from pypdf import PdfReader

    # Source books and full extraction may not be placed under curriculum/docs.
    repo = Path(__file__).resolve().parents[1]
    if repo == source_dir.resolve() or repo in source_dir.resolve().parents:
        raise ValueError('source_directory_must_be_outside_repository')
    private_root = repo / '.local'
    if private_root.resolve() not in cache.resolve().parents:
        raise ValueError('cache_must_be_in_ignored_private_local_directory')
    cache.mkdir(parents=True, exist_ok=True)
    result = []
    for grade, name in FILES.items():
        path = source_dir / name
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        reader = PdfReader(path)
        folder = cache / f'grade{grade}'
        folder.mkdir(exist_ok=True)
        private_pages, public_pages = [], []
        with pdfium.PdfDocument(path) as document:
            if len(document) != EXPECTED_COUNTS[grade]:
                raise ValueError(f'grade{grade}_unexpected_pdf_count:{len(document)}')
            for index in range(len(document)):
                page = document[index]
                text_page = page.get_textpage()
                text = text_page.get_text_range()
                text_page.close()
                bitmap = page.render(scale=120 / max(page.get_size()))
                bitmap.close()
                render = index < 4 or index >= len(document) - 10
                if render:
                    bitmap = page.render(scale=2000 / max(page.get_size()))
                    bitmap.to_pil().save(folder / f'pdf-{index+1:03}.png')
                    bitmap.close()
                page_info = {
                    'pdf_page': index + 1, 'size_points': list(page.get_size()),
                    'text_characters': len(text.strip()), 'decoded': True,
                    'image_rendered': render, 'visual_review': 'pending',
                    'printed_page': None, 'feature_inventory': 'pending_visual_review',
                }
                public_pages.append(page_info)
                private_pages.append(dict(page_info, text=text))
                page.close()
        (folder / 'extracted-pages.json').write_text(
            json.dumps(private_pages, ensure_ascii=False, indent=2), encoding='utf8')
        book = {
            'grade': grade, 'file_name': name, 'sha256': digest,
            'bytes': path.stat().st_size, 'pdf_page_count': len(public_pages),
            'decoded_pages': len(public_pages),
            'pages_with_text_layer_over_60_characters': sum(p['text_characters'] > 60 for p in public_pages),
            'bibliography_review': 'pending_original_page_images',
            'catalog_review': 'pending_contents_and_body_cross_check',
            'content_reviewed': False, 'course_ready': False,
            'pdf_metadata': {str(k): str(v) for k, v in (reader.metadata or {}).items()},
            'pages': public_pages,
        }
        result.append(book)
        print(json.dumps({k: v for k, v in book.items() if k not in {'pages', 'pdf_metadata'}}, ensure_ascii=False), flush=True)
    report = {'schema_version': 1, 'subject': 'jahon_tarixi',
              'pdf_pages': sum(b['pdf_page_count'] for b in result),
              'books': result, 'total_teaching_topics': None,
              'implemented_lessons': 0, 'remaining_lessons': None,
              'warning': 'Decoding and extraction are not visual fact approval. Topic count awaits source cataloguing.'}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path, required=True)
    parser.add_argument('--cache', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    audit(args.source_dir, args.cache, args.output)
