"""Pure source/content validation: no ORM, database imports or startup migration.

Safe for dry-run validation even when a production DATABASE_URL is present.
"""

import json
from pathlib import Path

CATALOG_PATH = (
    Path(__file__).resolve().parents[1] / "scripts/curriculum/biology_sources.json"
)
LESSON_PATH = CATALOG_PATH.with_name("biology_5_first_lesson.json")


def load_documents():
    return json.loads(CATALOG_PATH.read_text()), json.loads(LESSON_PATH.read_text())


def validate_catalog(catalog):
    if (
        catalog.get("schema_version") != 1
        or catalog.get("subject_slug") != "biologiya"
        or catalog.get("language") != "uz"
    ):
        raise ValueError("unsupported_catalog")
    books = catalog["books"]
    if sorted(b["grade"] for b in books) != list(range(5, 12)):
        raise ValueError("seven_unique_grades_required")
    for book in books:
        if book["status"].startswith("blocked_"):
            if book["records"] or any(k in book for k in ("year", "authors", "sha256")):
                raise ValueError("unread_source_must_not_claim_metadata")
            continue
        records = book["records"]
        if len({r["id"] for r in records}) != len(records):
            raise ValueError("duplicate_catalog_record")
        if sum(r["kind"] == "chapter" for r in records) != book["chapter_count"]:
            raise ValueError("chapter_coverage_mismatch")
        if sorted(r["paragraph"] for r in records if r.get("paragraph")) != list(
            range(1, book["paragraph_count"] + 1)
        ):
            raise ValueError("paragraph_coverage_mismatch")
        for r in records:
            if (
                not r.get("pdf_start")
                or not 1 <= r["pdf_start"] <= r["pdf_end"] <= book["pdf_page_count"]
            ):
                raise ValueError("invalid_catalog_page_range")
            if r.get("verification", {}).get("status") == "needs_visual_check":
                raise ValueError("unverified_catalog_heading")
        if book["rights"]["fulltext_republication"] != "not_authorized":
            raise ValueError("source_rights_must_be_explicit")


def validate_lesson(catalog, lesson):
    validate_catalog(catalog)
    books = {b["id"]: b for b in catalog["books"]}
    if (
        lesson.get("language") != "uz"
        or lesson.get("authorship") != "original_fact_based_adaptation"
    ):
        raise ValueError("original_uzbek_content_required")
    book = books.get(lesson["book_id"])
    if not book or book["status"] != "mapped":
        raise ValueError("verified_source_required")
    topics = {r["id"]: r for r in book["records"]}
    topic = topics.get(lesson["topic_id"])
    if not topic or topic["kind"] != "topic":
        raise ValueError("source_topic_required")
    if not lesson.get("theory") or not lesson.get("questions"):
        raise ValueError("theory_and_questions_required")
    facts = lesson["facts"]
    for fact in facts.values():
        if not fact.get("claim") or not fact.get("answer") or not fact.get("source"):
            raise ValueError("fact_evidence_required")
        source = fact["source"]
        if (
            source.get("verification") != "page_image_reviewed"
            or source.get("paragraph") != topic["paragraph"]
        ):
            raise ValueError("fact_must_be_page_verified")
        pdf_pages, printed = source["pdf_pages"], source["printed_pages"]
        if not pdf_pages or len(pdf_pages) != len(printed):
            raise ValueError("both_page_number_systems_required")
        for pdf, page in zip(pdf_pages, printed):
            if pdf - page != topic["pdf_start"] - topic["printed_start"]:
                raise ValueError("pdf_and_printed_page_mapping_mismatch")
            if (
                not topic["pdf_start"] <= pdf <= topic["pdf_end"]
                or not topic["printed_start"] <= page <= topic["printed_end"]
            ):
                raise ValueError("fact_outside_source_topic")
    for card in lesson["theory"]:
        if (
            not card.get("title")
            or not card.get("body")
            or not card.get("fact_ids")
            or any(f not in facts for f in card["fact_ids"])
        ):
            raise ValueError("teaching_card_evidence_required")
    keys = set()
    for q in lesson["questions"]:
        if not q.get("key") or q["key"] in keys:
            raise ValueError("unique_question_key_required")
        keys.add(q["key"])
        options = q.get("options", [])
        normalized = [s.strip().casefold() for s in options if isinstance(s, str)]
        if (
            len(options) != 4
            or len(normalized) != 4
            or len(set(normalized)) != 4
            or any(not s for s in normalized)
        ):
            raise ValueError("four_distinct_nonempty_options_required")
        fact = facts.get(q.get("fact_id"))
        if (
            not fact
            or q.get("correct_answer") != fact["answer"]
            or options.count(q.get("correct_answer")) != 1
        ):
            raise ValueError("answer_must_match_verified_fact")
        if not q.get("question_text") or not q.get("explanation"):
            raise ValueError("question_and_feedback_required")
    return book, topic
