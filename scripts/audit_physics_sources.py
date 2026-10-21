"""Offline, source-only Physics stage-one audit. Never imports ORM or publishes.

An internally consistent PARTIAL catalogue can pass. --require-mapped checks
the accepted section scope; --require-complete additionally requires all facts
and formulas. Optional --pdf-dir verifies private PDFs and raster anchors;
--ocr-dir also checks private OCR fingerprints (never committed).
PyMuPDF 1.26.6 is needed only for that optional source verification, not runtime.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "scripts/curriculum/physics/physics_sources.json"
FORMULAS = CATALOG.with_name("physics_formula_review.json")
SECTION_KINDS = {"topic", "laboratory", "home_practical", "practical", "problem_practice"}
EXPECTED_SECTIONS = {6: 61, 7: 46, 8: 60, 9: 59, 10: 45, 11: 45}


def require(condition, code):
    if not condition:
        raise ValueError(code)


def digest(value):
    return hashlib.sha256(value).hexdigest()


def canonical_digest(value):
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True).encode())


def is_digest(value):
    return isinstance(value, str) and bool(re.fullmatch(r"[0-9a-f]{64}", value))


def raster_region_digest(pixels, width, channels, box):
    """Fingerprint the original RGB coordinates without resizing the image."""
    x0, y0, x1, y1 = box
    stride = width * channels
    return digest(b"".join(pixels[y * stride + x0 * channels:y * stride + x1 * channels]
                           for y in range(y0, y1)))


def segment_at(book, page):
    return next(s for s in book["segments"] if s["start"] <= page <= s["end"])


def validate_segments(book):
    segments = book["segments"]
    require(segments and book["grade"] in (8, 9), "unexpected_segmented_book")
    require("sha256" not in book, "segment_set_is_not_a_whole_pdf_digest")
    cursor = 1
    for segment in segments:
        start, end = segment["start"], segment["end"]
        require(start == cursor and end >= start, "segment_gap_overlap_or_order")
        require(segment["pages"] == end - start + 1, "segment_page_count_mismatch")
        require(is_digest(segment["sha256"]), "invalid_segment_digest")
        require(re.fullmatch(rf"fizika_{book['grade']}_uzb_qism_\d+_pdf_{start}-{end}\.pdf",
                             segment["file_name"]), "segment_filename_range_mismatch")
        cursor = end + 1
    require(cursor == book["pdf_page_count"] + 1, "segment_total_page_count_mismatch")
    # This hashes a manifest, not the bytes of an imaginary merged PDF.
    require(book["source_set_sha256"] == digest(json.dumps(segments, sort_keys=True).encode()),
            "segment_manifest_digest_mismatch")


def validate_segment_citation(book, source, pdf):
    segment = segment_at(book, pdf)
    require(source["file_name"] == segment["file_name"]
            and source["sha256"] == segment["sha256"]
            and source["original_pdf_page"] == pdf
            and source["local_pdf_page"] == pdf - segment["start"] + 1,
            "segment_citation_mismatch")


def require_mapped(catalog):
    for book in catalog["books"]:
        require(book.get("mapping_scope_complete") is True
                and (book.get("counts") or {}).get("numbered_sections") == EXPECTED_SECTIONS[book["grade"]],
                "accepted_section_mapping_incomplete")
        if not book["source_complete"]:
            scope = book.get("accepted_mapping_scope", {})
            require(book["grade"] == 7 and scope.get("numbered_sections") == [1, 46]
                    and scope.get("missing_front_matter_blocks_mapping") is False
                    and book["page_numbering"]["missing_printed_pages"] == list(range(1, 8)),
                    "missing_source_not_covered_by_user_scope")


def require_complete(catalog, formulas):
    # Grade 7's explicitly accepted §1–46 scope applies to this gate too.
    # Missing front matter must not become a permanent course-authoring blocker.
    require_mapped(catalog)
    require(all(b.get("review", {}).get("all_facts_reviewed")
                and b.get("review", {}).get("all_formulas_reviewed") for b in catalog["books"])
            and formulas["full_formula_inventory_complete"], "complete_source_and_formula_review_blocked")


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
        require(publication == {"published": False, "ready_interactive_lessons": 0,
                                "ready_questions": 0, "runtime_import": False},
                "no_runtime_publication_or_import")
        if book["status"].startswith("blocked_"):
            require(not book["records"] and not book["page_audit"], "blocked_book_cannot_claim_mapping")
            require(book["counts"] is None, "unread_book_counts_are_unknown_not_zero")
            require(not any(k in book for k in ("authors", "year", "sha256", "title")),
                    "unread_book_cannot_claim_metadata")
            continue
        segmented = book.get("source_kind") == "ordered_pdf_segments"
        if segmented:
            validate_segments(book)
        else:
            require(is_digest(book["sha256"]), "invalid_source_digest")
        require(book["authors"] and book["year"] and book["bibliography_pdf_pages"],
                "bibliography_source_required")
        page_count = book["pdf_page_count"]
        pages = book["page_audit"]
        require([p["pdf_page"] for p in pages] == list(range(1, page_count + 1)),
                "all_actual_pdf_pages_must_be_accounted_for")
        for page in pages:
            require(re.fullmatch(r"[0-9a-f]{64}", page["text_sha256"]), "invalid_page_digest")
            require(page["review"] == ("ocr_extracted_not_fact_validated" if segmented
                                       else "digital_text_extracted_not_fact_validated"),
                    "extraction_is_not_fact_validation")
            if segmented:
                segment = segment_at(book, page["pdf_page"])
                require(page["segment_file_name"] == segment["file_name"]
                        and page["segment_local_pdf_page"] == page["pdf_page"] - segment["start"] + 1,
                        "page_segment_offset_mismatch")
                require(is_digest(page["digital_text_sha256"]) and is_digest(page["raster_sha256"]),
                        "raster_and_raw_text_digest_required")
                require(page["printed_label_review"] == ("page_image_label_checked" if page["printed_page"]
                                                           else "no_printed_label_visible"),
                        "printed_label_review_required")
        for exception in book["page_numbering"].get("exceptions", []):
            require(pages[exception["pdf_page"] - 1]["printed_page"] == exception["printed_page"],
                    "page_numbering_exception_mismatch")
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
        if segmented:
            expected["practicals"] = sum(r["kind"] == "practical" for r in sections)
            expected["problem_practice_sections"] = sum(r["kind"] == "problem_practice" for r in sections)
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
            require(row["source_status"] == ("body_heading_image_checked" if segmented
                                              else "body_heading_text_checked"),
                    "toc_alone_is_not_body_review")
            span = row["body_span"]
            require(span["next_boundary_is_exclusive"] is True, "explicit_shared_page_boundary_required")
            if segmented:
                require(span["start_pdf_page"] == row["pdf_start"]
                        and span["start_image_y"] == row["verification"]["image_bbox"][1],
                        "invalid_raster_span")
                require(row["pdf_start"] <= span["end_pdf_page"] <= page_count
                        and span["end_image_y_exclusive"] >= 0, "invalid_raster_end_span")
                verification = row["verification"]
                width, height = pages[row["pdf_start"] - 1]["raster_size"]
                x0, y0, x1, y1 = verification["image_bbox"]
                require(0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height,
                        "invalid_heading_raster_bbox")
                require(verification["page_raster_sha256"] == pages[row["pdf_start"] - 1]["raster_sha256"]
                        and is_digest(verification["image_region_sha256"]), "heading_raster_mismatch")
                regions = row["source_regions"]
                require([r["pdf_page"] for r in regions] == list(range(row["pdf_start"], row["pdf_end"] + 1)),
                        "source_region_gap_or_order")
                for region in regions:
                    p = region["pdf_page"]
                    width, height = pages[p - 1]["raster_size"]
                    x0, y0, x1, y1 = region["image_bbox"]
                    require(x0 == 0 and x1 == width and 0 <= y0 < y1 <= height,
                            "invalid_source_region_bbox")
                    require(y0 == (span["start_image_y"] if p == row["pdf_start"] else 0)
                            and y1 == (span["end_image_y_exclusive"] if p == span["end_pdf_page"] else height),
                            "region_must_match_clipped_span")
                    require(is_digest(region["ocr_text_sha256"]) and is_digest(region["image_region_sha256"]),
                            "region_fingerprints_required")
            else:
                require(span["start_pdf_page"] == row["pdf_start"] and span["start_text_offset"] >= 0,
                        "invalid_body_span")
                require(span["end_pdf_page"] >= span["start_pdf_page"] and span["end_text_offset_exclusive"] >= 0,
                        "invalid_end_span")
            analysis = row["source_analysis"]
            for field in ("worked_example_pdf_pages", "exercise_pdf_pages",
                          "practical_instruction_pdf_pages", "equation_candidate_pdf_pages",
                          *(('theory_source_pdf_pages', 'definition_candidate_pdf_pages',
                             'law_candidate_pdf_pages', 'unit_candidate_pdf_pages') if segmented else ())):
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
    require(isinstance(formulas.get("full_formula_inventory_complete"), bool), "formula_review_flag_required")
    if formulas["full_formula_inventory_complete"]:
        require(all(b.get("review", {}).get("all_formulas_reviewed") for b in books)
                and all(topic[1]["source_analysis"]["formula_inventory_complete"] for topic in topics.values()),
                "full_formula_claim_needs_topic_reviews")
    require(formulas.get("ready_questions") == 0, "formula_transcription_is_not_question_authoring")
    require(len({f["id"] for f in formulas["entries"]}) == len(formulas["entries"]), "duplicate_formula")
    for formula in formulas["entries"]:
        require(formula["topic_id"] in topics, "formula_topic_not_mapped")
        book, topic = topics[formula["topic_id"]]
        require(formula["grade"] == book["grade"], "formula_grade_mismatch")
        source = formula["source"]
        segmented = book.get("source_kind") == "ordered_pdf_segments"
        key = "source_set_sha256" if segmented else "sha256"
        require(source["book_id"] == book["id"] and source[key] == book[key]
                and source["file_name"] == book["file_name"], "formula_source_identity_mismatch")
        require(source["pdf_pages"] and len(source["pdf_pages"]) == len(source["printed_pages"]),
                "both_page_number_systems_required")
        for pdf, printed in zip(source["pdf_pages"], source["printed_pages"]):
            require(topic["pdf_start"] <= pdf <= topic["pdf_end"], "formula_outside_source_topic")
            require(book["page_audit"][pdf - 1]["printed_page"] == printed, "formula_printed_page_mismatch")
            require(book["page_audit"][pdf - 1]["text_sha256"] == source["page_text_sha256"],
                    "formula_page_digest_mismatch")
        if segmented:
            require(len(source["segment_citations"]) == len(source["pdf_pages"]),
                    "each_formula_page_needs_segment_citation")
            for citation, pdf in zip(source["segment_citations"], source["pdf_pages"]):
                validate_segment_citation(book, citation, pdf)
                require(source["page_raster_sha256"] == book["page_audit"][pdf - 1]["raster_sha256"],
                        "formula_raster_digest_mismatch")
        require(formula["verification"] == "page_image_transcription_reviewed", "formula_visual_review_required")
        require(formula["executable_grading_rule"] is False and formula["ready_for_publication"] is False,
                "stage_one_has_no_executable_grading_rules")
    baseline = catalog.get("preserved_mapping_baseline")
    if baseline:
        for grade, expected in baseline["grades"].items():
            book = next(b for b in books if b["grade"] == int(grade))
            for field, fingerprint in expected.items():
                require(canonical_digest(book[field]) == fingerprint, "baseline_source_mapping_changed")
        require(canonical_digest(formulas["entries"][:baseline["first_formula_entries"]])
                == baseline["first_formula_entries_sha256"], "baseline_formula_transcriptions_changed")
    return {"status": catalog["status"], "ready_lessons": 0,
            "selected_formula_transcriptions": len(formulas["entries"]),
            "full_formula_inventory_complete": formulas["full_formula_inventory_complete"],
            "formula_transcriptions_by_grade": dict(Counter(f["grade"] for f in formulas["entries"])),
            "grades": [{"grade": b["grade"], "status": b["status"], "counts": b["counts"]}
                       for b in books]}


def verify_private_sources(catalog, directory, ocr_directory=None):
    import fitz

    checked = 0
    ocr_checked = 0
    for book in catalog["books"]:
        if book["status"].startswith("blocked_"):
            continue
        if book.get("source_kind") == "ordered_pdf_segments":
            for segment in book["segments"]:
                candidates = directory.rglob(segment["file_name"])
                path = next((p for p in candidates if digest(p.read_bytes()) == segment["sha256"]), None)
                require(path is not None, f"private_segment_missing_or_changed_{segment['file_name']}")
                with fitz.open(path) as document:
                    require(len(document) == segment["pages"], "source_segment_page_count_changed")
                    for local, source_page in enumerate(document, 1):
                        p = segment["start"] + local - 1
                        page = book["page_audit"][p - 1]
                        require(digest(source_page.get_text().encode()) == page["digital_text_sha256"],
                                "source_raw_text_changed")
                        pixmap = source_page.get_pixmap(matrix=fitz.Matrix(2.2, 2.2))
                        pixels = pixmap.samples
                        require([pixmap.width, pixmap.height] == page["raster_size"]
                                and digest(pixels) == page["raster_sha256"],
                                "source_raster_changed_check_renderer_version")

                        ocr_root = ocr_directory / f"g{book['grade']}-ocr" if ocr_directory else None
                        if ocr_root:
                            text = (ocr_root / f"p{p:03}.txt").read_text()
                            require(digest(text.encode()) == page["text_sha256"], "private_ocr_page_changed")
                            ocr_checked += 1
                        for topic in book["records"]:
                            if topic["kind"] not in SECTION_KINDS:
                                continue
                            if topic["pdf_start"] == p:
                                require(raster_region_digest(pixels, pixmap.width, pixmap.n,
                                                             topic["verification"]["image_bbox"])
                                        == topic["verification"]["image_region_sha256"],
                                        "private_heading_raster_changed")
                            for region in topic["source_regions"]:
                                if region["pdf_page"] != p:
                                    continue
                                box = region["image_bbox"]
                                require(raster_region_digest(pixels, pixmap.width, pixmap.n, box)
                                        == region["image_region_sha256"],
                                        "private_region_raster_changed")
                                if ocr_root:
                                    whole = box == [0, 0, pixmap.width, pixmap.height]
                                    name = (f"p{p:03}.txt" if whole else
                                            f"section-{topic['number']:02}-p{p:03}.txt")
                                    value = (ocr_root / name).read_text()
                                    require(digest(value.encode()) == region["ocr_text_sha256"],
                                            "private_region_ocr_changed")
                        checked += 1
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
            require(re.search(pattern, tail, re.IGNORECASE), "body_heading_not_found_at_anchor")
    return {"private_pdf_pages_verified": checked, "private_ocr_pages_verified": ocr_checked}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-dir", type=Path, help="Private source directory; never committed")
    parser.add_argument("--ocr-dir", type=Path, help="Private cached OCR root; requires --pdf-dir")
    parser.add_argument("--require-mapped", action="store_true", help="Require all accepted section maps, not full formula review")
    parser.add_argument("--require-complete", action="store_true", help="Require full fact/formula review in the accepted source scope")
    args = parser.parse_args()
    try:
        catalog, formulas = load_documents()
        report = validate(catalog, formulas)
        require(args.ocr_dir is None or args.pdf_dir is not None, "ocr_verification_needs_private_pdfs")
        if args.pdf_dir:
            report.update(verify_private_sources(catalog, args.pdf_dir, args.ocr_dir))
        if args.require_mapped:
            require_mapped(catalog)
            report["accepted_section_mapping_complete"] = True
        if args.require_complete:
            require_complete(catalog, formulas)
        print(json.dumps(report, ensure_ascii=False, indent=2))
    except (ValueError, KeyError, OSError, StopIteration) as exc:
        print(f"Physics source audit: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
