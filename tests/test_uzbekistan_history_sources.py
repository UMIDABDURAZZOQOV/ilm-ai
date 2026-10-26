"""Real source catalog integrity; heading review does not imply lesson readiness."""

from copy import deepcopy

import pytest

from services.uzbekistan_history_sources import load_catalog, validate_catalog


def test_four_supplied_books_are_real_and_eighth_grade_remains_blocked():
    d = load_catalog()
    r = validate_catalog(d)
    assert r == {
        "available_books": 4,
        "blocked_grades": [8],
        "catalogued_teaching_entries": 131,
        "all_five_total": None,
    }
    assert [b["pdf_page_count"] for b in d["books"]] == [161, 160, 144, 144]
    assert [b["counts"]["teaching_entries"] for b in d["books"]] == [42, 39, 28, 22]
    assert [b["counts"]["chapters"] for b in d["books"]] == [6, 9, 6, 9]
    assert all(not t["facts_reviewed"] for b in d["books"] for t in b["topics"])


def test_combined_paragraphs_are_one_source_teaching_entry_each():
    b = next(b for b in load_catalog()["books"] if b["grade"] == 9)
    assert [
        t["source_numbers"] for t in b["topics"] if len(t["source_numbers"]) > 1
    ] == [[4, 5], [35, 36]]
    assert b["counts"]["numbered_paragraphs"] == 41
    assert len(b["topics"]) == 39


def test_start_boundary_and_intra_page_end_preserved():
    b = load_catalog()["books"][0]
    a, c = b["topics"][:2]
    assert a["pdf_page"] == a["printed_page"] == 6
    assert a["pdf_end"] == c["pdf_page"] == 8
    assert a["end_boundary"]["y"] == c["heading_bbox"][1]
    assert a["end_boundary"]["next_topic_id"] == c["id"]


def test_only_reviewed_toc_page_discrepancy_is_explicit():
    b = next(b for b in load_catalog()["books"] if b["grade"] == 10)
    t = b["topics"][24]
    assert t["source_numbers"] == [25] and t["toc_printed_start"] == 132
    assert t["pdf_page"] == t["printed_page"] == 123
    assert not t["toc_body_page_match"] and t["review_note"]
    t7 = load_catalog()["books"][0]["topics"][31]
    assert t7["title"] != t7["toc_title"] and t7["source_numbers"] == [32]


@pytest.mark.parametrize(
    "change",
    [
        "page_gap",
        "topic_duplicate",
        "source_paragraph_gap",
        "bad_source_sha",
        "fake_complete",
        "invented_total",
        "wrong_subject",
        "wrong_printed",
        "unknown_toc_discrepancy",
        "missing_image",
        "missing_chapter",
    ],
)
def test_tamper_is_rejected(change):
    d = deepcopy(load_catalog())
    b = d["books"][0]
    t = b["topics"][0]
    if change == "page_gap":
        b["pages"].pop(5)
    elif change == "topic_duplicate":
        b["topics"][1]["id"] = t["id"]
    elif change == "source_paragraph_gap":
        t["source_numbers"] = [2]
    elif change == "bad_source_sha":
        b["sha256"] = "wrong"
    elif change == "fake_complete":
        d["complete_source_catalog"] = True
    elif change == "invented_total":
        d["all_five_book_teaching_total"] = 200
    elif change == "wrong_subject":
        b["subject"] = "jahon_tarixi"
    elif change == "wrong_printed":
        t["printed_page"] = 7
    elif change == "unknown_toc_discrepancy":
        t["toc_body_page_match"] = False
    elif change == "missing_image":
        t["heading_image_review"]["verification"] = "ocr_only"
    elif change == "missing_chapter":
        t["chapter_id"] = "no_chapter"
    with pytest.raises(ValueError):
        validate_catalog(d)


def test_parallel_source_baseline_is_unchanged():
    import hashlib
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    baseline = json.loads(
        (
            root / "scripts/curriculum/uzbekistan_history/protected_baseline.json"
        ).read_text()
    )
    for record in baseline["protected_files"]:
        assert (
            hashlib.sha256((root / record["path"]).read_bytes()).hexdigest()
            == record["sha256"]
        ), record["path"]
