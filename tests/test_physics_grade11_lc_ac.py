"""Independent idealLC, phase conventions and sinusoidal RMS/idealC checks."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import NUMERIC_ORACLES, new_answer

from services.assessment_grading import PositiveSquareRoot, grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

LABELS = {
    11: ["Nol", "Saqlanadi", "Ortadi", "Manfiy emas"],
    12: ["−Imsin(theta)", "Bir xil", "|I|ortsa ortishi mumkin", "Issiqlikka"],
    13: [
        "Energiyaning yo‘qotishlarini",
        "Elektron kalit/boshqarish",
        "Teskari bog‘lanish",
        "Yo‘q, manba sarflangan energiyani beradi",
        "Mumkin emas, bosqich va bog‘lanish konvensiyasi bor",
    ],
    14: [
        "Bir xil",
        "Yo‘q, issiqlik bo‘yicha tenglashtiriladi",
        "Manfiy emas",
        "Ikkalasi amplituda",
    ],
    15: [
        "Yo‘q, o‘tkinchi tok bo‘lishi mumkin",
        "90°oldinda",
        "Kamayadi",
        "rad/s va Hz",
    ],
}
ORDERS = {
    11: ["s1", "s2", "s3"],
    12: ["s2", "s1", "s3"],
    13: ["s2", "s3", "s1"],
    14: ["s2", "s3", "s1"],
    15: ["s2", "s1", "s3"],
}


def question(seq, n):
    return deepcopy(
        load_batch("grade11_batch3")["lessons"][seq - 11]["assessments"][n - 1]
    )


@pytest.mark.parametrize("seq", range(11, 16))
def test_independent_concepts_order_and_no_fake_generator_formula(seq):
    l = load_batch("grade11_batch3")["lessons"][seq - 11]
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
    if seq == 13:
        assert not l["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in l["assessments"]
        )


@pytest.mark.parametrize(
    "identity", [k for k in NUMERIC_ORACLES if k[0] == 11 and 11 <= k[1] <= 15]
)
def test_independent_literals_alternatives_units_and_wrong_answers(identity):
    _, seq, n = identity
    l = load_batch("grade11_batch3")["lessons"][seq - 11]
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
        (11, 6, 0, "3.14159", "1"),
        (11, 6, 1, "0", "H"),
        (11, 7, 2, "0", "µF"),
        (11, 8, 1, "-1", "µF"),
        (11, 9, 0, "-4", "V"),
        (12, 6, 1, "-1.1", "1"),
        (12, 6, 0, "-6", "µC"),
        (12, 7, 1, "1.1", "1"),
        (12, 8, 1, "1.1", "1"),
        (12, 8, 0, "0", "mA"),
        (14, 6, 1, "0", "Ω"),
        (14, 7, 0, "-10", "V"),
        (14, 8, 0, "200", "V"),
        (14, 9, 0, "10", "A"),
        (14, 10, 2, "-1.1", "1"),
        (15, 6, 0, "1000", "Hz"),
        (15, 6, 1, "0", "µF"),
        (15, 7, 0, "3.14159", "1"),
        (15, 7, 1, "0", "Hz"),
        (15, 8, 2, "0", "µF"),
        (15, 8, 1, "0", "rad/s"),
        (15, 9, 1, "-1.1", "1"),
    ],
)
def test_model_dimensions_and_zero_domains(seq, n, gi, v, u):
    q = question(seq, n)
    q["public"]["givens"][gi].update(value=v, unit=u)
    with pytest.raises(ValueError):
        calculation_value(q)


def test_ideal_lc_conserves_sum_and_keeps_exact_reciprocal_frequency():
    assert calculation_value(question(11, 6)) == Fraction(157, 125000)
    assert calculation_value(question(11, 7)) == Fraction(125000, 157)
    assert calculation_value(question(11, 8)) == Fraction(1, 100000)
    assert calculation_value(question(11, 9)) == Fraction(1, 50)
    q = question(11, 8)
    q["public"]["givens"][0]["value"] = "4"
    q["public"]["givens"][3]["value"] = "-10"
    assert calculation_value(q) == Fraction(1, 100000)


def test_charge_derivative_and_ideal_cap_current_use_same_signed_convention():
    assert calculation_value(question(12, 6)) == Fraction(-36, 10**7)
    assert calculation_value(question(12, 7)) == -3
    assert calculation_value(question(12, 8)) == Fraction(-16, 1000)
    assert calculation_value(question(15, 9)) == Fraction(4, 100)
    q = question(12, 8)
    q["public"]["givens"][1]["value"] = "0"
    assert calculation_value(q) == 0
    q["public"]["givens"][1]["value"] = "-1"
    assert calculation_value(q) == Fraction(2, 100)


def test_rms_exact_root_truth_rounding_and_not_peak_or_signed_mean():
    assert calculation_value(question(14, 7)) == PositiveSquareRoot(Fraction(50))
    assert calculation_value(question(14, 8)) == PositiveSquareRoot(Fraction(1, 50))
    s = question(14, 7)["grading_spec"]
    a = {"formula": "Um/sqrt(2)", "value": "7.07", "unit": "V"}
    assert grade_answer(s, a) == "correct"
    assert grade_answer(s, {**a, "value": "7.08"}) == "out_of_tolerance"
    assert grade_answer(s, {**a, "value": "7.071"}) == "rounding_requirement"
    assert grade_answer(s, {**a, "value": "10"}) == "out_of_tolerance"
    s = question(14, 8)["grading_spec"]
    a = {"formula": "Im/sqrt(2)", "value": "141", "unit": "mA"}
    assert grade_answer(s, a) == "correct"
    assert grade_answer(s, {**a, "value": "142"}) == "out_of_tolerance"


def test_pure_resistor_power_and_reactive_capacitance_are_distinct():
    assert calculation_value(question(14, 9)) == 1
    assert calculation_value(question(14, 10)) == Fraction(72, 100)
    q = question(14, 10)
    q["public"]["givens"][2]["value"] = "0.6"
    assert calculation_value(q) == Fraction(72, 100)
    assert calculation_value(question(15, 6)) == 100
    assert calculation_value(question(15, 7)) == Fraction(25000, 157)
    assert calculation_value(question(15, 8)) == Fraction(5, 100)


def test_honest_source_counts_and_offset():
    d = load_batch("grade11_batch3")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 25,
        "formulas": 16,
        "worked_examples": 5,
        "assessments": 42,
        "frq": 16,
    }
    for l in d["lessons"]:
        assert l["review"]["independent_subject_expert"] == "not_claimed"
        assert not l["review"]["physical_experiment_completed"]
        for r in l["source_refs"]:
            assert r["printed_pages"] == [p - 1 for p in r["pdf_pages"]]
