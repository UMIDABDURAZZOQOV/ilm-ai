"""Signed work/heat and original-page-confirmed calorimeter plus-sign erratum."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    16: ["Manfiy", "Izobarik jarayonda", "Hajm kamayganini"],
    17: ["Issiqlik orqali uzatilgan energiya", "Manfiy", "Qo‘shiladi"],
    18: ["Yo‘lga bog‘liq emas", "Yo‘q,ish yo‘lga bog‘liq bo‘lishi mumkin", "1-eta"],
    19: [
        "2minutda ikkala suv313K bo‘lganda",
        "Manfiy",
        "Shartli raqamli jadval tahlil qilinganini",
    ],
    20: ["Qo‘shiladi", "Tc<Tf<Th", "Haqiqiy tajriba bajarilganini"],
}


@pytest.mark.parametrize("seq", range(16, 21))
def test_every_semantic_answer_distractor_and_order(seq):
    l = load_batch("grade9_batch4")["lessons"][seq - 16]
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


def test_independent_literals_all_equivalents_and_units():
    d = load_batch("grade9_batch4")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 24,
        "formulas": 18,
        "worked_examples": 5,
        "assessments": 40,
        "frq": 20,
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
                    s, {**a, "unit": "m" if s["dimension"] == "mass" else "kg"}
                )
                == "dimension_mismatch"
            )
            assert grade_answer(s, {**a, "value": "999999"}) == "out_of_tolerance"
            assert grade_answer(s, {**a, "formula": "1"}) == "wrong_formula"
    assert count == 20


@pytest.mark.parametrize(
    "seq,qi,gi,bad",
    [
        (16, 4, 0, "0"),
        (16, 5, 2, "0"),
        (16, 6, 0, "0"),
        (16, 7, 3, "0"),
        (16, 8, 1, "0"),
        (17, 4, 1, "0"),
        (17, 5, 0, "-1560"),
        (17, 5, 2, "300"),
        (17, 6, 0, "0"),
        (17, 6, 1, "293"),
        (17, 7, 4, "293"),
        (17, 7, 7, "303"),
        (17, 7, 6, "0"),
        (17, 8, 0, "10"),
        (18, 4, 3, "0"),
        (18, 5, 3, "0"),
        (18, 6, 2, "353"),
        (18, 7, 0, "1.01"),
        (18, 7, 2, "0"),
        (19, 4, 0, "0"),
        (19, 6, 1, "303"),
        (20, 4, 4, "293"),
        (20, 4, 7, "303"),
        (20, 4, 0, "0"),
        (20, 5, 1, "0"),
        (20, 6, 4, "293"),
    ],
)
def test_thermodynamic_model_domains(seq, qi, gi, bad):
    q = deepcopy(load_batch("grade9_batch4")["lessons"][seq - 16]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_original64_wrong_minus_rejected_by_58_positive_energy_balance():
    l = load_batch("grade9_batch4")["lessons"][-1]
    q = l["assessments"][4]
    s = q["grading_spec"]
    assert calculation_value(q) == 388
    assert (
        grade_answer(
            s,
            {
                "formula": "(mw*cw+mc*cc)*(Tf-Tc)/(mh*(Th-Tf))",
                "value": "388",
                "unit": "J/(kg*K)",
            },
        )
        == "correct"
    )
    # Water capacity210,calorimeter178 J/K. Published minus on64 gives32,
    # whereas independently applied heat conservation58 gives388.
    assert (
        grade_answer(
            s,
            {
                "formula": "(mw*cw-mc*cc)*(Tf-Tc)/(mh*(Th-Tf))",
                "value": "32",
                "unit": "J/(kg*K)",
            },
        )
        == "wrong_formula"
    )
    assert (
        grade_answer(
            s,
            {
                "formula": "(mw*cw+mc*cc)*(Tf-Tc)/(mh*(Th-Tf))",
                "value": "32",
                "unit": "J/(kg*K)",
            },
        )
        == "out_of_tolerance"
    )
    assert (
        l["review"]["scientific_erratum"]
        == "PDF64numerator_minus_corrected_by_PDF58_plus_heat_balance"
    )
    assert (
        l["review"]["independent_calorimetry_expert"]
        == "required_before_general_publication"
    )
    refs = q["source_refs"]
    assert any(
        r["topic_id"] == "physics-9-section-17" and 58 in r["pdf_pages"] for r in refs
    )
    assert any(
        r["topic_id"] == "physics-9-section-20" and 64 in r["pdf_pages"] for r in refs
    )


def test_signed_cooling_heat_and_compression_volume_change():
    d = load_batch("grade9_batch4")
    q = d["lessons"][0]["assessments"][8]
    s = q["grading_spec"]
    assert calculation_value(q) == Fraction(-1, 250)
    assert grade_answer(s, {"formula": "A/p", "value": "-4", "unit": "L"}) == "correct"
    assert (
        grade_answer(s, {"formula": "A/p", "value": "4", "unit": "L"}) == "sign_error"
    )
    q = deepcopy(d["lessons"][1]["assessments"][5])
    q["public"]["givens"][0]["value"] = "-1560"
    q["public"]["givens"][2]["value"] = "280"
    assert calculation_value(q) == 390
    q = d["lessons"][3]["assessments"][5]
    s = q["grading_spec"]
    assert (
        grade_answer(s, {"formula": "m*c*(T2-T1)", "value": "-8.4", "unit": "kJ"})
        == "correct"
    )
    assert (
        grade_answer(s, {"formula": "m*c*(T2-T1)", "value": "8.4", "unit": "kJ"})
        == "sign_error"
    )


def test_digital_pair_heat_balance_and_no_real_measurement_claim():
    d = load_batch("grade9_batch4")
    l = d["lessons"][3]
    assert (
        calculation_value(l["assessments"][4]) + calculation_value(l["assessments"][5])
        == 0
    )
    assert calculation_value(l["assessments"][6]) == 313
    for l in d["lessons"][-2:]:
        assert l["review"]["physical_experiment_completed"] is False
        assert (
            l["review"]["physical_measurements"]
            == "not_claimed_conditional_digital_data_only"
        )
    assert all(
        65 not in r["pdf_pages"]
        for f in d["lessons"][-1]["facts"].values()
        if f["claim"].startswith("Massalar")
        for r in f["source_refs"]
    )


def test_single_phase_and_work_scope_not_arbitrary_paths():
    d = load_batch("grade9_batch4")
    for q in d["lessons"][1]["assessments"]:
        s = q["grading_spec"]
        if s["kind"] == "numeric_quantity":
            assert "phasechange" in s["formula"]["conditions"]
    for q in d["lessons"][0]["assessments"]:
        s = q["grading_spec"]
        if s["kind"] == "numeric_quantity":
            assert "ISOBARIC" in s["formula"]["conditions"]
