"""Pure Chemistry evidence validation. No ORM, DB, network or LLM imports.

Keep Biology's validator and Physics's unfinished preview untouched. Catalogue
mapping is distinct from scientific claim review and executable lesson readiness.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "scripts/curriculum/chemistry"
SOURCE_PATH = DIRECTORY / "chemistry_sources.json"
PINNED_SOURCES = {
    7: ("a164c51ca0f55b8024e74d8e6daa32a3b10a3d45b33761630add81c47e24ce0a", 81, 51, 6, 16, 7),
    8: ("077e2c96380950d3dd4118489474a200a08d39ff226b7096dd48436df9bc8056", 208, 44, 6, 10, 5),
    9: ("ee3695eeb0598016629cc370dfcb0c73836250cf594f4d5d0cb2a06ea40c7386", 208, 41, 5, 17, 3),
    10: ("b9edd182161159f109fbbb668bc1656e00e221aab9411ec83b16ff1889244cb6", 160, 35, 4, 6, 0),
    11: ("ee3d429585691951eb0f5529553f5879869cd084e1886e01b950d6971cf2952b", 160, 33, 8, 0, 0),
}
TEACHING_KINDS = {"paragraph", "laboratory", "practical"}
HEADING_STATES = {"body_text_heading_verified", "body_image_heading_verified"}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def page_locator(grade, printed):
    if type(printed) is not int or printed < 1:
        raise ValueError("invalid_printed_page")
    if grade != 7:
        return {"pdf_page": printed, "region": "full"}
    if printed in {1, 160}:
        return {"pdf_page": 1 if printed == 1 else 81, "region": "full"}
    if printed > 160:
        raise ValueError("invalid_printed_page")
    return {"pdf_page": printed // 2 + 1,
            "region": "left" if printed % 2 == 0 else "right"}


def validate_catalog(catalog):
    if (catalog.get("schema_version") != 1 or catalog.get("subject_slug") != "kimyo"
            or catalog.get("language") != "uz"):
        raise ValueError("unsupported_chemistry_catalog")
    books = catalog.get("books", [])
    if sorted(b.get("grade", 0) for b in books) != list(range(7, 12)):
        raise ValueError("five_unique_chemistry_grades_required")
    all_ids = set()
    for book in books:
        grade = book["grade"]
        digest, pages, paras, chapters, labs, practicals = PINNED_SOURCES[grade]
        if (book.get("sha256") != digest or book.get("pdf_page_count") != pages
                or book.get("decoded_pages") != pages or book.get("source_status") != "mapped"):
            raise ValueError("unreviewed_source_identity_or_page_count")
        if (book.get("bibliography_review", {}).get("status") != "page_images_reviewed"
                or book.get("toc_review", {}).get("status") != "page_images_reviewed"):
            raise ValueError("source_image_review_required")
        if book.get("rights", {}).get("fulltext_republication") != "not_authorized":
            raise ValueError("source_rights_required")
        records = book.get("records", [])
        ids = {r["id"] for r in records}
        if len(ids) != len(records) or ids & all_ids:
            raise ValueError("duplicate_source_record")
        all_ids |= ids
        for kind, count in [("paragraph", paras), ("chapter", chapters),
                            ("laboratory", labs), ("practical", practicals)]:
            numbers = sorted(r["number"] for r in records if r["kind"] == kind)
            if numbers != list(range(1, count + 1)):
                raise ValueError("source_coverage_gap_or_duplicate")
        instructional = [r for r in records if r["kind"] in TEACHING_KINDS]
        for i, record in enumerate(instructional):
            expected = [instructional[i-1]["id"]] if i else []
            if record.get("sequence") != i+1 or record.get("prerequisite_ids") != expected:
                raise ValueError("source_prerequisite_order_mismatch")
        starts = [r["printed_start"] for r in records]
        if starts != sorted(starts):
            raise ValueError("source_order_changed")
        for r in records:
            if (r.get("source_id") != book["id"] or r.get("source_sha256") != digest
                    or r.get("source_file") != book["file_name"]):
                raise ValueError("record_source_identity_mismatch")
            if not 1 <= r["printed_start"] <= r["printed_end"] <= book["printed_page_count"]:
                raise ValueError("invalid_source_page_range")
            for name, field in [("start_locator", "printed_start"), ("end_locator", "printed_end")]:
                if r.get(name) != page_locator(grade, r[field]):
                    raise ValueError("printed_pdf_region_mapping_mismatch")
            state = r.get("heading_review", {}).get("status")
            if state not in HEADING_STATES or (grade >= 10 and state != "body_image_heading_verified"):
                raise ValueError("unreviewed_or_ocr_only_heading")
            if r["kind"] in TEACHING_KINDS and r.get("chapter_id") not in ids:
                raise ValueError("missing_source_container")
            if r.get("parent_id") and r["parent_id"] not in ids:
                raise ValueError("missing_source_parent")
            if r["kind"] in {"laboratory", "practical", "subactivity"}:
                if r.get("digital_activity_policy") != {
                    "mode": "guided_analysis", "physical_execution_required": False,
                    "real_lab_certification": False,
                }:
                    raise ValueError("digital_lab_policy_required")
    return catalog


def load_catalog():
    return validate_catalog(read_json(SOURCE_PATH))


def readiness(catalog, lessons=()):
    ready = {lesson["topic_id"] for lesson in lessons}
    result = []
    for book in catalog["books"]:
        rows = [r for r in book["records"] if r["kind"] in TEACHING_KINDS]
        result.append({"grade": book["grade"], "chapters": book["chapter_count"],
                       "paragraphs": book["paragraph_count"],
                       "laboratories": book["laboratory_count"],
                       "practicals": book["practical_count"],
                       "source_teaching_entries": len(rows),
                       "implemented_lessons": sum(r["id"] in ready for r in rows),
                       "remaining_ids": [r["id"] for r in rows if r["id"] not in ready],
                       "course_ready": all(r["id"] in ready for r in rows)})
    return result
