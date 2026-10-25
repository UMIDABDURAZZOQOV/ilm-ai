"""Signed momentum/work without relaxing positive magnitude domains elsewhere."""

from copy import deepcopy

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    36: [
        "Kuch va ta’sir vaqtiga",
        "Tezlik yo‘nalishi",
        "Natijaviy kuch impulsi o‘zgarmas massali jism dp siga teng",
    ],
    37: [
        "Jami impulsning vektor yig‘indisi",
        "Yopishib birga ketishga",
        "Qarama-qarshi ishoralar bilan",
    ],
    38: [
        "Chiqqan qismnikiga qarama-qarshi",
        "v bilan bir xil inertial sanoq sistemasida",
        "Yo‘q, bu cheklangan ikki qismli model",
    ],
    39: ["Nol", "Manfiy", "Ko‘chish yo‘nalishidagi kuch proyeksiyasi"],
    40: [
        "Ko‘taruvchi kuchning",
        "Nol, kuch ko‘chishga tik",
        "Yo‘q, kuchlar ham hisobga olinadi",
    ],
}


@pytest.mark.parametrize("seq", range(36, 41))
def test_momentum_work_concept_labels_and_wrong_choices(seq):
    l = load_batch("grade7_batch8")["lessons"][seq - 36]
    qs = [q for q in l["assessments"] if q["response_kind"] == "concept_selection"]
    assert len(qs) == len(KEYS[seq])
    for q, label in zip(qs, KEYS[seq]):
        assert label in [o["label"] for o in q["public"]["options"]]
        for o in q["public"]["options"]:
            assert grade_answer(q["grading_spec"], {"choice_id": o["id"]}) == (
                "correct" if o["label"] == label else "incorrect_concept"
            )
    if seq == 40:
        assert l["review"]["physical_experiment_completed"] is False
        assert (
            grade_answer(
                l["assessments"][3]["grading_spec"], {"order": ["s2", "s3", "s1"]}
            )
            == "correct"
        )


def test_signed_independent_oracles_and_strict_mass_time_distance_domains():
    doc = load_batch("grade7_batch8")
    assert validate_batch(doc) == {
        "lessons": 5,
        "cards": 22,
        "formulas": 9,
        "worked_examples": 5,
        "assessments": 34,
        "frq": 18,
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
    assert count == 18
    for li, qi, gi, bad in [
        (0, 3, 1, "-1"),
        (0, 4, 0, "0"),
        (1, 4, 2, "0"),
        (2, 3, 2, "0"),
        (3, 3, 1, "-1"),
        (4, 4, 0, "-1"),
    ]:
        q = deepcopy(doc["lessons"][li]["assessments"][qi])
        q["public"]["givens"][gi]["value"] = bad
        with pytest.raises(ValueError):
            calculation_value(q)
    # Negative momentum is a component, not a negative mass or time.
    q = doc["lessons"][0]["assessments"][4]
    a = new_answer(doc["lessons"][0], q)
    assert grade_answer(q["grading_spec"], {**a, "value": "2"}) == "sign_error"
    q = doc["lessons"][3]["assessments"][4]
    a = new_answer(doc["lessons"][3], q)
    assert grade_answer(q["grading_spec"], {**a, "value": "20"}) == "sign_error"
    assert calculation_value(doc["lessons"][1]["assessments"][6]) == 0
