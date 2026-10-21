"""Source-only stage gates: these do not assert ready Physics course content."""

import copy
import os
import subprocess
import sys

import pytest

from scripts.audit_physics_sources import ROOT, load_documents, validate


@pytest.fixture
def documents():
    return copy.deepcopy(load_documents())


def test_partial_map_reports_real_counts_without_claiming_lessons(documents):
    catalog, formulas = documents
    report = validate(catalog, formulas)
    assert report["ready_lessons"] == 0
    assert report["selected_formula_transcriptions"] == 37
    mapped = [b for b in catalog["books"] if b["counts"] is not None]
    assert sum(b["counts"]["numbered_sections"] for b in mapped) == 197
    assert sum(b["counts"]["theory_topics"] for b in mapped) == 176
    assert sum(b["counts"]["laboratories"] for b in mapped) == 20
    assert sum(b["counts"]["home_practicals"] for b in mapped) == 1
    assert sum(b["pdf_page_count"] for b in mapped) == 717


def test_unavailable_book_counts_remain_unknown(documents):
    catalog, formulas = documents
    book = next(b for b in catalog["books"] if b["grade"] == 8)
    assert book["counts"] is None
    book["counts"] = {"theory_topics": 0}
    with pytest.raises(ValueError, match="unread_book_counts_are_unknown"):
        validate(catalog, formulas)


def test_unavailable_book_cannot_invent_bibliography(documents):
    catalog, formulas = documents
    catalog["books"][3]["year"] = 2017
    with pytest.raises(ValueError, match="unread_book_cannot_claim_metadata"):
        validate(catalog, formulas)


def test_grade_seven_pdf_is_not_assumed_to_start_at_printed_one(documents):
    catalog, formulas = documents
    book = catalog["books"][1]
    first = next(r for r in book["records"] if r["kind"] == "topic")
    assert (first["pdf_start"], first["printed_start"]) == (1, 8)
    assert book["source_complete"] is False
    first["printed_start"] = 1
    with pytest.raises(ValueError, match="printed_and_pdf_page_mismatch"):
        validate(catalog, formulas)


def test_chapter_introduction_and_first_topic_are_distinct_pages(documents):
    catalog, _ = documents
    book = catalog["books"][5]
    chapter = next(r for r in book["records"] if r["id"] == "physics-11-chapter-3")
    topic = next(r for r in book["records"] if r["id"] == "physics-11-section-11")
    assert (chapter["printed_start"], chapter["pdf_start"]) == (41, 42)
    assert (topic["printed_start"], topic["pdf_start"]) == (42, 43)


def test_lab_and_home_practical_are_not_counted_as_theory(documents):
    catalog, formulas = documents
    book = catalog["books"][0]
    home = next(r for r in book["records"] if r["number"] == 13 and r["kind"] != "chapter")
    assert home["kind"] == "home_practical"
    home["kind"] = "topic"
    with pytest.raises(ValueError, match="counts_do_not_match_source_records"):
        validate(catalog, formulas)


def test_mundarija_only_is_not_body_verification(documents):
    catalog, formulas = documents
    topic = next(r for r in catalog["books"][0]["records"] if r["kind"] == "topic")
    topic["source_status"] = "toc_only"
    with pytest.raises(ValueError, match="toc_alone_is_not_body_review"):
        validate(catalog, formulas)


def test_wrong_book_formula_citation_is_rejected(documents):
    catalog, formulas = documents
    formulas["entries"][0]["source"]["sha256"] = "a" * 64
    with pytest.raises(ValueError, match="formula_source_identity_mismatch"):
        validate(catalog, formulas)


def test_formula_outside_its_topic_is_rejected(documents):
    catalog, formulas = documents
    formulas["entries"][0]["source"]["pdf_pages"] = [70]
    formulas["entries"][0]["source"]["printed_pages"] = [70]
    with pytest.raises(ValueError, match="formula_outside_source_topic"):
        validate(catalog, formulas)


def test_source_transcription_does_not_become_executable_grader(documents):
    catalog, formulas = documents
    formulas["entries"][0]["executable_grading_rule"] = True
    with pytest.raises(ValueError, match="stage_one_has_no_executable_grading_rules"):
        validate(catalog, formulas)


@pytest.mark.parametrize("field", ["physics_published", "ai_explain_planned"])
def test_stage_one_cannot_publish_or_enable_ai_explain(documents, field):
    catalog, formulas = documents
    catalog[field] = True
    with pytest.raises(ValueError):
        validate(catalog, formulas)


def test_exact_page_clipping_does_not_attach_previous_formula_to_new_topic(documents):
    catalog, _ = documents
    book = catalog["books"][0]
    lens = next(r for r in book["records"] if r["id"] == "physics-6-section-53")
    prism = next(r for r in book["records"] if r["id"] == "physics-6-section-54")
    assert 147 in lens["source_analysis"]["equation_candidate_pdf_pages"]
    assert 147 not in prism["source_analysis"]["equation_candidate_pdf_pages"]
    assert lens["body_span"]["end_pdf_page"] == prism["pdf_start"]
    assert lens["body_span"]["end_text_offset_exclusive"] == prism["heading_offset"]


def test_offline_audit_is_safe_even_with_unreachable_production_database_url():
    env = dict(os.environ, ENVIRONMENT="production",
               DATABASE_URL="postgresql://not-used.invalid/physics-audit-must-not-connect")
    result = subprocess.run([sys.executable, "scripts/audit_physics_sources.py"],
                            cwd=ROOT, env=env, capture_output=True, text=True, timeout=10)
    assert result.returncode == 0, result.stderr
    assert '"ready_lessons": 0' in result.stdout
    assert "private_pdf_pages_verified" not in result.stdout


def test_full_completion_gate_fails_truthfully():
    result = subprocess.run([sys.executable, "scripts/audit_physics_sources.py", "--require-complete"],
                            cwd=ROOT, capture_output=True, text=True, timeout=10)
    assert result.returncode == 2
    assert "complete_source_and_formula_review_blocked" in result.stderr
