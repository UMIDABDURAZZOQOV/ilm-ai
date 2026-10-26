"""Source-corrected series RLC, digital voltage sweep and RMS power tests."""

from copy import deepcopy
from decimal import Decimal, localcontext
from fractions import Fraction

import pytest
from test_physics_course import NUMERIC_ORACLES, new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

LABELS = {
    16: [
        "−Um*sin(theta)",
        "90°oldinda",
        "Ortadi",
        "Noto‘g‘ri, ideal Lenergiya saqlab/qaytaradi",
    ],
    17: [
        "Barcha elementlardan bir xil tok o‘tadi",
        "Yo‘q, fazorlar hisobga olinadi",
        "Ha, bu tangens nisbati",
        "Aktiv Rda",
    ],
    18: [
        "XL=XC",
        "Aktiv Rga",
        "Ular qarama-qarshi fazali reaktiv qismlar",
        "Yo‘q, tenglik va cho‘qqi yaqqolligi boshqa masala",
    ],
    19: [
        "100Hz",
        "UC",
        "UL",
        "Yo‘q, yuqori tomondan uzoqlashtiradi",
        "Yo‘q, bu hisobiy raqamli ma’lumot",
    ],
    20: [
        "RMSqiymatlar",
        "0dan1gacha",
        "Yo‘q, energiya davriy saqlanib qaytishi mumkin",
        "Yo‘q, davr bo‘yicha/barqaror o‘rtacha shartini tekshir",
    ],
}
ORDERS = {
    16: ["s2", "s1", "s3"],
    17: ["s2", "s3", "s1", "s4"],
    18: ["s2", "s1", "s3"],
    19: ["s2", "s3", "s4", "s1"],
    20: ["s2", "s1", "s3", "s4"],
}


def question(seq, n):
    return deepcopy(
        load_batch("grade11_batch4")["lessons"][seq - 16]["assessments"][n - 1]
    )


@pytest.mark.parametrize("seq", range(16, 21))
def test_independent_source_meaning_order_and_digital_activity(seq):
    l = load_batch("grade11_batch4")["lessons"][seq - 16]
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
    if seq == 19:
        assert not l["formulas"]
        assert (
            l["review"]["physical_measurements"]
            == "not_claimed_conditional_digital_data_only"
        )
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in l["assessments"]
        )


@pytest.mark.parametrize(
    "identity", [k for k in NUMERIC_ORACLES if k[0] == 11 and 16 <= k[1] <= 20]
)
def test_independent_literal_answers_closed_formulas_and_units(identity):
    _, seq, n = identity
    l = load_batch("grade11_batch4")["lessons"][seq - 16]
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
        (16, 6, 0, "1000", "Hz"),
        (16, 6, 1, "0", "mH"),
        (16, 7, 0, "3.14159", "1"),
        (16, 8, 1, "0", "rad/s"),
        (16, 9, 1, "-1.1", "1"),
        (17, 6, 0, "0", "Ω"),
        (17, 6, 1, "-1", "Ω"),
        (17, 7, 0, "-10", "V"),
        (17, 8, 2, "0", "Ω"),
        (17, 9, 1, "-10", "V"),
        (18, 6, 0, "0", "mH"),
        (18, 6, 1, "0", "µF"),
        (18, 7, 0, "3.14159", "1"),
        (18, 7, 1, "0", "Hz"),
        (18, 8, 1, "0", "Ω"),
        (18, 9, 1, "0", "Ω"),
        (18, 9, 3, "0", "µF"),
        (20, 6, 2, "1.1", "1"),
        (20, 6, 2, "-0.1", "1"),
        (20, 7, 3, "-5", "min"),
        (20, 8, 0, "60", "Ω"),
        (20, 8, 1, "0", "Ω"),
        (20, 9, 0, "7", "W"),
        (20, 9, 1, "0", "V"),
        (20, 9, 2, "0", "A"),
    ],
)
def test_source_model_domain_checks(seq, n, gi, v, u):
    q = question(seq, n)
    q["public"]["givens"][gi].update(value=v, unit=u)
    with pytest.raises(ValueError):
        calculation_value(q)


def test_inductor_derivative_voltage_and_tangent_may_exceed_one():
    assert calculation_value(question(16, 9)) == 3
    q = question(16, 9)
    q["public"]["givens"][1]["value"] = "0.6"
    assert calculation_value(q) == -3
    assert calculation_value(question(17, 8)) == Fraction(4, 3)
    q = question(17, 8)
    q["public"]["givens"][0]["value"] = "10"
    q["public"]["givens"][1]["value"] = "50"
    assert calculation_value(q) == Fraction(-4, 3)


def test_series_norm_current_resonance_and_internal_voltage_are_independent():
    assert calculation_value(question(17, 6)) == 50
    assert calculation_value(question(17, 7)) == Fraction(1, 5)
    assert calculation_value(question(17, 9)) == 10
    assert calculation_value(question(18, 6)) == 5000
    assert calculation_value(question(18, 7)) == Fraction(5, 49298)
    assert calculation_value(question(18, 8)) == Fraction(25, 1000)
    assert calculation_value(question(18, 9)) == 5
    q = question(17, 6)
    q["public"]["givens"][2]["value"] = "50"
    assert calculation_value(q) == 30  # XL=XC still has positive R


def test_digital_voltage_sweep_matches_independent_ideal_model():
    # Independent high precision reference, not production calculation or keys.
    with localcontext() as ctx:
        ctx.prec = 45
        p = Decimal("3.14")
        L = Decimal(1)
        R = Decimal(100)
        C = 1 / (4 * p * p * 100**2)
        rows = []
        for f in [50, 100, 150]:
            omega = 2 * p * f
            xl = omega * L
            xc = 1 / (omega * C)
            i = 1 / (R * R + (xl - xc) ** 2).sqrt()
            rows.append(
                ((i * xc).quantize(Decimal(".01")), (i * xl).quantize(Decimal(".01")))
            )
    assert rows == [
        (Decimal("1.33"), Decimal(".33")),
        (Decimal("6.28"), Decimal("6.28")),
        (Decimal(".79"), Decimal("1.77")),
    ]
    l = load_batch("grade11_batch4")["lessons"][3]
    assert "100Hz:UC=6,28V,UL=6,28V" in l["cards"][1]["body"]
    assert not l["review"]["physical_experiment_completed"]
    assert rows[0][0] > rows[0][1] and rows[2][0] < rows[2][1]


def test_rms_power_factor_work_and_passive_limits():
    assert calculation_value(question(20, 6)) == Fraction(36, 10)
    assert calculation_value(question(20, 7)) == 1080
    assert calculation_value(question(20, 8)) == Fraction(3, 5)
    assert calculation_value(question(20, 9)) == Fraction(3, 5)
    q = question(20, 8)
    q["public"]["givens"][0]["value"] = "50"
    assert calculation_value(q) == 1
    q["public"]["givens"][0]["value"] = "0"
    assert calculation_value(q) == 0
    q = question(20, 6)
    q["public"]["givens"][2]["value"] = "0"
    assert calculation_value(q) == 0


def test_honest_five_sections_source_offset_and_counts():
    d = load_batch("grade11_batch4")
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
