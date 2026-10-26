"""Render exact supplied history pages to the ignored review cache. No approval."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_world_history_sources import FILES


def render(source_dir, cache, grade, pages):
    import pypdfium2 as pdfium

    private = Path(__file__).resolve().parents[1] / '.local'
    if private.resolve() not in cache.resolve().parents:
        raise ValueError('private_cache_required')
    output = cache / f'grade{grade}'
    output.mkdir(parents=True, exist_ok=True)
    with pdfium.PdfDocument(source_dir / FILES[grade]) as document:
        for number in pages:
            if not 1 <= number <= len(document):
                raise ValueError('invalid_pdf_page')
            target = output / f'pdf-{number:03}.png'
            if target.exists():
                continue
            page = document[number-1]
            bitmap = page.render(scale=2000 / max(page.get_size()))
            bitmap.to_pil().save(target)
            bitmap.close()
            page.close()
    print(f'grade{grade}: {len(pages)} requested original pages available privately', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path, required=True)
    parser.add_argument('--cache', type=Path, required=True)
    parser.add_argument('--grade', type=int, choices=FILES, required=True)
    parser.add_argument('--pages', required=True, help='Comma-separated pages or ranges, e.g. 1-4,8-12')
    args = parser.parse_args()
    numbers = []
    for part in args.pages.split(','):
        bounds = list(map(int, part.split('-')))
        numbers.extend(range(bounds[0], bounds[-1]+1))
    render(args.source_dir, args.cache, args.grade, sorted(set(numbers)))
