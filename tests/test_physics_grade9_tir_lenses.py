"""Critical sine vs inequality, prism geometry and signed optics regressions."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    46: [
        "Bir xil vaqt davomida",
        "theta/2",
        "Haqiqiy nurlar ko‘zgu ortiga o‘tib yig‘ilganini",
    ],
    47: ["n1>n2", "Chegaraviy holatni", "O‘zak nqobiqdan katta"],
    48: [
        "Aynan chegaraviy burchak sinusi",
        "Tashqi muhit uchun shunday yaqinlashuv berilganda",
        "n2<1,2",
        "n1>1,6",
        "Yo‘q,qo‘shimcha chegara yoki ma’lumot kerak",
    ],
    49: ["Normal", "Berilgan sinus sonlari", "Berilgan shartli ma’lumot tahlilini"],
    50: ["Manfiy", "Metrda", "Nurlarning orqaga geometrik davomlari kesishishidan"],
}


@pytest.mark.parametrize("seq", range(46, 51))
def test_every_concept_choice_and_order(seq):
    l = load_batch("grade9_batch10")["lessons"][seq - 46]
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


def test_all_literal_oracles_equivalent_formulas_wrong_units_and_values():
    d = load_batch("grade9_batch10")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 22,
        "formulas": 12,
        "worked_examples": 5,
        "assessments": 34,
        "frq": 12,
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
    assert n == 12


@pytest.mark.parametrize(
    "seq,qi,gi,bad",
    [
        (46, 4, 0, "0.5"),
        (46, 4, 2, "0"),
        (46, 4, 2, "80"),
        (46, 5, 1, "1.01"),
        (46, 5, 3, "0"),
        (46, 5, 2, "0.5"),
        (46, 6, 0, "181"),
        (47, 4, 1, "1"),
        (47, 4, 0, "0.5"),
        (48, 6, 1, "0"),
        (48, 6, 1, "1"),
        (48, 7, 2, "0.5"),
        (48, 7, 0, "0"),
        (49, 4, 0, "0.4"),
        (49, 4, 0, "1.1"),
        (49, 4, 1, "0"),
        (49, 5, 1, "0.9"),
        (50, 4, 0, "0"),
        (50, 5, 0, "0"),
        (50, 6, 0, "1"),
        (50, 6, 1, "-12"),
        (50, 6, 2, "0"),
    ],
)
def test_index_sine_angle_and_lens_domain_limits(seq, qi, gi, bad):
    q = deepcopy(load_batch("grade9_batch10")["lessons"][seq - 46]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_tir_observation_is_a_strict_bound_not_a_unique_refractive_index():
    # n1=1.5,sin(alpha)=.8 gives n2<1.2,not n2==1.2.
    # Both distinct outer indices produce no propagating transmitted ray.
    q = deepcopy(load_batch("grade9_batch9")["lessons"][4]["assessments"][9])
    q["public"]["givens"][0]["value"] = "1.5"
    q["public"]["givens"][2]["value"] = "0.8"
    for outer in ("1.05", "1.15"):
        q["public"]["givens"][1]["value"] = outer
        with pytest.raises(ValueError, match="no_transmitted_ray"):
            calculation_value(q)
    q["public"]["givens"][1]["value"] = "1.2"
    assert calculation_value(q) == 1  # grazing critical border,not strictTIR


def test_critical_exact_ratio_rounding_and_outer_medium_factor():
    d = load_batch("grade9_batch10")
    q = d["lessons"][2]["assessments"][6]
    assert calculation_value(q) == Fraction(5, 3)
    f = "n2/sinCrit"
    assert (
        grade_answer(q["grading_spec"], {"formula": f, "value": "1.667", "unit": "1"})
        == "correct"
    )
    assert (
        grade_answer(q["grading_spec"], {"formula": f, "value": "1.666", "unit": "1"})
        == "out_of_tolerance"
    )
    q = deepcopy(d["lessons"][2]["assessments"][7])
    q["public"]["givens"][2]["value"] = "1.5"
    assert calculation_value(q) == 120000000


def test_signed_diverging_lens_does_not_relax_frozen_positive_grade6_model():
    d = load_batch("grade9_batch10")
    q = d["lessons"][4]["assessments"][4]
    assert calculation_value(q) == -5
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "F^-1", "value": "-5", "unit": "1/m"}
        )
        == "correct"
    )
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "1/F", "value": "5", "unit": "dptr"}
        )
        == "sign_error"
    )
    old = deepcopy(q)
    old["grading_spec"]["rule"] = "lens_power"
    with pytest.raises(ValueError):
        calculation_value(old)
    q = deepcopy(d["lessons"][4]["assessments"][5])
    q["public"]["givens"][0]["value"] = "-4"
    assert calculation_value(q) == Fraction(-1, 4)


def test_prism_ratio_uses_specified_normal_entry_sines_and_keeps_lab_digital():
    l = load_batch("grade9_batch10")["lessons"][3]
    assert not l["review"]["physical_experiment_completed"]
    q = l["assessments"][4]
    assert calculation_value(q) == Fraction(3, 2)
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "sinA/sinExit", "value": "1.5", "unit": "1"}
        )
        == "wrong_formula"
    )
    assert calculation_value(l["assessments"][5]) == Fraction(3, 2)
