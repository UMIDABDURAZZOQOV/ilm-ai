"""Source-checked illuminance, relativity and quantum foundations."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import NUMERIC_ORACLES, new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

LABELS = {
    31: [
        "Iv2dan kichik",
        "Ikki marta ortadi",
        "To‘rt marta kamayadi",
        "Yoritilganlikni",
    ],
    32: [
        "Bir xil",
        "Bir soat o‘z joyida qayd etgan interval",
        "Harakatga parallel uchlar bir vaqtda qaydiga",
        "c",
    ],
    33: ["O‘zgarmaydi", "E−E0", "Yo‘q, bu kichik tezlik yaqinlashuvi", "Ha, E=pc"],
    34: ["K", "Ikki marta kamayadi", "Bitta kvant energiyasi", "J*s"],
    35: [
        "Tashqi elektron chiqmaydi",
        "Elektronlar soni va to‘yinish tokini",
        "Elektron zaryadining musbat moduli",
        "0",
    ],
}
ORDERS = {
    31: ["s3", "s1", "s4", "s2"],
    32: ["s2", "s1", "s3"],
    33: ["s2", "s1", "s3"],
    34: ["s2", "s1", "s3"],
    35: ["s3", "s1", "s4", "s2"],
}


def question(seq, n):
    return deepcopy(
        load_batch("grade11_batch7")["lessons"][seq - 31]["assessments"][n - 1]
    )


@pytest.mark.parametrize("seq", range(31, 36))
def test_independent_source_meaning_order_and_digital_activity(seq):
    l = load_batch("grade11_batch7")["lessons"][seq - 31]
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


@pytest.mark.parametrize(
    "identity", [k for k in NUMERIC_ORACLES if k[0] == 11 and 31 <= k[1] <= 35]
)
def test_independent_literal_answers_closed_formulas_and_units(identity):
    _, seq, n = identity
    l = load_batch("grade11_batch7")["lessons"][seq - 31]
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
        (31, 6, "r1", "0", "m"),
        (31, 6, "r2", "-3", "m"),
        (32, 6, "v", "300000000", "m/s"),
        (32, 7, "v", "-300000000", "m/s"),
        (32, 8, "u", "300000001", "m/s"),
        (32, 9, "c", "299000000", "m/s"),
        (33, 6, "m0", "0", "kg"),
        (33, 7, "v", "-1", "m/s"),
        (33, 8, "v", "100000000", "m/s"),
        (34, 6, "T", "0", "K"),
        (34, 7, "Lpeak", "0", "nm"),
        (34, 8, "h", "6.626e-34", "J"),
        (34, 9, "h", "6.63e-34", "J*s"),
        (35, 6, "nu", "1e14", "Hz"),
        (35, 6, "A", "-1", "J"),
        (35, 7, "A", "0", "J"),
        (35, 8, "e", "-1.6e-19", "C"),
    ],
)
def test_models_reject_invalid_givens(seq, n, symbol, value, unit):
    q = question(seq, n)
    next(g for g in q["public"]["givens"] if g["symbol"] == symbol).update(
        value=value, unit=unit
    )
    with pytest.raises(ValueError):
        calculation_value(q)


def test_corrected_equal_illuminance_ratio_not_textbook_inverse():
    assert calculation_value(question(31, 6)) == 40
    assert Fraction(40, 2**2) == Fraction(90, 3**2)


def test_signed_collinear_light_limit_and_rounded_ratio():
    q = question(32, 8)
    q["public"]["givens"][0]["value"] = "300000000"
    assert calculation_value(q) == 300000000
    q = question(32, 9)
    q["public"]["givens"][0]["value"] = "-240000000"
    assert calculation_value(q) == Fraction(-1500000000, 13)
    q = question(32, 8)
    s = q["grading_spec"]
    a = new_answer(load_batch("grade11_batch7")["lessons"][1], q)
    assert grade_answer(s, {**a, "value": "264705883"}) == "out_of_tolerance"
    assert grade_answer(s, {**a, "value": "264705882.35"}) == "rounding_requirement"


def test_proper_time_and_parallel_length_exact_roots():
    assert calculation_value(question(32, 6)) == Fraction(75, 10**10)
    assert calculation_value(question(32, 7)) == Fraction(6, 5)
    q = question(32, 6)
    q["public"]["givens"][1]["value"] = "0"
    assert calculation_value(q) == Fraction(6, 10**9)


def test_rest_total_kinetic_and_momentum_independent_identity():
    e0 = Fraction(18, 10**11)
    e = Fraction(225, 10**12)
    k = Fraction(45, 10**12)
    mom = Fraction(45, 10**20)
    assert calculation_value(question(33, 6)) == e0
    assert calculation_value(question(33, 7)) == e
    assert calculation_value(question(33, 8)) == k == e - e0
    assert calculation_value(question(33, 9)) == mom
    assert e**2 == e0**2 + (mom * 300000000) ** 2


def test_threshold_equality_is_zero_not_negative_kinetic_emission():
    q = question(35, 6)
    q["public"]["givens"][2]["value"] = "6.626e-19"
    assert calculation_value(q) == 0
    assert calculation_value(question(34, 6)) == Fraction(69, 10**8)
    assert calculation_value(question(34, 7)) == 3000
    assert calculation_value(question(35, 8)) == 2


def test_honest_source_counts():
    d = load_batch("grade11_batch7")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 23,
        "formulas": 15,
        "worked_examples": 5,
        "assessments": 41,
        "frq": 16,
    }
    for l in d["lessons"]:
        assert l["review"]["independent_subject_expert"] == "not_claimed"
        assert not l["review"]["physical_experiment_completed"]
        for r in l["source_refs"]:
            assert r["printed_pages"] == [p - 1 for p in r["pdf_pages"]]
