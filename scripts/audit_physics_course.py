"""Audit actual reviewed v2 lessons, separately from the frozen source-only map.

--pdf-dir optionally verifies original private PDF bytes, text and rendered
pixels. Structural hashes are evidence of source identity, not expert approval.
"""

import argparse
import hashlib
import json
from pathlib import Path

from services.physics_curriculum import (
    DIRECTORY,
    REVIEWED_BATCHES,
    load_course,
    validate_batch,
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


def check_originals(directory):
    import fitz

    books = json.loads((DIRECTORY / "physics_sources.json").read_text())["books"]
    count = 0
    for name, (grade, _, _) in REVIEWED_BATCHES.items():
        doc = json.loads((DIRECTORY / f"{name}.json").read_text())
        validate_batch(doc)
        audit = json.loads((DIRECTORY / f"{name}_review.json").read_text())
        book = next(b for b in books if b["grade"] == grade)
        paths = list(Path(directory).rglob(book["file_name"]))
        if len(paths) != 1:
            raise ValueError("one_original_pdf_required")
        if hashlib.sha256(paths[0].read_bytes()).hexdigest() != audit["book_sha256"]:
            raise ValueError("original_pdf_hash_mismatch")
        with fitz.open(paths[0]) as pdf:
            for evidence in audit["pages"]:
                page = pdf[evidence["pdf_page"] - 1]
                if (
                    hashlib.sha256(page.get_text().encode()).hexdigest()
                    != evidence["text_sha256"]
                    or hashlib.sha256(
                        page.get_pixmap(matrix=fitz.Matrix(2, 2)).tobytes("png")
                    ).hexdigest()
                    != evidence["reviewed_render_sha256"]
                ):
                    raise ValueError("original_page_text_or_pixels_mismatch")
                count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-dir")
    args = parser.parse_args()
    result = report()
    if args.pdf_dir:
        result["original_page_checks"] = check_originals(args.pdf_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
