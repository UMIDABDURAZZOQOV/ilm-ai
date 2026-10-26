"""All59 source-ordered grade9 sections and final meaningful concept tasks."""

from copy import deepcopy

import pytest
from test_physics_course import new_answer

from scripts.audit_physics_course import report
from services.assessment_grading import grade_answer
from services.physics_curriculum import (
    calculation_value,
    load_batch,
    load_course,
    validate_batch,
)

KEYS = {
    56: [
        "Tasvir va buyumning musbat balandlik modullari",
        "Berilgan maktab yaqinlashuvi natijasi",
        "Yo‘q,bu darsdagi masofa modeli shaxsiy retsept emas",
    ],
    57: [
        "Quyosh energiyasi",
        "Quvvat/yuzani",
        "Quyosh energiyasini jamlashdan foydalanishga",
        "Quyosh energiyasidan amaliy foydalanishga",
        "Issiqqa chidamli materiallarni olishda",
    ],
    58: [
        "Tarixiy model tavsifi sifatida",
        "Faradey bilan",
        "Yo‘q,kitob kvant xossalarini ham muhokama qiladi",
        "Dalil va tekshirish imkonini beradi",
        "Yo‘q,matnning tarixiy doirasini saqlash kerak",
    ],
    59: [
        "Energiya,transport va aloqa bilan",
        "Fanlar akademiyasi va Fizika-texnika instituti",
        "Yarimo‘tkazgich va optika tadqiqotlari",
        "Nurlanishni qayd etish",
        "Yuqori chastotali diodni",
    ],
}


@pytest.mark.parametrize("seq", range(56, 60))
def test_final_semantic_options_order_and_no_fake_numeric_history(seq):
    l = load_batch("grade9_batch12")["lessons"][seq - 56]
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
    if seq >= 57:
        assert not l["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in l["assessments"]
        )


def test_final_literal_oracles_and_wrong_responses():
    d = load_batch("grade9_batch12")
    assert validate_batch(d) == {
        "lessons": 4,
        "cards": 16,
        "formulas": 4,
        "worked_examples": 4,
        "assessments": 26,
        "frq": 4,
    }
    for l in d["lessons"]:
        for q in l["assessments"]:
            s = q["grading_spec"]
            if s["kind"] != "numeric_quantity":
                continue
            a = new_answer(l, q)
            assert grade_answer(s, a) == "correct"
            for f in s["formula"]["equivalents"]:
                assert grade_answer(s, {**a, "formula": f}) == "correct"
            assert grade_answer(s, {**a, "unit": "kg"}) == "dimension_mismatch"
            assert grade_answer(s, {**a, "value": "999999"}) == "out_of_tolerance"
            assert grade_answer(s, {**a, "formula": "1"}) == "wrong_formula"


@pytest.mark.parametrize(
    "qi,gi,bad",
    [
        (4, 0, "0.1"),
        (4, 1, "0"),
        (4, 2, "0"),
        (5, 2, "0"),
        (5, 1, "-3"),
        (5, 0, "-10"),
        (6, 2, "0"),
        (6, 1, "30"),
        (7, 1, "-25"),
        (7, 0, "0"),
    ],
)
def test_final_model_domains(qi, gi, bad):
    q = deepcopy(load_batch("grade9_batch12")["lessons"][0]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_grade9_all59_coverage_includes_every_mapped_lab_and_practical():
    docs = [d for d in load_course() if d["grade"] == 9]
    ls = [l for d in docs for l in d["lessons"]]
    assert [l["sequence"] for l in ls] == list(range(1, 60))
    r = next(g for g in report()["grades"] if g["grade"] == 9)
    assert (r["source_sections"], r["authored"], r["remaining"], r["next_section"]) == (
        59,
        59,
        0,
        None,
    )
    assert (
        r["cards"],
        r["formula_entries"],
        r["examples"],
        r["assessments"],
        r["frq"],
    ) == (271, 202, 61, 461, 205)
    assert (r["laboratories"], r["practicals"]) == (6, 2)
    for seq in [13, 19, 20, 25, 34, 42, 49, 53]:
        l = ls[seq - 1]
        assert not l["review"]["physical_experiment_completed"]
    assert report()["authored"] == 226 and report()["remaining"] == 90
