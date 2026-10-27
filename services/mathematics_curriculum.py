"""Reviewed Math documents and explicit immutable local/test import.

Source availability, topic mapping and completed lessons are separate counts.
Never import automatically from production startup or existing subject seeds.
"""

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "scripts/curriculum/mathematics"
SHAPES = {"circle", "square", "triangle", "rectangle", "sphere", "cube"}
COLORS = {"indigo", "yellow", "turquoise"}


def digest(value):
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()


def require(condition, code):
    if not condition:
        raise ValueError(code)


def manifest():
    return json.loads((ROOT / "source_manifest.json").read_text())


def validate_scene(scene):
    require(scene["type"] in {"shape_board", "bars"}, "unsupported_math_visual")
    items = scene["items"]
    require(
        1 <= len(items) <= 9 and len({i["id"] for i in items}) == len(items),
        "invalid_math_objects",
    )
    for item in items:
        require(
            item["shape"] in SHAPES and item["color"] in COLORS, "invalid_math_shape"
        )
        require(
            all(type(item[k]) in {int, float} for k in ["size", "x", "y"]),
            "invalid_math_geometry",
        )
        require(
            0.4 <= item["size"] <= 1.4
            and 0.1 <= item["x"] <= 0.9
            and 0.1 <= item["y"] <= 0.9,
            "math_geometry_outside_board",
        )


def model_answer(public, rule):
    items = public["visual"]["items"]
    op = rule["test"]
    if op == "count":
        return str(
            sum("shape" not in rule or i["shape"] == rule["shape"] for i in items)
        )
    if op == "same_property":
        reference = next(i for i in items if i["id"] == rule["reference"])
        matches = [
            i
            for i in items
            if i["id"] != reference["id"]
            and i[rule["property"]] == reference[rule["property"]]
        ]
    elif op == "shape":
        matches = [i for i in items if i["shape"] == rule["value"]]
    elif op == "left_of":
        reference = next(i for i in items if i["id"] == rule["reference"])
        matches = [i for i in items if i["x"] < reference["x"]]
    elif op in {"max_property", "min_property"}:
        values = [i[rule["property"]] for i in items]
        best = (max if op == "max_property" else min)(values)
        matches = [i for i in items if i[rule["property"]] == best]
    else:
        raise ValueError("unsupported_math_model_rule")
    require(len(matches) == 1, "ambiguous_math_model_answer")
    return matches[0]["id"]


def load_course():
    document = json.loads((ROOT / "grade1_part1_batch1.json").read_text())
    review = json.loads((ROOT / "grade1_part1_review.json").read_text())
    source = next(b for b in manifest()["books"] if b["book_id"] == review["book_id"])
    require(review["book_sha256"] == source["sha256"], "math_source_sha_mismatch")
    topics = {t["topic_id"]: t for t in review["topics"]}
    seen = set()
    for lesson in document["lessons"]:
        require(lesson["key"] not in seen, "duplicate_math_lesson")
        seen.add(lesson["key"])
        topic = topics[lesson["topic_id"]]
        require(
            topic["verification"] == "body_images_reviewed", "math_topic_unreviewed"
        )
        refs = {r["fact_id"]: r for r in topic["facts"]}
        require(
            lesson["source_refs"] == topic["facts"] and lesson["xp_reward"] == 10,
            "math_lesson_contract",
        )
        require(
            lesson["formulas"] == [], "early_properties_need_no_artificial_formulas"
        )
        units = [
            *lesson["cards"],
            *lesson["examples"],
            lesson["explorer"],
            *lesson["questions"],
        ]
        units += [s for e in lesson["examples"] for s in e["steps"]]
        for unit in units:
            require(bool(unit["source_refs"]), "math_missing_source_ref")
            if "visual" in unit:
                validate_scene(unit["visual"])
            for ref in unit["source_refs"]:
                require(ref == refs.get(ref["fact_id"]), "math_unreviewed_fact")
        require(
            len(lesson["cards"]) >= 5 and bool(lesson["examples"]),
            "incomplete_math_instruction",
        )
        require(
            {q["public"]["phase"] for q in lesson["questions"]}
            >= {"guided", "mcq", "frq", "transfer"},
            "incomplete_math_practice",
        )
        keys = [q["id"] for q in lesson["questions"]]
        require(len(set(keys)) == len(keys), "duplicate_math_question")
        for q in lesson["questions"]:
            public, spec = q["public"], q["grading"]
            require(public["response_kind"] == spec["kind"], "math_response_contract")
            require(
                not (
                    {"expected", "aliases", "grading", "solution", "correct_answer"}
                    & set(public)
                ),
                "math_private_key_public",
            )
            require(
                len(spec["hints"]) >= 3 and bool(spec["solution"]),
                "math_missing_scaffolding",
            )
            if "visual" in public:
                validate_scene(public["visual"])
            if "model_rule" in spec:
                require(
                    model_answer(public, spec["model_rule"]) == spec["expected"],
                    "math_model_answer_mismatch",
                )
            if spec["kind"] == "choice":
                require(
                    [c["id"] for c in public["choices"]] == spec["choice_ids"],
                    "math_choice_ids_mismatch",
                )
                require(
                    spec["expected"] in spec["choice_ids"], "math_answer_not_in_choices"
                )
    return document["lessons"]


def staging_url(url):
    local = (
        url.get_backend_name() == "sqlite"
        and "mathematics_staging" in (url.database or "")
    ) or (
        url.get_backend_name() == "postgresql"
        and url.host in {"localhost", "127.0.0.1", "::1"}
        and "staging" in (url.database or "")
    )
    require(
        os.getenv("ENVIRONMENT", "development") in {"development", "test"} and local,
        "math_owned_local_staging_only",
    )


def import_course(db):
    from services.mathematics_models import MathLesson

    staging_url(db.get_bind().url)
    lessons = load_course()  # Validate everything before any write.
    result = {"created": 0, "skipped": 0}
    for lesson in lessons:
        old = db.get(MathLesson, lesson["key"])
        if old:
            require(
                old.sha256 == digest(lesson), "math_revision_change_requires_new_review"
            )
            result["skipped"] += 1
        else:
            db.add(
                MathLesson(
                    key=lesson["key"],
                    grade=lesson["grade"],
                    part=lesson["part"],
                    sequence=lesson["sequence"],
                    sha256=digest(lesson),
                    document=lesson,
                )
            )
            result["created"] += 1
    return result
