"""Explicit G/g, distinct bodies/support, contact and projectile projections."""

from copy import deepcopy

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    26: ["Modullari teng", "To‘rt marta kamayadi", "Massalar markazlari oralig‘ini"],
    27: ["Yer tortayotgan jismga", "Bir xil", "Turli kattaliklar"],
    28: ["Tayanch yoki osmaga", "N", "Vertikal a=0"],
    29: ["Yuqoriga yo‘nalgan tezlanish moduli", "Nol bo‘lmasligi mumkin", "P/(m*g)"],
    30: ["Gorizontal", "R+h", "Ayni aylana orbita radiusidagi"],
}


@pytest.mark.parametrize("seq", range(26, 31))
def test_gravity_concepts_wrong_choices_and_source_pages(seq):
    l = load_batch("grade7_batch6")["lessons"][seq - 26]
    qs = [q for q in l["assessments"] if q["response_kind"] == "concept_selection"]
    assert len(qs) == len(KEYS[seq])
    for q, label in zip(qs, KEYS[seq]):
        assert label in [o["label"] for o in q["public"]["options"]]
        for o in q["public"]["options"]:
            assert grade_answer(q["grading_spec"], {"choice_id": o["id"]}) == (
                "correct" if o["label"] == label else "incorrect_concept"
            )


def test_gravity_independent_oracles_constants_and_contact_domains():
    doc = load_batch("grade7_batch6")
    assert validate_batch(doc) == {
        "lessons": 5,
        "cards": 20,
        "formulas": 11,
        "worked_examples": 5,
        "assessments": 31,
        "frq": 16,
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
    assert count == 16
    for li, qi, gi, bad in [
        (0, 3, 0, "1"),
        (0, 3, 3, "0"),
        (1, 3, 1, "1"),
        (3, 4, 2, "11"),
        (4, 5, 3, "-1"),
        (4, 6, 1, "0"),
    ]:
        q = deepcopy(doc["lessons"][li]["assessments"][qi])
        q["public"]["givens"][gi]["value"] = bad
        with pytest.raises(ValueError):
            calculation_value(q)
    free = doc["lessons"][3]["assessments"][6]
    assert calculation_value(free) == 0
    # G cannot be supplied as dimensionless, even with matching numeric digits.
    q = deepcopy(doc["lessons"][0]["assessments"][3])
    q["public"]["givens"][0]["unit"] = "1"
    with pytest.raises(ValueError):
        calculation_value(q)
