"""Explicit first Physics batch, source validation and immutable preview import.

Loading/validating documents never imports ORM or opens a database. There is no
glob publication, startup seed, runtime generation, or modification of Biology.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

from services.assessment_grading import UNITS, formula_ast, grade_answer, numeric

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "scripts/curriculum/physics"
BATCH = DIRECTORY / "grade6_batch1.json"

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


def fingerprint(document):
    return hashlib.sha256(
        json.dumps(document, ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()


def require(condition, code):
    if not condition:
        raise ValueError(code)


def load_batch():
    document = json.loads(BATCH.read_text())
    validate_batch(document)
    validate_review_evidence(document)
    return document


def validate_review_evidence(document):
    audit = json.loads((DIRECTORY / "grade6_batch1_review.json").read_text())
    require(
        audit["batch_file_sha256"] == hashlib.sha256(BATCH.read_bytes()).hexdigest()
        and fingerprint(document) == fingerprint(json.loads(BATCH.read_text())),
        "changed_content_requires_new_reviewed_revision",
    )
    book = json.loads((DIRECTORY / "physics_sources.json").read_text())["books"][0]
    require(
        audit["book_sha256"] == book["sha256"]
        and not audit["ready_for_general_publication"]
        and audit["independent_subject_expert"] == "not_claimed",
        "source_review_scope",
    )
    require(
        [p["pdf_page"] for p in audit["pages"]] == list(range(3, 17)),
        "all_first_batch_pages_reviewed",
    )
    for page in audit["pages"]:
        source = book["page_audit"][page["pdf_page"] - 1]
        require(
            page["printed_page"] == source["printed_page"]
            and page["text_sha256"] == source["text_sha256"]
            and page["original_text_and_image_checked"] is True
            and len(page["reviewed_render_sha256"]) == 64,
            "page_review_evidence",
        )


def calculation_value(question):
    rule = question["grading_spec"]["rule"]
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
    book = catalog["books"][0]
    require(
        document["schema_version"] == 2
        and document["subject"] == "fizika"
        and document["language"] == "uz"
        and document["grade"] == 6,
        "physics_batch_identity",
    )
    require(
        document["publication"] == "local_test_preview_only"
        and document["ai_explain"] is False,
        "no_physics_publication",
    )
    lessons = document["lessons"]
    require(
        [l["sequence"] for l in lessons] == list(range(1, 8)),
        "first_batch_only_sections_1_to_7",
    )
    keys = set()

    def references(refs):
        require(isinstance(refs, list) and refs, "source_refs_required")
        for ref in refs:
            topic = next(
                (r for r in book["records"] if r["id"] == ref["topic_id"]), None
            )
            require(
                topic is not None and topic["kind"] == "topic" and topic["number"] <= 7,
                "source_outside_reviewed_first_batch",
            )
            require(
                ref["book_id"] == book["id"]
                and ref["sha256"] == book["sha256"]
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
            for pdf, label, digest in zip(pp, printed, ref["page_text_sha256"]):
                require(
                    topic["pdf_start"] <= pdf <= topic["pdf_end"],
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
            lesson["topic_id"] == f"physics-6-section-{lesson['sequence']}"
            and lesson["revision"] == 1
            and lesson["xp_reward"] == 10,
            "lesson_source_order",
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
        if lesson["sequence"] <= 5:
            require(
                not lesson["formulas"], "no_artificial_formulas_for_conceptual_topics"
            )
        question_keys = set()
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
                    lesson["sequence"] in {6, 7}, "calculation_not_in_conceptual_topic"
                )
                require(
                    spec["formula"] == FORMULAS[spec["rule"]],
                    "unreviewed_formula_equivalent",
                )
                require(
                    Fraction(Decimal(spec["expected_si"]))
                    == calculation_value(question),
                    "calculation_answer_mismatch",
                )
                require(
                    spec["dimension"] == "length"
                    and numeric(spec["abs_tol_si"]) >= 0
                    and numeric(spec["rel_tol"]) >= 0,
                    "numeric_rubric_domain",
                )
                require(
                    set(public["symbols"]) == set(spec["formula"]["variables"]),
                    "public_symbol_mismatch",
                )
                for expression in spec["formula"]["equivalents"]:
                    formula_ast(expression, spec["formula"])
                correct = {
                    "value": spec["expected_si"],
                    "unit": "m",
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
                grade=6,
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
