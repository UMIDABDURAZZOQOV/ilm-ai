"""Original grade10 source offsets, signed components, angular units and domains."""

from copy import deepcopy

import pytest
from test_physics_course import NUMERIC_ORACLES, new_answer

from scripts.audit_physics_course import report
from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    1: [
        "Natijani tajriba bilan solishtirish",
        "Masala uchun muhim xossalar ajratilishini",
        "Ta’sir va model cheklovlarini qayd etish",
        "Yangi nazariya tegishli chegarada eski muvaffaqiyatli natijalarni beradi",
        "Yo‘q, dalil va qo‘llanish doirasi tekshiriladi",
    ],
    2: [
        "Yo‘nalishi o‘zgaradi",
        "Ikkinchi tarkib o‘qqa teskari ekanini",
        "x0+v0*t+a*t²/2 ga ishorasi bilan qo‘yamiz",
    ],
    3: [
        "Yo‘q, v nol bo‘lsa ham g saqlanadi",
        "Proyeksiya teskari, modul boshlang‘ichga teng",
        "Qarshiliksiz aynan otilgan balandlikka",
    ],
    4: ["rad/s²", "Manfiy", "Tik tarkiblarning kvadratlari yig‘indisidan ildiz bilan"],
    5: [
        "Tutashuvdagi chiziqli tezliklar",
        "Butun tishlar sonini",
        "Qarama-qarshi tomonga",
        "Bir xil aylanish yo‘nalishini",
    ],
}


@pytest.mark.parametrize("seq", range(1, 6))
def test_meaningful_concepts_order_and_separate_pdf_printed_pages(seq):
    l = load_batch("grade10_batch1")["lessons"][seq - 1]
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
    for ref in l["source_refs"]:
        assert ref["printed_pages"] == [p - 1 for p in ref["pdf_pages"]]
        assert ref["book_id"] == "physics-uz-grade-10"
        assert "segment_pages" not in ref
    if seq == 1:
        assert not l["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in l["assessments"]
        )


@pytest.mark.parametrize(
    "identity", [k for k in NUMERIC_ORACLES if k[0] == 10 and k[1] <= 5]
)
def test_every_numeric_literal_oracle_alternative_formula_unit_and_wrong_answer(
    identity,
):
    _, seq, number = identity
    l = load_batch("grade10_batch1")["lessons"][seq - 1]
    q = l["assessments"][number - 1]
    spec = q["grading_spec"]
    answer = new_answer(l, q)
    assert grade_answer(spec, answer) == "correct"
    for f in spec["formula"]["equivalents"]:
        assert grade_answer(spec, {**answer, "formula": f}) == "correct"
    assert grade_answer(spec, {**answer, "unit": "kg"}) == "dimension_mismatch"
    assert grade_answer(spec, {**answer, "formula": "1"}) == "wrong_formula"
    assert grade_answer(spec, {**answer, "value": "999999"}) == "out_of_tolerance"
    assert (
        grade_answer(spec, {**answer, "expected_si": answer["value"]})
        == "answer_required"
    )


@pytest.mark.parametrize(
    "seq,number,gi,value,unit",
    [
        (2, 6, 3, "-1", "s"),
        (2, 7, 1, "0", "m/s"),
        (2, 7, 2, "-1", "m/s"),
        (3, 5, 2, "7", "s"),
        (3, 6, 2, "5", "s"),
        (3, 7, 0, "0", "m/s"),
        (3, 8, 1, "0", "m/s2"),
        (3, 8, 1, "9.81", "m/s2"),
        (3, 8, 1, "10", "N/kg"),
        (3, 9, 0, "-1", "m/s"),
        (3, 11, 2, "-1", "m"),
        (4, 7, 2, "0", "s"),
        (4, 7, 0, "4", "Hz"),
        (4, 8, 1, "-2", "rad/s"),
        (4, 9, 2, "-1", "s"),
        (4, 10, 1, "0", "cm"),
        (4, 11, 1, "-4", "m/s2"),
        (5, 6, 2, "0", "m"),
        (5, 6, 0, "-4", "rad/s"),
        (5, 7, 0, "24.5", "1"),
        (5, 7, 2, "0", "1"),
    ],
)
def test_model_domain_rejects_bad_givens(seq, number, gi, value, unit):
    q = deepcopy(
        load_batch("grade10_batch1")["lessons"][seq - 1]["assessments"][number - 1]
    )
    q["public"]["givens"][gi].update(value=value, unit=unit)
    with pytest.raises(ValueError):
        calculation_value(q)


def test_angular_units_are_distinct_and_negative_axis_is_not_forced_positive():
    ls = load_batch("grade10_batch1")["lessons"]
    q = ls[3]["assessments"][6]
    s = q["grading_spec"]
    a = new_answer(ls[3], q)
    for unit in ["rad/s2", "rad/s^2", "rad/s²"]:
        assert grade_answer(s, {**a, "unit": unit}) == "correct"
    for unit in ["rad", "rad/s", "Hz", "1/s", "m/s2"]:
        assert grade_answer(s, {**a, "unit": unit}) == "dimension_mismatch"
    # Both angular velocities may be negative components; beta is +2, not a speed-up claim.
    q = deepcopy(q)
    q["public"]["givens"][0]["value"] = "-4"
    q["public"]["givens"][1]["value"] = "-12"
    assert calculation_value(q) == 2
    p = deepcopy(ls[1]["assessments"][5])
    p["public"]["givens"][0]["value"] = "-10"
    assert calculation_value(p) == -6


def test_grade10_batch_honest_counts_and_no_general_publication():
    d = load_batch("grade10_batch1")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 24,
        "formulas": 20,
        "worked_examples": 6,
        "assessments": 43,
        "frq": 20,
    }
    r = next(g for g in report()["grades"] if g["grade"] == 10)
    assert r["authored"] >= 5
    assert r["remaining"] == 45 - r["authored"]
    assert r["next_section"] == (r["authored"] + 1 if r["remaining"] else None)
    assert d["publication"] == "local_test_preview_only" and not d["ai_explain"]
    assert all(not l["review"]["physical_experiment_completed"] for l in d["lessons"])
