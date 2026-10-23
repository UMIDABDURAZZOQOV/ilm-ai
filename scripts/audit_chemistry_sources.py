"""Read user PDFs into a PRIVATE cache. Never treats OCR/extraction as approval.

Uses pypdf and pypdfium2. No DB, network, LLM or application imports.
The cache must be outside tracked paths (normally .local/source-review).
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

FILES = {
    7: "kimyo_7_uzb.pdf",
    8: "kimyo_8_uzb.pdf",
    9: "kimyo_9_uzb.pdf",
    10: "organik_kimyo_10_uzb.pdf",
    11: "umumiy_kimyo_11_uzb.pdf",
}


def audit(source_dir: Path, cache: Path, scan_images: bool = False):
    import pypdfium2 as pdfium
    from pypdf import PdfReader

    cache.mkdir(parents=True, exist_ok=True)
    result = []
    for grade, name in FILES.items():
        path = source_dir / name
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        reader = PdfReader(path)
        doc = pdfium.PdfDocument(path)
        folder = cache / f"grade{grade}"
        folder.mkdir(exist_ok=True)
        pages = []
        for index in range(len(doc)):
            page = doc[index]
            text_page = page.get_textpage()
            text = text_page.get_text_range()
            text_page.close()
            # Decode every PDF page, including empty and malformed scans.
            small = page.render(scale=120 / max(page.get_size()))
            small.close()
            render = index < 3 or index >= len(doc) - 6 or (scan_images and grade >= 10)
            if render:
                bitmap = page.render(scale=1700 / max(page.get_size()))
                bitmap.to_pil().save(folder / f"pdf-{index+1:03}.png")
                bitmap.close()
            pages.append({"pdf_page": index + 1, "size": page.get_size(),
                          "text": text, "characters": len(text.strip()),
                          "decoded": True, "image_rendered": render})
            page.close()
        doc.close()
        (folder / "extracted-pages.json").write_text(
            json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
        book = {"grade": grade, "file_name": name, "sha256": digest,
                "pdf_page_count": len(pages), "decoded_pages": len(pages),
                "text_pages": sum(p["characters"] > 60 for p in pages),
                "metadata": {str(k): str(v) for k, v in (reader.metadata or {}).items()},
                "content_reviewed": False}
        result.append(book)
        print(json.dumps(book, ensure_ascii=False), flush=True)
    (cache / "inventory.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--scan-images", action="store_true")
    args = parser.parse_args()
    audit(args.source_dir, args.cache, args.scan_images)
