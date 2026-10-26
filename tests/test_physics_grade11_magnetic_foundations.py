"""Independent oriented flux, loop torque, long-wire geometry and work oracles."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import NUMERIC_ORACLES, new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

LABELS = {
    1: ["Yuzaning normaliga", "Yo‘q, yo‘nalish sabab ham oqim0bo‘lishi mumkin", "T"],
    2: [
        "Ta’sir chiziqlari turli bo‘lib, juft moment hosil qiladi",
        "Tik",
        "Hissalar qo‘shilib N ko‘paytuvchi bo‘ladi",
    ],
    3: ["Sim o‘qidan tik masofa", "Markazida", "Mumkin emas, geometriya sharti boshqa"],
    4: [
        "Maydondagi tokli uzunlik va kuch bo‘yicha siljish",
        "Kuch va ish0",
        "Tok manbaidan",
    ],
    5: ["Tortishadi", "Sim o‘qlari orasidagi masofa", "Ikki baravar ortadi"],
}
ORDERS = {
    1: ["s2", "s1", "s3"],
    2: ["s1", "s3", "s2"],
    3: ["s2", "s1", "s3"],
    4: ["s2", "s3", "s1"],
    5: ["s2", "s3", "s1"],
}


def question(seq, n):
    return deepcopy(
        load_batch("grade11_batch1")["lessons"][seq - 1]["assessments"][n - 1]
    )


@pytest.mark.parametrize("seq", range(1, 6))
def test_source_concepts_and_order(seq):
    l = load_batch("grade11_batch1")["lessons"][seq - 1]
    qs = [q for q in l["assessments"] if q["response_kind"] == "concept_selection"]
    assert len(qs) == len(LABELS[seq]) == 3
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
    "identity", [k for k in NUMERIC_ORACLES if k[0] == 11 and 1 <= k[1] <= 5]
)
def test_independent_units_closed_formulas_and_no_wrong_quantity_acceptance(identity):
    _, seq, n = identity
    l = load_batch("grade11_batch1")["lessons"][seq - 1]
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
        (1, 5, 0, "-40", "mT"),
        (1, 5, 1, "0", "cm2"),
        (1, 5, 2, "1.1", "1"),
        (1, 5, 2, "-1.1", "1"),
        (1, 6, 0, "-80", "µWb"),
        (1, 6, 1, "0", "cm2"),
        (2, 5, 0, "20.5", "1"),
        (2, 5, 0, "2000", "%"),
        (2, 5, 4, "-0.5", "1"),
        (2, 5, 4, "1.1", "1"),
        (2, 6, 0, "0.002", "J"),
        (2, 6, 2, "0", "A"),
        (2, 6, 3, "0", "cm2"),
        (3, 5, 0, "1.25e-6", "N/A2"),
        (3, 5, 2, "3.14159", "1"),
        (3, 5, 3, "0", "cm"),
        (3, 6, 2, "0", "cm"),
        (3, 7, 1, "0", "1"),
        (3, 7, 1, "2.5", "1"),
        (3, 7, 0, "1.256e-6", "T"),
        (3, 8, 0, "-30", "Wb"),
        (4, 5, 4, "1.1", "1"),
        (4, 5, 2, "0", "cm"),
        (4, 5, 3, "-5", "cm"),
        (4, 6, 0, "0", "A"),
        (4, 6, 1, "-3", "T"),
        (5, 5, 5, "0", "cm"),
        (5, 5, 3, "0", "m"),
    ],
)
def test_geometry_angle_constants_turn_counts_and_dimensions(seq, n, gi, v, u):
    q = question(seq, n)
    q["public"]["givens"][gi].update(value=v, unit=u)
    with pytest.raises(ValueError):
        calculation_value(q)


def test_oriented_flux_zero_and_reversal_do_not_change_area_or_field():
    q = question(1, 5)
    for cos, expected in [
        ("0", 0),
        ("1", Fraction(12, 100000)),
        ("-1", Fraction(-12, 100000)),
    ]:
        q["public"]["givens"][2]["value"] = cos
        assert calculation_value(q) == expected
    q = question(3, 8)
    q["public"]["givens"][1]["value"] = "30"
    assert calculation_value(q) == 0


def test_loop_moment_uses_sine_not_flux_cosine_and_torque_is_not_energy():
    q = question(2, 5)
    assert calculation_value(q) == Fraction(12, 10000)
    q["public"]["givens"][4]["value"] = "0"
    assert calculation_value(q) == 0
    s = question(2, 5)["grading_spec"]
    assert (
        grade_answer(s, {"formula": "n*B*I*S*sinAlpha", "value": "0.0012", "unit": "J"})
        == "dimension_mismatch"
    )


def test_wire_loop_coil_distance_and_turn_scaling_are_independent():
    assert calculation_value(question(3, 5)) == Fraction(1, 100000)
    assert calculation_value(question(3, 6)) == Fraction(1256, 10**8)
    assert calculation_value(question(3, 7)) == Fraction(628, 10**7)
    q = question(3, 5)
    q["public"]["givens"][3]["value"] = "8"
    assert calculation_value(q) == Fraction(1, 200000)
    q = question(3, 7)
    q["public"]["givens"][1]["value"] = "1"
    assert calculation_value(q) == Fraction(314, 10**8)
    assert calculation_value(question(5, 5)) == Fraction(6, 100000)


def test_source_supplied_mechanical_work_signed_flux_and_parallel_zero():
    assert calculation_value(question(4, 5)) == Fraction(6, 1000)
    assert calculation_value(question(4, 6)) == Fraction(-6, 1000)
    q = question(4, 5)
    q["public"]["givens"][4]["value"] = "0"
    assert calculation_value(q) == 0


def test_honest_new_grade_and_whole_pdf_offset():
    d = load_batch("grade11_batch1")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 25,
        "formulas": 12,
        "worked_examples": 5,
        "assessments": 32,
        "frq": 12,
    }
    assert d["grade"] == 11 and d["publication"] == "local_test_preview_only"
    for l in d["lessons"]:
        assert l["review"]["independent_subject_expert"] == "not_claimed"
        assert not l["review"]["physical_experiment_completed"]
        for r in l["source_refs"]:
            assert r["printed_pages"] == [p - 1 for p in r["pdf_pages"]]
            assert r["book_id"] == "physics-uz-grade-11"
