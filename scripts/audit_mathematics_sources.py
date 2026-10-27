"""Private-file audit, emitting only hashes/counts: no PDF/OCR copying to Git."""

import argparse
import hashlib
import json
from pathlib import Path

from services.mathematics_curriculum import ROOT, load_course, manifest, require


def audit(source_directory):
    import fitz

    catalog = manifest()
    index = json.loads((ROOT / "page_inventory.json").read_text())
    supplied = list(Path(source_directory).rglob("*.pdf"))
    paths = {}
    for book in catalog["books"]:
        matches = [p for p in supplied if p.name == book["original_filename"]]
        require(
            len(matches) == 1, "math_missing_or_duplicate_source:" + book["book_id"]
        )
        path = paths[book["book_id"]] = matches[0]
        require(
            hashlib.sha256(path.read_bytes()).hexdigest() == book["sha256"],
            "math_pdf_hash_changed",
        )
        with fitz.open(path) as pdf:
            require(
                len(pdf) == book["pdf_pages"] == len(index[book["book_id"]]),
                "math_pdf_page_count_changed",
            )
            for page, saved in zip(pdf, index[book["book_id"]]):
                require(page.number + 1 == saved["pdf_page"], "math_pdf_page_gap")
                require(
                    hashlib.sha256(page.get_text().encode()).hexdigest()
                    == saved["native_text_sha256"],
                    "math_page_text_changed",
                )
    review = json.loads((ROOT / "grade1_part1_review.json").read_text())
    with fitz.open(paths[review["book_id"]]) as pdf:
        for topic in review["topics"]:
            for page in topic["pages"]:
                actual = (
                    pdf[page["pdf_page"] - 1]
                    .get_pixmap(matrix=fitz.Matrix(1.3, 1.3))
                    .tobytes("png")
                )
                require(
                    hashlib.sha256(actual).hexdigest() == page["image_sha256"],
                    "math_reviewed_image_changed",
                )
        mapping = json.loads((ROOT / "grade1_part1_map.json").read_text())
        require(
            [t["source_number"] for t in mapping["topics"]] == list(range(1, 42)),
            "math_toc_topic_gap_or_duplicate",
        )
        require(
            mapping["topics"][24]["duplicate_pdf_pages"] == [55, 56],
            "math_duplicate_pages_not_recorded",
        )
        for saved in mapping["additional_image_checks"]:
            page = pdf[saved["pdf_page"] - 1]
            require(
                hashlib.sha256(page.get_text().encode()).hexdigest()
                == saved["native_sha256"],
                "math_mapping_native_changed",
            )
            actual = page.get_pixmap(matrix=fitz.Matrix(1.3, 1.3)).tobytes("png")
            require(
                hashlib.sha256(actual).hexdigest() == saved["png_sha256"],
                "math_mapping_image_changed",
            )
    lessons = load_course()
    return {
        "available_pdfs": len(paths),
        "available_pages": sum(b["pdf_pages"] for b in catalog["books"]),
        "body_image_reviewed_topics": len(review["topics"]),
        "reviewed_body_pages": sum(len(t["pages"]) for t in review["topics"]),
        "interactive_lessons": len(lessons),
        "theory_cards": sum(len(l["cards"]) for l in lessons),
        "questions": sum(len(l["questions"]) for l in lessons),
        "blocked_sources": catalog["blocked_sources"],
        "full_curriculum_topic_count": None,
        "course_ready": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", required=True)
    args = parser.parse_args()
    print(json.dumps(audit(args.sources), ensure_ascii=False, indent=2))
