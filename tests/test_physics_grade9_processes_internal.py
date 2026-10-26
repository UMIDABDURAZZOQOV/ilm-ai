"""Fixed-gas conditions, effective digital models and signed monatomic energy."""

from copy import deepcopy

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    11: ["Bosim", "Kelvin temperaturasi", "T1-T2 musbat farqi"],
    12: ["Hajm", "Absolyut bosim", "Hajm mutlaqo o‘zgarmasligini"],
    13: [
        "Shartli raqamli modellar tahlil qilinganini",
        "Samarali qatlam qalinligi bahosi",
        "n son konsentratsiyasi,rho massa zichligi",
    ],
    14: [
        "0,6",
        "Bosimning dastlabkiga nisbiy ortishini",
        "Bir xil temperatura va saqlangan gaz miqdori modeli",
    ],
    15: ["Bir atomli klassik ideal gaz", "U2-U1", "Manfiy"],
}


@pytest.mark.parametrize("seq", range(11, 16))
def test_semantic_keys_every_distractor_and_order(seq):
    l = load_batch("grade9_batch3")["lessons"][seq - 11]
    qs = [q for q in l["assessments"] if q["response_kind"] == "concept_selection"]
    assert len(qs) == len(KEYS[seq])
    for q, label in zip(qs, KEYS[seq]):
        assert label in [o["label"] for o in q["public"]["options"]]
        for opt in q["public"]["options"]:
            assert grade_answer(q["grading_spec"], {"choice_id": opt["id"]}) == (
                "correct" if opt["label"] == label else "incorrect_concept"
            )
    for q in l["assessments"]:
        if q["response_kind"] == "ordering":
            assert (
                grade_answer(q["grading_spec"], {"order": ["s2", "s3", "s1"]})
                == "correct"
            )
            assert (
                grade_answer(q["grading_spec"], {"order": ["s1", "s3", "s2"]})
                != "correct"
            )


def test_all_independent_literals_alternatives_units_and_errors():
    d = load_batch("grade9_batch3")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 24,
        "formulas": 22,
        "worked_examples": 5,
        "assessments": 42,
        "frq": 22,
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
            assert grade_answer(s, {**a, "unit": "kg"}) == "dimension_mismatch"
            assert grade_answer(s, {**a, "value": "999999"}) == "out_of_tolerance"
            assert grade_answer(s, {**a, "formula": "1"}) == "wrong_formula"
    assert count == 22


@pytest.mark.parametrize(
    "seq,qi,gi,bad",
    [
        (11, 4, 2, "0"),
        (11, 5, 2, "0"),
        (11, 6, 1, "20"),
        (11, 7, 1, "4"),
        (12, 4, 2, "0"),
        (12, 5, 2, "0"),
        (12, 6, 2, "320"),
        (13, 4, 1, "0"),
        (13, 5, 1, "0"),
        (13, 5, 1, "2.5"),
        (13, 6, 0, "0"),
        (13, 7, 1, "32"),
        (13, 7, 3, "0"),
        (13, 8, 2, "0"),
        (13, 9, 1, "0"),
        (14, 4, 0, "1.01"),
        (14, 4, 0, "-0.1"),
        (14, 4, 3, "0"),
        (14, 5, 2, "0"),
        (14, 6, 1, "0"),
        (14, 7, 1, "9.81"),
        (14, 8, 0, "0.9"),
        (15, 4, 1, "8.3"),
        (15, 5, 3, "0"),
        (15, 6, 1, "0"),
        (15, 7, 0, "0"),
    ],
)
def test_condition_and_measurement_domains(seq, qi, gi, bad):
    q = deepcopy(load_batch("grade9_batch3")["lessons"][seq - 11]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_negative_energy_change_keeps_sign_and_unit_conversion():
    q = load_batch("grade9_batch3")["lessons"][-1]["assessments"][5]
    s = q["grading_spec"]
    assert (
        grade_answer(
            s, {"formula": "3*nu*R*(T2-T1)/2", "value": "-3739.5", "unit": "J"}
        )
        == "correct"
    )
    assert (
        grade_answer(
            s, {"formula": "3*nu*R*(T2-T1)/2", "value": "3.7395", "unit": "kJ"}
        )
        == "sign_error"
    )
    q = deepcopy(q)
    q["public"]["givens"][2]["value"] = "350"
    q["public"]["givens"][3]["value"] = "250"
    assert calculation_value(q) == 3739.5
    # Difference is signed under the same constant-p model, without loosening
    # other unsigned force/speed/quantity domains.
    q = deepcopy(load_batch("grade9_batch3")["lessons"][-1]["assessments"][7])
    q["public"]["givens"][1]["value"] = "1"
    assert calculation_value(q) == -150


def test_digital_practical_has_no_physical_measurement_claim():
    l = load_batch("grade9_batch3")["lessons"][2]
    assert l["review"]["physical_experiment_completed"] is False
    assert (
        l["review"]["physical_measurements"]
        == "not_claimed_conditional_digital_data_only"
    )
    assert "samarali" in l["facts"]["layer"]["claim"]
    assert "aniq diametri deb" in l["facts"]["layer"]["claim"]


def test_remaining_fraction_and_pressure_fraction_are_different_models():
    d = load_batch("grade9_batch3")
    q = deepcopy(d["lessons"][3]["assessments"][4])
    q["public"]["givens"][0].update(value="50", unit="%")
    assert calculation_value(q) == 75000
    q["public"]["givens"][0]["value"] = "0"
    assert calculation_value(q) == 0
    p = deepcopy(d["lessons"][3]["assessments"][6])
    p["public"]["givens"][1].update(value="5", unit="%")
    assert calculation_value(p) == 300


def test_internal_energy_formulas_explicitly_monatomic_and_not_next_work_topic():
    l = load_batch("grade9_batch3")["lessons"][-1]
    for f in l["formulas"]:
        assert "MONATOMIC" in f["expression"] or "MONATOMIC" in next(
            q["grading_spec"]["formula"]["conditions"]
            for q in l["assessments"]
            if q["response_kind"] == "numeric_quantity"
            and q["grading_spec"]["rule"] == f["rule"]
        )
    assert all(
        53 not in r["pdf_pages"]
        for fact in l["facts"].values()
        for r in fact["source_refs"]
    )
