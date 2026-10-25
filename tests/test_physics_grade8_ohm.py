"""Ohmic domain, independent wire arithmetic and explicitly digital activities."""

from copy import deepcopy

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    16: [
        "Ma’lum qarshilikli element",
        "Zanjirga kirgan simning faol qismini",
        "Potensiometr",
        "Ommetr",
    ],
    17: [
        "Uch marta ortadi",
        "Ikki marta kamayadi",
        "Ampermetr kichik,voltmeter katta qarshilikli",
    ],
    18: [
        "1e-6",
        "Harorat/material ta’siri sabab modelni qayta tekshirish kerak",
        "Elektronlar soni",
    ],
    19: [
        "Parallel",
        "0,04A",
        "R ning o‘zgarishini aytishdan oldin shartlarni tekshiramiz",
    ],
    20: [
        "Eng katta faol qarshilik holati",
        "Kalit uziladi",
        "Ortadi",
        "Haqiqiy sonli o‘lchovlar hali berilmaganini",
    ],
}


@pytest.mark.parametrize("sequence", range(16, 21))
def test_semantic_keys_wrong_options_and_ordering(sequence):
    lesson = load_batch("grade8_batch4")["lessons"][sequence - 16]
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
    assert lesson["review"]["physical_experiment_completed"] is False
    if sequence in [16, 20]:
        assert not lesson["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in lesson["assessments"]
        )


def test_independent_numeric_oracles_and_every_allowed_alternative():
    doc = load_batch("grade8_batch4")
    assert validate_batch(doc) == {
        "lessons": 5,
        "cards": 20,
        "formulas": 11,
        "worked_examples": 6,
        "assessments": 33,
        "frq": 11,
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
    assert count == 11


@pytest.mark.parametrize(
    "li,qi,gi,bad",
    [
        (1, 4, 1, "0"),
        (1, 6, 1, "0"),
        (1, 7, 2, "0"),
        (1, 7, 3, "0"),
        (2, 4, 3, "0"),
        (2, 6, 3, "0"),
        (2, 7, 2, "0"),
        (2, 8, 3, "1.7e-19"),
        (2, 8, 0, "0.0000000000000000001"),
        (3, 5, 0, "-1"),
    ],
)
def test_invalid_denominators_constants_counts_and_average(li, qi, gi, bad):
    q = deepcopy(load_batch("grade8_batch4")["lessons"][li]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_lab_is_explicitly_hypothetical_and_not_next_lesson_theory():
    lessons = load_batch("grade8_batch4")["lessons"]
    lab = lessons[3]
    for q in lab["assessments"]:
        if q["response_kind"] == "numeric_quantity":
            assert "shartli" in q["public"]["prompt"].lower()
            assert "haqiqiy tajriba" in q["public"]["prompt"].lower()
    # Lower part of inclusive page64 introduces series circuits; no sum formula was imposed.
    assert not lessons[4]["formulas"]
