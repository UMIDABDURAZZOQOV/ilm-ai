"""Capacitance versus charge/force, source constants and scoped work arithmetic."""

from copy import deepcopy

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    26: [
        "Butun juftlik uchlariga",
        "R1 uchlaridagi U1 ni",
        "Qo‘shimcha ketma-ket qism bo‘lsa avtomatik teng emas",
    ],
    27: ["8nC", "1e-9F", "O‘zgarmaydi"],
    28: ["Sig‘imlar yig‘indisi", "Har ikkalasidan kichik", "C ga mutanosib turlicha"],
    29: ["a²", "Birliksiz", "Avval juftlik ekvivalenti,keyin C3 qo‘shiladi"],
    30: ["Joul", "Doimiy R li ohmik element", "Sarflangan elektr energiyani"],
}


@pytest.mark.parametrize("sequence", range(26, 31))
def test_source_semantics_and_wrong_choices(sequence):
    lesson = load_batch("grade8_batch6")["lessons"][sequence - 26]
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


def test_all_seventeen_independent_answers_and_equivalent_formulas():
    doc = load_batch("grade8_batch6")
    assert validate_batch(doc) == {
        "lessons": 5,
        "cards": 21,
        "formulas": 17,
        "worked_examples": 6,
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
        (0, 6, 2, "0"),
        (1, 4, 1, "0"),
        (1, 7, 1, "8.85e-2"),
        (1, 7, 0, "0.5"),
        (1, 7, 3, "0"),
        (2, 5, 0, "0"),
        (2, 6, 2, "0"),
        (3, 4, 2, "0"),
        (3, 4, 1, "8.85e-11"),
        (3, 5, 0, "1"),
        (3, 6, 1, "0"),
        (4, 6, 2, "0"),
    ],
)
def test_source_domains_constants_and_denominators(li, qi, gi, bad):
    q = deepcopy(load_batch("grade8_batch6")["lessons"][li]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_capacitance_prefixes_do_not_confuse_charge_or_force():
    lessons = load_batch("grade8_batch6")["lessons"]
    spec = lessons[2]["assessments"][5]["grading_spec"]
    for unit in ["µF", "μF", "uF"]:
        assert (
            grade_answer(spec, {"value": "3", "unit": unit, "formula": "1/(1/C1+1/C2)"})
            == "correct"
        )
    assert (
        grade_answer(spec, {"value": "3", "unit": "nF", "formula": "1/(1/C1+1/C2)"})
        == "out_of_tolerance"
    )
    for unit in ["C", "N"]:
        assert (
            grade_answer(spec, {"value": "3", "unit": unit, "formula": "1/(1/C1+1/C2)"})
            == "dimension_mismatch"
        )
    assert calculation_value(lessons[2]["assessments"][5]) < calculation_value(
        lessons[2]["assessments"][4]
    )
    spec = lessons[0]["assessments"][6]["grading_spec"]
    # Known voltage belongs to parallel pair: interpreting it across total series/mixed network is wrong.
    assert (
        grade_answer(spec, {"value": "0.75", "unit": "A", "formula": "U/(R1+R2)"})
        == "wrong_formula"
    )
