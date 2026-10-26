"""Source-reviewed collision balances, signed moments, contact geometry and flow."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import NUMERIC_ORACLES, new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    16: [
        "Tashqi impuls e’tiborsiz bo‘lgan tizimda",
        "Jami impuls va jami kinetik energiya",
        "−6J",
    ],
    17: [
        "Aylantiruvchi momentlar",
        "Massalar taqsimotini ifodalovchi hisobiy nuqta",
        "Turg‘un",
        "Turg‘unmas",
        "Har bir arqondan vertikalgacha",
    ],
    18: [
        "O‘qdan ta’sir chizig‘igacha tik masofa",
        "F*d",
        "Yukni ushlab turgan ip segmentlari soni",
    ],
    19: [
        "Markazga yo‘nalgan natijaviy kuch talabi",
        "Ikkalasi markazga, pastga",
        "N=0 kontakt chegarasi",
    ],
    20: [
        "S1*v1=S2*v2",
        "Balandlik va shartlar",
        "Model yoki berilganlarni qayta tekshiramiz",
    ],
}


@pytest.mark.parametrize("seq", range(16, 21))
def test_source_semantics_and_order(seq):
    l = load_batch("grade10_batch4")["lessons"][seq - 16]
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


@pytest.mark.parametrize(
    "identity", [k for k in NUMERIC_ORACLES if k[0] == 10 and 16 <= k[1] <= 20]
)
def test_literal_oracle_alternative_units_and_every_formula(identity):
    _, seq, n = identity
    l = load_batch("grade10_batch4")["lessons"][seq - 16]
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
        (16, 6, 0, "0", "kg"),
        (16, 7, 2, "-3", "kg"),
        (16, 8, 1, "4", "N"),
        (17, 7, 2, "0", "1"),
        (17, 7, 2, "1.01", "1"),
        (17, 7, 2, "0.6", "°"),
        (18, 5, 1, "-1", "cm"),
        (18, 6, 0, "-4", "N"),
        (18, 7, 1, "0", "cm"),
        (18, 8, 2, "0", "cm"),
        (18, 9, 1, "2.5", "1"),
        (18, 9, 1, "0", "1"),
        (19, 6, 1, "3", "m/s"),
        (19, 7, 1, "6", "m/s"),
        (19, 8, 1, "9.81", "m/s2"),
        (19, 5, 2, "0", "m"),
        (20, 5, 2, "0", "cm2"),
        (20, 6, 0, "0", "kg/m3"),
        (20, 7, 0, "1", "kPa"),
        (20, 7, 2, "0", "m/s2"),
        (20, 8, 4, "0", "cm2"),
        (20, 8, 3, "0", "kg/m3"),
        (20, 8, 1, "-0.2", "m"),
    ],
)
def test_model_domain_rejects_invalid_data(seq, n, gi, value, unit):
    q = deepcopy(
        load_batch("grade10_batch4")["lessons"][seq - 16]["assessments"][n - 1]
    )
    q["public"]["givens"][gi].update(value=value, unit=unit)
    with pytest.raises(ValueError):
        calculation_value(q)


def test_elastic_results_obey_independent_momentum_and_energy_and_sticking_loss():
    l = load_batch("grade10_batch4")["lessons"][0]
    u1 = calculation_value(l["assessments"][5])
    u2 = calculation_value(l["assessments"][6])
    assert (u1, u2) == (-2, 2)
    assert 1 * u1 + 3 * u2 == 4
    assert Fraction(1, 2) * u1**2 + Fraction(3, 2) * u2**2 == 8
    common = calculation_value(l["assessments"][4])
    loss = calculation_value(l["assessments"][7])
    assert common == 1 and loss == 6 and Fraction(4, 2) * common**2 + loss == 8
    # Equal masses exchange velocities; signed components retain their signs.
    first = deepcopy(l["assessments"][5])
    second = deepcopy(l["assessments"][6])
    for q in [first, second]:
        q["public"]["givens"][2]["value"] = "1"
        q["public"]["givens"][3]["value"] = "-2"
    assert calculation_value(first) == -2 and calculation_value(second) == 4


def test_torque_zero_balance_and_named_torque_unit_are_distinct_from_energy():
    l = load_batch("grade10_batch4")["lessons"][2]
    q = deepcopy(l["assessments"][5])
    q["public"]["givens"][2]["value"] = "5"
    assert calculation_value(q) == 0  # 4*.5=5*.4.
    through_axis = deepcopy(l["assessments"][4])
    through_axis["public"]["givens"][1]["value"] = "0"
    assert calculation_value(through_axis) == 0
    s = l["assessments"][4]["grading_spec"]
    a = new_answer(l, l["assessments"][4])
    assert grade_answer(s, {**a, "unit": "J"}) == "dimension_mismatch"


def test_both_contact_geometries_accept_only_their_domains_and_boundary():
    ls = load_batch("grade10_batch4")["lessons"]
    inside = deepcopy(ls[3]["assessments"][5])
    outside = deepcopy(ls[3]["assessments"][6])
    # v=10,R=10 => mv²/R=mg in both geometries => zero contact normal.
    for q in [inside, outside]:
        q["public"]["givens"][1]["value"] = "10"
        q["public"]["givens"][2]["value"] = "10"
        assert calculation_value(q) == 0
    assert calculation_value(ls[3]["assessments"][7]) == 10


def test_bernoulli_signed_difference_balance_and_root_final_grid():
    ls = load_batch("grade10_batch4")["lessons"]
    q = deepcopy(ls[4]["assessments"][5])
    q["public"]["givens"][1]["value"] = "4"
    q["public"]["givens"][2]["value"] = "2"
    assert calculation_value(q) == -6000  # dp defined p1-p2, not absolute pressure.
    assert (
        100000 + 1000 * 10 * 2 + 1000 * 2**2 / 2
        == 84000 + 1000 * 10 * 3 + 1000 * 4**2 / 2
    )
    q = ls[4]["assessments"][7]
    s = q["grading_spec"]
    a = new_answer(ls[4], q)
    assert s["expected_root_rational"] == {"numerator": "5", "denominator": "1"}
    assert grade_answer(s, a) == "correct"
    assert grade_answer(s, {**a, "value": "2.23"}) == "out_of_tolerance"
    assert grade_answer(s, {**a, "value": "2.241"}) == "rounding_requirement"
    assert grade_answer(s, {**a, "expected_si": "2.241"}) == "answer_required"


def test_batch_honest_counts_no_new_llm_or_publication():
    d = load_batch("grade10_batch4")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 21,
        "formulas": 19,
        "worked_examples": 5,
        "assessments": 41,
        "frq": 19,
    }
    assert d["publication"] == "local_test_preview_only" and not d["ai_explain"]
