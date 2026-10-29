"""Source-checked photon, Bohr, laser, nucleus and detector activities."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import NUMERIC_ORACLES, new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

LABELS = {
    36: ["Yo‘q, vakuumda p=Eq/c", "Ikki baravar", "W/m²", "Yo‘q"],
    37: ["Uzluksiz nurlanmaydi", "Ei−Ef musbat", "1", "To‘rt marta ortadi"],
    38: [
        "Majburiy nurlanish",
        "Nisbatan uzoq yashovchi uyg‘ongan holat",
        "Xrom ionlari",
        "Yo‘q",
        "Yo‘q",
    ],
    39: [
        "Jami nuklonlar sonini",
        "Izotoplar",
        "Yadroning massasi",
        "Energiya ajralishi",
    ],
    40: [
        "Gaz ionlashishidan",
        "Ionlar atrofidagi bug‘ tomchilaridan",
        "Chaqnashni",
        "Model chegarasini buzishi mumkin",
    ],
}
ORDERS = {
    36: ["s3", "s1", "s2"],
    37: ["s2", "s1", "s3"],
    38: ["s2", "s1", "s3", "s4"],
    39: ["s3", "s1", "s4", "s2"],
    40: ["s3", "s1", "s2"],
}


def question(seq, n):
    return deepcopy(
        load_batch("grade11_batch8")["lessons"][seq - 36]["assessments"][n - 1]
    )


@pytest.mark.parametrize("seq", range(36, 41))
def test_independent_source_meaning_order_and_digital_activity(seq):
    l = load_batch("grade11_batch8")["lessons"][seq - 36]
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
    if seq == 38:
        assert not l["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in l["assessments"]
        )


@pytest.mark.parametrize(
    "identity", [k for k in NUMERIC_ORACLES if k[0] == 11 and 36 <= k[1] <= 40]
)
def test_independent_literal_answers_closed_formulas_and_units(identity):
    _, seq, n = identity
    l = load_batch("grade11_batch8")["lessons"][seq - 36]
    q = l["assessments"][n - 1]
    s = q["grading_spec"]
    a = new_answer(l, q)
    assert grade_answer(s, a) == "correct"
    for f in s["formula"]["equivalents"]:
        assert grade_answer(s, {**a, "formula": f}) == "correct"
    assert grade_answer(s, {**a, "unit": "s"}) == "dimension_mismatch"
    assert grade_answer(s, {**a, "formula": "__import__(x)"}) != "correct"
    assert grade_answer(s, {**a, "value": "1000000"}) == "out_of_tolerance"


@pytest.mark.parametrize(
    "seq,n,symbol,value,unit",
    [
        (36, 6, "Lw", "0", "nm"),
        (36, 6, "c", "299000000", "m/s"),
        (36, 7, "h", "6.6e-63", "J*s"),
        (36, 8, "Iflux", "-600", "W/m2"),
        (37, 6, "n", "0", "1"),
        (37, 6, "n", "1.5", "1"),
        (37, 7, "Ei", "-4e-19", "J"),
        (37, 7, "Ei", "0", "J"),
        (37, 8, "n", "-2", "1"),
        (37, 9, "a0", "0", "m"),
        (39, 6, "A", "26.5", "1"),
        (39, 6, "Z", "28", "1"),
        (39, 7, "mNuc", "7e-27", "kg"),
        (39, 7, "Z", "-1", "1"),
        (39, 8, "Dm", "-1", "kg"),
        (39, 9, "A", "0", "1"),
        (40, 6, "B", "10", "mT"),
        (40, 6, "q", "-1.6e-19", "C"),
    ],
)
def test_photon_atomic_nuclear_and_track_domains(seq, n, symbol, value, unit):
    q = question(seq, n)
    next(g for g in q["public"]["givens"] if g["symbol"] == symbol).update(
        value=value, unit=unit
    )
    with pytest.raises(ValueError):
        calculation_value(q)


def test_normal_mirror_pressure_and_vacuum_momentum_independent():
    assert (
        calculation_value(question(36, 9))
        == 2 * calculation_value(question(36, 8))
        == Fraction(4, 10**6)
    )
    assert calculation_value(question(36, 6)) == Fraction(3313, 10**22)
    assert calculation_value(question(36, 7)) == Fraction(13252, 10**31)


def test_negative_hydrogen_energy_and_radius_n_squared():
    assert calculation_value(question(37, 8)) == Fraction(-544, 10**21)
    assert calculation_value(question(37, 9)) == 9 * Fraction(529, 10**13)
    assert calculation_value(question(37, 7)) == 300000000000000


def test_nuclear_mass_balance_from_independent_decimal_givens():
    free = 2 * Fraction("1.6726e-27") + 2 * Fraction("1.6749e-27")
    dm = free - Fraction("6.644e-27")
    assert dm == Fraction("5.1e-29") == calculation_value(question(39, 7))
    energy = dm * 300000000**2
    assert energy == Fraction("4.59e-12") == calculation_value(question(39, 8))
    assert energy / 4 == calculation_value(question(39, 9))
    assert calculation_value(question(39, 6)) == 14


def test_low_speed_track_and_rounding_are_not_relativistic_claim():
    q = question(40, 6)
    assert calculation_value(q) == Fraction(80000000, 91)
    a = new_answer(load_batch("grade11_batch8")["lessons"][4], q)
    assert (
        grade_answer(q["grading_spec"], {**a, "value": "880000"}) == "out_of_tolerance"
    )
    assert (
        grade_answer(q["grading_spec"], {**a, "value": "879120"})
        == "rounding_requirement"
    )


def test_honest_source_counts():
    d = load_batch("grade11_batch8")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 25,
        "formulas": 13,
        "worked_examples": 5,
        "assessments": 39,
        "frq": 13,
    }
    for l in d["lessons"]:
        assert not l["review"]["physical_experiment_completed"]
        assert l["review"]["independent_subject_expert"] == "not_claimed"
        for r in l["source_refs"]:
            assert r["printed_pages"] == [p - 1 for p in r["pdf_pages"]]
