"""Independent semantic and dimensional checks for source-reviewed grade8 §11–15."""

from copy import deepcopy

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    11: ["Har 1C uchun 3J ish", "Voltmeter lampochkaga parallel", "0,002V"],
    12: ["Amper", "Ketma-ket", "Tok bir xil"],
    13: [
        "Sekund",
        "Kesimdan o‘tgan elektronlarning hisobiy jami massasi",
        "I va t noldan katta",
    ],
    14: [
        "Birinchi lampa uchlaridagi kuchlanish",
        "Kalitni uzish",
        "O‘lchov yo‘q,qayd etilmagan",
        "Lampalar bilan ketma-ket yo‘lda",
        "Sxema va qayd tartibi tushunilganini",
    ],
    15: ["2marta ortadi", "3marta kamayadi", "Ω*m", "Uzunlik va yuzani aralashtiramiz"],
}


@pytest.mark.parametrize("sequence", range(11, 16))
def test_semantic_answers_and_each_wrong_option(sequence):
    lesson = load_batch("grade8_batch3")["lessons"][sequence - 11]
    questions = [
        q for q in lesson["assessments"] if q["response_kind"] == "concept_selection"
    ]
    assert len(questions) == len(KEYS[sequence])
    for question, label in zip(questions, KEYS[sequence]):
        assert label in [o["label"] for o in question["public"]["options"]]
        for option in question["public"]["options"]:
            assert grade_answer(
                question["grading_spec"], {"choice_id": option["id"]}
            ) == ("correct" if option["label"] == label else "incorrect_concept")
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
    if sequence == 14:
        assert lesson["review"]["physical_experiment_completed"] is False
        assert not lesson["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in lesson["assessments"]
        )


def test_independent_numeric_oracles_alternatives_and_wrong_dimensions():
    doc = load_batch("grade8_batch3")
    assert validate_batch(doc) == {
        "lessons": 5,
        "cards": 21,
        "formulas": 16,
        "worked_examples": 6,
        "assessments": 39,
        "frq": 16,
    }
    seen = 0
    for lesson in doc["lessons"]:
        for q in lesson["assessments"]:
            spec = q["grading_spec"]
            if spec["kind"] != "numeric_quantity":
                continue
            seen += 1
            answer = new_answer(lesson, q)
            for formula in spec["formula"]["equivalents"]:
                assert grade_answer(spec, {**answer, "formula": formula}) == "correct"
            assert (
                grade_answer(
                    spec,
                    {**answer, "unit": "s" if spec["dimension"] != "time" else "V"},
                )
                == "dimension_mismatch"
            )
            assert (
                grade_answer(spec, {**answer, "value": "123456789"})
                == "out_of_tolerance"
            )
            assert grade_answer(spec, {**answer, "formula": "1"}) == "wrong_formula"
    assert seen == 16


@pytest.mark.parametrize(
    "li,qi,gi,bad",
    [
        (0, 4, 1, "0"),  # U=A/q requires q>0.
        (0, 7, 0, "2.5"),  # Fractional galvanic element.
        (1, 4, 1, "0"),  # Current denominator time.
        (1, 6, 1, "0"),  # Time denominator current.
        (1, 7, 2, "1.7e-19"),  # Source elementary charge.
        (1, 7, 0, "0.00000000000000001"),  # Fractional electron count.
        (2, 6, 3, "1e-30"),  # Source electron mass.
        (4, 5, 2, "0"),  # Wire area.
        (4, 6, 2, "0"),  # Resistivity denominator length.
        (4, 7, 2, "0"),  # Wire length denominator rho.
        (4, 8, 2, "0"),  # Wire area denominator R.
    ],
)
def test_reject_inconsistent_source_domains(li, qi, gi, bad):
    q = deepcopy(load_batch("grade8_batch3")["lessons"][li]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_current_micro_prefix_and_area_square_prefix_are_exact():
    lessons = load_batch("grade8_batch3")["lessons"]
    current = lessons[1]["assessments"][4]["grading_spec"]
    for unit in ["µA", "μA", "uA"]:
        assert (
            grade_answer(current, {"value": "200000", "unit": unit, "formula": "q/t"})
            == "correct"
        )
    # Unit A is case-sensitive; a is not an invented alternate for amperes.
    assert (
        grade_answer(current, {"value": "0.2", "unit": "a", "formula": "q/t"})
        == "unknown_unit"
    )
    area = lessons[4]["assessments"][8]["grading_spec"]
    assert (
        grade_answer(area, {"value": "0.005", "unit": "cm2", "formula": "rho*l/R"})
        == "correct"
    )
    assert (
        grade_answer(area, {"value": "0.5", "unit": "m2", "formula": "rho*l/R"})
        == "out_of_tolerance"
    )
    assert (
        grade_answer(area, {"value": "0.5", "unit": "mm", "formula": "rho*l/R"})
        == "dimension_mismatch"
    )
    assert all(
        52 not in r["pdf_pages"]
        for fact in lessons[3]["facts"].values()
        for r in fact["source_refs"]
    )
