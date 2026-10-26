"""Fuel magnitudes, signed first-law work and narrow prior-source evidence."""

from copy import deepcopy

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    21: [
        "J/kg",
        "Batamom yonish va berilgan q uchun",
        "Boshqa qismlar yoki atrofga uzatiladi",
    ],
    22: ["Gazning tashqi kuchlarga qarshi bajargan ishi", "Q=0", "Q=DU"],
    23: ["Bir atomli klassik ideal gazning izobarik jarayoniga", "DU ga", "-A"],
    24: [
        "Atrofda ham o‘zgarish qolmasligi",
        "Qaytmas issiqlik jarayoni",
        "Boshqa o‘zgarishsiz o‘z-o‘zidan uzatish",
        "Yo‘q",
        "Ishqalanishsiz va noelastik deformatsiyasiz model",
    ],
    25: [
        "Issiq suv bergan energiyaning musbat moduli",
        "Qhot=Qcold",
        "Idish/atrof va o‘lchash/model shartlarini tahlil qilamiz",
    ],
}


@pytest.mark.parametrize("seq", range(21, 26))
def test_semantic_all_options_order_and_no_forced_second_law_math(seq):
    l = load_batch("grade9_batch5")["lessons"][seq - 21]
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
    if seq == 24:
        assert not l["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in l["assessments"]
        )


def test_all_literal_oracles_equivalents_and_unit_prefixes():
    d = load_batch("grade9_batch5")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 22,
        "formulas": 18,
        "worked_examples": 5,
        "assessments": 40,
        "frq": 18,
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
    assert count == 18


@pytest.mark.parametrize(
    "seq,qi,gi,bad",
    [
        (21, 4, 0, "0"),
        (21, 5, 1, "0"),
        (21, 6, 1, "0"),
        (21, 7, 2, "0"),
        (21, 8, 0, "1.01"),
        (21, 8, 0, "-0.1"),
        (21, 4, 1, "-0.5"),
        (23, 4, 0, "-400"),
        (23, 5, 2, "0"),
        (23, 5, 3, "8.30"),
        (23, 5, 0, "0"),
        (23, 6, 2, "0"),
        (23, 7, 2, "0"),
        (25, 4, 2, "313"),
        (25, 4, 1, "0"),
        (25, 5, 3, "313"),
        (25, 5, 0, "0"),
        (25, 6, 0, "-1"),
    ],
)
def test_released_magnitudes_heating_domains_and_fractions(seq, qi, gi, bad):
    q = deepcopy(load_batch("grade9_batch5")["lessons"][seq - 21]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_first_law_by_and_on_signs_and_signed_cooling():
    l = load_batch("grade9_batch5")["lessons"][1]
    q = l["assessments"][7]
    s = q["grading_spec"]
    assert calculation_value(q) == 400
    assert (
        grade_answer(s, {"formula": "DU-Q", "value": "400", "unit": "J"}) == "correct"
    )
    assert (
        grade_answer(s, {"formula": "Q-DU", "value": "-400", "unit": "J"})
        == "wrong_formula"
    )
    assert (
        grade_answer(s, {"formula": "DU-Q", "value": "-400", "unit": "J"})
        == "sign_error"
    )
    q = l["assessments"][9]
    assert calculation_value(q) == -700
    assert (
        grade_answer(q["grading_spec"], {"formula": "Q", "value": "-0.7", "unit": "kJ"})
        == "correct"
    )
    q = deepcopy(l["assessments"][8])
    q["public"]["givens"][0]["value"] = "450"
    assert calculation_value(q) == -450


def test_continuation_exact_page_note_and_original_map_boundary():
    d = load_batch("grade9_batch5")
    l = d["lessons"][-1]
    refs = [r for r in l["source_refs"] if r["pdf_pages"] == [74]]
    assert len(refs) == 1 and refs[0]["topic_id"] == "physics-9-section-25"
    assert refs[0]["extent_note"] == "original_image_continues_before_next_heading"
    bad = deepcopy(d)
    ref = next(r for r in bad["lessons"][-1]["source_refs"] if r["pdf_pages"] == [74])
    ref.pop("extent_note")
    with pytest.raises(ValueError, match="citation_outside_topic"):
        validate_batch(bad)
    bad = deepcopy(d)
    ref = next(r for r in bad["lessons"][-1]["source_refs"] if r["pdf_pages"] == [74])
    ref["pdf_pages"] = [75]
    with pytest.raises(ValueError):
        validate_batch(bad)


@pytest.mark.parametrize(
    "mutation", ["missing_note", "digest", "owner", "unlisted_page", "unlisted_topic"]
)
def test_prior_source_is_explicit_immutable_and_narrow(mutation):
    d = load_batch("grade9_batch5")
    l = d["lessons"][-1]
    ref = next(r for r in l["source_refs"] if r["topic_id"] == "physics-9-section-17")
    assert ref["pdf_pages"] == [56]
    assert ref["prerequisite_batch"] == "grade9_batch4"
    if mutation == "missing_note":
        ref.pop("prerequisite_note")
    elif mutation == "digest":
        ref["prerequisite_batch_sha256"] = "0" * 64
    elif mutation == "owner":
        ref["prerequisite_batch"] = "grade9_batch5"
    elif mutation == "unlisted_page":
        ref["pdf_pages"] = [55]
    else:
        ref["topic_id"] = "physics-9-section-16"
    with pytest.raises(
        ValueError,
        match="source_outside_reviewed_batch|source_prerequisite_review_binding",
    ):
        validate_batch(d)


def test_lab_magnitudes_distinct_from_signed_heat_and_not_real_measurements():
    l = load_batch("grade9_batch5")["lessons"][-1]
    assert (
        calculation_value(l["assessments"][4])
        == calculation_value(l["assessments"][5])
        == 12600
    )
    q = l["assessments"][4]
    s = q["grading_spec"]
    assert (
        grade_answer(s, {"formula": "c*mh*(Th-Tf)", "value": "-12600", "unit": "J"})
        == "sign_error"
    )
    assert l["review"]["physical_experiment_completed"] is False
    assert (
        l["review"]["physical_measurements"]
        == "not_claimed_conditional_digital_data_only"
    )
    q = deepcopy(l["assessments"][6])
    q["public"]["givens"][1]["value"] = "13000"
    assert calculation_value(q) == -400
