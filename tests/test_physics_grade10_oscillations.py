"""Source-checked signed oscillator, ideal efflux and conditional pendulum lab."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import NUMERIC_ORACLES, new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

LABELS = {
    21: [
        "Teshikdan sirtgacha chuqurlik",
        "Yo‘q, bu shart majburiy emas",
        "Aylanuvchi to‘p atrofidagi oqimga",
    ],
    22: [
        "a=0, tezlik moduli maksimal",
        "Tezlanish siljishga qarshiligini",
        "Berilgan faza sinusining birliksiz qiymati",
    ],
    23: [
        "Muvozanat holatidan",
        "Kichik burchakli ideal yaqinlashuvda",
        "To‘rt baravar",
    ],
    24: [
        "Bitta to‘liq tebranishning2s vaqtini",
        "Osilish nuqtasidan massa markazigacha",
        "Haqiqiy sekundomer bilan o‘lchov bajarilganini",
    ],
    25: [
        "Erkin so‘nuvchi tebranish",
        "Majburlovchi kuch chastotasiga",
        "Tashqi va xususiy chastotalar",
        "Tebranishlarni tezroq so‘ndirishga",
        "Yo‘q, ichki manba va rostlash kerak",
    ],
}
ORDERS = {
    21: ["s3", "s1", "s4", "s2"],
    22: ["s2", "s1", "s3"],
    23: ["s2", "s3", "s1"],
    24: ["s2", "s3", "s1", "s4"],
    25: ["s2", "s1", "s3"],
}


@pytest.mark.parametrize("seq", range(21, 26))
def test_independent_semantic_choices_and_varied_order(seq):
    l = load_batch("grade10_batch5")["lessons"][seq - 21]
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
    assert (
        grade_answer(q["grading_spec"], {"order": list(reversed(ORDERS[seq]))})
        != "correct"
    )
    if seq == 25:
        assert not l["formulas"] and not any(
            q["response_kind"] == "numeric_quantity" for q in l["assessments"]
        )


@pytest.mark.parametrize(
    "identity", [k for k in NUMERIC_ORACLES if k[0] == 10 and 21 <= k[1] <= 25]
)
def test_literal_oracle_units_and_every_reviewed_formula(identity):
    _, seq, n = identity
    l = load_batch("grade10_batch5")["lessons"][seq - 21]
    q = l["assessments"][n - 1]
    s = q["grading_spec"]
    a = new_answer(l, q)
    assert grade_answer(s, a) == "correct"
    for f in s["formula"]["equivalents"]:
        assert grade_answer(s, {**a, "formula": f}) == "correct"
    assert grade_answer(s, {**a, "unit": "K"}) == "dimension_mismatch"
    assert grade_answer(s, {**a, "formula": "1"}) == "wrong_formula"
    assert grade_answer(s, {**a, "value": "999999"}) == "out_of_tolerance"


@pytest.mark.parametrize(
    "seq,n,gi,value,unit",
    [
        (21, 5, 0, "9.81", "m/s2"),
        (21, 6, 2, "5", "m"),
        (21, 6, 2, "-1", "m"),
        (22, 5, 0, "0", "N/m"),
        (22, 6, 0, "4", "Hz"),
        (22, 7, 0, "0", "cm"),
        (22, 9, 1, "1.1", "1"),
        (22, 10, 2, "-1.1", "1"),
        (22, 10, 2, "0.8", "°"),
        (22, 11, 0, "30.5", "1"),
        (22, 12, 0, "3.14159", "1"),
        (23, 5, 1, "0", "g"),
        (23, 6, 2, "0", "N/m"),
        (23, 7, 2, "0", "m/s2"),
        (23, 8, 0, "0", "s"),
        (24, 6, 1, "20.5", "1"),
        (24, 7, 2, "0", "s"),
        (24, 7, 0, "3", "1"),
    ],
)
def test_model_and_unit_domains(seq, n, gi, value, unit):
    q = deepcopy(
        load_batch("grade10_batch5")["lessons"][seq - 21]["assessments"][n - 1]
    )
    q["public"]["givens"][gi].update(value=value, unit=unit)
    with pytest.raises(ValueError):
        calculation_value(q)


def test_signed_phase_endpoints_and_derivative_sign():
    ls = load_batch("grade10_batch5")["lessons"]
    q = deepcopy(ls[1]["assessments"][5])
    q["public"]["givens"][1]["value"] = "-3"
    assert calculation_value(q) == Fraction(48, 100)
    q = deepcopy(ls[1]["assessments"][8])
    q["public"]["givens"][1]["value"] = "-1"
    assert calculation_value(q) == Fraction(-5, 100)
    q["public"]["givens"][1]["value"] = "0"
    assert calculation_value(q) == 0
    q["public"]["givens"][1]["value"] = "1"
    assert calculation_value(q) == Fraction(5, 100)
    # For x=A*sin(theta), restoring acceleration at positive x is negative.
    assert calculation_value(ls[1]["assessments"][5]) == Fraction(-48, 100)


def test_periods_energy_and_digital_gravity_have_independent_exact_values():
    ls = load_batch("grade10_batch5")["lessons"]
    assert calculation_value(ls[2]["assessments"][5]) == Fraction(157, 250)
    assert calculation_value(ls[2]["assessments"][6]) == Fraction(471, 250)
    assert calculation_value(ls[2]["assessments"][7]) == 10
    assert calculation_value(ls[2]["assessments"][8]) == Fraction(1, 10)
    assert calculation_value(ls[3]["assessments"][6]) == Fraction(24649, 2500)
    assert not ls[3]["review"]["physical_experiment_completed"]


def test_five_honest_source_sections_counts_and_offset():
    d = load_batch("grade10_batch5")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 21,
        "formulas": 19,
        "worked_examples": 5,
        "assessments": 41,
        "frq": 19,
    }
    for l in d["lessons"]:
        for r in l["source_refs"]:
            assert r["printed_pages"] == [p - 1 for p in r["pdf_pages"]]
    assert d["publication"] == "local_test_preview_only" and not d["ai_explain"]
