"""Independent classical/Lenz/linkage/diamagnetic/linear energy checks."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import NUMERIC_ORACLES, new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

LABELS = {
    6: ["Nol", "Teskari", "Bga tik kirish", "Berilgan sekin/norelativistik modelda"],
    7: [
        "Yo‘q, oqim o‘zgarishi kerak",
        "O‘rtacha qiymatni",
        "Uni hosil qilgan oqim o‘zgarishiga",
        "Induksiyalangan EYuK ham albatta yo‘qligini",
    ],
    8: [
        "N*Phi oqim bog‘lanishi",
        "Kamayishga qarshi tokni saqlashga intiladi",
        "H",
        "Shartsiz mumkin emas",
    ],
    9: ["Birliksiz", "0va1orasida", "1dan biroz katta", "Shartsiz to‘g‘ri emas"],
    10: [
        "To‘rt baravar",
        "Moduli",
        "Yo‘q, issiqlik ham ajralishi mumkin",
        "Nolga bo‘lish ruxsat etilmaydi",
    ],
}
ORDERS = {
    6: ["s2", "s1", "s3"],
    7: ["s2", "s3", "s1", "s4"],
    8: ["s2", "s1", "s3"],
    9: ["s2", "s1", "s3"],
    10: ["s1", "s2", "s3"],
}


def question(seq, n):
    return deepcopy(
        load_batch("grade11_batch2")["lessons"][seq - 6]["assessments"][n - 1]
    )


@pytest.mark.parametrize("seq", range(6, 11))
def test_meaning_and_order(seq):
    l = load_batch("grade11_batch2")["lessons"][seq - 6]
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
    "identity", [k for k in NUMERIC_ORACLES if k[0] == 11 and 6 <= k[1] <= 10]
)
def test_independent_literal_answers_units_and_equivalents(identity):
    _, seq, n = identity
    l = load_batch("grade11_batch2")["lessons"][seq - 6]
    q = l["assessments"][n - 1]
    s = q["grading_spec"]
    a = new_answer(l, q)
    assert grade_answer(s, a) == "correct"
    for f in s["formula"]["equivalents"]:
        assert grade_answer(s, {**a, "formula": f}) == "correct"
    assert grade_answer(s, {**a, "unit": "kg"}) == "dimension_mismatch"
    assert grade_answer(s, {**a, "formula": "__import__(x)"}) != "correct"
    assert grade_answer(s, {**a, "value": "999999"}) == "out_of_tolerance"


@pytest.mark.parametrize(
    "seq,n,gi,v,u",
    [
        (6, 6, 3, "1.1", "1"),
        (6, 6, 1, "299792458", "m/s"),
        (6, 7, 1, "3e6", "m/s"),
        (6, 7, 2, "0", "C"),
        (6, 7, 3, "0", "T"),
        (6, 8, 0, "3.14159", "1"),
        (6, 8, 1, "0", "kg"),
        (6, 9, 3, "1e-30", "kg"),
        (7, 6, 0, "50.5", "1"),
        (7, 6, 0, "5000", "%"),
        (7, 6, 2, "0", "s"),
        (7, 7, 1, "3", "T"),
        (7, 8, 1, "0", "Ω"),
        (8, 6, 0, "0", "H"),
        (8, 6, 1, "-3", "V"),
        (8, 6, 2, "0", "s"),
        (8, 7, 0, "-3", "V"),
        (8, 7, 2, "0", "A"),
        (8, 8, 0, "0", "H"),
        (8, 9, 0, "1.25e-6", "N/A2"),
        (8, 9, 1, "0", "1"),
        (8, 9, 2, "100.5", "1"),
        (8, 9, 3, "0", "cm2"),
        (8, 9, 4, "0", "cm"),
        (9, 6, 0, "0", "1"),
        (9, 7, 1, "0", "mT"),
        (10, 6, 0, "0", "H"),
        (10, 7, 0, "-16", "mJ"),
        (10, 7, 1, "0", "H"),
        (10, 8, 1, "0", "A"),
    ],
)
def test_models_units_turns_zero_and_low_speed_policy(seq, n, gi, v, u):
    q = question(seq, n)
    q["public"]["givens"][gi].update(value=v, unit=u)
    with pytest.raises(ValueError):
        calculation_value(q)


def test_lenz_sign_changes_and_flux_linkage_are_not_per_turn_flux():
    assert calculation_value(question(7, 6)) == 1
    q = question(7, 6)
    q["public"]["givens"][1]["value"] = "2"
    assert calculation_value(q) == -1
    q["public"]["givens"][1]["value"] = "0"
    assert calculation_value(q) == 0
    assert calculation_value(question(7, 7)) == Fraction(-1, 5)
    assert calculation_value(question(7, 8)) == Fraction(-1, 20)
    q = question(8, 6)
    q["public"]["givens"][1]["value"] = "3"
    assert calculation_value(q) == -6
    assert calculation_value(question(8, 8)) == Fraction(8, 100)
    q = question(8, 8)
    q["public"]["givens"][1]["value"] = "-0.4"
    assert calculation_value(q) == Fraction(-8, 100)


def test_diamagnetic_mu_below_one_is_allowed_unlike_dielectric_eps():
    assert calculation_value(question(9, 6)) == Fraction(1998, 100000)
    assert calculation_value(question(9, 7)) == Fraction(1002, 1000)
    q = question(8, 9)
    q["public"]["givens"][1]["value"] = "0.999"
    assert calculation_value(q) == Fraction(1256, 10**8) * Fraction(999, 1000)


def test_classical_radius_period_low_speed_and_saturation_independence_are_explicit():
    assert calculation_value(question(6, 6)) == Fraction(16, 10**16)
    assert calculation_value(question(6, 7)) == Fraction(4, 100)
    assert calculation_value(question(6, 8)) == Fraction(2512, 10**9)
    assert calculation_value(question(6, 9)) == 100000
    assert calculation_value(question(8, 9)) == Fraction(1256, 10**8)


def test_stored_energy_even_in_current_and_inverse_magnitude():
    assert calculation_value(question(10, 6)) == Fraction(16, 1000)
    q = question(10, 6)
    q["public"]["givens"][1]["value"] = "-0.4"
    assert calculation_value(q) == Fraction(16, 1000)
    assert calculation_value(question(10, 7)) == Fraction(4, 10)
    assert calculation_value(question(10, 8)) == Fraction(2, 10)
    q = question(10, 8)
    q["public"]["givens"][1]["value"] = "-0.3"
    assert calculation_value(q) == Fraction(2, 10)
    # Source39 keys are inconsistent; new answers must not inherit them.
    assert Fraction(5, 1000) * Fraction(4, 10) ** 2 / 2 == Fraction(4, 10000)
    assert 2 * Fraction(60, 1000) / 9 == Fraction(1, 75)


def test_five_sections_honest_scope_and_source_offsets():
    d = load_batch("grade11_batch2")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 25,
        "formulas": 16,
        "worked_examples": 5,
        "assessments": 41,
        "frq": 16,
    }
    assert d["publication"] == "local_test_preview_only"
    for l in d["lessons"]:
        assert l["review"]["independent_subject_expert"] == "not_claimed"
        assert not l["review"]["physical_experiment_completed"]
        for r in l["source_refs"]:
            assert r["printed_pages"] == [p - 1 for p in r["pdf_pages"]]
