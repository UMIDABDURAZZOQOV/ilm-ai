"""Source-correct relative mass, molar units, number density and ideal-gas RMS."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import new_answer

from services.assessment_grading import UNITS, grade_answer
from services.physics_curriculum import (
    calculation_value,
    load_batch,
    public_book,
    validate_batch,
)

KEYS = {
    1: [
        "Zarralar,ularning tartibsiz harakati va o‘zaro ta’siri",
        "To‘qnashuvlar yo‘nalishni ko‘p o‘zgartiradi",
        "Atrofdagi molekulalarning tartibsiz zarbalari",
        "Harakatni tasavvur qiluvchi mexanik model",
        "Tartibsiz siljishlarga",
    ],
    2: ["2H va1O", "O‘lchamsiz", "Bir tekis bir molekulyar qatlam"],
    3: ["mol", "M kg/mol,Mr o‘lchamsiz", "1/m3"],
    4: ["Kesim yuzasi va uzunlik ko‘paytmasi", "Asossiz yana2ga ko‘paytirish", "D/k"],
    5: [
        "Zarralar o‘lchami va to‘qnashuvlar orasidagi ta’sirni",
        "Molekulalar devorga urilib impuls almashadi",
        "Bitta molekulaning o‘rtacha ilgarilanma kinetik energiyasi",
    ],
}


@pytest.mark.parametrize("seq", range(1, 6))
def test_semantic_labels_all_distractors_order_and_conceptual_only_mkn(seq):
    l = load_batch("grade9_batch1")["lessons"][seq - 1]
    qs = [q for q in l["assessments"] if q["response_kind"] == "concept_selection"]
    assert len(qs) == len(KEYS[seq])
    for q, label in zip(qs, KEYS[seq]):
        assert label in [o["label"] for o in q["public"]["options"]]
        for opt in q["public"]["options"]:
            assert grade_answer(q["grading_spec"], {"choice_id": opt["id"]}) == (
                "correct" if opt["label"] == label else "incorrect_concept"
            )
    for q in l["assessments"]:
        if q["response_kind"] == "ordering":
            assert (
                grade_answer(q["grading_spec"], {"order": ["s2", "s3", "s1"]})
                == "correct"
            )
            assert (
                grade_answer(q["grading_spec"], {"order": ["s1", "s2", "s3"]})
                != "correct"
            )
    if seq == 1:
        assert not l["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in l["assessments"]
        )


def test_all_literal_numeric_oracles_formulas_and_error_feedback():
    d = load_batch("grade9_batch1")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 24,
        "formulas": 24,
        "worked_examples": 6,
        "assessments": 46,
        "frq": 24,
    }
    count = 0
    for l in d["lessons"]:
        for q in l["assessments"]:
            s = q["grading_spec"]
            if s["kind"] != "numeric_quantity":
                continue
            count += 1
            a = new_answer(l, q)
            for f in s["formula"]["equivalents"]:
                assert grade_answer(s, {**a, "formula": f}) == "correct", (
                    q["key"],
                    a,
                    f,
                )
            wrongunit = "kg" if s["dimension"] != "mass" else "m"
            assert grade_answer(s, {**a, "unit": wrongunit}) == "dimension_mismatch"
            assert grade_answer(s, {**a, "value": "999999"}) == "out_of_tolerance"
            assert grade_answer(s, {**a, "formula": "1"}) == "wrong_formula"
    assert count == 24


@pytest.mark.parametrize(
    "seq,qi,gi,bad",
    [
        (2, 4, 1, "0"),
        (2, 5, 1, "1.7e-27"),
        (2, 6, 0, "0"),
        (2, 7, 1, "0"),
        (2, 7, 0, "1e-27"),
        (3, 4, 1, "6.5e23"),
        (3, 5, 0, "1.5"),
        (3, 6, 1, "0"),
        (3, 7, 1, "0"),
        (3, 10, 1, "0"),
        (4, 4, 3, "0"),
        (4, 5, 3, "0"),
        (4, 6, 4, "0"),
        (4, 7, 3, "0"),
        (4, 8, 1, "0"),
        (5, 4, 0, "0"),
        (5, 5, 1, "0"),
        (5, 5, 0, "0.4"),
        (5, 8, 1, "0"),
        (5, 9, 1, "0"),
    ],
)
def test_constant_integer_positive_denominator_and_rational_root_domains(
    seq, qi, gi, bad
):
    q = deepcopy(load_batch("grade9_batch1")["lessons"][seq - 1]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_mass_ratio_not_mass_molar_amount_not_number_density():
    d = load_batch("grade9_batch1")
    ratio = d["lessons"][1]["assessments"][5]["grading_spec"]
    assert (
        grade_answer(ratio, {"formula": "m0/u", "value": "24", "unit": "1"})
        == "correct"
    )
    assert (
        grade_answer(ratio, {"formula": "m0/u", "value": "24", "unit": "kg"})
        == "dimension_mismatch"
    )
    amount = d["lessons"][2]["assessments"][6]["grading_spec"]
    assert (
        grade_answer(amount, {"formula": "m/M", "value": "2", "unit": "mol"})
        == "correct"
    )
    assert (
        grade_answer(amount, {"formula": "m/M", "value": "2", "unit": "1"})
        == "dimension_mismatch"
    )
    concentration = d["lessons"][2]["assessments"][10]["grading_spec"]
    assert (
        grade_answer(
            concentration, {"formula": "N/V", "value": "6.022e26", "unit": "m⁻³"}
        )
        == "correct"
    )
    assert (
        grade_answer(
            concentration, {"formula": "N/V", "value": "6.022e26", "unit": "mol"}
        )
        == "dimension_mismatch"
    )
    assert UNITS["mm3"] == ("volume", Fraction(1, 10**9))
    assert UNITS["1/mol"][0] == "avogadro_constant"


def test_rms_root_optin_and_arithmetic_mean_not_accepted():
    q = load_batch("grade9_batch1")["lessons"][4]["assessments"][5]
    s = q["grading_spec"]
    assert (
        grade_answer(s, {"formula": "sqrt(3*p/rho)", "value": "600", "unit": "m/s"})
        == "correct"
    )
    assert (
        grade_answer(s, {"formula": "3*p/rho", "value": "360000", "unit": "m/s"})
        == "wrong_formula"
    )
    assert (
        grade_answer(s, {"formula": "(3*p/rho)^0.5", "value": "0.6", "unit": "km/s"})
        == "correct"
    )
    legacy = load_batch("grade9_batch1")["lessons"][4]["assessments"][4]["grading_spec"]
    assert "allow_square_root" not in legacy["formula"]
    assert (
        grade_answer(
            legacy, {"formula": "sqrt(rho*v^2/3)", "value": "100000", "unit": "Pa"}
        )
        == "invalid_expression"
    )


def test_grade9_public_bibliography_and_local_preview_scope():
    book = public_book(9)
    assert book["grade"] == 9 and book["year"] == 2019
    assert book["id"] == "physics-uz-grade-9"
    assert "Habibullayev" in str(book["authors"])
    d = load_batch("grade9_batch1")
    assert d["publication"] == "local_test_preview_only" and not d["ai_explain"]
    assert all(
        l["review"]["physical_experiment_completed"] is False for l in d["lessons"]
    )
