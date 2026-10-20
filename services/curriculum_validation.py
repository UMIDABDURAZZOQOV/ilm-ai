"""Pure source/content validation: no ORM, database imports or startup migration.

Safe for dry-run validation even when a production DATABASE_URL is present.
"""

import hashlib
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
        if "segments" in book:
            segments = book["segments"]
            cursor, names = 1, set()
            for segment in segments:
                if (
                    segment["start"] != cursor
                    or segment["end"] < cursor
                    or segment["pages"] != segment["end"] - cursor + 1
                ):
                    raise ValueError("source_segment_gap_overlap_or_page_count")
                if segment["file_name"] in names or len(segment["sha256"]) != 64:
                    raise ValueError("source_segment_identity_invalid")
                names.add(segment["file_name"])
                cursor = segment["end"] + 1
            digest = hashlib.sha256(
                json.dumps(segments, sort_keys=True).encode()
            ).hexdigest()
            if (
                cursor - 1 != book["pdf_page_count"]
                or digest != book.get("source_set_sha256")
                or "sha256" in book
            ):
                raise ValueError("source_set_digest_or_page_count_mismatch")
        records = book["records"]
        if len({r["id"] for r in records}) != len(records):
            raise ValueError("duplicate_catalog_record")
        if sum(r["kind"] == "chapter" for r in records) != book["chapter_count"]:
            raise ValueError("chapter_coverage_mismatch")
        if sorted(r["paragraph"] for r in records if r.get("paragraph")) != list(
            range(1, book["paragraph_count"] + 1)
        ):
            raise ValueError("paragraph_coverage_mismatch")
        owners = {r["id"] for r in records if r["kind"] in {"chapter", "introduction"}}
        if sum(r["kind"] == "introduction" for r in records) != book.get(
            "introduction_count", 0
        ):
            raise ValueError("introduction_coverage_mismatch")
        for r in records:
            if (
                r["kind"] in {"topic", "laboratory", "practical"}
                and r.get("chapter_id") not in owners
            ):
                raise ValueError("topic_without_source_chapter")
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
    if not topic or topic["kind"] not in {"topic", "laboratory", "practical"}:
        raise ValueError("source_topic_required")
    if topic["kind"] != "topic":
        activity = lesson.get("activity", {})
        if (
            activity.get("kind") != topic["kind"]
            or activity.get("mode") != "guided_analysis"
            or activity.get("physical_execution_required") is not False
            or not activity.get("goal")
            or not activity.get("steps")
        ):
            raise ValueError("reviewed_guided_activity_required")
        for step in activity["steps"]:
            if (
                not step.get("instruction")
                or not step.get("fact_ids")
                or any(f not in lesson["facts"] for f in step["fact_ids"])
            ):
                raise ValueError("activity_step_evidence_required")
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
        # Calculation activities may rely on a rule taught in an earlier
        # paragraph. Keep the exercise citation and validate the additional
        # evidence separately instead of mislabelling its source paragraph.
        for supporting in source.get("supporting_sources", []):
            supporting_topic = topics.get(supporting.get("topic_id"))
            if (
                not supporting_topic
                or supporting_topic["kind"] not in {"topic", "laboratory", "practical"}
                or supporting.get("paragraph") != supporting_topic["paragraph"]
                or supporting.get("verification") != "page_image_reviewed"
                or not supporting.get("reviewed_on")
            ):
                raise ValueError("supporting_source_must_be_page_verified")
            supporting_pdf = supporting.get("pdf_pages", [])
            supporting_printed = supporting.get("printed_pages", [])
            if not supporting_pdf or len(supporting_pdf) != len(supporting_printed):
                raise ValueError("supporting_source_pages_required")
            for pdf, page in zip(supporting_pdf, supporting_printed):
                if (
                    not supporting_topic["pdf_start"] <= pdf <= supporting_topic["pdf_end"]
                    or not supporting_topic["printed_start"] <= page <= supporting_topic["printed_end"]
                    or pdf - page != supporting_topic["pdf_start"] - supporting_topic["printed_start"]
                ):
                    raise ValueError("supporting_source_outside_topic")
    for card in lesson["theory"]:
        if (
            not card.get("title")
            or not card.get("body")
            or not card.get("fact_ids")
            or any(f not in facts for f in card["fact_ids"])
        ):
            raise ValueError("teaching_card_evidence_required")
    taught = {fact_id for card in lesson["theory"] for fact_id in card["fact_ids"]}
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
        if q.get("fact_id") not in taught:
            raise ValueError("assessed_fact_must_be_taught")
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


def load_lesson_set(batch=None):
    """Explicit reviewed manifest list: no draft file is published by globbing."""
    index = json.loads(CATALOG_PATH.with_name("biology_lessons.json").read_text())
    names = index["lessons"] if batch is None else index["batches"][batch]
    if len(names) != len(set(names)) or any(
        name not in index["lessons"] for name in names
    ):
        raise ValueError("invalid_reviewed_batch")
    lessons = [json.loads(CATALOG_PATH.with_name(name).read_text()) for name in names]
    if len({lesson["key"] for lesson in lessons}) != len(lessons):
        raise ValueError("duplicate_content_key")
    return lessons


def readiness_report(catalog, lessons):
    """Source headings and usable digital lessons are separate quantities."""
    for lesson in lessons:
        validate_lesson(catalog, lesson)
    result = []
    for book in catalog["books"]:
        ready = [lesson for lesson in lessons if lesson["book_id"] == book["id"]]
        topics = [r for r in book["records"] if r["kind"] == "topic"]
        kinds = {r["id"]: r["kind"] for r in book["records"]}
        ids = {
            lesson["topic_id"]
            for lesson in ready
            if kinds[lesson["topic_id"]] == "topic"
        }
        activities = [
            r for r in book["records"] if r["kind"] in {"laboratory", "practical"}
        ]
        activity_ids = {
            lesson["topic_id"]
            for lesson in ready
            if kinds[lesson["topic_id"]] != "topic"
        }
        result.append(
            {
                "grade": book["grade"],
                "chapters": book.get("chapter_count", 0),
                "introductions": book.get("introduction_count", 0),
                "numbered_paragraphs": book.get("paragraph_count", 0),
                "topics": len(topics),
                "laboratories": sum(r["kind"] == "laboratory" for r in book["records"]),
                "practicals": sum(r["kind"] == "practical" for r in book["records"]),
                "ready_topics": len(ids),
                "ready_lessons": len(ready),
                "ready_theory_lessons": sum(
                    kinds[l["topic_id"]] == "topic" for l in ready
                ),
                "ready_activities": len(activity_ids),
                "remaining_topics": len(topics) - len(ids),
                "remaining_activity_ids": [
                    r["id"] for r in activities if r["id"] not in activity_ids
                ],
                "questions": sum(len(lesson["questions"]) for lesson in ready),
                "remaining_topic_ids": [r["id"] for r in topics if r["id"] not in ids],
                "course_ready": len(ids) == len(topics)
                and len(activity_ids) == len(activities)
                and bool(topics),
            }
        )
    return result
