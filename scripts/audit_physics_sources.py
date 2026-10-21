"""Offline, source-only Physics stage-one audit. Never imports ORM or publishes.

An internally consistent PARTIAL catalogue can pass. --require-complete is a
separate gate and must fail while a book/formula review is missing. Optional
--pdf-dir verifies the private PDFs, every extracted page, and body anchors.
PyMuPDF 1.26.6 is needed only for that optional source verification, not runtime.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "scripts/curriculum/physics/physics_sources.json"
FORMULAS = CATALOG.with_name("physics_formula_review.json")
SECTION_KINDS = {"topic", "laboratory", "home_practical"}


def require(condition, code):
    if not condition:
        raise ValueError(code)


def digest(value):
    return hashlib.sha256(value).hexdigest()


def load_documents():
    return json.loads(CATALOG.read_text()), json.loads(FORMULAS.read_text())


def validate(catalog, formulas):
    require(catalog.get("schema_version") == 1, "unsupported_catalog")
    require(catalog.get("subject_slug") == "fizika", "wrong_subject")
    require(catalog.get("language") == "uz", "uzbek_source_required")
    require(catalog.get("stage") == "source_mapping_and_design_only", "wrong_stage")
    require(catalog.get("physics_published") is False, "physics_must_remain_unpublished")
    require(catalog.get("ai_explain_planned") is False, "ai_explain_out_of_scope")
    require(catalog.get("ready_interactive_lessons") == 0, "no_authored_lessons_in_stage_one")
    require(catalog.get("ready_questions") == 0, "no_ready_questions_in_stage_one")
    books = catalog["books"]
    require([b["grade"] for b in books] == list(range(6, 12)), "six_ordered_grades_required")
    require(len({b["id"] for b in books}) == 6, "unique_book_ids_required")
    topics = {}
    for book in books:
        grade = book["grade"]
        require(book["file_name"] == f"fizika_{grade}_uzb.pdf", "unexpected_source_file")
        publication = book["publication"]
        require(publication == dict(published=False, ready_interactive_lessons=0,
                                    ready_questions=0, runtime_import=False),
                "no_runtime_publication_or_import")
        if book["status"].startswith("blocked_"):
            require(not book["records"] and not book["page_audit"], "blocked_book_cannot_claim_mapping")
            require(book["counts"] is None, "unread_book_counts_are_unknown_not_zero")
            require(not any(k in book for k in ("authors", "year", "sha256", "title")),
                    "unread_book_cannot_claim_metadata")
            continue
        require(re.fullmatch(r"[0-9a-f]{64}", book["sha256"]), "invalid_source_digest")
        require(book["authors"] and book["year"] and book["bibliography_pdf_pages"],
                "bibliography_source_required")
        page_count = book["pdf_page_count"]
        pages = book["page_audit"]
        require([p["pdf_page"] for p in pages] == list(range(1, page_count + 1)),
                "all_actual_pdf_pages_must_be_accounted_for")
        for page in pages:
            require(re.fullmatch(r"[0-9a-f]{64}", page["text_sha256"]), "invalid_page_digest")
            require(page["review"] == "digital_text_extracted_not_fact_validated",
                    "extraction_is_not_fact_validation")
        require(book["review"]["fulltext_republication"] == "not_authorized", "private_pdf_policy")
        records = book["records"]
        require(len({r["id"] for r in records}) == len(records), "duplicate_record")
        owners = {r["id"] for r in records if r["kind"] in {"chapter", "introduction"}}
        sections = [r for r in records if r["kind"] in SECTION_KINDS]
        require([r["number"] for r in sections] == list(range(1, len(sections) + 1)),
                "source_section_order_or_gap")
        expected = {
            "numbered_sections": len(sections),
            "theory_topics": sum(r["kind"] == "topic" for r in sections),
            "laboratories": sum(r["kind"] == "laboratory" for r in sections),
            "home_practicals": sum(r["kind"] == "home_practical" for r in sections),
            "chapters": sum(r["kind"] == "chapter" for r in records),
            "supplement_heading_counts": dict(Counter(s["kind"] for s in book["supplementary_sections"])),
        }
        require(book["counts"] == expected, "counts_do_not_match_source_records")
        for row in records:
            require(row["content_status"] == "not_authored", "mapping_is_not_a_ready_lesson")
            require(1 <= row["pdf_start"] <= page_count, "invalid_pdf_anchor")
            require(pages[row["pdf_start"] - 1]["printed_page"] == row["printed_start"],
                    "printed_and_pdf_page_mismatch")
        for row in sections:
            require(row["chapter_id"] in owners, "section_without_source_owner")
            require(1 <= row["toc_pdf_page"] <= page_count, "invalid_toc_anchor")
            require(row["toc_printed_start"] == row["printed_start"], "toc_body_discrepancy_requires_review")
            require(row["pdf_start"] <= row["pdf_end"] <= page_count, "invalid_topic_extent")
            require(pages[row["pdf_end"] - 1]["printed_page"] == row["printed_end"],
                    "invalid_topic_end_page")
            require(row["verification"]["body_page_text_sha256"] == pages[row["pdf_start"] - 1]["text_sha256"],
                    "body_anchor_digest_mismatch")
            require(row["source_status"] == "body_heading_text_checked", "toc_alone_is_not_body_review")
            span = row["body_span"]
            require(span["next_boundary_is_exclusive"] is True, "explicit_shared_page_boundary_required")
            require(span["start_pdf_page"] == row["pdf_start"] and span["start_text_offset"] >= 0,
                    "invalid_body_span")
            require(span["end_pdf_page"] >= span["start_pdf_page"] and span["end_text_offset_exclusive"] >= 0,
                    "invalid_end_span")
            analysis = row["source_analysis"]
            for field in ("worked_example_pdf_pages", "exercise_pdf_pages",
                          "practical_instruction_pdf_pages", "equation_candidate_pdf_pages"):
                require(all(row["pdf_start"] <= p <= row["pdf_end"] for p in analysis[field]),
                        "analysis_outside_source_topic")
            require(analysis["physical_experiment_completion_claim"] is False, "no_fake_physical_activity")
            require(row["id"] not in topics, "duplicate_topic_id")
            topics[row["id"]] = (book, row)
        for section in book["supplementary_sections"]:
            require(section["content_status"] == "not_authored", "no_ready_supplement")
            p = section["pdf_start"]
            require(1 <= p <= page_count and pages[p - 1]["printed_page"] == section["printed_start"],
                    "invalid_supplement_citation")
            require(section["chapter_id"] is None or section["chapter_id"] in owners,
                    "invalid_supplement_owner")
        for section in book["reference_sections"]:
            p = section["pdf_start"]
            require(1 <= p <= page_count and pages[p - 1]["printed_page"] == section["printed_start"],
                    "invalid_reference_citation")
        if not book["source_complete"]:
            require(book["uncertainties"], "partial_book_must_explain_gaps")

    require(formulas.get("schema_version") == 1 and formulas.get("subject_slug") == "fizika",
            "unsupported_formula_review")
    require(formulas.get("full_formula_inventory_complete") is False, "full_formula_review_not_done")
    require(formulas.get("ready_questions") == 0, "formula_transcription_is_not_question_authoring")
    require(len({f["id"] for f in formulas["entries"]}) == len(formulas["entries"]), "duplicate_formula")
    for formula in formulas["entries"]:
        require(formula["topic_id"] in topics, "formula_topic_not_mapped")
        book, topic = topics[formula["topic_id"]]
        require(formula["grade"] == book["grade"], "formula_grade_mismatch")
        source = formula["source"]
        require(source["book_id"] == book["id"] and source["sha256"] == book["sha256"]
                and source["file_name"] == book["file_name"], "formula_source_identity_mismatch")
        require(source["pdf_pages"] and len(source["pdf_pages"]) == len(source["printed_pages"]),
                "both_page_number_systems_required")
        for pdf, printed in zip(source["pdf_pages"], source["printed_pages"]):
            require(topic["pdf_start"] <= pdf <= topic["pdf_end"], "formula_outside_source_topic")
            require(book["page_audit"][pdf - 1]["printed_page"] == printed, "formula_printed_page_mismatch")
            require(book["page_audit"][pdf - 1]["text_sha256"] == source["page_text_sha256"],
                    "formula_page_digest_mismatch")
        require(formula["verification"] == "page_image_transcription_reviewed", "formula_visual_review_required")
        require(formula["executable_grading_rule"] is False and formula["ready_for_publication"] is False,
                "stage_one_has_no_executable_grading_rules")
    return {"status": catalog["status"], "ready_lessons": 0,
            "selected_formula_transcriptions": len(formulas["entries"]),
            "grades": [{"grade": b["grade"], "status": b["status"], "counts": b["counts"]}
                       for b in books]}


def verify_private_sources(catalog, directory):
    import fitz

    checked = 0
    for book in catalog["books"]:
        if book["status"].startswith("blocked_"):
            continue
        candidates = list(directory.rglob(book["file_name"]))
        path = next((p for p in candidates if digest(p.read_bytes()) == book["sha256"]), None)
        require(path is not None, f"private_source_missing_or_changed_grade_{book['grade']}")
        with fitz.open(path) as document:
            require(len(document) == book["pdf_page_count"], "source_page_count_changed")
            text = [p.get_text() for p in document]
            # Decode every actual page, including image-only front/back covers.
            # Small renders verify readability; they do not review physics facts.
            for page in document:
                pixmap = page.get_pixmap(matrix=fitz.Matrix(0.15, 0.15))
                require(pixmap.width > 0 and pixmap.height > 0 and pixmap.samples,
                        "pdf_page_cannot_be_decoded")
        for page in book["page_audit"]:
            value = text[page["pdf_page"] - 1]
            require(digest(value.encode()) == page["text_sha256"], "page_text_changed_check_extractor_version")
            if page["printed_page"] is not None:
                lines = [s.strip() for s in value.splitlines() if s.strip()]
                require(str(page["printed_page"]) in lines[:4] + lines[-4:], "printed_label_not_found")
            checked += 1
        for topic in book["records"]:
            if topic["kind"] not in SECTION_KINDS:
                continue
            page = text[topic["pdf_start"] - 1]
            offset = topic["heading_offset"]
            tail = page[offset:]
            pattern = rf"^\s*{topic['number']}\s*[-–]\s*(?:MAVZU(?:\.|\s|$)|§\.?\s*)"
            require(re.search(pattern, tail, re.I), "body_heading_not_found_at_anchor")
    return checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-dir", type=Path, help="Private source directory; never committed")
    parser.add_argument("--require-complete", action="store_true", help="Fail on every unresolved source/fact/formula gate")
    args = parser.parse_args()
    try:
        catalog, formulas = load_documents()
        report = validate(catalog, formulas)
        if args.pdf_dir:
            report["private_pdf_pages_verified"] = verify_private_sources(catalog, args.pdf_dir)
        if args.require_complete:
            require(all(b.get("source_complete") and b.get("review", {}).get("all_facts_reviewed")
                        and b.get("review", {}).get("all_formulas_reviewed") for b in catalog["books"])
                    and formulas["full_formula_inventory_complete"], "complete_source_and_formula_review_blocked")
        print(json.dumps(report, ensure_ascii=False, indent=2))
    except (ValueError, KeyError, OSError) as exc:
        print(f"Physics source audit: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
