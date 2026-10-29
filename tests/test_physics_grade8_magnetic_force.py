"""Independent magnetic-force answers, SI prefixes, geometry and source limits."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import new_answer

from services.assessment_grading import UNITS, grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    51: [
        "Turgan joyidagi magnit maydon",
        "Aynan bir nuqta bo‘lishi shart emas",
        "S ga",
        "Qutb hududlari bilan",
        "Darslikdagi tasvir ma’lumoti,bugungi aniq manzil kafolati emas",
    ],
    52: [
        "Tokli sim atrofida magnit maydon mavjud",
        "Simni o‘ragan aylanalar",
        "Teskarilanadi",
        "Shartli tok yo‘nalishiga",
        "N vaS qutbli",
    ],
    53: ["Maydonga tik to‘g‘ri sim qismi uchun", "Teskarilanadi", "Tortishadi"],
    54: ["0,05T", "F — N,B — T", "Maydonga tik"],
    55: [
        "Qarama-qarshi tomonlardagi kuchlar jufti",
        "Spiral prujina",
        "Simdagi tok yo‘nalishi ham avtomatik almashishini",
        "Darajalangan shkaladan",
        "Ramkaga keladigan tokning mos holatdagi ulanishi",
    ],
}


@pytest.mark.parametrize("seq", range(51, 56))
def test_semantic_labels_wrong_options_order_and_no_forced_math(seq):
    l = load_batch("grade8_batch11")["lessons"][seq - 51]
    qs = [q for q in l["assessments"] if q["response_kind"] == "concept_selection"]
    assert len(qs) == len(KEYS[seq])
    for q, label in zip(qs, KEYS[seq]):
        assert label in [o["label"] for o in q["public"]["options"]]
        for option in q["public"]["options"]:
            assert grade_answer(q["grading_spec"], {"choice_id": option["id"]}) == (
                "correct" if option["label"] == label else "incorrect_concept"
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
    if seq in (51, 52, 55):
        assert not l["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in l["assessments"]
        )


def test_every_numeric_rule_has_independent_answer_and_equivalent_forms():
    doc = load_batch("grade8_batch11")
    assert validate_batch(doc) == {
        "lessons": 5,
        "cards": 20,
        "formulas": 10,
        "worked_examples": 6,
        "assessments": 36,
        "frq": 10,
    }
    count = 0
    for l in doc["lessons"]:
        for q in l["assessments"]:
            spec = q["grading_spec"]
            if spec["kind"] != "numeric_quantity":
                continue
            count += 1
            answer = new_answer(l, q)
            for formula in spec["formula"]["equivalents"]:
                assert grade_answer(spec, {**answer, "formula": formula}) == "correct"
            assert grade_answer(spec, {**answer, "unit": "kg"}) == "dimension_mismatch"
            assert (
                grade_answer(spec, {**answer, "value": "123456"}) == "out_of_tolerance"
            )
            assert grade_answer(spec, {**answer, "formula": "1"}) == "wrong_formula"
            assert "TIK" in spec["formula"]["conditions"]
    assert count == 10


@pytest.mark.parametrize(
    "seq,qi,gi,bad",
    [
        (53, 4, 0, "-0.3"),
        (53, 5, 1, "0"),
        (53, 5, 2, "0"),
        (53, 6, 1, "0"),
        (53, 7, 2, "0"),
        (54, 7, 3, "0"),
        (54, 8, 3, "0"),
        (54, 8, 1, "-24"),
    ],
)
def test_nonnegative_magnitudes_and_nonzero_denominators(seq, qi, gi, bad):
    q = deepcopy(load_batch("grade8_batch11")["lessons"][seq - 51]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_magnetic_units_keep_case_and_dimension_separate():
    assert UNITS["T"] == ("magnetic_induction", Fraction(1))
    assert UNITS["mT"] == ("magnetic_induction", Fraction(1, 1000))
    assert UNITS["µT"] == ("magnetic_induction", Fraction(1, 10**6))
    q = load_batch("grade8_batch11")["lessons"][2]["assessments"][6]
    answer = {"formula": "F/(I*l)", "value": "100000", "unit": "μT"}
    assert grade_answer(q["grading_spec"], answer) == "correct"
    assert (
        grade_answer(q["grading_spec"], {**answer, "unit": "t"}) == "dimension_mismatch"
    )
    assert (
        grade_answer(q["grading_spec"], {**answer, "unit": "mN"})
        == "dimension_mismatch"
    )


def test_next_lorentz_section_not_used_as_frame_fact():
    l = load_batch("grade8_batch11")["lessons"][-1]
    assert all(
        155 not in r["pdf_pages"] for f in l["facts"].values() for r in f["source_refs"]
    )
