"""Source-checked grating lab, dispersion, Malus and photometry."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import NUMERIC_ORACLES, new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

LABELS = {
    26: [
        "Yo‘q, x ekrangacha, y markazdan maksimumgacha",
        "Kichik y/x yaqinlashuvida",
        "610nm",
        "Yo‘q",
    ],
    27: [
        "n ning chastotaga bog‘liqligi",
        "Yo‘q, bir nechta chiziq bo‘lishi mumkin",
        "Yutilish chiziqlari",
        "Bir xil",
    ],
    28: [
        "Tebranish yo‘nalishini",
        "Nol o‘tish",
        "Analizator oldidagi chiziqli qutblangan nur",
        "Yo‘q, kvadrat0,25",
    ],
    29: [
        "Infraqizil",
        "Atmosferada yutilish",
        "Rentgen hosil qilishda",
        "Yutilishdagi farqdan",
        "Yo‘q",
    ],
    30: [
        "lm",
        "Sfera sirtining bo‘lagi",
        "Shu yuzaga tushgan yorug‘lik oqimi",
        "Yarmi",
    ],
}
ORDERS = {
    26: ["s3", "s1", "s4", "s2"],
    27: ["s2", "s1", "s3"],
    28: ["s2", "s1", "s3"],
    29: ["s2", "s1", "s3"],
    30: ["s2", "s1", "s3"],
}


def question(seq, n):
    return deepcopy(
        load_batch("grade11_batch6")["lessons"][seq - 26]["assessments"][n - 1]
    )


@pytest.mark.parametrize("seq", range(26, 31))
def test_independent_source_meaning_order_and_digital_activity(seq):
    l = load_batch("grade11_batch6")["lessons"][seq - 26]
    qs = [q for q in l["assessments"] if q["response_kind"] == "concept_selection"]
    assert len(qs) == len(LABELS[seq])
    for q, label in zip(qs, LABELS[seq]):
        assert label in [o["label"] for o in q["public"]["options"]]
        for o in q["public"]["options"]:
            assert grade_answer(q["grading_spec"], {"choice_id": o["id"]}) == (
                "correct" if o["label"] == label else "incorrect_concept"
            )
    q = next(q for q in l["assessments"] if q["response_kind"] == "ordering")
    assert grade_answer(q["grading_spec"], {"order": ORDERS[seq]}) == "correct"
    assert grade_answer(q["grading_spec"], {"order": ORDERS[seq][::-1]}) != "correct"
    if seq == 29:
        assert not l["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in l["assessments"]
        )


@pytest.mark.parametrize(
    "identity", [k for k in NUMERIC_ORACLES if k[0] == 11 and 26 <= k[1] <= 30]
)
def test_independent_literal_answers_closed_formulas_and_units(identity):
    _, seq, n = identity
    l = load_batch("grade11_batch6")["lessons"][seq - 26]
    q = l["assessments"][n - 1]
    s = q["grading_spec"]
    a = new_answer(l, q)
    assert grade_answer(s, a) == "correct"
    for f in s["formula"]["equivalents"]:
        assert grade_answer(s, {**a, "formula": f}) == "correct"
    assert grade_answer(s, {**a, "unit": "kg"}) == "dimension_mismatch"
    assert grade_answer(s, {**a, "formula": "__import__(x)"}) != "correct"
    assert grade_answer(s, {**a, "value": "999990"}) == "out_of_tolerance"


@pytest.mark.parametrize(
    "seq,n,symbol,value,unit",
    [
        (26, 6, "y", "51", "mm"),
        (26, 6, "n", "0", "1"),
        (26, 6, "n", "1.5", "1"),
        (26, 6, "x", "0", "m"),
        (27, 6, "v", "300000001", "m/s"),
        (27, 7, "n", "1", "1"),
        (28, 6, "cosA", "1.01", "1"),
        (28, 7, "cosA", "-1.01", "1"),
        (30, 6, "R", "0", "m"),
        (30, 7, "Omega", "0", "sr"),
        (30, 7, "Phi", "18", "W"),
        (30, 9, "S", "0", "m2"),
        (30, 10, "cosA", "-0.1", "1"),
        (30, 10, "cosA", "1.1", "1"),
        (30, 10, "r", "0", "m"),
    ],
)
def test_source_geometry_units_and_domains(seq, n, symbol, value, unit):
    q = question(seq, n)
    next(g for g in q["public"]["givens"] if g["symbol"] == symbol).update(
        value=value, unit=unit
    )
    with pytest.raises(ValueError):
        calculation_value(q)


def test_malus_signed_cosine_and_zero_orthogonal_limit():
    assert calculation_value(question(28, 7)) == Fraction(36, 100)
    q = question(28, 6)
    next(g for g in q["public"]["givens"] if g["symbol"] == "cosA")["value"] = "0"
    assert calculation_value(q) == 0
    q["public"]["givens"][1]["value"] = "-1"
    assert calculation_value(q) == 8


def test_photometry_distance_normal_and_no_radiometric_unit_confusion():
    q = question(30, 10)
    assert calculation_value(q) == 10
    next(g for g in q["public"]["givens"] if g["symbol"] == "r")["value"] = "4"
    assert calculation_value(q) == Fraction(5, 2)
    next(g for g in q["public"]["givens"] if g["symbol"] == "cosA")["value"] = "0"
    assert calculation_value(q) == 0
    assert calculation_value(question(30, 6)) == 2
    assert calculation_value(question(30, 9)) == 30


def test_original_digital_mean_deviation_and_honest_coverage():
    d = load_batch("grade11_batch6")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 24,
        "formulas": 10,
        "worked_examples": 5,
        "assessments": 37,
        "frq": 11,
    }
    assert not d["lessons"][3]["formulas"]
    assert (600 + 620) / 2 == 610
    assert abs(600 - 610) == abs(620 - 610) == 10
    for l in d["lessons"]:
        assert l["review"]["independent_subject_expert"] == "not_claimed"
        assert not l["review"]["physical_experiment_completed"]
        for r in l["source_refs"]:
            assert r["printed_pages"] == [p - 1 for p in r["pdf_pages"]]
