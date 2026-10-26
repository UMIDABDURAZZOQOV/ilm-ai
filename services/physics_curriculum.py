"""Explicit reviewed Physics batches, validation and immutable preview import.

Loading/validating documents never imports ORM or opens a database. There is no
glob publication, startup seed, runtime generation, or modification of Biology.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

from services.assessment_grading import (
    UNITS,
    expected_quantity,
    formula_ast,
    grade_answer,
    numeric,
)
from services.physics_rules import (
    DIMENSION_UNIT,
    REVIEWED_FORMULAS,
    reviewed_calculation,
)
from services.physics_source_documents import segment_page, source_identity

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "scripts/curriculum/physics"
BATCH = DIRECTORY / "grade6_batch1.json"
# Explicitly reviewed ranges only. Adding an unrelated JSON file never publishes
# or imports it. The original first-batch entry and byte hashes remain frozen.
REVIEWED_BATCHES = {
    "grade6_batch1": (6, 1, 7),
    "grade6_batch2": (6, 8, 17),
    "grade6_batch3": (6, 18, 24),
    "grade6_batch4": (6, 25, 29),
    "grade6_batch5": (6, 30, 35),
    "grade6_batch6": (6, 36, 42),
    "grade6_batch7": (6, 43, 46),
    "grade6_batch8": (6, 47, 56),
    "grade6_batch9": (6, 57, 61),
    "grade7_batch1": (7, 1, 5),
    "grade7_batch2": (7, 6, 10),
    "grade7_batch3": (7, 11, 15),
    "grade7_batch4": (7, 16, 20),
    "grade7_batch5": (7, 21, 25),
    "grade7_batch6": (7, 26, 30),
    "grade7_batch7": (7, 31, 35),
    "grade7_batch8": (7, 36, 40),
    "grade7_batch9": (7, 41, 46),
    "grade8_batch1": (8, 1, 5),
    "grade8_batch2": (8, 6, 10),
    "grade8_batch3": (8, 11, 15),
    "grade8_batch4": (8, 16, 20),
    "grade8_batch5": (8, 21, 25),
    "grade8_batch6": (8, 26, 30),
    "grade8_batch7": (8, 31, 35),
    "grade8_batch8": (8, 36, 40),
    "grade8_batch9": (8, 41, 45),
    "grade8_batch10": (8, 46, 50),
    "grade8_batch11": (8, 51, 55),
    "grade8_batch12": (8, 56, 60),
    "grade9_batch1": (9, 1, 5),
    "grade9_batch2": (9, 6, 10),
    "grade9_batch3": (9, 11, 15),
    "grade9_batch4": (9, 16, 20),
    "grade9_batch5": (9, 21, 25),
    "grade9_batch6": (9, 26, 30),
    "grade9_batch7": (9, 31, 35),
    "grade9_batch8": (9, 36, 40),
    "grade9_batch9": (9, 41, 45),
}
# Image-checked continuation missed by the old digital text boundary. Preserve
# the frozen stage-one archive; permit only this explicitly documented page.
SOURCE_CONTINUATIONS = {
    ("physics-uz-grade-6", "physics-6-section-32"): {90},
    # Original page112 upper21-mashq continues §39 before chapter-review heading.
    ("physics-uz-grade-8", "physics-8-section-39"): {112},
    # Original166 upper27-mashq2–5 continues §60 before V chapter review.
    ("physics-uz-grade-8", "physics-8-section-60"): {166},
    # Original74 upper lab steps2–7/analysis precede the chapter-review heading.
    ("physics-uz-grade-9", "physics-9-section-25"): {74},
    # Original126 upper23-mashq precedes IV chapter-review heading.
    ("physics-uz-grade-9", "physics-9-section-43"): {126},
}

# Explicit prior-source dependencies, never an unrestricted citation escape.
# Lab25 reuses the water-specific-heat table previously reviewed in §17.
SOURCE_PREREQUISITES = {
    ("grade9_batch5", "physics-9-section-17"): {56},
}

# Algebraic alternatives reviewed under the stated source domains. No guessing
# at symbolic equivalence or random-point numerical acceptance.
FORMULAS = {
    "m_to_cm": {
        "target": "y",
        "variables": ["x"],
        "equivalents": ["100*x", "x*100"],
        "conditions": "x metrlarda, y santimetrlarda; PDF13",
    },
    "mm_to_m": {
        "target": "y",
        "variables": ["x"],
        "equivalents": ["x/1000", "0.001*x"],
        "conditions": "x millimetrlarda, y metrlarda; PDF13",
    },
    "scale": {
        "target": "d",
        "variables": ["b", "a", "n"],
        "equivalents": ["(b-a)/n", "b/n-a/n"],
        "conditions": "b>a, n musbat butun oraliqlar soni; a,b bir birlikda; PDF14",
    },
    "mean2": {
        "target": "a_ort",
        "variables": ["x1", "x2"],
        "equivalents": ["(x1+x2)/2", "x1/2+x2/2", "0.5*(x1+x2)"],
        "conditions": "ikki bir xil kattalik o‘lchovi bir birlikda; PDF15",
    },
    "half_division": {
        "target": "delta",
        "variables": ["d"],
        "equivalents": ["d/2", "0.5*d"],
        "conditions": "shu oddiy shkala modeli uchun, d eng kichik bo‘linma; PDF15",
    },
}
FORMULAS.update(REVIEWED_FORMULAS)


def fingerprint(document):
    return hashlib.sha256(
        json.dumps(document, ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()


def public_book(grade):
    """Bibliography only; no OCR, private source paths or answer rubrics."""
    book = next(
        b
        for b in json.loads((DIRECTORY / "physics_sources.json").read_text())["books"]
        if b["grade"] == grade
    )
    return {
        key: deepcopy(book[key])
        for key in ("id", "grade", "title", "authors", "publisher", "year")
    }


def require(condition, code):
    if not condition:
        raise ValueError(code)


def load_batch(batch_id="grade6_batch1"):
    require(batch_id in REVIEWED_BATCHES, "batch_not_reviewed")
    document = json.loads((DIRECTORY / f"{batch_id}.json").read_text())
    validate_batch(document)
    validate_review_evidence(document)
    return document


def load_course():
    documents = [load_batch(name) for name in REVIEWED_BATCHES]
    seen, prompts = set(), set()
    for document in documents:
        for lesson in document["lessons"]:
            require(lesson["key"] not in seen, "overlapping_reviewed_batches")
            seen.add(lesson["key"])
            for question in lesson["assessments"]:
                prompt = question["public"]["prompt"].strip().casefold()
                require(prompt not in prompts, "duplicate_course_prompt")
                prompts.add(prompt)
    return documents


def batch_identity(document):
    identity = (
        document["grade"],
        document["lessons"][0]["sequence"],
        document["lessons"][-1]["sequence"],
    )
    name = next((k for k, v in REVIEWED_BATCHES.items() if v == identity), None)
    require(name is not None, "batch_not_reviewed")
    return name


def validate_review_evidence(document):
    name = batch_identity(document)
    path = DIRECTORY / f"{name}.json"
    audit = json.loads((DIRECTORY / f"{name}_review.json").read_text())
    require(
        audit["batch_file_sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
        and fingerprint(document) == fingerprint(json.loads(path.read_text())),
        "changed_content_requires_new_reviewed_revision",
    )
    book = next(
        b
        for b in json.loads((DIRECTORY / "physics_sources.json").read_text())["books"]
        if b["grade"] == document["grade"]
    )
    identity = source_identity(book)
    if "sha256" in identity:
        require(
            audit.get("book_sha256") == identity["sha256"], "source_review_identity"
        )
    else:
        require(
            audit.get("source_kind") == identity["source_kind"]
            and audit.get("book_source_set_sha256") == identity["source_set_sha256"]
            and "book_sha256" not in audit,
            "source_review_segment_manifest_identity",
        )
    require(
        not audit["ready_for_general_publication"]
        and audit["independent_subject_expert"] == "not_claimed",
        "source_review_scope",
    )
    require(
        [p["pdf_page"] for p in audit["pages"]]
        == sorted(
            {
                p
                for lesson in document["lessons"]
                for ref in lesson["source_refs"]
                for p in ref["pdf_pages"]
            }
        ),
        "all_batch_pages_reviewed",
    )
    for page in audit["pages"]:
        source = book["page_audit"][page["pdf_page"] - 1]
        if "source_set_sha256" in identity:
            require(
                page.get("text_origin") == "cached_ocr_checked_against_original_image"
                and page.get("digital_text_sha256") == source["digital_text_sha256"]
                and page.get("source_segment") == segment_page(book, page["pdf_page"]),
                "segmented_page_review_evidence",
            )
        require(
            page["printed_page"] == source["printed_page"]
            and page["text_sha256"] == source["text_sha256"]
            and page["original_text_and_image_checked"] is True
            and len(page["reviewed_render_sha256"]) == 64,
            "page_review_evidence",
        )


def calculation_value(question):
    rule = question["grading_spec"]["rule"]
    if rule in REVIEWED_FORMULAS:
        return reviewed_calculation(question)[0]
    givens = {v["symbol"]: v for v in question["public"]["givens"]}

    def value(key):
        v = givens[key]
        return numeric(v["value"])

    def scale(key):
        return UNITS[givens[key]["unit"]][1]

    if rule in {"m_to_cm", "mm_to_m"}:
        require(
            givens["x"]["unit"] == ("m" if rule == "m_to_cm" else "mm"),
            "conversion_given_unit",
        )
        return value("x") * scale("x")
    if rule == "scale":
        require(
            givens["a"]["unit"] == givens["b"]["unit"]
            and value("b") > value("a")
            and value("n") > 0
            and value("n").denominator == 1,
            "scale_domain",
        )
        return (value("b") - value("a")) / value("n") * scale("a")
    if rule == "mean2":
        require(givens["x1"]["unit"] == givens["x2"]["unit"], "mean_unit_domain")
        return (value("x1") + value("x2")) / 2 * scale("x1")
    if rule == "half_division":
        require(value("d") > 0, "positive_scale_division")
        return value("d") / 2 * scale("d")
    raise ValueError("unreviewed_formula_rule")


def validate_batch(document):
    catalog = json.loads((DIRECTORY / "physics_sources.json").read_text())
    require(
        document["schema_version"] == 2
        and document["subject"] == "fizika"
        and document["language"] == "uz"
        and document["grade"] in range(6, 12),
        "physics_batch_identity",
    )
    book = next(b for b in catalog["books"] if b["grade"] == document["grade"])
    require(
        document["publication"] == "local_test_preview_only"
        and document["ai_explain"] is False,
        "no_physics_publication",
    )
    lessons = document["lessons"]
    require(lessons, "empty_batch")
    batch_name = batch_identity(document)
    first, last = REVIEWED_BATCHES[batch_name][1:]
    require(
        [l["sequence"] for l in lessons] == list(range(first, last + 1)),
        "reviewed_batch_source_order",
    )
    keys = set()

    def references(refs):
        require(isinstance(refs, list) and refs, "source_refs_required")
        for ref in refs:
            topic = next(
                (r for r in book["records"] if r["id"] == ref["topic_id"]), None
            )
            require(topic is not None, "source_outside_reviewed_batch")
            if not first <= (topic.get("number") or 0) <= last:
                allowed = SOURCE_PREREQUISITES.get((batch_name, topic["id"]), set())
                require(
                    allowed
                    and ref.get("pdf_pages")
                    and set(ref["pdf_pages"]) <= allowed
                    and ref.get("prerequisite_note") == "previous_reviewed_foundation",
                    "source_outside_reviewed_batch",
                )
                owner = next(
                    (
                        name
                        for name, (grade, start, end) in REVIEWED_BATCHES.items()
                        if grade == book["grade"]
                        and start <= topic["number"] <= end < first
                    ),
                    None,
                )
                require(owner is not None, "source_prerequisite_not_previous")
                digest = hashlib.sha256(
                    (DIRECTORY / f"{owner}.json").read_bytes()
                ).hexdigest()
                evidence = json.loads((DIRECTORY / f"{owner}_review.json").read_text())
                reviewed = {
                    p["pdf_page"]
                    for p in evidence["pages"]
                    if p["original_text_and_image_checked"] is True
                }
                require(
                    ref.get("prerequisite_batch") == owner
                    and ref.get("prerequisite_batch_sha256") == digest
                    and evidence["batch_file_sha256"] == digest
                    and set(ref["pdf_pages"]) <= reviewed,
                    "source_prerequisite_review_binding",
                )
            require(
                ref["book_id"] == book["id"]
                and all(ref.get(k) == v for k, v in source_identity(book).items())
                and ref["file_name"] == book["file_name"]
                and ref["chapter_id"] == topic["chapter_id"],
                "source_identity_mismatch",
            )
            require(
                ref["verification"] == "original_pdf_text_and_image_checked",
                "unreviewed_source",
            )
            pp, printed = ref["pdf_pages"], ref["printed_pages"]
            require(
                pp and len(pp) == len(printed) == len(ref["page_text_sha256"]),
                "both_page_systems_required",
            )
            if book.get("source_kind") == "ordered_pdf_segments":
                require(
                    "sha256" not in ref
                    and ref.get("segment_pages") == [segment_page(book, p) for p in pp],
                    "source_segment_page_binding",
                )
            for pdf, label, digest in zip(pp, printed, ref["page_text_sha256"]):
                require(
                    topic["pdf_start"] <= pdf <= topic["pdf_end"]
                    or (
                        pdf
                        in SOURCE_CONTINUATIONS.get((book["id"], topic["id"]), set())
                        and ref.get("extent_note")
                        == "original_image_continues_before_next_heading"
                    ),
                    "citation_outside_topic",
                )
                page = book["page_audit"][pdf - 1]
                require(
                    page["printed_page"] == label and page["text_sha256"] == digest,
                    "page_evidence_mismatch",
                )

    for lesson in lessons:
        require(lesson["key"] not in keys, "duplicate_lesson")
        keys.add(lesson["key"])
        require(
            lesson["topic_id"]
            == f"physics-{book['grade']}-section-{lesson['sequence']}"
            and lesson["revision"] == 1
            and lesson["xp_reward"] == 10,
            "lesson_source_order",
        )
        topic = next(r for r in book["records"] if r["id"] == lesson["topic_id"])
        require(lesson["title"] == topic["title"], "source_title_mismatch")
        if topic["kind"] != "topic":
            require(
                lesson["review"].get("physical_experiment_completed") is False,
                "digital_activity_is_not_physical_experiment",
            )
        require(
            lesson["review"]["source_text_and_images_checked"] is True
            and lesson["review"]["independent_subject_expert"] == "not_claimed",
            "honest_review_required",
        )
        facts = lesson["facts"]
        require(
            facts
            and len(lesson["cards"]) >= 3
            and lesson["examples"]
            and len(lesson["assessments"]) >= 5,
            "substantial_lesson_required",
        )
        references(lesson["source_refs"])
        for fact in facts.values():
            require(fact["claim"].strip(), "empty_fact")
            references(fact["source_refs"])
        taught = set()
        for card in lesson["cards"]:
            require(
                card["body"].strip()
                and card["fact_ids"]
                and set(card["fact_ids"]) <= facts.keys(),
                "unsupported_card",
            )
            references(card["source_refs"])
            taught.update(card["fact_ids"])
        for item in [*lesson["formulas"], *lesson["examples"]]:
            references(item["source_refs"])
            require(set(item["fact_ids"]) <= taught, "example_or_formula_not_taught")
            for step in item.get("steps", []):
                references(step["source_refs"])
        if book["grade"] == 6 and lesson["sequence"] <= 5:
            require(
                not lesson["formulas"], "no_artificial_formulas_for_conceptual_topics"
            )
        question_keys = set()
        taught_rules = {f["rule"] for f in lesson["formulas"]}
        for question in lesson["assessments"]:
            require(question["key"] not in question_keys, "duplicate_assessment")
            question_keys.add(question["key"])
            require(
                set(question["fact_ids"]) <= taught and question["fact_ids"],
                "answer_not_taught",
            )
            references(question["source_refs"])
            require(question["phase"] in {"guided", "independent"}, "assessment_phase")
            public, spec = question["public"], question["grading_spec"]
            require(
                public["prompt"].strip()
                and spec["kind"] == question["response_kind"]
                and spec["kind"]
                in {"concept_selection", "ordering", "numeric_quantity"},
                "assessment_contract",
            )
            require(
                set(public)
                <= {
                    "prompt",
                    "options",
                    "items",
                    "givens",
                    "symbols",
                    "suggested_unit",
                    "unit_choices",
                },
                "private_grading_must_not_enter_public_prompt",
            )
            require(
                spec["feedback"]["correct"].strip()
                and spec["feedback"]["incorrect"].strip()
                and spec["solution"],
                "authored_feedback_and_solution_required",
            )
            for step in spec["solution"]:
                require(step["body"].strip(), "empty_solution_step")
                references(step["source_refs"])
            if spec["kind"] == "concept_selection":
                choices = [o["id"] for o in public["options"]]
                require(
                    len(choices) >= 3
                    and len(set(choices)) == len(choices)
                    and choices == spec["choice_ids"]
                    and spec["expected_choice"] in choices,
                    "invalid_choices",
                )
                require(
                    len({o["label"] for o in public["options"]}) == len(choices),
                    "duplicate_choices",
                )
                correct = {"choice_id": spec["expected_choice"]}
            elif spec["kind"] == "ordering":
                choices = [o["id"] for o in public["items"]]
                require(
                    len(choices) >= 3
                    and set(choices) == set(spec["expected_order"])
                    and len(set(choices))
                    == len(choices)
                    == len(spec["expected_order"]),
                    "invalid_ordering",
                )
                correct = {"order": spec["expected_order"]}
            else:
                require(
                    spec["rule"] in taught_rules,
                    "calculation_rule_not_taught",
                )
                require(
                    spec["formula"] == FORMULAS[spec["rule"]],
                    "unreviewed_formula_equivalent",
                )
                require(
                    expected_quantity(spec) == calculation_value(question),
                    "calculation_answer_mismatch",
                )
                require(
                    spec["dimension"] in DIMENSION_UNIT
                    and numeric(spec["abs_tol_si"]) >= 0
                    and numeric(spec["rel_tol"]) >= 0,
                    "numeric_rubric_domain",
                )
                if spec["rule"] in REVIEWED_FORMULAS:
                    require(
                        reviewed_calculation(question)[1] == spec["dimension"],
                        "calculation_dimension_mismatch",
                    )
                else:
                    require(
                        spec["dimension"] == "length", "legacy_length_rule_dimension"
                    )
                if "unit_choices" in public:
                    require(
                        public["unit_choices"]
                        and all(
                            u in UNITS and UNITS[u][0] == spec["dimension"]
                            for u in public["unit_choices"]
                        ),
                        "public_unit_choice_dimension",
                    )
                require(
                    set(public["symbols"]) == set(spec["formula"]["variables"]),
                    "public_symbol_mismatch",
                )
                for expression in spec["formula"]["equivalents"]:
                    formula_ast(expression, spec["formula"])
                correct = {
                    "value": spec["expected_si"],
                    "unit": DIMENSION_UNIT[spec["dimension"]],
                    "formula": spec["formula"]["equivalents"][0],
                }
            require(
                grade_answer(spec, correct) == "correct",
                "authored_answer_does_not_grade",
            )
    return {
        "lessons": len(lessons),
        "cards": sum(len(l["cards"]) for l in lessons),
        "formulas": sum(len(l["formulas"]) for l in lessons),
        "worked_examples": sum(len(l["examples"]) for l in lessons),
        "assessments": sum(len(l["assessments"]) for l in lessons),
        "frq": sum(
            q["response_kind"] == "numeric_quantity"
            for l in lessons
            for q in l["assessments"]
        ),
    }


def import_batch(db, document):
    """Caller owns the transaction. Never load legacy DB/startup migration hooks.

    Reflect only the two installed content tables. Importing ORM models would
    load services.db, whose historical import hooks can alter an old users table.
    This CLI must only write the explicit reviewed Physics rows.
    """
    from sqlalchemy import MetaData, Table, select

    report = validate_batch(document)
    validate_review_evidence(document)
    metadata = MetaData()
    lessons_table = Table(
        "curriculum_v2_lessons", metadata, autoload_with=db.connection()
    )
    questions_table = Table(
        "curriculum_assessments_v2", metadata, autoload_with=db.connection()
    )
    for lesson in document["lessons"]:
        digest = fingerprint(lesson)
        saved = db.execute(
            select(lessons_table.c.content_sha256).where(
                lessons_table.c.key == lesson["key"]
            )
        ).scalar_one_or_none()
        if saved is not None:
            require(saved == digest, "changed_content_requires_new_reviewed_revision")
            continue
        content = {
            k: deepcopy(lesson[k])
            for k in ("cards", "formulas", "examples", "source_refs", "xp_reward")
        }
        db.execute(
            lessons_table.insert().values(
                key=lesson["key"],
                subject="fizika",
                grade=document["grade"],
                sequence=lesson["sequence"],
                revision=lesson["revision"],
                topic_id=lesson["topic_id"],
                content_sha256=digest,
                title=lesson["title"],
                content=content,
            )
        )
        for index, q in enumerate(lesson["assessments"]):
            db.execute(
                questions_table.insert().values(
                    key=q["key"],
                    lesson_key=lesson["key"],
                    order_index=index,
                    response_kind=q["response_kind"],
                    public_prompt={"phase": q["phase"], **q["public"]},
                    grading_spec=q["grading_spec"],
                    source_refs=q["source_refs"],
                )
            )
    return report
