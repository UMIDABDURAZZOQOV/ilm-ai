"""Uzbekistan history source identity, separately from World history/other subjects.

No database/model/network import. Source headings are not publication approval.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

DIRECTORY = (
    Path(__file__).resolve().parents[1] / "scripts/curriculum/uzbekistan_history"
)
SUBJECT = "ozbekiston_tarixi"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()


def load_catalog():
    return json.loads((DIRECTORY / "sources.json").read_text())


def validate_catalog(catalog):
    require(
        catalog["schema_version"] == 1 and catalog["subject"] == SUBJECT,
        "source_schema_or_subject",
    )
    require(
        catalog["language"] == "uz" and catalog["publication"] == "not_published",
        "source_publication",
    )
    grades = [b["grade"] for b in catalog["books"]]
    blocked = [b["grade"] for b in catalog["blocked_books"]]
    require(
        len(grades + blocked) == len(set(grades + blocked))
        and sorted(grades + blocked) == list(range(7, 12)),
        "five_grade_inventory",
    )
    count = 0
    for book in catalog["books"]:
        grade = book["grade"]
        require(
            book["id"] == f"uzbekistan-history-uz-grade-{grade}"
            and book["subject"] == SUBJECT,
            "book_identity",
        )
        require(
            len(book["sha256"]) == 64
            and all(c in "0123456789abcdef" for c in book["sha256"]),
            "book_digest",
        )
        require(
            book["authors"]
            and book["isbn"]
            and book["publisher"]
            and 2000 <= book["year"] <= 2026,
            "bibliography_missing",
        )
        require(
            book["file_name"] == f"ozbekiston_tarixi_{grade}_uzb.pdf", "source_filename"
        )
        require(
            [p["pdf_page"] for p in book["pages"]]
            == list(range(1, book["pdf_page_count"] + 1)),
            "page_gap_or_duplicate",
        )
        require(
            all(len(p["native_text_sha256"]) == 64 for p in book["pages"]),
            "native_page_digest",
        )
        chapters = {c["id"]: c for c in book["chapters"]}
        require(
            len(chapters) == len(book["chapters"])
            and [c["order"] for c in book["chapters"]]
            == list(range(1, len(chapters) + 1)),
            "chapter_order",
        )
        topics = book["topics"]
        require(
            [t["sequence"] for t in topics] == list(range(1, len(topics) + 1)),
            "topic_sequence",
        )
        numbers = [n for t in topics for n in t["source_numbers"]]
        require(
            numbers == list(range(1, max(numbers) + 1)),
            "source_paragraph_gap_or_duplicate",
        )
        require(len({t["id"] for t in topics}) == len(topics), "duplicate_topic")
        previous = (0, 0)
        for t in topics:
            require(
                t["chapter_id"] in chapters
                and t["title"]
                and t["verification"] == "original_heading_image_and_toc_checked",
                "topic_source_review",
            )
            pos = t["pdf_page"], t["heading_bbox"][1]
            require(
                pos > previous
                and 1 <= t["pdf_page"] <= t["pdf_end"] <= book["pdf_page_count"],
                "topic_page_order",
            )
            previous = pos
            require(
                t["printed_page"] == book["pages"][t["pdf_page"] - 1]["printed_page"],
                "printed_page_identity",
            )
            require(
                t["heading_image_review"]["verification"]
                == "original_heading_image_checked",
                "heading_image_review_missing",
            )
            require(t["facts_reviewed"] is False, "catalog_is_not_fact_approval")
            require(
                t["toc_body_page_match"]
                == (t["toc_printed_start"] == t["printed_page"]),
                "false_toc_body_match",
            )
            if not t["toc_body_page_match"]:
                require(
                    (
                        grade,
                        t["source_numbers"],
                        t["toc_printed_start"],
                        t["printed_page"],
                    )
                    == (10, [25], 132, 123)
                    and bool(t["review_note"]),
                    "unreviewed_toc_body_discrepancy",
                )
        require(
            book["counts"]
            == {
                "chapters": len(chapters),
                "teaching_entries": len(topics),
                "numbered_paragraphs": len(numbers),
            },
            "source_counts",
        )
        count += len(topics)
    require(catalog["known_catalogued_teaching_entries"] == count, "catalogued_total")
    require(
        catalog["complete_source_catalog"] == (not blocked), "false_source_complete"
    )
    require(
        catalog["all_five_book_teaching_total"] == (count if not blocked else None),
        "invented_five_book_total",
    )
    for b in catalog["blocked_books"]:
        require(
            b["status"] == "not_transferred" and b["sha256"] is None,
            "unread_source_must_not_claim_identity",
        )
    return {
        "available_books": len(grades),
        "blocked_grades": blocked,
        "catalogued_teaching_entries": count,
        "all_five_total": catalog["all_five_book_teaching_total"],
    }


def verify_originals(catalog, directory):
    """Optional actual supplied bytes/native hashes/reviewed header pixels check."""
    import fitz

    validate_catalog(catalog)
    count = 0
    for book in catalog["books"]:
        matches = [
            p
            for p in Path(directory).rglob(book["file_name"])
            if hashlib.sha256(p.read_bytes()).hexdigest() == book["sha256"]
        ]
        require(bool(matches), "pinned_original_not_available")
        with fitz.open(matches[0]) as pdf:
            require(len(pdf) == book["pdf_page_count"], "original_page_count")
            for audit, page in zip(book["pages"], pdf):
                require(
                    hashlib.sha256(page.get_text().encode()).hexdigest()
                    == audit["native_text_sha256"],
                    "original_native_text_changed",
                )
                count += 1
            for topic in book["topics"]:
                review = topic["heading_image_review"]
                # Match original unrounded clip coordinates used for the viewed crop.
                page = pdf[topic["pdf_page"] - 1]
                y = topic["heading_bbox"][1]
                clip = fitz.Rect(
                    20,
                    max(0, y - 4),
                    page.rect.width - 20,
                    min(page.rect.height, y + 80),
                )
                actual = page.get_pixmap(
                    matrix=fitz.Matrix(1.8, 1.8), clip=clip
                ).tobytes("png")
                require(
                    hashlib.sha256(actual).hexdigest() == review["sha256"],
                    "original_heading_image_changed",
                )
    return {
        "original_pages": count,
        "original_heading_images": sum(len(b["topics"]) for b in catalog["books"]),
    }
