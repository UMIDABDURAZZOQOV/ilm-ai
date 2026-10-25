"""Original source concepts, grade-aware arithmetic and rotational unit boundaries."""

from copy import deepcopy

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    16: [
        "Kattaroq",
        "T bir aylanish, t esa n aylanishning umumiy vaqti",
        "nu1/s, omega rad/s",
    ],
    17: ["Urinma bo‘ylab", "Markazga yo‘nalgan", "Ikki marta ortadi"],
    18: [
        "Magnit ta’siri",
        "Moduli, yo‘nalishi va qo‘yilish nuqtasi",
        "N va dinamometr",
        "Nol",
    ],
    19: [
        "To‘g‘ri chiziqli tekis",
        "Tortish va ip ta’siri tenglashishi mumkin",
        "Oldingi harakatni saqlashga intilishga",
        "Yo‘q, avvalgi tekis harakatni saqlashi mumkin",
        "Birinchi qonunni tezlanayotgan har qanday sistemaga shartsiz qo‘llamaslik uchun",
    ],
    20: [
        "Massa",
        "Skalyar va kg",
        "Tezlanish modullarini",
        "Joy almashishning o‘zi massani o‘zgartirmaydi",
    ],
}


@pytest.mark.parametrize("seq", range(16, 21))
def test_rotation_inertia_semantics_and_wrong_options(seq):
    lesson = load_batch("grade7_batch4")["lessons"][seq - 16]
    qs = [q for q in lesson["assessments"] if q["response_kind"] == "concept_selection"]
    assert len(qs) == len(KEYS[seq])
    for q, label in zip(qs, KEYS[seq]):
        assert label in [o["label"] for o in q["public"]["options"]]
        for o in q["public"]["options"]:
            assert grade_answer(q["grading_spec"], {"choice_id": o["id"]}) == (
                "correct" if o["label"] == label else "incorrect_concept"
            )
    if seq == 19:
        assert not lesson["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in lesson["assessments"]
        )
        assert (
            grade_answer(
                lesson["assessments"][-1]["grading_spec"], {"order": ["s2", "s3", "s1"]}
            )
            == "correct"
        )


def test_rotation_oracles_rounding_units_and_domains():
    doc = load_batch("grade7_batch4")
    assert validate_batch(doc) == {
        "lessons": 5,
        "cards": 21,
        "formulas": 9,
        "worked_examples": 5,
        "assessments": 32,
        "frq": 12,
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
            assert grade_answer(spec, {**a, "unit": "m3"}) == "dimension_mismatch"
            assert grade_answer(spec, {**a, "value": "123456789"}) == "out_of_tolerance"
            assert grade_answer(spec, {**a, "formula": "1"}) == "wrong_formula"
    assert count == 12
    q = doc["lessons"][0]["assessments"][6]
    a = new_answer(doc["lessons"][0], q)
    for value in ("3.135", "3.145", "3.14159"):
        assert grade_answer(q["grading_spec"], {**a, "value": value}) == "correct"
    for value in ("3.1349", "3.1451"):
        assert (
            grade_answer(q["grading_spec"], {**a, "value": value}) == "out_of_tolerance"
        )
    q = doc["lessons"][0]["assessments"][5]
    a = new_answer(doc["lessons"][0], q)
    assert (
        grade_answer(q["grading_spec"], {**a, "value": "2.5", "unit": "1/s"})
        == "correct"
    )
    assert (
        grade_answer(q["grading_spec"], {**a, "unit": "rad/s"}) == "dimension_mismatch"
    )
    for li, qi, gi, value in [
        (0, 4, 1, "2.5"),
        (0, 5, 1, "0"),
        (0, 6, 0, "3"),
        (1, 3, 1, "0"),
        (1, 4, 1, "0"),
        (2, 5, 1, "20"),
    ]:
        q = deepcopy(doc["lessons"][li]["assessments"][qi])
        q["public"]["givens"][gi]["value"] = value
        with pytest.raises(ValueError):
            calculation_value(q)
