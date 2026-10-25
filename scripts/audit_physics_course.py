"""Audit actual reviewed v2 lessons, separately from the frozen source-only map.

--pdf-dir optionally verifies original private PDF bytes, text and rendered
pixels. Structural hashes are evidence of source identity, not expert approval.
"""

import argparse
import json

from services.physics_curriculum import (
    DIRECTORY,
    REVIEWED_BATCHES,
    load_course,
    validate_batch,
    validate_review_evidence,
)


def report():
    documents = load_course()
    books = json.loads((DIRECTORY / "physics_sources.json").read_text())["books"]
    rows = []
    for book in books:
        lessons = [
            l for d in documents if d["grade"] == book["grade"] for l in d["lessons"]
        ]
        source_topics = {
            r["id"]: r
            for r in book["records"]
            if r["id"].startswith(f"physics-{book['grade']}-section-")
        }
        rows.append(
            {
                "grade": book["grade"],
                "source_sections": book["counts"]["numbered_sections"],
                "authored": len(lessons),
                "remaining": book["counts"]["numbered_sections"] - len(lessons),
                "cards": sum(len(l["cards"]) for l in lessons),
                "formula_entries": sum(len(l["formulas"]) for l in lessons),
                "examples": sum(len(l["examples"]) for l in lessons),
                "assessments": sum(len(l["assessments"]) for l in lessons),
                "frq": sum(
                    q["response_kind"] == "numeric_quantity"
                    for l in lessons
                    for q in l["assessments"]
                ),
                "laboratories": sum(
                    source_topics[l["topic_id"]]["kind"] == "laboratory"
                    for l in lessons
                ),
                "practicals": sum(
                    source_topics[l["topic_id"]]["kind"]
                    in {"home_practical", "practical"}
                    for l in lessons
                ),
                "next_section": next(
                    (
                        r["number"]
                        for r in source_topics.values()
                        if r["id"] not in {l["topic_id"] for l in lessons}
                    ),
                    None,
                ),
            }
        )
    return {
        "publication": "local_test_preview_only",
        "independent_expert": "not_claimed",
        "source_total": 316,
        "authored": sum(r["authored"] for r in rows),
        "remaining": sum(r["remaining"] for r in rows),
        "grades": rows,
    }


def check_originals(directory, ocr_directory=None):
    from scripts.audit_physics_source_pages import check_book_pages

    books = json.loads((DIRECTORY / "physics_sources.json").read_text())["books"]
    count = 0
    for name, (grade, _, _) in REVIEWED_BATCHES.items():
        doc = json.loads((DIRECTORY / f"{name}.json").read_text())
        validate_batch(doc)
        validate_review_evidence(doc)
        audit = json.loads((DIRECTORY / f"{name}_review.json").read_text())
        book = next(b for b in books if b["grade"] == grade)
        count += check_book_pages(book, audit["pages"], directory, ocr_directory)
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-dir")
    parser.add_argument(
        "--ocr-dir", help="Private cached OCR root for segmented scan sources"
    )
    args = parser.parse_args()
    if args.ocr_dir and not args.pdf_dir:
        parser.error("ocr_dir_requires_original_pdf_dir")
    result = report()
    if args.pdf_dir:
        result["original_page_checks"] = check_originals(args.pdf_dir, args.ocr_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
