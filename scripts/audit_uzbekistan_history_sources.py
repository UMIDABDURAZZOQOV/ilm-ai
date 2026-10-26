"""Read-only source audit; missing books stay blocked, never generated."""

import argparse
import json

from services.uzbekistan_history_sources import (
    load_catalog,
    validate_catalog,
    verify_originals,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-dir")
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--include-lessons", action="store_true")
    args = parser.parse_args()
    catalog = load_catalog()
    result = validate_catalog(catalog)
    if args.pdf_dir:
        result.update(verify_originals(catalog, args.pdf_dir))
    if args.include_lessons:
        from services.uzbekistan_history_validation import (
            BATCHES,
            load_course,
            validate_batch,
        )

        documents = load_course()
        result["interactive_batches"] = [validate_batch(d) for d in documents]
        if args.pdf_dir:
            import hashlib
            from pathlib import Path

            import fitz

            checked = 0
            for name, document in zip(BATCHES, documents):
                book = next(b for b in catalog["books"] if b["grade"] == document["grade"])
                original = next(
                    p for p in Path(args.pdf_dir).rglob(book["file_name"])
                    if hashlib.sha256(p.read_bytes()).hexdigest() == book["sha256"]
                )
                from services.uzbekistan_history_sources import DIRECTORY, require

                review = json.loads((DIRECTORY / f"{name}_review.json").read_text())
                # Separate document/render context from the heading audit above.
                with fitz.open(original) as pdf:
                    for evidence in review["pages"]:
                        pixels = pdf[evidence["pdf_page"] - 1].get_pixmap(
                            matrix=fitz.Matrix(*evidence["image_matrix"])
                        ).tobytes("png")
                        require(hashlib.sha256(pixels).hexdigest() == evidence["image_sha256"],
                                "lesson_original_full_page_image_changed")
                        checked += 1
            result["lesson_full_page_images"] = checked
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if args.require_complete and result["blocked_grades"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
