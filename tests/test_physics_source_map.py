"""Source-only stage gates: these do not assert ready Physics course content."""

import copy
import json
import os
import subprocess
import sys

import pytest

from scripts.audit_physics_sources import (
    ROOT,
    canonical_digest,
    load_documents,
    require_complete,
    require_mapped,
    validate,
    validate_segments,
)


@pytest.fixture
def documents():
    return copy.deepcopy(load_documents())


def test_six_available_maps_report_real_counts_without_claiming_lessons(documents):
    catalog, formulas = documents
    report = validate(catalog, formulas)
    assert report["ready_lessons"] == 0
    assert report["selected_formula_transcriptions"] == 145
    assert report["formula_transcriptions_by_grade"] == {6: 13, 7: 5, 8: 41, 9: 67, 10: 7, 11: 12}
    mapped = [b for b in catalog["books"] if b["counts"] is not None]
    assert sum(b["counts"]["numbered_sections"] for b in mapped) == 316
    assert sum(b["counts"]["theory_topics"] for b in mapped) == 254
    assert sum(b["counts"]["laboratories"] for b in mapped) == 31
    assert sum(b["counts"]["home_practicals"] for b in mapped) == 1
    assert sum(b["counts"].get("practicals", 0) for b in mapped) == 4
    assert sum(b["counts"].get("problem_practice_sections", 0) for b in mapped) == 26
    assert sum(b["pdf_page_count"] for b in mapped) == 1069
    assert report["full_formula_inventory_complete"] is False


def make_unavailable(book):
    for field in ("authors", "year", "sha256", "title"):
        book.pop(field, None)
    book.update(status="blocked_unavailable_test_source", records=[], page_audit=[], counts=None)


def test_unavailable_book_counts_remain_unknown(documents):
    catalog, formulas = documents
    book = next(b for b in catalog["books"] if b["grade"] == 8)
    make_unavailable(book)
    assert book["counts"] is None
    book["counts"] = {"theory_topics": 0}
    with pytest.raises(ValueError, match="unread_book_counts_are_unknown"):
        validate(catalog, formulas)


def test_unavailable_book_cannot_invent_bibliography(documents):
    catalog, formulas = documents
    make_unavailable(catalog["books"][3])
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
                            cwd=ROOT, env=env, capture_output=True, text=True, timeout=10, check=False)
    assert result.returncode == 0, result.stderr
    assert '"ready_lessons": 0' in result.stdout
    assert "private_pdf_pages_verified" not in result.stdout


def test_full_completion_gate_fails_truthfully():
    result = subprocess.run([sys.executable, "scripts/audit_physics_sources.py", "--require-complete"],
                            cwd=ROOT, capture_output=True, text=True, timeout=10, check=False)
    assert result.returncode == 2
    assert "complete_source_and_formula_review_blocked" in result.stderr


def test_previous_four_maps_and_first_37_formula_transcriptions_are_preserved(documents):
    catalog, formulas = documents
    baseline = catalog["preserved_mapping_baseline"]
    assert baseline["commit"] == "29e7d1e796267d59e320c6bb39809b365daca37c"
    assert canonical_digest(formulas["entries"][:37]) == (
        "3754f7aa4932b60798f1957fb40c2971541d63d8040088f2b7e5b7cbcacc7d94")
    assert sum(b["counts"]["numbered_sections"] for b in catalog["books"]
               if b["grade"] in (6, 7, 10, 11)) == 197
    for book in catalog["books"]:
        if str(book["grade"]) in baseline["grades"]:
            for field, fingerprint in baseline["grades"][str(book["grade"])].items():
                assert canonical_digest(book[field]) == fingerprint


def test_user_accepted_grade_seven_scope_does_not_claim_missing_pages(documents):
    catalog, _ = documents
    require_mapped(catalog)
    seven = catalog["books"][1]
    assert seven["source_complete"] is False
    assert seven["accepted_mapping_scope"]["numbered_sections"] == [1, 46]
    seven["accepted_mapping_scope"]["missing_front_matter_blocks_mapping"] = True
    with pytest.raises(ValueError, match="missing_source_not_covered_by_user_scope"):
        require_mapped(catalog)


def test_mapping_gate_cannot_ignore_an_unmapped_grade(documents):
    catalog, _ = documents
    catalog["books"][3]["mapping_scope_complete"] = False
    with pytest.raises(ValueError, match="accepted_section_mapping_incomplete"):
        require_mapped(catalog)


@pytest.mark.parametrize("grade,kind,count", [(8, "laboratory", 5), (8, "practical", 2),
                                            (8, "problem_practice", 12), (9, "laboratory", 6),
                                            (9, "practical", 2), (9, "problem_practice", 14)])
def test_labs_practicals_and_problem_sections_are_not_extra_theory(documents, grade, kind, count):
    catalog, _ = documents
    assert sum(r["kind"] == kind for r in catalog["books"][grade - 6]["records"]) == count


@pytest.mark.parametrize("change", ["gap", "overlap", "reverse", "page_count", "manifest_digest"])
def test_segment_gap_overlap_order_count_or_identity_is_rejected(documents, change):
    catalog, _ = documents
    book = catalog["books"][3]
    if change == "gap":
        book["segments"][1]["start"] += 1
    elif change == "overlap":
        book["segments"][1]["start"] -= 1
    elif change == "reverse":
        book["segments"].reverse()
    elif change == "page_count":
        book["segments"][0]["pages"] -= 1
    else:
        book["source_set_sha256"] = "a" * 64
    with pytest.raises(ValueError):
        validate_segments(book)


def test_segment_manifest_is_not_falsely_called_a_whole_pdf_digest(documents):
    catalog, _ = documents
    book = catalog["books"][2]
    book["sha256"] = book["source_set_sha256"]
    with pytest.raises(ValueError, match="segment_set_is_not_a_whole_pdf_digest"):
        validate_segments(book)


def test_original_pdf_and_segment_local_formula_pages_are_distinct(documents):
    catalog, formulas = documents
    entry = next(f for f in formulas["entries"] if f["grade"] == 8 and f["source"]["pdf_pages"] == [89])
    assert entry["source"]["segment_citations"][0]["local_pdf_page"] == 1
    entry["source"]["segment_citations"][0]["local_pdf_page"] = 89
    with pytest.raises(ValueError, match="segment_citation_mismatch"):
        validate(catalog, formulas)


def test_all_page_segment_offsets_are_checked_not_only_formulas(documents):
    catalog, formulas = documents
    catalog["books"][3]["page_audit"][132]["segment_local_pdf_page"] = 133
    with pytest.raises(ValueError, match="page_segment_offset_mismatch"):
        validate(catalog, formulas)


def test_grade_nine_original_toc_page_order_is_preserved(documents):
    catalog, formulas = documents
    book = catalog["books"][3]
    assert book["toc_pdf_pages"] == [172, 173, 171]
    assert [r["printed_page"] for r in book["page_audit"][170:173]] == [173, 171, 172]
    book["page_audit"][171]["printed_page"] = 172
    with pytest.raises(ValueError, match="page_numbering_exception_mismatch"):
        validate(catalog, formulas)


def test_unnumbered_grade_eight_last_toc_page_has_no_invented_printed_label(documents):
    catalog, _ = documents
    assert catalog["books"][2]["page_audit"][173]["printed_page"] is None


def test_scanned_shared_page_regions_are_clipped_before_next_heading(documents):
    catalog, formulas = documents
    book = catalog["books"][3]
    old = next(r for r in book["records"] if r["id"] == "physics-9-section-31")
    new = next(r for r in book["records"] if r["id"] == "physics-9-section-32")
    assert old["body_span"]["end_pdf_page"] == new["pdf_start"] == 97
    assert old["body_span"]["end_image_y_exclusive"] == new["body_span"]["start_image_y"]
    assert old["source_regions"][-1]["image_bbox"][3] == new["source_regions"][0]["image_bbox"][1]
    old["source_regions"][-1]["image_bbox"][3] += 1
    with pytest.raises(ValueError, match="region_must_match_clipped_span"):
        validate(catalog, formulas)


def test_reviewed_transcription_never_implicitly_approves_a_source_typo(documents):
    catalog, formulas = documents
    eight, nine = catalog["books"][2:4]
    assert any(u["code"] == "source_capacitor_sum_sign_typo" and u["pdf_pages"] == [82, 83]
               for u in eight["uncertainties"])
    assert any(u["code"] == "source_worked_example_parameter_conflict" and u["pdf_pages"] == [109]
               for u in nine["uncertainties"])
    assert all(not f["ready_for_publication"] and not f["executable_grading_rule"] for f in formulas["entries"])


def test_saved_audit_counts_do_not_drift_from_the_source_documents(documents):
    catalog, formulas = documents
    snapshot = json.loads((ROOT / "scripts/curriculum/physics/physics_map_audit.json").read_text())
    saved = snapshot["report"]
    for key in ("private_pdf_pages_verified", "private_ocr_pages_verified", "accepted_section_mapping_complete"):
        saved.pop(key)
    # JSON object keys are strings after serialization (grade counter keys are ints in Python).
    assert saved == json.loads(json.dumps(validate(catalog, formulas)))
    assert snapshot["private_sources_stored_in_git"] is False


def test_grade_seven_accepted_scope_also_applies_to_future_full_review_gate(documents):
    catalog, formulas = documents
    # Hypothetical reviewed copies only; no course, data or source file is changed.
    for book in catalog["books"]:
        book["review"]["all_facts_reviewed"] = True
        book["review"]["all_formulas_reviewed"] = True
    formulas["full_formula_inventory_complete"] = True
    assert catalog["books"][1]["source_complete"] is False
    require_complete(catalog, formulas)


def test_toggling_inventory_flag_cannot_replace_topic_formula_review(documents):
    catalog, formulas = documents
    formulas["full_formula_inventory_complete"] = True
    with pytest.raises(ValueError, match="full_formula_claim_needs_topic_reviews"):
        validate(catalog, formulas)
