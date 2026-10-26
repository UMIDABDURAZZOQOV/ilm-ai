"""Independent heat-engine balance, reversible-limit and source-scope checks."""

import json
from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import (
    DIRECTORY,
    calculation_value,
    load_batch,
    validate_batch,
)

KEYS = {
    26: [
        "Yoqilg‘i silindr ichida yonishiga",
        "Siqilgan havo",
        "Shatun",
        "Ishga kerakli moddalarni o‘zida olib ketishi",
        "Aniq quvvat va FIK sonini",
    ],
    27: [
        "Nol",
        "A/Qh nisbatining maxrajida",
        "Ikki rezervuar orasidagi qaytar Karno maksimumini",
    ],
    28: [
        "A+Qc",
        "Kelvindagi absolyut qiymatlar",
        "Yo‘q,bu yerda qaytar Karno sharti kerak",
    ],
    29: [
        "Yo‘q",
        "Atmosferaga gaz chiqmayotganini",
        "Yo‘q,joriy dalil bo‘lmasa bunday da’vo qilmaymiz",
        "Quyosh energiyasidan foydalanish",
        "Tirik organizmlarni zararli qisqa to‘lqinli nurlanishdan himoyalash",
    ],
    30: ["Berilgan foydali chiqish quvvati", "eta*mf*q", "rho*V"],
}


@pytest.mark.parametrize("seq", range(26, 31))
def test_semantic_choices_and_complete_carnot_order(seq):
    l = load_batch("grade9_batch6")["lessons"][seq - 26]
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
            order = ["s2", "s4", "s1", "s3"] if seq == 27 else ["s2", "s3", "s1"]
            assert grade_answer(q["grading_spec"], {"order": order}) == "correct"
            assert (
                grade_answer(q["grading_spec"], {"order": list(reversed(order))})
                != "correct"
            )
    if seq in (26, 29):
        assert not l["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in l["assessments"]
        )


def test_all_numeric_oracles_alternative_formulas_prefixes_and_wrong_responses():
    d = load_batch("grade9_batch6")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 21,
        "formulas": 13,
        "worked_examples": 5,
        "assessments": 37,
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
            assert grade_answer(s, a) == "correct"
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
        (27, 4, 0, "0"),
        (27, 4, 1, "-1"),
        (27, 4, 1, "2"),
        (27, 5, 1, "5"),
        (27, 6, 0, "300"),
        (27, 6, 1, "0"),
        (27, 6, 1, "-300"),
        (27, 7, 1, "100"),
        (27, 7, 1, "0"),
        (27, 7, 1, "-1"),
        (28, 4, 0, "0"),
        (28, 5, 1, "1"),
        (28, 5, 1, "0"),
        (28, 6, 0, "100"),
        (28, 7, 2, "-2400"),
        (28, 8, 0, "0"),
        (28, 8, 2, "900"),
        (30, 4, 0, "0"),
        (30, 4, 2, "0"),
        (30, 4, 3, "1"),
        (30, 5, 0, "100"),
        (30, 5, 3, "0"),
        (30, 5, 4, "0"),
        (30, 6, 5, "0"),
        (30, 6, 4, "-25"),
        (30, 7, 2, "1"),
        (30, 7, 3, "0"),
    ],
)
def test_nonphysical_or_degenerate_engine_inputs_rejected(seq, qi, gi, bad):
    q = deepcopy(load_batch("grade9_batch6")["lessons"][seq - 26]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_same_temperature_difference_is_not_same_carnot_efficiency():
    q = deepcopy(load_batch("grade9_batch6")["lessons"][1]["assessments"][6])
    assert calculation_value(q) == Fraction(1, 2)  # 600K / 300K
    q["public"]["givens"][0]["value"] = "1200"
    q["public"]["givens"][1]["value"] = "900"
    assert calculation_value(q) == Fraction(1, 4)  # same 300K difference
    # Celsius numbers are not interchangeable with absolute Kelvin ratios.
    q["public"]["givens"][0]["unit"] = "°C"
    with pytest.raises(ValueError):
        calculation_value(q)


def test_percent_fraction_and_balance_denominator_are_distinct():
    d = load_batch("grade9_batch6")
    q = d["lessons"][1]["assessments"][5]
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "1-Qc/Qh", "value": "40", "unit": "%"}
        )
        == "correct"
    )
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "1-Qc/Qh", "value": "0.4", "unit": "1"}
        )
        == "correct"
    )
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "1-Qc/Qh", "value": "40", "unit": "1"}
        )
        == "out_of_tolerance"
    )
    q = d["lessons"][2]["assessments"][4]
    assert (
        grade_answer(q["grading_spec"], {"formula": "A/Qc", "value": "40", "unit": "%"})
        == "wrong_formula"
    )
    assert calculation_value(q) == Fraction(2, 5)


def test_scope_review_notes_preserve_historical_and_scientific_uncertainties():
    r = json.loads((DIRECTORY / "grade9_batch6_review.json").read_text())
    notes = " ".join(x["decision"] for x in r["scientific_decisions"])
    assert "temperature difference" in notes and "denominator Th" in notes
    assert "kerosene46MJ/kg" in notes and "table66kerosene42" in notes
    assert not r["ready_for_general_publication"]
    assert r["independent_subject_expert"] == "not_claimed"
    assert [p["pdf_page"] for p in r["pages"]] == list(range(81, 91))
