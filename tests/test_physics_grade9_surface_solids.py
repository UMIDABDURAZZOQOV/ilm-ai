"""Independent source-scoped surface force, energy and capillary regressions."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import new_answer

from services.assessment_grading import UNITS, grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    31: [
        "Idish shaklini oladi,hajmi deyarli saqlanadi",
        "Berilgan samarali jami kontakt chizig‘i uzunligi",
        "Hisobga olingan jami sirt yuzi",
    ],
    32: [
        "Suyuqlik va qattiq sirt juftiga",
        "Botiq",
        "Ideal to‘liq ho‘llovchi vertikal doiraviy nayga",
    ],
    33: [
        "d=2*r",
        "Ikki uzun kontakt tomoni hisobga olingani uchun",
        "Ichki va tashqi ikki sirt",
    ],
    34: [
        "Simning boshlang‘ich og‘irlik hissasini ajratish uchun",
        "Berilgan modelning ikki kontakt chizig‘iga",
        "Shartli raqamli natijalar tahlil qilinganini",
    ],
    35: [
        "Zarrachalarning tartibli joylashishini",
        "Anizotropiya",
        "Polikristall",
        "Shisha",
        "Yo‘q,muvozanat atrofida tebranadi",
    ],
}


@pytest.mark.parametrize("seq", range(31, 36))
def test_semantic_every_option_and_order(seq):
    l = load_batch("grade9_batch7")["lessons"][seq - 31]
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
    if seq == 35:
        assert not l["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in l["assessments"]
        )


def test_explicit_oracles_and_all_formula_variants_reject_wrong_units_numbers():
    d = load_batch("grade9_batch7")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 22,
        "formulas": 13,
        "worked_examples": 6,
        "assessments": 35,
        "frq": 13,
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
            assert (
                grade_answer(
                    s, {**a, "unit": "J" if s["dimension"] == "mass" else "kg"}
                )
                == "dimension_mismatch"
            )
            assert grade_answer(s, {**a, "value": "999999"}) == "out_of_tolerance"
            assert grade_answer(s, {**a, "formula": "1"}) == "wrong_formula"
    assert n == 13


@pytest.mark.parametrize(
    "seq,qi,gi,bad",
    [
        (31, 4, 0, "0"),
        (31, 5, 1, "0"),
        (31, 7, 1, "0"),
        (32, 4, 1, "0"),
        (32, 4, 2, "10"),
        (32, 4, 3, "0"),
        (32, 5, 3, "0"),
        (33, 4, 3, "0"),
        (33, 5, 1, "0"),
        (33, 6, 1, "3.14159"),
        (33, 6, 3, "0"),
        (33, 7, 2, "0.5"),
        (33, 7, 1, "3"),
        (33, 8, 0, "0"),
        (34, 4, 0, "0.1"),
        (34, 4, 1, "-0.1"),
        (34, 4, 2, "0"),
        (34, 5, 0, "0"),
    ],
)
def test_nonphysical_inputs_and_source_constants(seq, qi, gi, bad):
    q = deepcopy(load_batch("grade9_batch7")["lessons"][seq - 31]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_exact_rational_rounding_never_uses_truncated_expected_as_truth():
    d = load_batch("grade9_batch7")
    h, r = d["lessons"][1]["assessments"][4:6]
    assert calculation_value(h) == Fraction(73, 4905)
    assert calculation_value(r) == Fraction(73, 98100)
    for q, good, bad in [(h, "14.9", "14.8"), (r, "0.744", "0.745")]:
        f = q["grading_spec"]["formula"]["equivalents"][0]
        assert (
            grade_answer(q["grading_spec"], {"formula": f, "value": good, "unit": "mm"})
            == "correct"
        )
        assert (
            grade_answer(q["grading_spec"], {"formula": f, "value": bad, "unit": "mm"})
            == "out_of_tolerance"
        )


def test_boundary_length_needle_contacts_and_bubble_two_faces_are_distinct():
    d = load_batch("grade9_batch7")
    needle = d["lessons"][2]["assessments"][5]
    assert calculation_value(needle) == Fraction(146, 12500)
    assert (
        grade_answer(
            needle["grading_spec"],
            {"formula": "sigma*l", "value": "5.84", "unit": "mN"},
        )
        == "wrong_formula"
    )
    bubble = d["lessons"][2]["assessments"][7]
    assert calculation_value(bubble) == Fraction(80384, 100000000)
    assert (
        grade_answer(
            bubble["grading_spec"],
            {"formula": "4*pi*sigma*(R2^2-R1^2)", "value": "0.40192", "unit": "mJ"},
        )
        == "wrong_formula"
    )


def test_lab_subtracts_weight_and_coefficients_preserve_force_per_length_units():
    d = load_batch("grade9_batch7")
    lab = d["lessons"][3]
    assert not lab["review"]["physical_experiment_completed"]
    q = lab["assessments"][4]
    assert calculation_value(q) == Fraction(73, 1000)
    for value, unit in [("73", "mN/m"), ("0.073", "J/m2"), ("73", "mJ/m2")]:
        assert (
            grade_answer(
                q["grading_spec"],
                {"formula": "(F2-F1)/2/l", "value": value, "unit": unit},
            )
            == "correct"
        )
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "F2/(2*l)", "value": "0.323", "unit": "N/m"}
        )
        == "wrong_formula"
    )
    assert UNITS["N/m"] == (
        "stiffness",
        Fraction(1),
    )  # legacy spring contract unchanged
    assert UNITS["kN/m"] == ("stiffness", Fraction(1000))
