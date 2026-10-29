"""Local-g orbit, support/contact, friction regime and work/FIK source models."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import NUMERIC_ORACLES, new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    11: ["Markazga intilma tezlanish", "Aynan berilgan orbital radiusga", "r−R"],
    12: ["mg", "Pastga", "Tayanch/osmaga ta’sir moduli"],
    13: [
        "Bitta o‘rganilayotgan jismga",
        "Yo‘q, zarur qiymati maksimal chegaragacha moslashadi",
        "Bir xil T",
    ],
    14: [
        "Manfiy",
        "Mexanik E har doim o‘zgarmasligini",
        "Parallel kuch bilan doimiy tezlikda yuqoriga tortish",
    ],
    15: [
        "Qiya yo‘l va vertikal balandlik",
        "80%",
        "Yo‘q, bu tayyor raqamli qayd tahlili",
    ],
}


@pytest.mark.parametrize("seq", range(11, 16))
def test_source_choices_order_pdf_offset_and_actual_digital_lab(seq):
    l = load_batch("grade10_batch3")["lessons"][seq - 11]
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
                grade_answer(q["grading_spec"], {"order": ["s3", "s2", "s1"]})
                != "correct"
            )
    for ref in l["source_refs"]:
        assert ref["printed_pages"] == [p - 1 for p in ref["pdf_pages"]]
    assert not l["review"]["physical_experiment_completed"]
    if seq == 15:
        assert (
            l["review"]["physical_measurements"]
            == "not_claimed_conditional_digital_data_only"
        )


@pytest.mark.parametrize(
    "identity", [k for k in NUMERIC_ORACLES if k[0] == 10 and 11 <= k[1] <= 15]
)
def test_independent_oracle_equivalent_units_and_all_reviewed_formulas(identity):
    _, seq, n = identity
    l = load_batch("grade10_batch3")["lessons"][seq - 11]
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
        (11, 5, 0, "0", "m/s2"),
        (11, 5, 1, "0", "km"),
        (11, 6, 0, "0", "s"),
        (11, 6, 1, "5000", "km"),
        (11, 6, 2, "0", "km"),
        (11, 7, 1, "0", "m/s2"),
        (12, 5, 0, "-40", "kg"),
        (12, 7, 2, "11", "m/s2"),
        (12, 8, 0, "0", "m/s2"),
        (13, 5, 2, "0", "kg"),
        (13, 5, 0, "-3", "N"),
        (13, 6, 3, "0.7", "1"),
        (13, 6, 2, "-0.5", "1"),
        (13, 6, 1, "30", "°"),
        (13, 7, 0, "5", "kg"),
        (13, 8, 0, "0", "kg"),
        (13, 7, 2, "9.81", "m/s2"),
        (14, 8, 2, "0", "m"),
        (14, 8, 4, "0", "1"),
        (14, 8, 3, "-0.5", "1"),
        (14, 9, 1, "0.75", "°"),
        (14, 10, 4, "0.7", "1"),
        (15, 7, 1, "2", "m"),
        (15, 7, 2, "0", "N"),
        (15, 7, 0, "100", "N"),
    ],
)
def test_quantity_domains_and_source_model_rejections(seq, n, gi, value, unit):
    q = deepcopy(
        load_batch("grade10_batch3")["lessons"][seq - 11]["assessments"][n - 1]
    )
    q["public"]["givens"][gi].update(value=value, unit=unit)
    with pytest.raises(ValueError):
        calculation_value(q)


def test_contact_freefall_and_already_sliding_are_different_domains():
    ls = load_batch("grade10_batch3")["lessons"]
    q = deepcopy(ls[1]["assessments"][6])
    q["public"]["givens"][2]["value"] = "10"
    assert calculation_value(q) == 0
    q = deepcopy(ls[2]["assessments"][5])
    q["public"]["givens"][2]["value"] = "1"
    assert (
        calculation_value(q) == -2
    )  # already sliding downhill, negative a decelerates.
    q["public"]["givens"][2]["value"] = "0.75"
    assert calculation_value(q) == 0  # boundary does not require accelerated onset.


def test_independent_atwood_balances_and_radius_scaling():
    ls = load_batch("grade10_batch3")["lessons"]
    a = calculation_value(ls[2]["assessments"][6])
    t = calculation_value(ls[2]["assessments"][7])
    assert a == Fraction(5, 2) and t == Fraction(75, 2)
    assert t - 3 * 10 == 3 * a and 5 * 10 - t == 5 * a
    q = deepcopy(ls[0]["assessments"][5])
    q["public"]["givens"][1]["value"] = "6000"
    assert calculation_value(q) == 5000  # same radius => same period.
    q["public"]["givens"][1]["value"] = "24000"
    assert calculation_value(q) == 40000  # radiusx4 => periodx8, notx4.


def test_exact_ratio_percentage_rounding_and_ideal_ramp_limit():
    ls = load_batch("grade10_batch3")["lessons"]
    for seq, n, truth, percent in [
        (14, 9, Fraction(8, 11), "72.73"),
        (15, 7, Fraction(2, 3), "66.67"),
    ]:
        q = ls[seq - 11]["assessments"][n - 1]
        s = q["grading_spec"]
        a = new_answer(ls[seq - 11], q)
        assert calculation_value(q) == truth
        assert s["expected_rational"] == {
            "numerator": str(truth.numerator),
            "denominator": str(truth.denominator),
        }
        assert grade_answer(s, {**a, "value": percent, "unit": "%"}) == "correct"
        assert (
            grade_answer(
                s, {**a, "value": "72.731" if seq == 14 else "66.671", "unit": "%"}
            )
            == "rounding_requirement"
        )
        assert (
            grade_answer(s, {**a, "value": percent, "unit": "1"}) == "out_of_tolerance"
        )
    q = deepcopy(ls[3]["assessments"][8])
    q["public"]["givens"][0]["value"] = "0"
    assert calculation_value(q) == 1  # ideal limit, no false >100%.
    # Same original model: F=22N,path=h/sin=1m; input22J, useful16J, ratio8/11.
    assert 22 * Fraction(4, 5) / Fraction(4, 5) == 22
    assert Fraction(16, 22) == Fraction(8, 11)


def test_batch_counts_are_five_actual_source_sections():
    d = load_batch("grade10_batch3")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 22,
        "formulas": 20,
        "worked_examples": 5,
        "assessments": 40,
        "frq": 20,
    }
    assert d["publication"] == "local_test_preview_only" and not d["ai_explain"]
