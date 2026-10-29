"""Image-checked grade-eight charge, Coulomb practice and electric field."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import new_answer

from services.assessment_grading import AnswerError, formula_ast, grade_answer, numeric
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    1: [
        "Itariladi",
        "Bir xil ishorali yaproqlarning itarilishi",
        "Metall",
        "Yo‘q, faqat tortilish yetarli emas",
        "Rasmdagi qismlar vazifasini tahlil qilishni",
    ],
    2: [
        "Manfiy",
        "Proton va elektron",
        "Musbat elementar zaryad moduli sifatida",
        "kg va C",
    ],
    3: ["Musbat zaryad modullari", "To‘rt marta kamayadi", "Tortiladi"],
    4: [
        "Musbat modulni",
        "Bir xil ikki metall shar",
        "Oldingi bir xil masofaga qaytarilganda",
    ],
    5: [
        "Musbat sinov zaryadiga kuch yo‘nalishi bilan",
        "N/C",
        "To‘rt marta kamayadi",
        "E0/E",
    ],
}


@pytest.mark.parametrize("seq", range(1, 6))
def test_electrostatic_semantic_keys_and_all_wrong_choices(seq):
    l = load_batch("grade8_batch1")["lessons"][seq - 1]
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
    if seq == 1:
        assert not l["formulas"]
    if seq == 4:
        assert l["review"]["physical_experiment_completed"] is False


def test_electrostatic_independent_oracles_and_source_domains():
    doc = load_batch("grade8_batch1")
    assert validate_batch(doc) == {
        "lessons": 5,
        "cards": 23,
        "formulas": 13,
        "worked_examples": 6,
        "assessments": 36,
        "frq": 15,
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
    assert count == 15
    for li, qi, gi, bad in [
        (1, 4, 0, "1.5"),
        (1, 5, 0, "3.3e-18"),
        (1, 6, 1, "1"),
        (2, 3, 0, "1"),
        (2, 3, 3, "0"),
        (3, 4, 0, "2"),
        (4, 4, 1, "0"),
        (4, 7, 1, "0.5"),
        (4, 8, 0, "100"),
    ]:
        q = deepcopy(doc["lessons"][li]["assessments"][qi])
        q["public"]["givens"][gi]["value"] = bad
        with pytest.raises(ValueError):
            calculation_value(q)
    # Earlier formula pages stay attached to their real prior topic identity.
    r = doc["lessons"][4]["facts"]["point"]["source_refs"]
    assert any(
        ref["topic_id"] == "physics-8-section-3" and ref["pdf_pages"] == [14]
        for ref in r
    )
    changed = deepcopy(doc)
    changed["lessons"][0]["source_refs"][0]["segment_pages"][0][
        "segment_local_pdf_page"
    ] += 1
    with pytest.raises(ValueError, match="source_segment_page_binding"):
        validate_batch(changed)


def test_root_notation_exact_arithmetic_and_legacy_default_remains_closed():
    q = load_batch("grade8_batch1")["lessons"][3]["assessments"][4]
    spec = q["grading_spec"]
    for formula in ["sqrt(F*r^2/k)", "(F*r^2/k)^0.5", "(F*r^2/k)^(1/2)", "r*sqrt(F/k)"]:
        assert (
            grade_answer(spec, {"formula": formula, "value": "4", "unit": "nC"})
            == "correct"
        )
    assert (
        grade_answer(
            spec, {"formula": "sqrt(F*r^2/k)", "value": "sqrt(16e-18)", "unit": "C"}
        )
        == "correct"
    )
    assert numeric("sqrt(16e-18)", allow_square_root=True) == Fraction("4e-9")
    for value in ["sqrt(-4)", "sqrt(2)", "4^0.25"]:
        with pytest.raises(AnswerError):
            numeric(value, allow_square_root=True)
    with pytest.raises(AnswerError):
        numeric("sqrt(4)")
    legacy = load_batch()["lessons"][5]["assessments"][2]["grading_spec"]
    with pytest.raises(AnswerError):
        formula_ast("sqrt(x)", legacy["formula"])
    assert (
        grade_answer(
            legacy,
            {
                "formula": "sqrt(x)",
                "value": "170",
                "unit": "cm",
                "allow_square_root": True,
            },
        )
        == "answer_required"
    )
    for formula in [
        "eval(F)",
        "sqrt(F,r)",
        "sqrt(F, x=1)",
        "F.__class__",
        "sqrt(__import__('os'))",
    ]:
        assert grade_answer(spec, {"formula": formula, "value": "4", "unit": "nC"}) in {
            "invalid_expression",
            "domain_error",
            "wrong_formula",
        }
    with pytest.raises(AnswerError):
        numeric("sqrt(" * 15 + "4" + ")" * 15, allow_square_root=True)
