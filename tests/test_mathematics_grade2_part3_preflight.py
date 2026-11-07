"""Boundary inventory is not lesson/body completeness."""

import json

from services.mathematics_curriculum import ROOT, load_course, manifest


def test_part3_real48_boundaries_do_not_create_any_completed_lessons():
    d = json.loads((ROOT / "grade2_part3_preflight.json").read_text())
    b = next(b for b in manifest()["books"] if b["book_id"] == d["book_id"])
    assert d["sha256"] == b["sha256"] and d["pdf_pages"] == b["pdf_pages"] == 106
    assert d["mapped_body_units"] == 48 and d["numbered_units"] == 44
    assert d["unnumbered_summaries"] == 3 and d["logical_collections"] == 1
    assert [t["source_number"] for t in d["topics"] if t["source_number"]] == list(
        range(73, 117)
    )
    assert [p for t in d["topics"] for p in t["pdf_pages"]] == list(range(5, 102))
    assert all(
        t["printed_pages"] == [p - 1 for p in t["pdf_pages"]] for t in d["topics"]
    )
    assert all(
        t["boundary_images_reviewed"] and not t["interactive_lesson_created"]
        for t in d["topics"]
    )
    assert sum(t["body_images_reviewed"] for t in d["topics"]) == 5
    assert not d["all_body_content_reviewed"] and not d["course_ready"]
    assert d["authored_lessons"] == 0
    mapping = json.loads((ROOT / "grade2_part3_map.json").read_text())
    assert (
        sum(l["grade"] == 2 and l["part"] == 3 for l in load_course())
        == mapping["authored_lessons"]
    )
    assert (
        d["topics"][22]["source_number"] == 94
        and d["topics"][23]["source_number"] == 95
    )
    assert d["topics"][22]["pdf_pages"] != d["topics"][23]["pdf_pages"]
