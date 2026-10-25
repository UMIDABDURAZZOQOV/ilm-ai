"""Power/energy prefixes, topology, laboratory mean correction and exact heat root."""

from copy import deepcopy

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    31: ["W va J", "Energiya", "Yorug‘lik miqdori aynan tengligini"],
    32: [
        "U",
        "Bir xil I da R ga to‘g‘ri proporsional",
        "Keyingi R hisobida qo‘shimcha xatoga",
    ],
    33: ["Parallel", "(P1+P2+P3)/3", "U,I va nominal ishlash sharoiti"],
    34: ["To‘rt marta ortadi", "75%", "Ular turli fizik kattaliklar"],
    35: ["0,8", "Bir xil vaqt va doimiy quvvatlarda", "Kichikroq"],
}


@pytest.mark.parametrize("sequence", range(31, 36))
def test_semantic_keys_and_wrong_options(sequence):
    lesson = load_batch("grade8_batch7")["lessons"][sequence - 31]
    qs = [q for q in lesson["assessments"] if q["response_kind"] == "concept_selection"]
    assert len(qs) == len(KEYS[sequence])
    for q, label in zip(qs, KEYS[sequence]):
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
                grade_answer(q["grading_spec"], {"order": ["s1", "s2", "s3"]})
                != "correct"
            )


def test_all_independent_power_heat_answers_alternatives_and_wrong_units():
    doc = load_batch("grade8_batch7")
    assert validate_batch(doc) == {
        "lessons": 5,
        "cards": 22,
        "formulas": 17,
        "worked_examples": 5,
        "assessments": 37,
        "frq": 17,
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
    assert count == 17


@pytest.mark.parametrize(
    "li,qi,gi,bad",
    [
        (0, 6, 1, "0"),
        (0, 7, 0, "100"),
        (1, 4, 1, "0"),
        (1, 5, 2, "0"),
        (1, 6, 1, "0"),
        (2, 5, 0, "-1"),
        (3, 6, 0, "601"),
        (3, 7, 0, "25"),
        (3, 8, 0, "1441"),
        (3, 8, 1, "0"),
        (3, 8, 2, "0"),
        (4, 4, 0, "101"),
        (4, 5, 1, "0"),
        (4, 6, 2, "0"),
    ],
)
def test_model_bounds_meter_reset_efficiency_and_exact_root(li, qi, gi, bad):
    q = deepcopy(load_batch("grade8_batch7")["lessons"][li]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_wh_is_energy_not_power_and_mean_stays_between_extremes():
    lessons = load_batch("grade8_batch7")["lessons"]
    energy = lessons[0]["assessments"][5]["grading_spec"]
    assert (
        grade_answer(energy, {"value": "90", "unit": "Wh", "formula": "P*t"})
        == "correct"
    )
    assert (
        grade_answer(energy, {"value": "90", "unit": "W", "formula": "P*t"})
        == "dimension_mismatch"
    )
    assert (
        grade_answer(energy, {"value": "90", "unit": "kWh", "formula": "P*t"})
        == "out_of_tolerance"
    )
    mean = lessons[2]["assessments"][5]
    assert 1 < calculation_value(mean) < 2
    assert (
        grade_answer(
            mean["grading_spec"],
            {"value": "1.2", "unit": "W", "formula": "(P1+P2-P3)/3"},
        )
        == "wrong_formula"
    )
    for q in lessons[2]["assessments"]:
        if q["response_kind"] == "numeric_quantity":
            assert "haqiqiy tajriba emas" in q["public"]["prompt"]


def test_exact_root_is_scoped_to_reviewed_current_rule():
    lessons = load_batch("grade8_batch7")["lessons"]
    root = lessons[3]["assessments"][8]["grading_spec"]
    answer = {"value": "sqrt(4)", "unit": "A", "formula": "sqrt(Q/(R*t))"}
    assert grade_answer(root, answer) == "correct"
    assert grade_answer(root, {**answer, "value": "-2"}) == "sign_error"
    for bad in ["sqrt(-4)", "sqrt(4,2)", "__import__('os')", "sqrt(2)"]:
        assert grade_answer(root, {**answer, "value": bad}) != "correct"
    legacy = lessons[0]["assessments"][4]["grading_spec"]
    assert (
        grade_answer(legacy, {"value": "sqrt(9)", "unit": "W", "formula": "I*U"})
        == "invalid_expression"
    )
