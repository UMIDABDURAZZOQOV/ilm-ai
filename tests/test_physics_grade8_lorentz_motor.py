"""Literal Lorentz oracles, charge magnitudes and honest digital laboratory scope."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import new_answer

from services.assessment_grading import UNITS, grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    56: [
        "Magnit maydonda harakatlanayotgan zaryadli zarraga",
        "Zaryadning musbat moduli sifatida",
        "Nol",
    ],
    57: [
        "Simli g‘altak va temir o‘zak",
        "Qolgan shartlarni bir xil tutish",
        "Elektromagnit rele",
        "Yo‘q,kontakt turi va sxema ko‘rsatilishi kerak",
        "Tayyor rele holatlarini izohlash",
    ],
    58: [
        "Raqamli sxema va qaydlar tahlili bajarilganini",
        "Magnit ta’sirni kuzatish",
        "Qolgan shartlarni bir xil tutish",
        "Faqat berilgan sifat farqini aytamiz",
        "Yo‘q,tayyor raqamli sxema tahlil qilinadi",
    ],
    59: [
        "Elektr energiyasi mexanik energiyaga",
        "Stator",
        "Ramkadagi tokni mos holatda almashtiradi",
        "Aylanishni ravonroq qilish",
        "Barcha motorlarga bir xil aniq FIK foizini berishdan",
    ],
    60: ["1e-12N", "Modulini", "Yo‘q,tezlik va zaryad ham kerak"],
}


@pytest.mark.parametrize("seq", range(56, 61))
def test_semantic_answers_every_wrong_option_and_order(seq):
    l = load_batch("grade8_batch12")["lessons"][seq - 56]
    qs = [q for q in l["assessments"] if q["response_kind"] == "concept_selection"]
    assert len(qs) == len(KEYS[seq])
    for q, label in zip(qs, KEYS[seq]):
        assert label in [o["label"] for o in q["public"]["options"]]
        for option in q["public"]["options"]:
            assert grade_answer(q["grading_spec"], {"choice_id": option["id"]}) == (
                "correct" if option["label"] == label else "incorrect_concept"
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
    if seq in (57, 58, 59):
        assert not l["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in l["assessments"]
        )


def test_literal_numeric_answers_all_formulas_and_errors():
    doc = load_batch("grade8_batch12")
    assert validate_batch(doc) == {
        "lessons": 5,
        "cards": 22,
        "formulas": 8,
        "worked_examples": 6,
        "assessments": 36,
        "frq": 10,
    }
    count = 0
    for l in doc["lessons"]:
        for q in l["assessments"]:
            s = q["grading_spec"]
            if s["kind"] != "numeric_quantity":
                continue
            count += 1
            answer = new_answer(l, q)
            for f in s["formula"]["equivalents"]:
                assert grade_answer(s, {**answer, "formula": f}) == "correct"
            assert grade_answer(s, {**answer, "unit": "kg"}) == "dimension_mismatch"
            assert (
                grade_answer(s, {**answer, "value": "987654321"}) == "out_of_tolerance"
            )
            assert grade_answer(s, {**answer, "formula": "1"}) == "wrong_formula"
            assert "TIK" in s["formula"]["conditions"]
    assert count == 10


@pytest.mark.parametrize(
    "qi,gi,bad",
    [
        (4, 0, "-1.6e-19"),
        (4, 0, "0"),
        (4, 1, "-3000000"),
        (5, 1, "0"),
        (5, 2, "0"),
        (5, 0, "0"),
        (6, 1, "0"),
        (6, 2, "0"),
        (7, 2, "0"),
        (7, 1, "0"),
    ],
)
def test_positive_charge_magnitudes_and_denominator_domains(qi, gi, bad):
    q = deepcopy(load_batch("grade8_batch12")["lessons"][0]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_pico_not_nano_or_milli_and_negative_force_not_a_magnitude():
    assert UNITS["pN"] == ("force", Fraction(1, 10**12))
    q = load_batch("grade8_batch12")["lessons"][0]["assessments"][4]
    s = q["grading_spec"]
    answer = {"formula": "q*v*B", "value": "0.24", "unit": "pN"}
    assert grade_answer(s, answer) == "correct"
    assert grade_answer(s, {**answer, "unit": "nN"}) == "out_of_tolerance"
    assert grade_answer(s, {**answer, "unit": "mN"}) == "out_of_tolerance"
    assert grade_answer(s, {**answer, "value": "-0.24"}) == "sign_error"


def test_digital_lab_never_records_physical_assembly():
    l = load_batch("grade8_batch12")["lessons"][2]
    assert l["review"]["physical_experiment_completed"] is False
    assert l["review"]["physical_assembly"] == "not_assigned_digital_model_only"
    assert (
        l["review"]["electrical_safety_expert"] == "required_before_general_publication"
    )
    assert "shartli" in l["facts"]["record"]["claim"]


def test_original166_continuation_exact_section_and_required_note():
    doc = load_batch("grade8_batch12")
    ref = doc["lessons"][-1]["source_refs"][-1]
    assert ref["pdf_pages"] == [166]
    assert ref["topic_id"] == "physics-8-section-60"
    assert ref["extent_note"] == "original_image_continues_before_next_heading"
    bad = deepcopy(doc)
    bad["lessons"][-1]["source_refs"][-1].pop("extent_note")
    with pytest.raises(ValueError, match="citation_outside_topic"):
        validate_batch(bad)
    bad = deepcopy(doc)
    bad["lessons"][-1]["source_refs"][-1]["pdf_pages"] = [167]
    with pytest.raises(ValueError):
        validate_batch(bad)
