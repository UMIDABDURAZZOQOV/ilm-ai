"""Source-checked final decay, reaction, particle and energy activities."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import NUMERIC_ORACLES, new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

LABELS = {
    41: [
        "Ehtimollik va ko‘p yadro statistik tavsifini",
        "1/8",
        "Bq",
        "Elektromagnit kvantlar",
    ],
    42: [
        "Nuklonlar balansi,kgdagi tinch massa aynan teng bo‘lishi shart emas",
        "Ikkiga kamayadi",
        "O‘zgarmaydi",
        "Ikkalasi saqlanadi",
    ],
    43: ["Yo‘q,kvark tarkibi bor", "Pozitron", "uud", "Qarama-qarshi"],
    44: [
        "Boshlang‘ich va yakuniy bog‘lanish energiyalari",
        "Turbina",
        "Yo‘q,vaqt va tizim dinamikasi ham muhim",
        "Yo‘q",
    ],
    45: [
        "Radiatsion materialshunoslik",
        "Yadro fizikasi instituti",
        "Zarralar izlari haqidagi ma’lumot",
        "Yo‘q",
        "Qo‘shimcha tekshirishsiz to‘g‘ri emas",
    ],
}
ORDERS = {
    41: ["s3", "s1", "s4", "s2"],
    42: ["s3", "s1", "s4", "s2"],
    43: ["s2", "s1", "s3"],
    44: ["s2", "s4", "s1", "s3"],
    45: ["s2", "s1", "s3"],
}


def question(seq, n):
    return deepcopy(
        load_batch("grade11_batch9")["lessons"][seq - 41]["assessments"][n - 1]
    )


@pytest.mark.parametrize("seq", range(41, 46))
def test_independent_source_meaning_order_and_digital_activity(seq):
    l = load_batch("grade11_batch9")["lessons"][seq - 41]
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
    if seq == 45:
        assert not l["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in l["assessments"]
        )


@pytest.mark.parametrize(
    "identity", [k for k in NUMERIC_ORACLES if k[0] == 11 and 41 <= k[1] <= 45]
)
def test_independent_literal_answers_closed_formulas_and_units(identity):
    _, seq, n = identity
    l = load_batch("grade11_batch9")["lessons"][seq - 41]
    q = l["assessments"][n - 1]
    s = q["grading_spec"]
    a = new_answer(l, q)
    assert grade_answer(s, a) == "correct"
    for f in s["formula"]["equivalents"]:
        assert grade_answer(s, {**a, "formula": f}) == "correct"
    assert grade_answer(s, {**a, "unit": "kg"}) == "dimension_mismatch"
    assert grade_answer(s, {**a, "formula": "__import__(x)"}) != "correct"
    assert grade_answer(s, {**a, "value": "999990"}) == "out_of_tolerance"


@pytest.mark.parametrize(
    "seq,n,symbol,value,unit",
    [
        (41, 6, "N0", "0", "1"),
        (41, 6, "N0", "1.5", "1"),
        (41, 6, "T", "0", "s"),
        (41, 6, "t", "-1", "s"),
        (41, 6, "t", "25", "s"),
        (41, 7, "t", "20485", "s"),
        (41, 8, "N", "3.5", "1"),
        (41, 8, "decayRate", "0.002", "Hz"),
        (41, 9, "ell2", "0.6931", "1"),
        (42, 6, "A", "4", "1"),
        (42, 7, "Z", "1", "1"),
        (42, 7, "Z", "209", "1"),
        (42, 8, "Z", "24", "1"),
        (42, 9, "mOut", "0", "kg"),
        (43, 6, "nU", "1.5", "1"),
        (43, 6, "nD", "0", "1"),
        (43, 7, "mParent", "0", "kg"),
        (44, 6, "Nevents", "1.5", "1"),
    ],
)
def test_closed_source_domains(seq, n, symbol, value, unit):
    q = question(seq, n)
    next(g for g in q["public"]["givens"] if g["symbol"] == symbol).update(
        value=value, unit=unit
    )
    with pytest.raises(ValueError):
        calculation_value(q)


def test_decay_zero_time_whole_halfperiods_and_positive_activity():
    q = question(41, 6)
    q["public"]["givens"][1]["value"] = "0"
    assert calculation_value(q) == 9600
    assert calculation_value(question(41, 6)) == 1200
    assert calculation_value(question(41, 7)) == Fraction(1, 16)
    assert calculation_value(question(41, 8)) == 12
    assert calculation_value(question(41, 9)) == Fraction(231, 10000)
    q = question(41, 8)
    q["public"]["givens"][1]["value"] = "0"
    assert calculation_value(q) == 0


def test_variable_power_is_only_closed_structural_opt_in_never_execution():
    from services.assessment_grading import AnswerError, formula_ast
    from services.physics_rules import REVIEWED_FORMULAS

    spec = question(41, 6)["grading_spec"]
    a = {"formula": "N0/(2^(t/T))", "value": "1200", "unit": "1"}
    assert grade_answer(spec, a) == "correct"
    assert grade_answer(spec, {**a, "formula": "N0*2^(-T/t)"}) == "wrong_formula"
    for expression in [
        "N0*2^(t**t)",
        "__import__('os')",
        "N0*2^(open(x))",
        "N0*2^(-t/unknown)",
    ]:
        assert grade_answer(spec, {**a, "formula": expression}) != "correct"
    plain = deepcopy(REVIEWED_FORMULAS["whole_half_life_remaining"])
    plain.pop("allow_variable_power")
    with pytest.raises(AnswerError):
        formula_ast("N0*2^(-t/T)", plain)
    for name, rule in REVIEWED_FORMULAS.items():
        assert bool(rule.get("allow_variable_power")) == (
            name in {"whole_half_life_remaining", "whole_half_life_fraction"}
        )


def test_alpha_beta_gamma_bookkeeping_and_signed_q():
    assert calculation_value(question(42, 6)) + 4 == 210
    assert calculation_value(question(42, 7)) + 2 == 84
    assert calculation_value(question(42, 8)) == 12
    q = question(42, 9)
    assert calculation_value(q) == Fraction("4.5e-13")
    q["public"]["givens"][0]["value"] = "6.71e-27"
    assert calculation_value(q) == Fraction("-4.5e-13")


def test_valence_charge_and_two_photon_rest_energy_conservation():
    assert calculation_value(question(43, 6)) == 1
    q = question(43, 6)
    q["public"]["givens"][0]["value"] = "1"
    q["public"]["givens"][1]["value"] = "2"
    assert calculation_value(q) == 0
    assert 2 * calculation_value(question(43, 7)) == Fraction("2.4e-28") * 300000000**2
    assert calculation_value(question(44, 6)) == Fraction("1.92e-10")


def test_final_five_source_scoped_original_lessons():
    d = load_batch("grade11_batch9")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 25,
        "formulas": 11,
        "worked_examples": 5,
        "assessments": 37,
        "frq": 11,
    }
    for l in d["lessons"]:
        assert not l["review"]["physical_experiment_completed"]
        assert l["review"]["independent_subject_expert"] == "not_claimed"
        for r in l["source_refs"]:
            assert r["printed_pages"] == [p - 1 for p in r["pdf_pages"]]
