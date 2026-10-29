"""Vacuum integer counts, discharge graph scope and magnetic vector concepts."""

from copy import deepcopy

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    46: [
        "Qizdirilgan metall sirtidan elektron ajralishi",
        "Qizdirilgan katoddan anodga",
        "Elektronlar soni",
    ],
    47: [
        "Gaz orqali elektr toki o‘tishi",
        "Ionlar va erkin elektronlar",
        "Rekombinatsiya",
        "Ular turli vazifali tushunchalar",
        "Tayyor rasmdagi tashuvchilarni izohlash",
    ],
    48: [
        "Nomustaqil",
        "To‘yinish tokiga yaqin sohani",
        "Tashqi ionizatorning davomiy ta’siridan",
        "Uchqun razryad",
        "Siyrak gazli yorug‘lik lampalari",
    ],
    49: [
        "Tortiladi",
        "Itariladi",
        "Har bo‘lakdaN vaS hosil bo‘ladi",
        "N/S yorlig‘i va o‘zaro ta’sir sharti",
        "Butun o‘rta hududda B aynan nol ekanini",
    ],
    50: [
        "Berk konturlar",
        "N danS ga",
        "Tesla",
        "Maydon chizig‘iga urinma bo‘ylab",
        "Aniq tesla qiymatini",
    ],
}


@pytest.mark.parametrize("sequence", range(46, 51))
def test_semantic_answers_all_wrong_options_and_no_forced_math(sequence):
    lesson = load_batch("grade8_batch10")["lessons"][sequence - 46]
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
                grade_answer(q["grading_spec"], {"order": ["s3", "s2", "s1"]})
                != "correct"
            )
    if sequence >= 47:
        assert not lesson["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in lesson["assessments"]
        )


def test_vacuum_independent_oracles_and_every_formula_alternative():
    doc = load_batch("grade8_batch10")
    assert validate_batch(doc) == {
        "lessons": 5,
        "cards": 21,
        "formulas": 3,
        "worked_examples": 5,
        "assessments": 31,
        "frq": 3,
    }
    lesson = doc["lessons"][0]
    count = 0
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
            grade_answer(spec, {**answer, "value": "123456789"}) == "out_of_tolerance"
        )
        assert grade_answer(spec, {**answer, "formula": "1"}) == "wrong_formula"
    assert count == 3


@pytest.mark.parametrize(
    "qi,gi,bad",
    [
        (4, 0, "2.5"),
        (4, 1, "1.7e-19"),
        (4, 2, "0"),
        (5, 0, "0.0000000000000000001"),
        (6, 1, "0"),
        (6, 0, "0.0000000000000000001"),
    ],
)
def test_vacuum_integer_counts_constants_and_denominators(qi, gi, bad):
    q = deepcopy(load_batch("grade8_batch10")["lessons"][0]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_next_earth_field_heading_not_used_as_previous_section_teaching():
    lesson = load_batch("grade8_batch10")["lessons"][-1]
    assert all(
        145 not in ref["pdf_pages"]
        for fact in lesson["facts"].values()
        for ref in fact["source_refs"]
    )
