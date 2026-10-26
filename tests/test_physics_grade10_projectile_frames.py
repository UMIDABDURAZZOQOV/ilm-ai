"""Source-scoped projectile data, digital lab and translating frame signs."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import NUMERIC_ORACLES, new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    6: ["y=h", "Gorizontal tarkib", "Yo‘q, ular turli kattaliklar"],
    7: [
        "Vertikal tezlik tarkibi",
        "Burchak sinusining birliksiz qiymati",
        "Bir xil v0, teng balandlik va qarshiliksiz modelga",
    ],
    8: [
        "Tayyor shartli uzoqlik jadvallari",
        "Boshlang‘ich tezlik bir xil olinadi",
        "Yo‘q, tarqalish va model chegarasi qoladi",
        "Shu shartli jadvalda45° uzoqroq",
    ],
    9: [
        "Tinch yoki to‘g‘ri chiziqli tekis harakatda qoladi",
        "Barcha kuchlarning natijaviy kuchi",
        "Ular turli jismlarga qo‘yilgani uchun",
    ],
    10: [
        "Klassik modelda ham inersial",
        "Tanlangan o‘qqa nisbatan manfiy olinadi",
        "Tezlanayotgan sanoq sistemasiga bog‘liq hisob tarkibi",
    ],
}


@pytest.mark.parametrize("seq", range(6, 11))
def test_source_semantic_choices_order_and_digital_only(seq):
    l = load_batch("grade10_batch2")["lessons"][seq - 6]
    qs = [q for q in l["assessments"] if q["response_kind"] == "concept_selection"]
    assert len(qs) == len(KEYS[seq])
    for q, label in zip(qs, KEYS[seq]):
        assert label in [o["label"] for o in q["public"]["options"]]
        for o in q["public"]["options"]:
            assert grade_answer(q["grading_spec"], {"choice_id": o["id"]}) == (
                "correct" if o["label"] == label else "incorrect_concept"
            )
    for q in l["assessments"]:
        if q["response_kind"] == "ordering":
            assert (
                grade_answer(q["grading_spec"], {"order": ["s2", "s3", "s1"]})
                == "correct"
            )
            assert (
                grade_answer(q["grading_spec"], {"order": ["s1", "s2", "s3"]})
                != "correct"
            )
    for ref in l["source_refs"]:
        assert ref["printed_pages"] == [p - 1 for p in ref["pdf_pages"]]
    assert not l["review"]["physical_experiment_completed"]
    if seq == 8:
        assert (
            l["review"]["physical_measurements"]
            == "not_claimed_conditional_digital_data_only"
        )


@pytest.mark.parametrize(
    "identity", [k for k in NUMERIC_ORACLES if k[0] == 10 and 6 <= k[1] <= 10]
)
def test_independent_literal_oracle_equivalent_units_and_every_allowed_formula(
    identity,
):
    _, seq, number = identity
    l = load_batch("grade10_batch2")["lessons"][seq - 6]
    q = l["assessments"][number - 1]
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
        (6, 5, 0, "0", "m"),
        (6, 5, 1, "9.81", "m/s2"),
        (6, 6, 0, "-1", "m/s"),
        (6, 7, 2, "3", "s"),
        (6, 8, 2, "0", "m"),
        (6, 7, 2, "-1", "s"),
        (7, 5, 1, "30", "1"),
        (7, 5, 1, "1", "1"),
        (7, 5, 1, "0.8", "°"),
        (7, 6, 1, "-0.6", "1"),
        (7, 6, 3, "3", "s"),
        (7, 7, 2, "-1", "s"),
        (7, 8, 2, "0", "m/s2"),
        (7, 9, 0, "0", "m/s"),
        (7, 10, 2, "0.7", "1"),
        (8, 6, 0, "0", "cm"),
        (9, 5, 1, "0", "kg"),
        (9, 8, 0, "0", "m/s2"),
        (10, 6, 0, "-2", "kg"),
        (10, 7, 1, "0", "kg"),
        (10, 7, 2, "3", "m/s"),
    ],
)
def test_model_domain_rejects_invalid_given_values_or_units(seq, n, gi, value, unit):
    q = deepcopy(load_batch("grade10_batch2")["lessons"][seq - 6]["assessments"][n - 1])
    q["public"]["givens"][gi].update(value=value, unit=unit)
    with pytest.raises(ValueError):
        calculation_value(q)


def test_irrational_flight_time_uses_exact_square_truth_and_rounding_grid():
    q = load_batch("grade10_batch2")["lessons"][0]["assessments"][4]
    s = q["grading_spec"]
    a = {"formula": "sqrt(2*h/g)", "unit": "s", "value": "1.73"}
    assert s["expected_root_rational"] == {"numerator": "3", "denominator": "1"}
    assert grade_answer(s, a) == "correct"
    assert grade_answer(s, {**a, "value": "1.74"}) == "out_of_tolerance"
    assert grade_answer(s, {**a, "value": "1.731"}) == "rounding_requirement"
    assert (
        grade_answer(
            s, {**a, "expected_root_rational": {"numerator": "1", "denominator": "1"}}
        )
        == "answer_required"
    )
    # Valid grid with long decimal isn't silently converted to the canonical expected_si.
    assert Fraction(173, 100) ** 2 < 3 < Fraction(174, 100) ** 2


def test_ground_boundary_and_same_height_return_are_inclusive():
    ls = load_batch("grade10_batch2")["lessons"]
    q = deepcopy(ls[0]["assessments"][6])
    q["public"]["givens"][2]["value"] = "2"
    assert calculation_value(q) == 0
    q = deepcopy(ls[1]["assessments"][5])
    q["public"]["givens"][3]["value"] = "2.4"
    assert calculation_value(q) == -12


def test_frame_opposite_acceleration_and_real_force_signs_follow_newton_balance():
    ls = load_batch("grade10_batch2")["lessons"]
    q = deepcopy(ls[4]["assessments"][5])
    q["public"]["givens"][1]["value"] = "-3"
    assert calculation_value(q) == 6
    q = deepcopy(ls[4]["assessments"][6])
    q["public"]["givens"][0]["value"] = "-10"
    q["public"]["givens"][2]["value"] = "-3"
    assert calculation_value(q) == -2
    # m*ar=F+Fi with m=2,F=-10,A=-3 => Fi=+6 and ar=-2.
    assert 2 * (-2) == -10 + 6


def test_batch_counts_and_canonical_source_identity():
    d = load_batch("grade10_batch2")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 23,
        "formulas": 19,
        "worked_examples": 5,
        "assessments": 40,
        "frq": 19,
    }
    assert [l["sequence"] for l in d["lessons"]] == list(range(6, 11))
    assert d["publication"] == "local_test_preview_only" and not d["ai_explain"]
