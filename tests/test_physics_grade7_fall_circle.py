"""Source-reviewed displacement/path, digital lab, flight and radian quantities."""

from copy import deepcopy

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    11: ["4marta", "Parabola", "To‘xtashgacha, yo‘nalish almashmaguncha"],
    12: [
        "Tinch holatdan",
        "Har qayd uchun alohida a1,a2,a3",
        "Berilgan qaydlar va reja tahlil qilindi",
    ],
    13: ["Bir xil g tezlanish bilan", "Berilgan10 ni ishlatamiz", "v0=0"],
    14: [
        "Oniy tezlik",
        "Manfiy",
        "Havosiz doimiy g va bir xil boshlash/qaytish sathida",
    ],
    15: [
        "Moduli bir xil, yo‘nalishi o‘zgaradi",
        "Yoy uzunligini",
        "Bir xil vaqt ichida bir xil burilish burchagini",
    ],
}


@pytest.mark.parametrize("seq", range(11, 16))
def test_fall_circle_concepts_and_all_wrong_choices(seq):
    l = load_batch("grade7_batch3")["lessons"][seq - 11]
    qs = [q for q in l["assessments"] if q["response_kind"] == "concept_selection"]
    assert len(qs) == len(KEYS[seq])
    for q, label in zip(qs, KEYS[seq]):
        assert label in [o["label"] for o in q["public"]["options"]]
        for o in q["public"]["options"]:
            assert grade_answer(q["grading_spec"], {"choice_id": o["id"]}) == (
                "correct" if o["label"] == label else "incorrect_concept"
            )
    if seq == 12:
        q = l["assessments"][3]
        assert (
            grade_answer(q["grading_spec"], {"order": ["s2", "s3", "s1"]}) == "correct"
        )
        assert l["review"]["physical_experiment_completed"] is False


def test_numeric_oracles_gravity_flight_and_angle_domains():
    doc = load_batch("grade7_batch3")
    assert validate_batch(doc) == {
        "lessons": 5,
        "cards": 20,
        "formulas": 11,
        "worked_examples": 5,
        "assessments": 31,
        "frq": 15,
    }
    count = 0
    for l in doc["lessons"]:
        for q in l["assessments"]:
            spec = q["grading_spec"]
            if spec["kind"] != "numeric_quantity":
                continue
            a = new_answer(l, q)
            count += 1
            for f in spec["formula"]["equivalents"]:
                assert grade_answer(spec, {**a, "formula": f}) == "correct"
            assert grade_answer(spec, {**a, "unit": "kg"}) == "dimension_mismatch"
            assert grade_answer(spec, {**a, "value": "123456789"}) == "out_of_tolerance"
            assert grade_answer(spec, {**a, "formula": "1"}) == "wrong_formula"
    assert count == 15
    # Gravity model, observation time, flight interval and radius are explicit.
    for li, qi, gi, bad in [
        (2, 3, 1, "11"),
        (1, 4, 1, "0"),
        (3, 4, 2, "7"),
        (4, 3, 1, "0"),
        (0, 5, 2, "8"),
    ]:
        q = deepcopy(doc["lessons"][li]["assessments"][qi])
        q["public"]["givens"][gi]["value"] = bad
        with pytest.raises(ValueError):
            calculation_value(q)
    q = doc["lessons"][3]["assessments"][4]
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "v0-g*t", "value": "10", "unit": "m/s"}
        )
        == "sign_error"
    )
    q = doc["lessons"][4]["assessments"][4]
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "phi/t", "value": "4", "unit": "Hz"}
        )
        == "dimension_mismatch"
    )
