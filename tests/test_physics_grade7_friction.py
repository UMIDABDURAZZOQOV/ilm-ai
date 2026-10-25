"""Static threshold, relative slip, dimensional rolling coefficient and lab refs."""

from copy import deepcopy

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    31: [
        "Inson yaratib orbitaga chiqarishi",
        "R+h",
        "Ob-havo kuzatuvi va aloqa",
        "Taxminiy misol, universal minimum emas",
    ],
    32: [
        "Ha, nisbiy sirpanishga qarshi",
        "Yo‘q, talab etilgan qiymatga moslashadi",
        "Molekulalar o‘zaro ta’siri sabab",
    ],
    33: ["Sirtga tik", "Uzunlik birligi", "Ikki marta kamayadi"],
    34: ["Tekis sirpanishdagi", "Taxtacha va yukning umumiy massasini", "Yo‘q"],
    35: [
        "Foydali ilashish beradi",
        "Mos moylash va podshipnik",
        "Dumalashdan",
        "To‘rt marta ortadi",
        "Ba’zi kontaktlarda ilashish foydali",
    ],
}


@pytest.mark.parametrize("seq", range(31, 36))
def test_friction_source_concept_keys_and_wrong_options(seq):
    l = load_batch("grade7_batch7")["lessons"][seq - 31]
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


def test_friction_oracles_static_boundary_and_lab_reference_correction():
    doc = load_batch("grade7_batch7")
    assert validate_batch(doc) == {
        "lessons": 5,
        "cards": 22,
        "formulas": 7,
        "worked_examples": 5,
        "assessments": 31,
        "frq": 10,
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
    assert count == 10
    for li, qi, gi, bad in [
        (0, 5, 2, "7000000"),
        (1, 3, 0, "10"),
        (2, 3, 1, "0"),
        (2, 5, 2, "0"),
        (3, 4, 1, "0"),
        (3, 4, 2, "9.8"),
    ]:
        q = deepcopy(doc["lessons"][li]["assessments"][qi])
        q["public"]["givens"][gi]["value"] = bad
        with pytest.raises(ValueError):
            calculation_value(q)
    assert calculation_value(doc["lessons"][1]["assessments"][4]) == 8
    q = deepcopy(doc["lessons"][2]["assessments"][5])
    q["public"]["givens"][0]["unit"] = "1"
    with pytest.raises(ValueError):
        calculation_value(q)
    lab = doc["lessons"][3]
    assert lab["review"]["physical_experiment_completed"] is False
    assert any(
        r["topic_id"] == "physics-7-section-33" and r["pdf_pages"] == [112]
        for r in lab["facts"]["mu"]["source_refs"]
    )
