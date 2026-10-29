"""Conservative conditions, signed work and distinct input/useful power."""

from copy import deepcopy

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    41: [
        "Tanlangan nol sathga",
        "Manfiy",
        "O‘zaro ta’sir qiluvchi jismlarning nisbiy vaziyatiga",
    ],
    42: ["To‘rt marta ortadi", "Manfiy", "Ek bir xil bo‘ladi"],
    43: [
        "So‘nish va hisobga olinmagan tashqi ish yo‘q",
        "Ek ortadi",
        "Muvozanatdan deformatsiya moduli",
        "Berilgan holat modelga mos emas",
    ],
    44: [
        "Tezlik moduli",
        "Tinch boshlash va doimiy tezlanish",
        "Berilgan qaydlar tahlil qilinganini",
    ],
    45: ["Ikki marta katta", "W", "Harakat tomonidagi kuch uchun"],
    46: [
        "Ichki/issiqlik energiyaga aylanishni",
        "Kirish yoki sarflangan jami ish",
        "75%",
        "Berilganlar, birliklar va kirish/chiqish ta’rifini qayta tekshiramiz",
    ],
}


@pytest.mark.parametrize("seq", range(41, 47))
def test_energy_semantic_keys_and_wrong_choices(seq):
    l = load_batch("grade7_batch9")["lessons"][seq - 41]
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
    if seq == 44:
        assert l["review"]["physical_experiment_completed"] is False


def test_energy_independent_oracles_domain_and_case_sensitive_power_units():
    doc = load_batch("grade7_batch9")
    assert validate_batch(doc) == {
        "lessons": 6,
        "cards": 26,
        "formulas": 17,
        "worked_examples": 7,
        "assessments": 43,
        "frq": 21,
    }
    count = 0
    for l in doc["lessons"]:
        for q in l["assessments"]:
            spec = q["grading_spec"]
            if spec["kind"] != "numeric_quantity":
                continue
            count += 1
            a = new_answer(l, q)
            for f in spec["formula"]["equivalents"]:
                assert grade_answer(spec, {**a, "formula": f}) == "correct"
            assert grade_answer(spec, {**a, "unit": "s"}) == "dimension_mismatch"
            assert grade_answer(spec, {**a, "value": "123456789"}) == "out_of_tolerance"
            assert grade_answer(spec, {**a, "formula": "1"}) == "wrong_formula"
    assert count == 21
    for li, qi, gi, bad in [
        (0, 3, 1, "0"),
        (1, 3, 1, "-3"),
        (2, 5, 0, "0"),
        (2, 6, 2, "40"),
        (3, 4, 1, "0"),
        (4, 3, 1, "0"),
        (4, 6, 1, "0"),
        (5, 5, 0, "300"),
        (5, 6, 0, "101"),
        (5, 7, 3, "1"),
    ]:
        q = deepcopy(doc["lessons"][li]["assessments"][qi])
        q["public"]["givens"][gi]["value"] = bad
        with pytest.raises(ValueError):
            calculation_value(q)
    q = doc["lessons"][4]["assessments"][3]
    a = new_answer(doc["lessons"][4], q)
    assert (
        grade_answer(q["grading_spec"], {**a, "value": "300000", "unit": "mW"})
        == "correct"
    )
    assert grade_answer(q["grading_spec"], {**a, "unit": "mw"}) == "unknown_unit"
    # End-of-book engineering count and input power don't alter old grade-six rubric.
    assert len(doc["lessons"]) == 6
