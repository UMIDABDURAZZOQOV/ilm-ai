"""Source-checked EM waves, intensity, radar and optical interference."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import NUMERIC_ORACLES, new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

LABELS = {
    21: ["Yo‘q, ular boshqa kattaliklar", "Yo‘q", "Kamayadi", "1e6"],
    22: [
        "Chastotasi",
        "W/m²",
        "Izotrop nuqtaviy uzoq manba/noabsorbsiya",
        "O‘rtacha hajmiy energiya zichligi",
    ],
    23: [
        "Kerakli tashuvchi stansiyani",
        "Tashuvchidan xabar qismini ajratish",
        "Borish-qaytishning jami vaqti",
        "Bitta impuls ichidagi davrlar soni",
    ],
    24: [
        "Videokamera",
        "Karnayga",
        "Kerakli dasturni ajratib olish",
        "Toshkent",
        "To‘g‘ri emas, model doirasi bor",
    ],
    25: [
        "Yo‘q, faza/chastota bog‘liqligi ham kerak",
        "Kuchayish",
        "Linzaning egrilik radiusi",
        "Yo‘q, bu universal zarur shart emas",
        "Panjara davri",
    ],
}
ORDERS = {
    21: ["s2", "s1", "s3"],
    22: ["s2", "s1", "s3"],
    23: ["s2", "s1", "s3"],
    24: ["s2", "s3", "s1", "s4"],
    25: ["s2", "s1", "s3"],
}


def question(seq, n):
    return deepcopy(
        load_batch("grade11_batch5")["lessons"][seq - 21]["assessments"][n - 1]
    )


@pytest.mark.parametrize("seq", range(21, 26))
def test_independent_source_meaning_order_and_digital_activity(seq):
    l = load_batch("grade11_batch5")["lessons"][seq - 21]
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
    if seq == 24:
        assert not l["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in l["assessments"]
        )


@pytest.mark.parametrize(
    "identity", [k for k in NUMERIC_ORACLES if k[0] == 11 and 21 <= k[1] <= 25]
)
def test_independent_literal_answers_closed_formulas_and_units(identity):
    _, seq, n = identity
    l = load_batch("grade11_batch5")["lessons"][seq - 21]
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
        (21, 6, "v", "300000001", "m/s"),
        (21, 6, "nu", "0", "MHz"),
        (21, 8, "Lw", "31", "cm"),
        (22, 6, "v2", "0", "m/s"),
        (22, 7, "S", "0", "cm2"),
        (22, 7, "dt", "-1", "s"),
        (22, 8, "c", "299000000", "m/s"),
        (22, 9, "R", "0", "m"),
        (22, 9, "p", "3.14159", "1"),
        (23, 6, "tEcho", "-1", "µs"),
        (23, 8, "tPulse", "0.0001", "µs"),
        (25, 7, "m", "2.5", "1"),
        (25, 7, "m", "-1", "1"),
        (25, 9, "R", "0", "m"),
        (25, 11, "n", "0", "1"),
        (25, 11, "n", "1.5", "1"),
        (25, 11, "sinPhi", "1.1", "1"),
        (25, 12, "sinPhi", "0", "1"),
    ],
)
def test_source_domains(seq, n, symbol, value, unit):
    q = question(seq, n)
    next(g for g in q["public"]["givens"] if g["symbol"] == symbol).update(
        value=value, unit=unit
    )
    with pytest.raises(ValueError):
        calculation_value(q)


def test_radar_roundtrip_and_pulse_cycles_not_repetition_frequency():
    assert calculation_value(question(23, 6)) == 3000
    assert calculation_value(question(23, 7)) == Fraction(1, 100000)
    assert calculation_value(question(23, 8)) == 1000
    q = question(23, 6)
    q["public"]["givens"][1]["value"] = "0"
    assert calculation_value(q) == 0


def test_relative_index_may_be_below_one_and_newton_dark_center_zero():
    q = question(22, 6)
    q["public"]["givens"][0]["value"] = "200000000"
    q["public"]["givens"][1]["value"] = "300000000"
    assert calculation_value(q) == Fraction(2, 3)
    q = question(25, 9)
    next(g for g in q["public"]["givens"] if g["symbol"] == "m")["value"] = "0"
    assert calculation_value(q) == 0
    assert calculation_value(question(25, 10)) == Fraction(1, 2000)
    assert calculation_value(question(25, 11)) == Fraction(6, 10**7)


def test_source_linked_counts_and_no_artificial_tv_formula():
    d = load_batch("grade11_batch5")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 28,
        "formulas": 16,
        "worked_examples": 5,
        "assessments": 43,
        "frq": 16,
    }
    assert not d["lessons"][3]["formulas"]
    for l in d["lessons"]:
        assert l["review"]["independent_subject_expert"] == "not_claimed"
        assert not l["review"]["physical_experiment_completed"]
        for ref in l["source_refs"]:
            assert ref["printed_pages"] == [p - 1 for p in ref["pdf_pages"]]
