"""Independent humidity units, sourced table cells and geometrical optics."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    41: ["Havodagi suv bug‘ining massasi", "Suv bug‘ining parsial bosimi", "60%"],
    42: [
        "62%",
        "Quruq termometr ko‘rsatkichi bo‘yicha",
        "Shartli ko‘rsatkich va jadval tahlilini",
    ],
    43: [
        "Suv bug‘ining parsial bosimi",
        "Suv bug‘ining massasi",
        "Havoning hozirgi temperaturasiga",
    ],
    44: ["2*l", "Aylanish chastotasi Hz", "Maktab yaqinlashuvi va aniq SI qiymati"],
    45: [
        "Sirt normalidan",
        "Muhitning absolyut sindirish ko‘rsatkichi",
        "Yo‘q,bu aniqlash uchun yaroqli nisbat emas",
    ],
}


@pytest.mark.parametrize("seq", range(41, 46))
def test_semantic_every_choice_and_order(seq):
    l = load_batch("grade9_batch9")["lessons"][seq - 41]
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


def test_independent_literal_oracles_equivalent_formulas_and_wrong_answers():
    d = load_batch("grade9_batch9")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 24,
        "formulas": 21,
        "worked_examples": 5,
        "assessments": 41,
        "frq": 21,
    }
    count = 0
    for l in d["lessons"]:
        for q in l["assessments"]:
            s = q["grading_spec"]
            if s["kind"] != "numeric_quantity":
                continue
            count += 1
            a = new_answer(l, q)
            assert grade_answer(s, a) == "correct", q["key"]
            for f in s["formula"]["equivalents"]:
                assert grade_answer(s, {**a, "formula": f}) == "correct"
            assert grade_answer(s, {**a, "unit": "kg"}) == "dimension_mismatch"
            assert grade_answer(s, {**a, "value": "999999"}) == "out_of_tolerance"
            assert grade_answer(s, {**a, "formula": "1"}) == "wrong_formula"
    assert count == 21


@pytest.mark.parametrize(
    "seq,qi,gi,bad",
    [
        (41, 4, 1, "0"),
        (41, 5, 0, "18"),
        (41, 5, 1, "0"),
        (41, 6, 0, "3"),
        (41, 7, 0, "101"),
        (42, 4, 1, "25"),
        (42, 5, 1, "0"),
        (43, 4, 0, "-1"),
        (43, 5, 0, "0"),
        (43, 5, 1, "0"),
        (43, 5, 2, "8.30"),
        (43, 5, 3, "0"),
        (43, 6, 0, "80"),
        (43, 7, 0, "101"),
        (44, 4, 1, "0"),
        (44, 5, 1, "-0.25"),
        (44, 6, 0, "0"),
        (44, 7, 0, "500.5"),
        (44, 7, 2, "0"),
        (44, 8, 1, "-600"),
        (44, 8, 2, "0"),
        (45, 4, 0, "91"),
        (45, 5, 0, "-1"),
        (45, 6, 1, "4e8"),
        (45, 7, 1, "0.5"),
        (45, 8, 1, "0"),
        (45, 8, 0, "1.01"),
        (45, 9, 2, "0.8"),
    ],
)
def test_domain_saturation_angles_teeth_counts_and_transmitted_ray(seq, qi, gi, bad):
    q = deepcopy(load_batch("grade9_batch9")["lessons"][seq - 41]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_partial_pressure_density_and_percent_are_different_dimensions():
    d = load_batch("grade9_batch9")
    q = d["lessons"][0]["assessments"][5]
    assert calculation_value(q) == Fraction(1, 2)
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "rho/rhoSat", "value": "50", "unit": "%"}
        )
        == "correct"
    )
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "rho/rhoSat", "value": "50", "unit": "1"}
        )
        == "out_of_tolerance"
    )
    q = deepcopy(d["lessons"][0]["assessments"][6])
    q["public"]["givens"][0]["unit"] = "g/m3"
    with pytest.raises(ValueError):
        calculation_value(q)
    assert calculation_value(d["lessons"][1]["assessments"][5]) == Fraction(
        13516, 1000000
    )
    assert calculation_value(d["lessons"][2]["assessments"][5]) == Fraction(12, 1000)


def test_degree_angles_are_not_radians_and_sines_are_not_angle_inputs():
    d = load_batch("grade9_batch9")
    q = d["lessons"][4]["assessments"][4]
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "alpha", "value": "35", "unit": "deg"}
        )
        == "correct"
    )
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "alpha", "value": "35", "unit": "rad"}
        )
        == "dimension_mismatch"
    )
    q = deepcopy(q)
    q["public"]["givens"][0]["unit"] = "rad"
    with pytest.raises(ValueError):
        calculation_value(q)
    q = d["lessons"][4]["assessments"][9]
    assert calculation_value(q) == Fraction(3, 5)
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "n1*sina/n2", "value": "0.6", "unit": "1"}
        )
        == "correct"
    )
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "n1*sina/n2", "value": "0.6", "unit": "deg"}
        )
        == "dimension_mismatch"
    )


def test_fizeau_frequency_is_rotation_and_one_way_distance_requires_round_trip():
    d = load_batch("grade9_batch9")
    q = d["lessons"][3]["assessments"][6]
    assert calculation_value(q) == Fraction(1, 5000)
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "l/c", "value": "0.0001", "unit": "s"}
        )
        == "wrong_formula"
    )
    q = d["lessons"][3]["assessments"][7]
    assert calculation_value(q) == 300000000
    q = deepcopy(q)
    q["public"]["givens"][2]["unit"] = "rad/s"
    with pytest.raises(ValueError):
        calculation_value(q)


def test_section43_continuation_only_before_chapter_review():
    d = load_batch("grade9_batch9")
    l = d["lessons"][2]
    assert any(
        126 in r["pdf_pages"]
        and r.get("extent_note") == "original_image_continues_before_next_heading"
        for r in l["source_refs"]
    )
    bad = deepcopy(d)
    for r in bad["lessons"][2]["source_refs"]:
        if 126 in r["pdf_pages"]:
            r.pop("extent_note")
    with pytest.raises(ValueError):
        validate_batch(bad)
