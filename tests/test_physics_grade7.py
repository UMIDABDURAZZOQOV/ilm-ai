"""Image-reviewed grade7PDF1–21; source-meaning keys and independent arithmetic."""

from copy import deepcopy

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    1: [
        "Harakat sanoq jismga nisbiy",
        "Sanoq jism",
        "Sanoq jism, koordinatalar va vaqt sanog‘i",
        "Ayni chiziq va bir yo‘nalishli klassik model",
    ],
    2: [
        "Bitta o‘q",
        "Uch o‘lchamli koordinatalar",
        "Sekund",
        "Harakatda qachon shu vaziyatda bo‘lganini bilish uchun",
    ],
    3: [
        "Moddiy nuqta",
        "Yo‘q, shu vazifada o‘lcham muhim",
        "Yo‘q, harakat nuqtalari chizig‘i tasavvur qilinadi",
        "Nol",
        "Egri bo‘lishi ham mumkin",
        "Jismning vaqt bo‘yicha vaziyatini",
    ],
    4: [
        "Ko‘chish va kuch",
        "Moduli va yo‘nalishi bir xil bo‘lishi",
        "Teskariga o‘zgaradi",
        "Ha, modul va proyeksiya alohida",
    ],
    5: [
        "To‘g‘ri chiziqli, ammo tekis emas",
        "Yo‘q, trayektoriyasi aylana",
        "Tomchilar teng vaqt oraliqlarida tushishi",
        "5ta",
    ],
}


@pytest.mark.parametrize("sequence", range(1, 6))
def test_grade7_conceptual_keys_match_reviewed_source_meanings(sequence):
    l = load_batch("grade7_batch1")["lessons"][sequence - 1]
    qs = [q for q in l["assessments"] if q["response_kind"] == "concept_selection"]
    assert len(qs) == len(KEYS[sequence])
    for q, label in zip(qs, KEYS[sequence]):
        assert label in [o["label"] for o in q["public"]["options"]]
        for o in q["public"]["options"]:
            assert grade_answer(q["grading_spec"], {"choice_id": o["id"]}) == (
                "correct" if o["label"] == label else "incorrect_concept"
            )
    if sequence == 3:
        assert not l["formulas"]
    if sequence == 4:
        q = l["assessments"][4]
        items = {v["label"]: v["id"] for v in q["public"]["items"]}
        order = [
            items[s]
            for s in [
                "Birinchi vektorni yo‘nalishi va masshtabi bilan chizish",
                "Ikkinchi vektor boshini birinchi uchiga qo‘yish",
                "Birinchi boshdan ikkinchi uchga natija chizish",
            ]
        ]
        assert grade_answer(q["grading_spec"], {"order": order}) == "correct"
        assert (
            grade_answer(q["grading_spec"], {"order": order[::-1]}) == "incorrect_order"
        )


def test_grade7_numeric_oracles_units_alternatives_and_model_domains():
    doc = load_batch("grade7_batch1")
    assert validate_batch(doc) == {
        "lessons": 5,
        "cards": 23,
        "formulas": 6,
        "worked_examples": 5,
        "assessments": 32,
        "frq": 9,
    }
    seen = 0
    for l in doc["lessons"]:
        for q in l["assessments"]:
            spec = q["grading_spec"]
            if spec["kind"] != "numeric_quantity":
                continue
            seen += 1
            a = new_answer(l, q)
            for f in spec["formula"]["equivalents"]:
                assert grade_answer(spec, {**a, "formula": f}) == "correct"
            assert grade_answer(spec, {**a, "unit": "kg"}) == "dimension_mismatch"
            assert (
                grade_answer(spec, {**a, "value": "999999999999"}) == "out_of_tolerance"
            )
            assert grade_answer(spec, {**a, "formula": "1"}) == "wrong_formula"
    assert seen == 9
    # Wrong directions/domain cannot silently change the source model.
    for li, qi, gi, key, bad in [
        (3, 6, 0, "value", "3"),
        (3, 7, 1, "value", "-2"),
        (4, 4, 1, "value", "2.5"),
        (4, 4, 1, "unit", "%"),
    ]:
        q = deepcopy(doc["lessons"][li]["assessments"][qi])
        q["public"]["givens"][gi][key] = bad
        with pytest.raises(ValueError):
            calculation_value(q)
    assert doc["lessons"][0]["source_refs"][0]["printed_pages"] == [8, 9, 10, 11]
    assert doc["lessons"][0]["source_refs"][0]["pdf_pages"] == [1, 2, 3, 4]
