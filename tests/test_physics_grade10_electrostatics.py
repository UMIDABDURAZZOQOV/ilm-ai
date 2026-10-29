"""Literal electrostatic sign, geometry, linear-energy and conductance regressions."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import NUMERIC_ORACLES, new_answer

from services.assessment_grading import UNITS, grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

LABELS = {
    31: [
        "Nol",
        "R+h",
        "Birliksiz",
        "Bog‘langan musbat/manfiy markazlarning siljishi bilan",
    ],
    32: [
        "Tanlangan cheksiz nolga nisbatan manfiy",
        "Yo‘q, phi manba va nol tanlashga tegishli",
        "Yo‘q, u bir xil sirt qiymati bo‘lishi mumkin",
        "Bir jinsli maydon va aniq yo‘naltirilgan masofa uchun",
    ],
    33: [
        "W_initial−W_final ga",
        "Manfiy",
        "Yo‘q, faqat endpointlarga bog‘liq",
        "Maydon va ko‘chish orasidagi kosinus qiymati",
    ],
    34: [
        "Bitta qoplama zaryadining moduli",
        "Ikki baravar ortadi",
        "Ikki baravar kamayadi",
        "J/m³",
    ],
    35: ["S", "Erkin elektronlarni", "R=U/I", "Tartibli o‘rtacha drift tezligi moduli"],
}
ORDERS = {
    31: ["s2", "s1", "s3"],
    32: ["s1", "s3", "s2"],
    33: ["s2", "s1", "s3"],
    34: ["s2", "s3", "s1"],
    35: ["s2", "s3", "s1", "s4"],
}


def question(seq, n):
    return deepcopy(
        load_batch("grade10_batch7")["lessons"][seq - 31]["assessments"][n - 1]
    )


@pytest.mark.parametrize("seq", range(31, 36))
def test_independent_semantic_concepts_and_order(seq):
    l = load_batch("grade10_batch7")["lessons"][seq - 31]
    qs = [q for q in l["assessments"] if q["response_kind"] == "concept_selection"]
    assert len(qs) == len(LABELS[seq]) == 4
    for q, label in zip(qs, LABELS[seq]):
        assert label in [o["label"] for o in q["public"]["options"]]
        for o in q["public"]["options"]:
            assert grade_answer(q["grading_spec"], {"choice_id": o["id"]}) == (
                "correct" if o["label"] == label else "incorrect_concept"
            )
    q = next(q for q in l["assessments"] if q["response_kind"] == "ordering")
    assert grade_answer(q["grading_spec"], {"order": ORDERS[seq]}) == "correct"
    assert grade_answer(q["grading_spec"], {"order": ORDERS[seq][::-1]}) != "correct"


@pytest.mark.parametrize(
    "identity", [k for k in NUMERIC_ORACLES if k[0] == 10 and 31 <= k[1] <= 35]
)
def test_independently_calculated_units_and_every_allowed_formula(identity):
    _, seq, n = identity
    l = load_batch("grade10_batch7")["lessons"][seq - 31]
    q = l["assessments"][n - 1]
    s = q["grading_spec"]
    a = new_answer(l, q)
    assert grade_answer(s, a) == "correct"
    for f in s["formula"]["equivalents"]:
        assert grade_answer(s, {**a, "formula": f}) == "correct"
    assert grade_answer(s, {**a, "unit": "kg"}) == "dimension_mismatch"
    assert grade_answer(s, {**a, "formula": "__import__(x)"}) != "correct"
    assert grade_answer(s, {**a, "value": "999999"}) == "out_of_tolerance"


@pytest.mark.parametrize(
    "seq,n,gi,v,u",
    [
        (31, 6, 2, "9", "cm"),
        (31, 6, 3, "0", "cm"),
        (31, 6, 1, "-2", "nC"),
        (31, 6, 0, "1e9", "N*m2/C2"),
        (31, 7, 1, "0.5", "1"),
        (31, 8, 1, "0", "N/C"),
        (32, 6, 2, "0.5", "1"),
        (32, 6, 3, "0", "cm"),
        (32, 6, 1, "-2", "V"),
        (32, 7, 1, "-30", "J"),
        (32, 8, 1, "50", "C"),
        (32, 9, 3, "21", "cm"),
        (32, 9, 3, "-1", "cm"),
        (32, 9, 2, "0", "cm"),
        (32, 10, 2, "0", "cm"),
        (32, 10, 2, "20", "s"),
        (33, 6, 0, "2", "V"),
        (33, 7, 1, "-500", "V"),
        (33, 8, 3, "1.1", "1"),
        (33, 8, 3, "-1.1", "1"),
        (33, 8, 2, "-20", "cm"),
        (34, 6, 0, "-8", "µC"),
        (34, 7, 0, "0", "µF"),
        (34, 7, 1, "-30", "V"),
        (34, 8, 1, "0", "µF"),
        (34, 9, 0, "8e-12", "F/m"),
        (34, 9, 1, "0.5", "1"),
        (34, 9, 2, "-1000", "N/C"),
        (35, 6, 0, "0", "Ω"),
        (35, 6, 0, "250", "S"),
        (35, 7, 0, "0", "mS"),
        (35, 7, 0, "4", "s"),
        (35, 9, 1, "1.5e-19", "C"),
        (35, 9, 2, "0", "mm2"),
        (35, 9, 3, "-0.001", "m/s"),
        (35, 9, 0, "0", "1/m3"),
    ],
)
def test_geometry_sign_model_and_si_domains(seq, n, gi, v, u):
    q = question(seq, n)
    q["public"]["givens"][gi].update(value=v, unit=u)
    with pytest.raises(ValueError):
        calculation_value(q)


def test_sphere_boundary_inside_centre_and_exterior_are_distinct():
    q = question(31, 6)
    q["public"]["givens"][2]["value"] = "10"
    assert calculation_value(q) == 1800  # just outside surface, not internal zero
    q = question(32, 9)
    for r in ["0", "0.1", "0.2"]:
        q["public"]["givens"][3].update(value=r, unit="m")
        assert calculation_value(q) == -180


def test_potential_gauge_invariance_and_work_reversal():
    q = question(32, 8)
    assert calculation_value(q) == -70
    q["public"]["givens"][0]["value"] = "80"
    q["public"]["givens"][1]["value"] = "150"
    assert calculation_value(q) == -70
    q = question(33, 6)
    assert calculation_value(q) == Fraction(12, 100000)
    q["public"]["givens"][1]["value"] = "20"
    q["public"]["givens"][2]["value"] = "80"
    assert calculation_value(q) == Fraction(-12, 100000)
    q["public"]["givens"][0]["value"] = "-2"
    assert calculation_value(q) == Fraction(12, 100000)
    q = question(33, 7)
    q["public"]["givens"][2]["value"] = "-20"
    assert calculation_value(q) == Fraction(3, 10000)


def test_field_unit_aliases_and_si_case_are_explicit():
    assert UNITS["V/m"] == UNITS["N/C"]
    assert UNITS["kV/m"] == ("electric_field", 1000)
    assert UNITS["S"][0] == "conductance" and UNITS["s"][0] == "time"
    q = question(31, 6)
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "k*q/r^2", "value": "0.2", "unit": "kV/m"}
        )
        == "correct"
    )
    q = question(35, 6)
    a = {"formula": "1/R", "value": "4", "unit": "mS"}
    assert grade_answer(q["grading_spec"], a) == "correct"
    assert grade_answer(q["grading_spec"], {**a, "unit": "ms"}) != "correct"


def test_half_energy_density_and_drift_have_independent_exact_values():
    assert calculation_value(question(34, 6)) == Fraction(2, 10000)
    assert calculation_value(question(34, 7)) == Fraction(9, 10000)
    assert calculation_value(question(34, 8)) == Fraction(6, 10**6)
    assert calculation_value(question(34, 9)) == Fraction(177, 10**7)
    assert calculation_value(question(35, 6)) == Fraction(1, 250)
    assert calculation_value(question(35, 9)) == Fraction(24, 5)
    # Same capacitor, all three paths agree for C2uF,U30V,q60uC.
    q = question(34, 6)
    q["public"]["givens"][0]["value"] = "60"
    q["public"]["givens"][1]["value"] = "30"
    assert calculation_value(q) == Fraction(9, 10000)
    q = question(34, 8)
    q["public"]["givens"][0]["value"] = "60"
    q["public"]["givens"][1]["value"] = "2"
    assert calculation_value(q) == Fraction(9, 10000)


def test_honest_five_source_sections_and_printed_offset():
    d = load_batch("grade10_batch7")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 25,
        "formulas": 19,
        "worked_examples": 5,
        "assessments": 44,
        "frq": 19,
    }
    for l in d["lessons"]:
        assert not l["review"]["physical_experiment_completed"]
        assert l["review"]["independent_subject_expert"] == "not_claimed"
        for r in l["source_refs"]:
            assert r["printed_pages"] == [p - 1 for p in r["pdf_pages"]]
