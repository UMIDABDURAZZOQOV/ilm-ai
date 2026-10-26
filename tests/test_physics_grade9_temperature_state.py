"""Source-based temperature, statistics, rounded roots and closed-gas conditions."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import new_answer

from services.assessment_grading import (
    PositiveSquareRoot,
    expected_quantity,
    grade_answer,
)
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    6: [
        "Kelvindagi absolyut temperatura",
        "Bitta molekulaning o‘rtacha ilgarilanma kinetik energiyasini",
        "Absolyut bosim",
    ],
    7: ["Turli statistik kattaliklar", "Kattalashadi", "Tashqi silindr radiusi"],
    8: [
        "Teng temperaturani",
        "Ikki marta",
        "Bitta molekulaning o‘rtacha ilgarilanma energiyasi",
    ],
    9: [
        "Absolyut p va Kelvin T",
        "Bir xil gazning modda miqdori va tarkibi",
        "Universal gaz doimiysi",
    ],
    10: ["Bir xil gaz miqdorida T o‘zgarmas", "Giperbola", "p1+dp"],
}


@pytest.mark.parametrize("seq", range(6, 11))
def test_semantic_keys_distractors_and_order(seq):
    l = load_batch("grade9_batch2")["lessons"][seq - 6]
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


def test_every_literal_oracle_equivalent_unit_and_formula():
    d = load_batch("grade9_batch2")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 25,
        "formulas": 24,
        "worked_examples": 5,
        "assessments": 44,
        "frq": 24,
    }
    count = 0
    for l in d["lessons"]:
        for q in l["assessments"]:
            s = q["grading_spec"]
            if s["kind"] != "numeric_quantity":
                continue
            count += 1
            a = new_answer(l, q)
            for f in s["formula"]["equivalents"]:
                assert grade_answer(s, {**a, "formula": f}) == "correct", (
                    q["key"],
                    a,
                    f,
                )
            assert (
                grade_answer(
                    s, {**a, "unit": "kg" if s["dimension"] != "mass" else "m"}
                )
                == "dimension_mismatch"
            )
            assert grade_answer(s, {**a, "value": "999999"}) == "out_of_tolerance"
            assert grade_answer(s, {**a, "formula": "1"}) == "wrong_formula"
    assert count == 24


@pytest.mark.parametrize(
    "seq,qi,gi,bad",
    [
        (6, 4, 0, "-273.16"),
        (6, 5, 0, "1.4e-23"),
        (6, 6, 2, "0"),
        (6, 7, 2, "0"),
        (7, 4, 2, "0"),
        (7, 5, 0, "8.30"),
        (7, 5, 2, "0"),
        (7, 6, 1, "0"),
        (7, 7, 1, "6.022e23"),
        (7, 8, 2, "16"),
        (7, 8, 3, "0"),
        (7, 9, 2, "0"),
        (8, 4, 2, "0"),
        (8, 5, 1, "300"),
        (8, 5, 2, "0"),
        (8, 6, 1, "0"),
        (9, 4, 3, "0"),
        (9, 5, 3, "0"),
        (9, 6, 3, "0"),
        (9, 7, 4, "0"),
        (9, 8, 3, "0"),
        (10, 4, 2, "0"),
        (10, 5, 2, "0"),
        (10, 6, 2, "0"),
        (10, 7, 2, "1"),
        (10, 8, 0, "0"),
    ],
)
def test_model_domains_and_constants_do_not_silently_change(seq, qi, gi, bad):
    q = deepcopy(load_batch("grade9_batch2")["lessons"][seq - 6]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_celsius_signed_input_exact27315_and_explicit_kelvin_output():
    d = load_batch("grade9_batch2")
    q = deepcopy(d["lessons"][0]["assessments"][4])
    assert calculation_value(q) == 240
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "theta+273.15", "value": "240", "unit": "K"}
        )
        == "correct"
    )
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "theta+273", "value": "239.85", "unit": "K"}
        )
        == "wrong_formula"
    )
    assert (
        grade_answer(
            q["grading_spec"],
            {"formula": "theta+273.15", "value": "-33.15", "unit": "°C"},
        )
        == "dimension_mismatch"
    )
    q["public"]["givens"][0]["value"] = "-273.15"
    assert calculation_value(q) == 0
    q["public"]["givens"][0]["unit"] = "C"
    with pytest.raises(ValueError):
        calculation_value(q)  # Coulomb is not Celsius.


def test_source_rounded_roots_have_exact_radicands_and_last_step_grid():
    l = load_batch("grade9_batch2")["lessons"][1]
    for qi, radicand, correct, wrong in [
        (4, 414000, "643.4", "643.5"),
        (5, 249300, "499.3", "499.2"),
    ]:
        q = l["assessments"][qi]
        s = q["grading_spec"]
        assert expected_quantity(s) == PositiveSquareRoot(Fraction(radicand))
        assert calculation_value(q) == PositiveSquareRoot(Fraction(radicand))
        assert (
            grade_answer(
                s,
                {
                    "formula": s["formula"]["equivalents"][0],
                    "value": correct,
                    "unit": "m/s",
                },
            )
            == "correct"
        )
        assert (
            grade_answer(
                s,
                {
                    "formula": s["formula"]["equivalents"][0],
                    "value": wrong,
                    "unit": "m/s",
                },
            )
            == "out_of_tolerance"
        )
        assert (
            grade_answer(
                s,
                {
                    "formula": s["formula"]["equivalents"][0],
                    "value": correct + "1",
                    "unit": "m/s",
                },
            )
            == "rounding_requirement"
        )
    spec = l["assessments"][9]["grading_spec"]
    assert expected_quantity(spec) == Fraction(800000, 2493)
    assert (
        grade_answer(spec, {"formula": "M*v^2/(3*R)", "value": "320.9", "unit": "K"})
        == "correct"
    )


def test_changed_private_root_radicand_and_rounding_are_not_reviewed():
    d = load_batch("grade9_batch2")
    bad = deepcopy(d)
    bad["lessons"][1]["assessments"][4]["grading_spec"]["expected_root_rational"][
        "numerator"
    ] = "413000"
    with pytest.raises(ValueError, match="calculation_answer_mismatch"):
        validate_batch(bad)
    bad = deepcopy(d)
    bad["lessons"][1]["assessments"][4]["grading_spec"]["expected_si"] = "643.5"
    with pytest.raises(ValueError, match="authored_answer_does_not_grade"):
        validate_batch(bad)
    bad = deepcopy(d)
    bad["lessons"][1]["assessments"][4]["grading_spec"]["abs_tol_si"] = "0.1"
    with pytest.raises(ValueError, match="authored_answer_does_not_grade"):
        validate_batch(bad)


def test_all_pressure_rules_state_absolute_and_isothermal_same_gas():
    d = load_batch("grade9_batch2")
    for l in d["lessons"][-2:]:
        for q in l["assessments"]:
            s = q["grading_spec"]
            if s["kind"] == "numeric_quantity":
                conditions = s["formula"]["conditions"].upper()
                assert "ABSOLUTE" in conditions or "ISOTHERMAL" in conditions

    assert all(not l["review"]["physical_experiment_completed"] for l in d["lessons"])
