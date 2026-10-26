"""Reviewed current-density, source topology and conditional meter/lab oracles."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import NUMERIC_ORACLES, new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

LABELS = {
    36: [
        "Kesimdan t ichida o‘tgan zaryad moduli",
        "Tok yo‘nalishiga tik ko‘ndalang kesim",
        "Qarama-qarshi",
        "pi*D²/4",
    ],
    37: [
        "V",
        "Tashqi R va ichki r yig‘indisi",
        "Emf ga",
        "Tashqi rezistordagi energiyani",
    ],
    38: [
        "n*r",
        "Emf",
        "Haqiqiy yo‘nalish tanlovga qarshi bo‘lishi mumkin",
        "Kiruvchi va chiquvchi toklarning algebraik yig‘indisi",
    ],
    39: ["Parallel", "Ketma-ket", "m−1ga", "Yo‘q, bu faqat raqamli model"],
    40: [
        "Real asbob bilan o‘lchov bajarilganini",
        "Ichki qarshilikdagi kuchlanish pasayishi",
        "Voltmeter yuklamasi e’tiborsizligi",
        "Uload+I*rni olish",
    ],
}
ORDERS = {
    36: ["s2", "s3", "s1", "s4"],
    37: ["s2", "s3", "s1"],
    38: ["s2", "s1", "s3"],
    39: ["s2", "s1", "s3"],
    40: ["s3", "s1", "s2"],
}


def question(seq, n):
    return deepcopy(
        load_batch("grade10_batch8")["lessons"][seq - 36]["assessments"][n - 1]
    )


@pytest.mark.parametrize("seq", range(36, 41))
def test_independent_meaning_and_order(seq):
    l = load_batch("grade10_batch8")["lessons"][seq - 36]
    qs = [q for q in l["assessments"] if q["response_kind"] == "concept_selection"]
    assert len(qs) == len(LABELS[seq]) == 4
    for q, label in zip(qs, LABELS[seq]):
        assert label in [o["label"] for o in q["public"]["options"]]
        for o in q["public"]["options"]:
            assert grade_answer(q["grading_spec"], {"choice_id": o["id"]}) == (
                "correct" if o["label"] == label else "incorrect_concept"
            )
    q = next(q for q in l["assessments"] if q["response_kind"] == "ordering")
    assert grade_answer(q["grading_spec"], {"order": ORDERS[seq]}) == "correct"
    assert grade_answer(q["grading_spec"], {"order": ORDERS[seq][::-1]}) != "correct"


@pytest.mark.parametrize(
    "identity", [k for k in NUMERIC_ORACLES if k[0] == 10 and 36 <= k[1] <= 40]
)
def test_literal_numeric_oracles_units_and_closed_formula_variants(identity):
    _, seq, n = identity
    l = load_batch("grade10_batch8")["lessons"][seq - 36]
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
    "seq,n,gi,v,u",
    [
        (36, 6, 1, "0", "s"),
        (36, 7, 1, "0", "mm2"),
        (36, 7, 0, "-3", "A"),
        (36, 8, 1, "1.5e-19", "C"),
        (36, 8, 0, "0", "1/m3"),
        (36, 9, 2, "0", "mm"),
        (36, 9, 1, "3.14159", "1"),
        (37, 7, 0, "0", "V"),
        (37, 7, 1, "0", "Ω"),
        (37, 7, 2, "-1", "Ω"),
        (37, 8, 0, "9", "N"),
        (37, 9, 0, "0", "Ω"),
        (38, 6, 0, "1.5", "1"),
        (38, 6, 0, "300", "%"),
        (38, 7, 0, "0", "1"),
        (38, 7, 3, "-1", "Ω"),
        (38, 8, 1, "0", "Ω"),
        (38, 9, 2, "-2", "V"),
        (39, 6, 1, "1", "1"),
        (39, 7, 1, "0.5", "1"),
        (39, 6, 0, "0", "Ω"),
        (39, 8, 2, "0", "Ω"),
        (39, 9, 0, "0", "mA"),
        (39, 9, 2, "-1", "Ω"),
        (40, 6, 1, "6", "V"),
        (40, 6, 1, "7", "V"),
        (40, 6, 2, "0", "mA"),
        (40, 7, 2, "-1", "Ω"),
    ],
)
def test_source_count_range_and_unit_model_domains(seq, n, gi, v, u):
    q = question(seq, n)
    q["public"]["givens"][gi].update(value=v, unit=u)
    with pytest.raises(ValueError):
        calculation_value(q)


def test_unloaded_unequal_sources_signed_current_and_kelvin_style_weighting():
    assert calculation_value(question(38, 8)) == Fraction(8, 3)
    assert calculation_value(question(38, 9)) == Fraction(-1, 2)
    q = question(38, 9)
    q["public"]["givens"][0]["value"] = "2"
    assert calculation_value(q) == 0
    q["public"]["givens"][0]["value"] = "1"
    assert calculation_value(q) == Fraction(1, 2)
    q = question(38, 8)
    s = q["grading_spec"]
    a = {"formula": "(E1*r2+E2*r1)/(r1+r2)", "value": "2.67", "unit": "V"}
    assert grade_answer(s, a) == "correct"
    assert grade_answer(s, {**a, "value": "2.66"}) == "out_of_tolerance"
    assert grade_answer(s, {**a, "value": "2.671"}) == "rounding_requirement"


def test_one_cell_series_parallel_equivalence_and_ideal_internal_resistance():
    q = question(38, 6)
    q["public"]["givens"][0]["value"] = "1"
    a = calculation_value(q)
    p = question(38, 7)
    p["public"]["givens"] = [
        {"symbol": "n", "value": "1", "unit": "1"},
        {"symbol": "Emf", "value": "2", "unit": "V"},
        {"symbol": "R", "value": "9", "unit": "Ω"},
        {"symbol": "r", "value": "1", "unit": "Ω"},
    ]
    assert a == calculation_value(p) == Fraction(1, 5)
    q = question(37, 9)
    q["public"]["givens"][1]["value"] = "0"
    assert calculation_value(q) == 1
    q = question(37, 7)
    q["public"]["givens"][2]["value"] = "0"
    assert calculation_value(q) == Fraction(3, 5)


def test_shunt_branch_vs_total_ratio_and_fractional_range_multiplier():
    assert calculation_value(question(39, 6)) == 25
    assert calculation_value(question(39, 8)) == Fraction(5, 1000)
    # Ig1mA and shunt4mA give TOTAL5mA, not6mA.
    assert Fraction(1, 1000) + Fraction(1, 1000) * 100 / 25 == Fraction(5, 1000)
    q = question(39, 6)
    q["public"]["givens"][1]["value"] = "1.5"
    assert calculation_value(q) == 200  # range multiplier is not an integer cell count
    assert calculation_value(question(39, 7)) == 1800
    assert calculation_value(question(39, 9)) == 2


def test_perpendicular_area_conversion_and_digital_lab_are_honest():
    assert calculation_value(question(36, 7)) == 2_000_000
    assert calculation_value(question(36, 8)) == 1_600_000
    assert calculation_value(question(36, 9)) == 2_000_000
    assert calculation_value(question(40, 6)) == 2
    assert calculation_value(question(40, 7)) == 5
    l = load_batch("grade10_batch8")["lessons"][4]
    assert not l["review"]["physical_experiment_completed"]
    assert (
        l["review"]["physical_measurements"]
        == "not_claimed_conditional_digital_data_only"
    )


def test_five_source_sections_counts_and_reference_offset():
    d = load_batch("grade10_batch8")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 25,
        "formulas": 18,
        "worked_examples": 5,
        "assessments": 43,
        "frq": 18,
    }
    for l in d["lessons"]:
        for r in l["source_refs"]:
            assert r["printed_pages"] == [p - 1 for p in r["pdf_pages"]]
