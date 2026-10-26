"""Signed thin lenses, distinct image branches and inverse mean focus."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    51: [
        "Manfiy",
        "Signed fning musbat moduli",
        "Yo‘q,modelda chekli tasvir masofasi yo‘q",
    ],
    52: ["Signed manfiy", "Yo‘q,haqiqiy yoki mavhumligini ham bilish kerak", "0<d<F"],
    53: [
        "Musbat,haqiqiy tasvir",
        "Avval Flarni o‘rtachalaydi,so‘ng teskarisini oladi",
        "Haqiqiy lampa/ekran o‘lchovi bajarilganini",
    ],
    54: [
        "Ko‘rish burchagini kattalashtirish",
        "Oraliq haqiqiy tasvirni hosil qiladi",
        "Shartlari berilgan maktab yaqinlashuvi",
    ],
    55: [
        "Haqiqiy,to‘nkarilgan,kichiklashgan",
        "Turli masofaga fokuslashga",
        "Manfiy sochuvchi linza sxemasini",
        "Musbat yig‘uvchi linza sxemasi",
        "Fazoviy chuqurlikni baholash bilan",
    ],
}


@pytest.mark.parametrize("seq", range(51, 56))
def test_every_semantic_option_and_order(seq):
    l = load_batch("grade9_batch11")["lessons"][seq - 51]
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
    if seq == 55:
        assert not l["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in l["assessments"]
        )


def test_all_literal_oracles_and_equivalent_formulas_wrong_responses():
    d = load_batch("grade9_batch11")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 23,
        "formulas": 12,
        "worked_examples": 5,
        "assessments": 36,
        "frq": 14,
    }
    n = 0
    for l in d["lessons"]:
        for q in l["assessments"]:
            s = q["grading_spec"]
            if s["kind"] != "numeric_quantity":
                continue
            n += 1
            a = new_answer(l, q)
            assert grade_answer(s, a) == "correct", q["key"]
            for f in s["formula"]["equivalents"]:
                assert grade_answer(s, {**a, "formula": f}) == "correct"
            assert grade_answer(s, {**a, "unit": "kg"}) == "dimension_mismatch"
            assert grade_answer(s, {**a, "value": "999999"}) == "out_of_tolerance"
            assert grade_answer(s, {**a, "formula": "1"}) == "wrong_formula"
    assert n == 14


@pytest.mark.parametrize(
    "seq,qi,gi,bad",
    [
        (51, 4, 0, "0"),
        (51, 4, 1, "20"),
        (51, 5, 1, "0"),
        (51, 7, 0, "-30"),
        (52, 4, 1, "-30"),
        (52, 5, 1, "0"),
        (52, 6, 1, "0"),
        (52, 7, 1, "1"),
        (52, 7, 1, "0.5"),
        (53, 4, 1, "-40"),
        (53, 5, 0, "0"),
        (53, 6, 2, "-25"),
        (54, 4, 0, "30"),
        (54, 4, 1, "0"),
        (54, 5, 1, "0"),
        (54, 6, 2, "0"),
        (54, 6, 1, "30"),
    ],
)
def test_finite_lens_real_screen_reference_and_branch_domains(seq, qi, gi, bad):
    q = deepcopy(load_batch("grade9_batch11")["lessons"][seq - 51]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_same_magnification_has_distinct_real_and_virtual_object_positions():
    d = load_batch("grade9_batch11")
    real, virtual = d["lessons"][1]["assessments"][6:8]
    assert calculation_value(real) == Fraction(1, 2)
    assert calculation_value(virtual) == Fraction(3, 10)
    # Same F=.4 and K=4,genuinely different branches,not interchangeable signs.
    for q, formula in [(real, "F*(1-1/K)"), (virtual, "F*(1+1/K)")]:
        assert (
            grade_answer(
                q["grading_spec"], {"formula": formula, "value": "0.3", "unit": "m"}
            )
            == "wrong_formula"
        )


def test_signed_images_do_not_imply_negative_size_ratio():
    d = load_batch("grade9_batch11")
    l = d["lessons"][0]
    assert calculation_value(l["assessments"][4]) == Fraction(3, 10)
    assert calculation_value(l["assessments"][5]) == Fraction(-1, 5)
    assert calculation_value(l["assessments"][6]) == Fraction(-1, 5)
    assert calculation_value(l["assessments"][7]) == 2
    q = l["assessments"][5]
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "F*d/(d-F)", "value": "-20", "unit": "cm"}
        )
        == "correct"
    )
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "F*d/(d-F)", "value": "20", "unit": "cm"}
        )
        == "sign_error"
    )


def test_inverse_of_mean_focal_is_not_mean_of_individual_powers():
    d = load_batch("grade9_batch11")
    q = d["lessons"][2]["assessments"][6]
    assert calculation_value(q) == 5
    mean_powers = (Fraction(20, 3) + 5 + 4) / 3
    assert mean_powers == Fraction(47, 9) and mean_powers != 5
    assert (
        grade_answer(
            q["grading_spec"],
            {"formula": "(1/F1+1/F2+1/F3)/3", "value": "5", "unit": "dptr"},
        )
        == "wrong_formula"
    )
    assert not d["lessons"][2]["review"]["physical_experiment_completed"]
