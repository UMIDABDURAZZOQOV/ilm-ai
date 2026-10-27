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


def validate_segment_manifest(manifest):
    """Segment byte identity and image mapping; never infer an unsplit PDF hash."""
    require(
        manifest["original_unsplit_sha256"] is None, "untransferred_unsplit_identity"
    )
    require(manifest["pdf_pages"] == 160, "segment_expected_page_count")
    sequence = []
    segments = {}
    for part in manifest["segments"]:
        require(
            Path(part["file_name"]).name == part["file_name"]
            and len(part["sha256"]) == 64
            and 0 < part["size_bytes"] < 32 * 1024 * 1024,
            "segment_identity",
        )
        first, last = part["first_pdf_page"], part["last_pdf_page"]
        require(last - first + 1 == part["pdf_page_count"], "segment_count")
        require(part["file_name"] not in segments, "duplicate_segment")
        segments[part["file_name"]] = part
        sequence.extend(range(first, last + 1))
    require(sequence == list(range(1, 161)), "segment_gap_overlap_or_order")
    require(
        [p["pdf_page"] for p in manifest["pages"]] == sequence, "segment_page_mapping"
    )
    seen = set()
    for page in manifest["pages"]:
        part = segments.get(page["segment_file_name"])
        require(
            part is not None
            and 1 <= page["segment_pdf_page"] <= part["pdf_page_count"]
            and page["pdf_page"]
            == part["first_pdf_page"] + page["segment_pdf_page"] - 1,
            "segment_local_page_mapping",
        )
        require(
            len(page["image_sha256"]) == 64 and page["image_sha256"] not in seen,
            "duplicate_or_missing_page_image",
        )
        seen.add(page["image_sha256"])
        n = page["pdf_page"]
        require(
            page["printed_page"] == (n if 3 <= n <= 159 else None),
            "segment_printed_mapping",
        )
        require(page["image_matrix"] == [1.4, 1.4], "segment_image_render")
    require(
        manifest["continuity_review"]["all_numbered_footers_visually_checked"] is True,
        "segment_footer_review_missing",
    )


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
        if book.get("source_kind") == "reassembled_uploaded_segments":
            require(
                book["source_manifest_file"] == "grade8_segments.json" and grade == 8,
                "unsupported_segment_manifest",
            )
            manifest = json.loads(
                (DIRECTORY / book["source_manifest_file"]).read_text()
            )
            validate_segment_manifest(manifest)
            require(
                digest(manifest) == book["source_manifest_sha256"]
                and manifest["derived_pdf_sha256"] == book["sha256"]
                and book["original_unsplit_sha256"] is None,
                "segment_manifest_digest",
            )
            require(
                all(
                    a["image_sha256"] == b.get("image_sha256")
                    and a["printed_page"] == b["printed_page"]
                    for a, b in zip(manifest["pages"], book["pages"])
                ),
                "segment_book_page_evidence",
            )
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
        if book.get("source_kind") == "reassembled_uploaded_segments":
            manifest = json.loads(
                (DIRECTORY / book["source_manifest_file"]).read_text()
            )
            for part in manifest["segments"]:
                originals = [
                    p
                    for p in Path(directory).rglob(part["file_name"])
                    if hashlib.sha256(p.read_bytes()).hexdigest() == part["sha256"]
                ]
                require(bool(originals), "pinned_segment_not_available")
                with fitz.open(originals[0]) as segment:
                    require(
                        len(segment) == part["pdf_page_count"],
                        "segment_actual_page_count",
                    )
                    for local, page in enumerate(segment, 1):
                        evidence = manifest["pages"][part["first_pdf_page"] + local - 2]
                        pixels = page.get_pixmap(matrix=fitz.Matrix(1.4, 1.4)).tobytes(
                            "png"
                        )
                        require(
                            hashlib.sha256(pixels).hexdigest()
                            == evidence["image_sha256"],
                            "original_segment_page_image_changed",
                        )
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
                if book.get("source_kind") == "reassembled_uploaded_segments":
                    pixels = page.get_pixmap(matrix=fitz.Matrix(1.4, 1.4)).tobytes(
                        "png"
                    )
                    require(
                        hashlib.sha256(pixels).hexdigest() == audit["image_sha256"],
                        "reassembled_page_differs_from_original_segment",
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
