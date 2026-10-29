"""Newton body identity, inward force and small-deformation spring domains."""

from copy import deepcopy

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    21: ["Bir jismga ta’sir qiluvchi natijaviy kuch", "Uch marta ortadi", "a=0"],
    22: [
        "Turli jismlarga",
        "Teng",
        "Chunki turli jismlarga qo‘yilgan",
        "Bir xil o‘zaro ta’sir vaqti va dastlab tinchlik",
    ],
    23: ["Markazga", "Ipga", "Urinma bo‘ylab"],
    24: [
        "Elastik",
        "Uzayish yoki siqilishning moduli",
        "Kichik chiziqli elastik deformatsiya doirasida",
        "Ikki marta katta",
    ],
    25: [
        "Yuksiz dastlabki ko‘rsatkichdan",
        "10m/s2",
        "Berilgan qayd va hisoblar tahlil qilinganini",
    ],
}


@pytest.mark.parametrize("seq", range(21, 26))
def test_newton_spring_semantic_keys_and_wrong_choices(seq):
    lesson = load_batch("grade7_batch5")["lessons"][seq - 21]
    qs = [q for q in lesson["assessments"] if q["response_kind"] == "concept_selection"]
    assert len(qs) == len(KEYS[seq])
    for q, label in zip(qs, KEYS[seq]):
        assert label in [o["label"] for o in q["public"]["options"]]
        for o in q["public"]["options"]:
            assert grade_answer(q["grading_spec"], {"choice_id": o["id"]}) == (
                "correct" if o["label"] == label else "incorrect_concept"
            )
    if seq == 25:
        assert lesson["review"]["physical_experiment_completed"] is False
        assert (
            grade_answer(
                lesson["assessments"][3]["grading_spec"], {"order": ["s2", "s3", "s1"]}
            )
            == "correct"
        )


def test_independent_newton_spring_oracles_and_denominator_boundaries():
    doc = load_batch("grade7_batch5")
    assert validate_batch(doc) == {
        "lessons": 5,
        "cards": 22,
        "formulas": 12,
        "worked_examples": 5,
        "assessments": 35,
        "frq": 17,
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
    assert count == 17
    for li, qi, gi, bad in [
        (0, 3, 1, "0"),
        (0, 5, 1, "0"),
        (1, 5, 2, "0"),
        (2, 3, 2, "0"),
        (3, 5, 1, "0"),
        (3, 6, 1, "0"),
        (3, 7, 2, "0"),
        (4, 4, 1, "9.81"),
        (4, 4, 2, "0"),
    ]:
        q = deepcopy(doc["lessons"][li]["assessments"][qi])
        q["public"]["givens"][gi]["value"] = bad
        with pytest.raises(ValueError):
            calculation_value(q)
    # Unit spelling denotes stiffness, not force or pressure.
    q = doc["lessons"][3]["assessments"][5]
    a = new_answer(doc["lessons"][3], q)
    for unit in ["N", "Pa", "N*m"]:
        assert (
            grade_answer(q["grading_spec"], {**a, "unit": unit}) == "dimension_mismatch"
        )
