"""Grade10 completion: verified diode regimes, modest linear metals, carrier concepts."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import NUMERIC_ORACLES, new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import (
    calculation_value,
    load_batch,
    load_course,
    validate_batch,
)

LABELS = {
    41: [
        "Katoddan yetarli elektron emissiyasi",
        "Yo‘q, biri yo‘naltirish, biri emissiya temperaturasiga bog‘liq",
        "Yo‘q, u ko‘rsatilgan rejimga tegishli",
        "Emissiyadan keladigan elektronlar oqimiga",
    ],
    42: [
        "Oxirgi va tayanch temperatura farqi",
        "1/K",
        "Yo‘q, rho materialning solishtirma qarshiligi",
        "Mumkin emas, qo‘llanish chegarasi bor",
    ],
    43: [
        "Aralashmasiz sof yarimo‘tkazgich modeli",
        "Elektronlar bo‘sh joyni to‘ldirganda bo‘sh joyning samarali siljishini",
        "Elektronlar",
        "Kovaklar",
        "Yo‘q, bu asosiy tashuvchining turini bildiradi",
        "Yo‘q, son tengligining o‘zi yetarli emas",
    ],
    44: [
        "Erkin harakatchan tashuvchilar",
        "pmusbat,nmanfiy",
        "Emitter,baza,kollektor",
        "To‘g‘ri",
        "Bir yo‘nalishli pulsatsiyalangan",
        "Tashqi manbadan",
    ],
    45: [
        "Yo‘q, bu shartli ma’lumot",
        "I",
        "Yo‘q, diod nochiziqli bo‘lishi mumkin",
        "Nolga bo‘lib sonli R yozmaslik",
    ],
}
ORDERS = {
    41: ["s2", "s1", "s3"],
    42: ["s3", "s1", "s4", "s2"],
    43: ["s2", "s1", "s3"],
    44: ["s1", "s3", "s2"],
    45: ["s2", "s1", "s3", "s4"],
}


def question(seq, n):
    return deepcopy(
        load_batch("grade10_batch9")["lessons"][seq - 41]["assessments"][n - 1]
    )


@pytest.mark.parametrize("seq", range(41, 46))
def test_meaning_and_nonfabricated_conceptual_topics(seq):
    l = load_batch("grade10_batch9")["lessons"][seq - 41]
    qs = [q for q in l["assessments"] if q["response_kind"] == "concept_selection"]
    assert len(qs) == len(LABELS[seq])
    for q, label in zip(qs, LABELS[seq]):
        assert label in [o["label"] for o in q["public"]["options"]]
        for o in q["public"]["options"]:
            assert grade_answer(q["grading_spec"], {"choice_id": o["id"]}) == (
                "correct" if o["label"] == label else "incorrect_concept"
            )
    q = next(q for q in l["assessments"] if q["response_kind"] == "ordering")
    assert grade_answer(q["grading_spec"], {"order": ORDERS[seq]}) == "correct"
    assert grade_answer(q["grading_spec"], {"order": ORDERS[seq][::-1]}) != "correct"
    if seq in {43, 44}:
        assert not l["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in l["assessments"]
        )


@pytest.mark.parametrize(
    "identity", [k for k in NUMERIC_ORACLES if k[0] == 10 and 41 <= k[1] <= 45]
)
def test_independent_exact_answers_units_and_alternatives(identity):
    _, seq, n = identity
    l = load_batch("grade10_batch9")["lessons"][seq - 41]
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
        (41, 6, 0, "0", "V"),
        (41, 6, 1, "-16", "V"),
        (41, 6, 0, "4", "A"),
        (42, 6, 0, "0", "Ω"),
        (42, 6, 1, "-0.004", "1/K"),
        (42, 6, 1, "0.004", "K"),
        (42, 6, 2, "-250", "K"),
        (42, 6, 2, "-273.15", "K"),
        (42, 7, 2, "0", "K"),
        (42, 7, 0, "40", "Ω"),
        (42, 8, 0, "0", "Ω*m"),
        (42, 8, 1, "0.004", "Ω"),
        (42, 9, 0, "0", "Ω"),
        (42, 9, 2, "-250", "K"),
        (45, 6, 1, "0", "mA"),
        (45, 7, 0, "-5", "V"),
        (45, 7, 1, "0.01", "A/m2"),
    ],
)
def test_source_model_domains(seq, n, gi, v, u):
    q = question(seq, n)
    q["public"]["givens"][gi].update(value=v, unit=u)
    with pytest.raises(ValueError):
        calculation_value(q)


def test_negative_temperature_difference_is_not_negative_absolute_temperature():
    q = question(42, 6)
    q["public"]["givens"][2]["value"] = "-50"
    assert calculation_value(q) == 40
    q = question(42, 7)
    q["public"]["givens"][0]["value"] = "40"
    q["public"]["givens"][2]["value"] = "-50"
    assert calculation_value(q) == Fraction(1, 250)
    q = question(42, 9)
    q["public"]["givens"][0]["value"] = "40"
    q["public"]["givens"][2]["value"] = "-50"
    assert calculation_value(q) == 50


def test_one_half_and_three_halves_models_not_confused():
    assert calculation_value(question(41, 6)) == 8
    q = question(41, 6)
    q["public"]["givens"][0]["value"] = "16"
    q["public"]["givens"][1]["value"] = "4"
    assert calculation_value(q) == Fraction(1, 8)
    s = question(41, 6)["grading_spec"]
    a = {"value": "8", "unit": "1", "formula": "U2/U1"}
    assert grade_answer(s, a) == "wrong_formula"  # linear Ohm ratio is not this regime


def test_conditional_diode_point_is_not_a_global_ohmic_law():
    assert calculation_value(question(45, 6)) == 30
    assert calculation_value(question(45, 7)) == 500000
    l = load_batch("grade10_batch9")["lessons"][4]
    assert not l["review"]["physical_experiment_completed"]
    assert (
        l["review"]["physical_measurements"]
        == "not_claimed_conditional_digital_data_only"
    )
    assert "barcha kuchlanishlar" in l["cards"][2]["body"]


def test_all_45_grade10_sections_once_in_source_order():
    ls = [l for d in load_course() if d["grade"] == 10 for l in d["lessons"]]
    assert [l["sequence"] for l in ls] == list(range(1, 46))
    assert len({l["topic_id"] for l in ls}) == 45
    assert sum(l["xp_reward"] for l in ls) == 450
    for l in ls:
        assert l["review"]["independent_subject_expert"] == "not_claimed"
        assert not l["review"]["physical_experiment_completed"]
        for r in l["source_refs"]:
            assert r["printed_pages"] == [p - 1 for p in r["pdf_pages"]]
    assert validate_batch(load_batch("grade10_batch9")) == {
        "lessons": 5,
        "cards": 28,
        "formulas": 6,
        "worked_examples": 5,
        "assessments": 36,
        "frq": 7,
    }
