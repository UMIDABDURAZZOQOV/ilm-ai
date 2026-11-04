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
EXPLORERS = {
    "tens_units_20",
    "number_pairs_12",
    "number_pairs_14",
    "number_pairs_16",
    "number_pairs_18",
    "number_pairs_20",
    "compare_place_value_20",
    "brackets_single",
    "brackets_double",
    "bridge_ten_intro",
    "bridge_ten_apply",
    "bridge_ten_line",
    "subtract_units_20",
    "subtract_bridge_ten",
    "missing_subtrahend",
    "inverse_family",
    "commutative",
    "addition_table",
    "compare_same_addend",
    "expression_steps",
    "segments",
    "missing_addend",
    "missing_minuend",
    "shape_properties",
    "compare_lengths",
    "positions",
    "count_once",
    "flat_solid",
    "timeline",
    "group_members",
    "pair_groups",
    "number_line",
    "addition",
    "subtraction",
    "comparison",
    "one_two",
    "compose_three",
    "compose_four",
    "compose_five",
    "compose_six",
    "compose_seven",
    "compose_eight",
    "compose_nine",
    "compose_ten",
    "part_whole_five",
    "steps_five",
    "zero",
    "ordering_numbers",
    "natural_numbers",
    "parity",
    "point_line",
}


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
        1 <= len(items) <= 10 and len({i["id"] for i in items}) == len(items),
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
    lessons = []
    for batch, review_file in BATCHES:
        document = json.loads((ROOT / batch).read_text())
        review = json.loads((ROOT / review_file).read_text())
        lessons.extend(validate_document(document, review))
    keys = [l["key"] for l in lessons]
    require(len(keys) == len(set(keys)), "duplicate_math_lesson_across_batches")
    coordinates = [(l["grade"], l["part"], l["sequence"]) for l in lessons]
    require(len(coordinates) == len(set(coordinates)), "duplicate_math_sequence")
    return sorted(lessons, key=lambda l: (l["grade"], l["part"], l["sequence"]))


BATCHES = [
    ("grade1_part1_batch1.json", "grade1_part1_review.json"),
    ("grade1_part1_batch2.json", "grade1_part1_batch2_review.json"),
    ("grade1_part1_batch3.json", "grade1_part1_batch3_review.json"),
    ("grade1_part1_batch4.json", "grade1_part1_batch4_review.json"),
    ("grade1_part1_batch5.json", "grade1_part1_batch5_review.json"),
    ("grade1_part1_batch6.json", "grade1_part1_batch6_review.json"),
    ("grade1_part1_batch7.json", "grade1_part1_batch7_review.json"),
    ("grade1_part1_batch8.json", "grade1_part1_batch8_review.json"),
    ("grade1_part2_batch1.json", "grade1_part2_batch1_review.json"),
    ("grade1_part2_batch2.json", "grade1_part2_batch2_review.json"),
    ("grade1_part2_batch3.json", "grade1_part2_batch3_review.json"),
]


def validate_document(document, review):
    source = next(b for b in manifest()["books"] if b["book_id"] == review["book_id"])
    require(review["book_sha256"] == source["sha256"], "math_source_sha_mismatch")
    topics = {t["topic_id"]: t for t in review["topics"]}
    require(len(topics) == len(review["topics"]), "duplicate_math_review_topic")
    seen = set()
    for lesson in document["lessons"]:
        require(lesson["key"] not in seen, "duplicate_math_lesson")
        seen.add(lesson["key"])
        topic = topics[lesson["topic_id"]]
        require(lesson["explorer"]["type"] in EXPLORERS, "unsupported_math_explorer")
        require(
            topic["verification"] == "body_images_reviewed", "math_topic_unreviewed"
        )
        refs = {r["fact_id"]: r for r in topic["facts"]}
        require(
            bool(refs) and len(refs) == len(topic["facts"]),
            "duplicate_or_missing_math_fact",
        )
        require(
            lesson["grade"] == source["grade"]
            and lesson["part"] == source["part"]
            and [p["pdf_page"] for p in topic["pages"]] == topic["pdf_pages"]
            and [p["printed_page"] for p in topic["pages"]] == topic["printed_pages"]
            and all(1 <= p <= source["pdf_pages"] for p in topic["pdf_pages"]),
            "math_review_page_mapping_mismatch",
        )
        for ref in refs.values():
            require(
                ref["book_id"] == review["book_id"]
                and ref["grade"] == lesson["grade"]
                and ref["part"] == lesson["part"]
                and ref["topic_id"] == lesson["topic_id"]
                and ref["pdf_pages"] == topic["pdf_pages"]
                and ref["printed_pages"] == topic["printed_pages"],
                "math_fact_pages_outside_review",
            )
        require(
            lesson["source_refs"] == topic["facts"] and lesson["xp_reward"] == 10,
            "math_lesson_contract",
        )
        require(
            (lesson["grade"], lesson["part"]) != (1, 1)
            or lesson["sequence"] >= 11
            or lesson["formulas"] == [],
            "early_properties_need_no_artificial_formulas",
        )
        from services.mathematics_grading import exact_number

        for notation in lesson["formulas"]:
            require(
                notation["kind"] == "worked_identity"
                and bool(notation["title"])
                and bool(notation["meaning"])
                and notation["expression"].count("=") == 1,
                "unsupported_math_notation",
            )
            left, right = notation["expression"].split("=")
            require(exact_number(left) == exact_number(right), "false_math_identity")
        units = [
            *lesson["cards"],
            *lesson["examples"],
            *lesson["formulas"],
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
            elif spec["kind"] == "ordering":
                ids = [item["id"] for item in public["items"]]
                require(
                    2 <= len(ids) <= 10
                    and len(ids) == len(set(ids))
                    and len(spec["expected"]) == len(ids)
                    and set(spec["expected"]) == set(ids),
                    "math_invalid_ordering",
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
