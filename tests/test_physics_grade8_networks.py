"""Independent node/topology and arithmetic checks for series/parallel networks."""

from copy import deepcopy

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    21: ["Tok kuchi", "Yagona tok yo‘li uziladi", "Ortadi"],
    22: ["Kuchlanish", "Kattaroq", "Eng kichigidan ham kichik"],
    23: [
        "Keyingi elementning manfiy uchiga",
        "DCV",
        "Nominal qiymat,qayd alohida tekshiriladi",
    ],
    24: ["I1=I2=I", "U1=U2=U", "O‘sha shoxobchaga ketma-ket"],
    25: [
        "Ikkala uchi bir xil ikki tugunga ulanadi",
        "R2||R3 ekvivalentini topish",
        "Ketma-ket/parallel bosqichlarga ajraladigan sxemalarga",
    ],
}


@pytest.mark.parametrize("sequence", range(21, 26))
def test_semantic_keys_and_wrong_options(sequence):
    lesson = load_batch("grade8_batch5")["lessons"][sequence - 21]
    questions = [
        q for q in lesson["assessments"] if q["response_kind"] == "concept_selection"
    ]
    assert len(questions) == len(KEYS[sequence])
    for q, label in zip(questions, KEYS[sequence]):
        assert label in [o["label"] for o in q["public"]["options"]]
        for option in q["public"]["options"]:
            assert grade_answer(q["grading_spec"], {"choice_id": option["id"]}) == (
                "correct" if option["label"] == label else "incorrect_concept"
            )
    for q in lesson["assessments"]:
        if q["response_kind"] == "ordering":
            assert (
                grade_answer(q["grading_spec"], {"order": ["s2", "s3", "s1"]})
                == "correct"
            )
            assert (
                grade_answer(q["grading_spec"], {"order": ["s3", "s2", "s1"]})
                != "correct"
            )


def test_all_network_numeric_answers_and_formula_alternatives():
    doc = load_batch("grade8_batch5")
    assert validate_batch(doc) == {
        "lessons": 5,
        "cards": 20,
        "formulas": 13,
        "worked_examples": 5,
        "assessments": 33,
        "frq": 13,
    }
    count = 0
    for lesson in doc["lessons"]:
        for q in lesson["assessments"]:
            spec = q["grading_spec"]
            if spec["kind"] != "numeric_quantity":
                continue
            count += 1
            answer = new_answer(lesson, q)
            for formula in spec["formula"]["equivalents"]:
                assert grade_answer(spec, {**answer, "formula": formula}) == "correct"
            assert grade_answer(spec, {**answer, "unit": "kg"}) == "dimension_mismatch"
            assert (
                grade_answer(spec, {**answer, "value": "123456789"})
                == "out_of_tolerance"
            )
            assert grade_answer(spec, {**answer, "formula": "1"}) == "wrong_formula"
    assert count == 13


@pytest.mark.parametrize(
    "li,qi,gi,bad",
    [
        (0, 4, 0, "-1"),
        (0, 6, 1, "0"),
        (1, 5, 0, "0"),
        (1, 6, 2, "0"),
        (2, 4, 1, "-1"),
        (3, 5, 1, "0"),
        (4, 4, 2, "0"),
        (4, 5, 3, "0"),
    ],
)
def test_invalid_network_component_domains(li, qi, gi, bad):
    q = deepcopy(load_batch("grade8_batch5")["lessons"][li]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_parallel_is_below_smallest_branch_and_topology_changes_answer():
    lessons = load_batch("grade8_batch5")["lessons"]
    parallel = lessons[1]["assessments"][5]
    assert calculation_value(parallel) < 12
    answer = new_answer(lessons[1], parallel)
    assert (
        grade_answer(parallel["grading_spec"], {**answer, "formula": "R1+R2"})
        == "wrong_formula"
    )
    mixed = lessons[4]["assessments"][4]
    assert calculation_value(mixed) == 8  # 4+(12||6), not (4+12)||6.
    wrong = {"value": "8", "unit": "Ω", "formula": "(R1+R2)*R3/(R1+R2+R3)"}
    assert grade_answer(mixed["grading_spec"], wrong) == "wrong_formula"
    lab = lessons[3]
    assert lab["review"]["physical_experiment_completed"] is False
    for q in lab["assessments"]:
        if q["response_kind"] == "numeric_quantity":
            assert "haqiqiy tajriba emas" in q["public"]["prompt"]
    rules = {f["rule"]: f for f in lab["formulas"]}
    assert any(
        r["topic_id"] == "physics-8-section-21" and 65 in r["pdf_pages"]
        for r in rules["series_resistance2"]["source_refs"]
    )
    assert any(
        r["topic_id"] == "physics-8-section-22" and 69 in r["pdf_pages"]
        for r in rules["parallel_resistance2"]["source_refs"]
    )
