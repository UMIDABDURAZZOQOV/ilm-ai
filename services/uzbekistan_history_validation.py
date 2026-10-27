"""No-DB validation for explicitly reviewed original Uzbekistan history lessons."""

from __future__ import annotations

import hashlib
import itertools
import json

from services.uzbekistan_history_grading import grade_answer
from services.uzbekistan_history_sources import (
    DIRECTORY,
    SUBJECT,
    digest,
    load_catalog,
    require,
    validate_catalog,
)

BATCHES = {
    "grade7_batch1": (7, 1, 5),
    "grade7_batch2": (7, 6, 10),
    "grade7_batch3": (7, 11, 15),
    "grade7_batch4": (7, 16, 20),
    "grade7_batch5": (7, 21, 25),
    "grade7_batch6": (7, 26, 30),
    "grade7_batch7": (7, 31, 35),
    "grade7_batch8": (7, 36, 40),
    "grade7_batch9": (7, 41, 42),
    "grade8_batch1": (8, 1, 5),
}

fingerprint = digest


def chronology_bounds(time):
    require(
        set(time) == {"era", "start_year", "end_year"} and time["era"] in {"CE", "BCE"},
        "date_schema",
    )
    require(
        all(
            type(time[k]) is int and 1 <= time[k] <= 9999
            for k in ["start_year", "end_year"]
        ),
        "display_year_zero_or_invalid",
    )
    sign = 1 if time["era"] == "CE" else -1
    a, b = sign * time["start_year"], sign * time["end_year"]
    require(a <= b, "date_interval_reversed")
    return a, b


def validate_ref(ref, book, topic, facts=None):
    if ref["topic_id"] != topic["id"]:
        prior = next((t for t in book["topics"] if t["id"] == ref["topic_id"]), None)
        require(
            prior is not None
            and prior["sequence"] < topic["sequence"]
            and ref.get("cross_topic_reference") == "reviewed_prior_context"
            and ref.get("source_topic_sha256") == digest(prior)
            and ref.get("source_title") == prior["title"],
            "unreviewed_or_future_context_reference",
        )
        topic = prior
    require(
        ref["book_id"] == book["id"]
        and ref["grade"] == book["grade"]
        and ref["chapter_id"] == topic["chapter_id"]
        and ref["topic_id"] == topic["id"],
        "reference_identity",
    )
    require(
        ref["sha256"] == book["sha256"] and ref["file_name"] == book["file_name"],
        "reference_source_digest",
    )
    pages = ref["pdf_pages"]
    require(
        pages
        and pages == sorted(set(pages))
        and all(
            type(p) is int and topic["pdf_page"] <= p <= topic["pdf_end"] for p in pages
        ),
        "reference_page_range",
    )
    require(
        ref["printed_pages"] == [book["pages"][p - 1]["printed_page"] for p in pages],
        "reference_printed_pages",
    )
    require(
        ref["native_text_sha256"]
        == [book["pages"][p - 1]["native_text_sha256"] for p in pages],
        "reference_native_hash",
    )
    scanned = book.get("source_kind") == "reassembled_uploaded_segments"
    require(
        ref["verification"]
        == (
            "original_image_checked_ocr_locator_only"
            if scanned
            else "original_text_and_image_checked"
        )
        and bool(ref["review_note"]),
        "reference_review",
    )
    if scanned:
        require(
            ref.get("page_image_sha256")
            == [book["pages"][p - 1]["image_sha256"] for p in pages],
            "scanned_reference_image_evidence",
        )
    require(
        bool(ref["fact_id"]) and (facts is None or ref["fact_id"] in facts),
        "reference_fact_identity",
    )
    # At an overlapping boundary page the clip must end before the next heading.
    boundary = topic["end_boundary"]
    if boundary.get("next_topic_id") and boundary["pdf_page"] in pages:
        require(
            ref.get("end_before_y") == boundary["y"], "reference_crosses_next_topic"
        )
    if topic["pdf_page"] in pages:
        require(
            ref.get("start_after_y") == topic["heading_bbox"][1],
            "reference_precedes_topic",
        )


def validate_batch(doc):
    catalog = load_catalog()
    validate_catalog(catalog)
    require(
        doc["schema_version"] == 1
        and doc["assessment_version"] == 2
        and doc["subject"] == SUBJECT
        and doc["language"] == "uz",
        "lesson_schema",
    )
    require(
        doc["publication"] == "local_test_preview_only" and not doc["ai_explain"],
        "lesson_publication",
    )
    book = next((b for b in catalog["books"] if b["grade"] == doc["grade"]), None)
    require(book is not None, "source_book_not_read")
    require(doc["book_sha256"] == book["sha256"], "lesson_book_digest")
    topics = {t["id"]: t for t in book["topics"]}
    seen = set()
    prompts = set()
    counts = {"lessons": 0, "cards": 0, "assessments": 0, "frq": 0, "chronologies": 0}
    for lesson in doc["lessons"]:
        topic = topics.get(lesson["topic_id"])
        require(topic is not None, "unknown_topic")
        require(
            lesson["key"] == f"uzh-{doc['grade']}-{topic['sequence']}-r1"
            and lesson["key"] not in seen
            and lesson["sequence"] == topic["sequence"],
            "lesson_identity",
        )
        seen.add(lesson["key"])
        require(lesson["source_topic_sha256"] == digest(topic), "source_topic_changed")
        require(
            lesson["title"] == topic["title"]
            and lesson["revision"] == 1
            and lesson["xp_reward"] == 10,
            "lesson_scope",
        )
        require(
            lesson["review"]["independent_history_teacher"] == "not_claimed"
            and not lesson["review"]["ready_for_general_publication"],
            "teacher_review_claim",
        )
        facts = lesson["facts"]
        require(
            facts and lesson["cards"] and lesson["examples"] and lesson["assessments"],
            "empty_teaching_lesson",
        )
        for fid, fact in facts.items():
            require(
                fid == fact["id"]
                and bool(fact["statement"])
                and fact["assertion_kind"]
                in {"source_statement", "source_interpretation"},
                "fact_schema",
            )
            for ref in fact["source_refs"]:
                validate_ref(ref, book, topic, facts)
                require(ref["fact_id"] == fid, "fact_reference_mismatch")
            require(fact["source_refs"], "fact_source_missing")
            if fact.get("time"):
                chronology_bounds(fact["time"])
            if fact["assertion_kind"] == "source_interpretation":
                require(
                    not fact["accepted_answers"], "interpretation_not_objective_key"
                )
        taught = set()
        expected_refs = [r for fact in facts.values() for r in fact["source_refs"]]
        require(
            {digest(r) for r in lesson["source_refs"]}
            == {digest(r) for r in expected_refs},
            "lesson_source_coverage",
        )
        for card in lesson["cards"]:
            require(
                card["fact_ids"]
                and set(card["fact_ids"]) <= facts.keys()
                and card["body"]
                and {r["fact_id"] for r in card["source_refs"]}
                == set(card["fact_ids"]),
                "untaught_card_fact",
            )
            taught.update(card["fact_ids"])
            for ref in card["source_refs"]:
                validate_ref(ref, book, topic, facts)
                require(ref["fact_id"] in card["fact_ids"], "card_reference_mismatch")
        for block in [*lesson["examples"], *lesson.get("reflections", [])]:
            require(
                block["fact_ids"]
                and set(block["fact_ids"]) <= taught
                and block["body"]
                and {r["fact_id"] for r in block["source_refs"]}
                == set(block["fact_ids"]),
                "example_or_reflection_untaught",
            )
            for ref in block["source_refs"]:
                validate_ref(ref, book, topic, facts)
        for question_number, q in enumerate(lesson["assessments"], start=1):
            require(
                q["fact_ids"] and set(q["fact_ids"]) <= taught, "question_untaught_fact"
            )
            require(
                all(
                    facts[f]["assertion_kind"] == "source_statement"
                    for f in q["fact_ids"]
                ),
                "interpretation_requires_self_or_teacher_review",
            )
            require(
                q["key"] == f"{lesson['key']}:q{question_number}",
                "question_order_key",
            )
            require(q["public"]["prompt"] not in prompts, "duplicate_question_prompt")
            prompts.add(q["public"]["prompt"])
            require(q["source_refs"], "question_source_missing")
            require(
                {r["fact_id"] for r in q["source_refs"]} == set(q["fact_ids"]),
                "question_source_coverage",
            )
            for ref in q["source_refs"]:
                validate_ref(ref, book, topic, facts)
                require(ref["fact_id"] in q["fact_ids"], "question_reference_mismatch")
            spec = q["grading_spec"]
            require(
                spec["kind"] == q["response_kind"]
                and spec["solution"]
                and spec["verified_answer"],
                "grading_scope",
            )
            require(
                all(
                    spec["feedback"].get(k)
                    for k in [
                        "correct",
                        "incorrect",
                        "invalid_answer",
                        "answer_required",
                    ]
                ),
                "authored_feedback_missing",
            )
            for solution in spec["solution"]:
                require(
                    solution["body"] and solution["source_refs"],
                    "solution_evidence_missing",
                )
                for ref in solution["source_refs"]:
                    validate_ref(ref, book, topic, facts)
                    require(ref["fact_id"] in q["fact_ids"], "solution_unlinked_fact")
            if spec["kind"] == "concept_selection":
                options = q["public"]["options"]
                require(
                    len(options) >= 3
                    and len({o["id"] for o in options}) == len(options)
                    and len({o["label"].strip().casefold() for o in options})
                    == len(options),
                    "option_schema",
                )
                require(
                    spec["choice_ids"] == [o["id"] for o in options], "choice_allowlist"
                )
                expected = next(
                    (o["label"] for o in options if o["id"] == spec["expected"]), None
                )
                require(
                    expected
                    in {a for f in q["fact_ids"] for a in facts[f]["accepted_answers"]},
                    "choice_key_not_source_verified",
                )
                require(
                    spec["verified_answer"] == expected,
                    "feedback_key_not_verified_choice",
                )
                answer = {"choice_id": spec["expected"]}
            elif spec["kind"] == "short_text":
                require(
                    len(q["fact_ids"]) == 1 and spec["aliases"], "short_answer_fact"
                )
                require(
                    set(spec["aliases"])
                    <= set(facts[q["fact_ids"][0]]["accepted_answers"])
                    and spec["expected"] in spec["aliases"]
                    and spec["verified_answer"] in spec["aliases"],
                    "unreviewed_answer_alias",
                )
                require(
                    "aliases" not in q["public"] and "expected" not in q["public"],
                    "private_key_leak",
                )
                for alias in spec["aliases"]:
                    require(
                        grade_answer(spec, {"value": alias}) == "correct",
                        "alias_does_not_grade",
                    )
                answer = {"value": spec["expected"]}
                counts["frq"] += 1
            elif spec["kind"] == "ordering":
                items = q["public"]["items"]
                require(
                    2 <= len(items) <= 20
                    and len({i["id"] for i in items}) == len(items),
                    "ordering_schema",
                )
                require(
                    spec["mode"] == "chronology"
                    and {i["fact_id"] for i in items} == set(q["fact_ids"]),
                    "chronology_evidence",
                )
                ordered = sorted(
                    items, key=lambda i: chronology_bounds(facts[i["fact_id"]]["time"])
                )
                bounds = [
                    chronology_bounds(facts[i["fact_id"]]["time"]) for i in ordered
                ]
                require(
                    all(a[1] < b[0] for a, b in itertools.pairwise(bounds)),
                    "overlapping_chronology_not_unique",
                )
                require(
                    spec["expected"] == [i["id"] for i in ordered],
                    "chronology_key_not_source_order",
                )
                answer = {"order": spec["expected"]}
                counts["chronologies"] += 1
            else:
                raise ValueError("unsupported_history_response_kind")
            require(
                grade_answer(spec, answer) == "correct",
                "authored_answer_does_not_grade",
            )
            counts["assessments"] += 1
        counts["lessons"] += 1
        counts["cards"] += len(lesson["cards"])
    require(
        [l["sequence"] for l in doc["lessons"]]
        == list(
            range(doc["lessons"][0]["sequence"], doc["lessons"][-1]["sequence"] + 1)
        ),
        "batch_source_gap",
    )
    return counts


def load_course():
    result = []
    for name, (grade, start, end) in BATCHES.items():
        path = DIRECTORY / f"{name}.json"
        doc = json.loads(path.read_text())
        validate_batch(doc)
        require(
            doc["grade"] == grade
            and [l["sequence"] for l in doc["lessons"]] == list(range(start, end + 1)),
            "unreviewed_batch_range",
        )
        review = json.loads((DIRECTORY / f"{name}_review.json").read_text())
        require(
            review["content_sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
            and review["book_sha256"] == doc["book_sha256"],
            "changed_content_requires_review",
        )
        require(
            review["independent_history_teacher"] == "not_claimed"
            and not review["ready_for_general_publication"],
            "false_release_approval",
        )
        book = next(b for b in load_catalog()["books"] if b["grade"] == grade)
        cited = sorted(
            {
                p
                for l in doc["lessons"]
                for f in l["facts"].values()
                for ref in f["source_refs"]
                for p in ref["pdf_pages"]
            }
        )
        require(
            [r["pdf_page"] for r in review["pages"]] == cited,
            "review_missing_cited_page",
        )
        for r in review["pages"]:
            page = book["pages"][r["pdf_page"] - 1]
            require(
                r["printed_page"] == page["printed_page"]
                and r["native_text_sha256"] == page["native_text_sha256"]
                and r["original_full_page_visually_read"] is True
                and len(r["image_sha256"]) == 64,
                "page_review_evidence",
            )
        result.append(doc)
    all_lessons = [lesson for doc in result for lesson in doc["lessons"]]
    require(
        len({l["topic_id"] for l in all_lessons}) == len(all_lessons),
        "duplicate_batch_topic",
    )
    questions = [q for l in all_lessons for q in l["assessments"]]
    require(
        len({q["key"] for q in questions}) == len(questions), "duplicate_batch_question"
    )
    require(
        len({q["public"]["prompt"] for q in questions}) == len(questions),
        "duplicate_batch_prompt",
    )
    for grade in {d["grade"] for d in result}:
        seq = [
            l["sequence"] for d in result if d["grade"] == grade for l in d["lessons"]
        ]
        require(seq == list(range(1, max(seq) + 1)), "cross_batch_source_gap")
    return result
