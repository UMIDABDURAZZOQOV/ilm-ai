"""Digital safety scope, source continuation and electron/current direction."""

from copy import deepcopy

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    36: [
        "Elektr energiyadan ichki energiyaga",
        "Katta solishtirma qarshilik va temperaturaga chidamlilik",
        "Tokdan ajratish va issiqlik uzatish",
        "Kavshar qotishmasini eritishga",
    ],
    37: [
        "Parallel",
        "Me’yordan ortiq tokda zanjirni uzish",
        "Qizib uzilishi mumkin",
        "Uni raqamli tahlilda nosoz deb belgilaymiz,o‘zimiz montaj qilmaymiz",
        "Barcha ochiq qismlarga tegish xavfsizligini",
    ],
    38: [
        "O‘quvchi tegib tekshirmaydi,yordam chaqiradi",
        "Bu holat kuchlanish yo‘qligini isbotlamaydi",
        "Mumkin emas",
        "Kichik qarshilikli yo‘ldan tokning keskin ortishi",
        "Bevosita tegmasdan kattalar va yordam xizmatini chaqirish",
    ],
    39: [
        "Hisoblanayotgan o‘tkazgich bo‘lagining",
        "Quvvatlar yig‘indisini umumiy U ga bo‘lib",
        "R ga",
    ],
    40: [
        "Erkin elektronlar",
        "O‘zi yo‘nalgan makroskopik tok degani emas",
        "Manfiydan musbatga",
        "Qarama-qarshi",
        "Tayyor bayondagi dalil va xulosani tahlil qilish",
    ],
}


@pytest.mark.parametrize("sequence", range(36, 41))
def test_semantic_answers_and_all_wrong_options(sequence):
    lesson = load_batch("grade8_batch8")["lessons"][sequence - 36]
    qs = [q for q in lesson["assessments"] if q["response_kind"] == "concept_selection"]
    assert len(qs) == len(KEYS[sequence])
    for q, label in zip(qs, KEYS[sequence]):
        assert label in [o["label"] for o in q["public"]["options"]]
        for option in q["public"]["options"]:
            assert grade_answer(q["grading_spec"], {"choice_id": option["id"]}) == (
                "correct" if option["label"] == label else "incorrect_concept"
            )
    for q in lesson["assessments"]:
        if q["response_kind"] == "ordering":
            assert (
                grade_answer(q["grading_spec"], {"order": ["s2", "s3", "s1"]})
                == "correct"
            )
            assert (
                grade_answer(q["grading_spec"], {"order": ["s3", "s2", "s1"]})
                != "correct"
            )
    if sequence in [37, 38, 40]:
        assert not lesson["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in lesson["assessments"]
        )
    if sequence in [37, 38]:
        assert (
            lesson["review"]["electrical_safety_expert"]
            == "required_before_general_publication"
        )
        assert lesson["review"]["physical_experiment_completed"] is False


def test_five_independent_numeric_answers_alternatives_and_wrong_dimensions():
    doc = load_batch("grade8_batch8")
    assert validate_batch(doc) == {
        "lessons": 5,
        "cards": 20,
        "formulas": 5,
        "worked_examples": 5,
        "assessments": 32,
        "frq": 5,
    }
    count = 0
    for lesson in doc["lessons"]:
        for q in lesson["assessments"]:
            spec = q["grading_spec"]
            if spec["kind"] != "numeric_quantity":
                continue
            count += 1
            answer = new_answer(lesson, q)
            for formula in spec["formula"]["equivalents"]:
                assert grade_answer(spec, {**answer, "formula": formula}) == "correct"
            assert grade_answer(spec, {**answer, "unit": "kg"}) == "dimension_mismatch"
            assert (
                grade_answer(spec, {**answer, "value": "123456789"})
                == "out_of_tolerance"
            )
            assert grade_answer(spec, {**answer, "formula": "1"}) == "wrong_formula"
    assert count == 5


@pytest.mark.parametrize(
    "qi,gi,bad", [(4, 3, "0"), (5, 3, "0"), (6, 2, "0"), (7, 1, "0")]
)
def test_wire_load_and_heat_ratio_denominators(qi, gi, bad):
    q = deepcopy(load_batch("grade8_batch8")["lessons"][3]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_original_page112_continuation_is_explicit_and_cannot_extend_arbitrarily():
    doc = load_batch("grade8_batch8")
    lesson = doc["lessons"][3]
    ref = lesson["source_refs"][-1]
    assert ref["topic_id"] == "physics-8-section-39"
    assert ref["pdf_pages"] == [112]
    assert ref["printed_pages"] == [112]
    assert ref["segment_pages"][0]["segment_local_pdf_page"] == 24
    assert ref["extent_note"] == "original_image_continues_before_next_heading"
    bad = deepcopy(doc)
    bad["lessons"][3]["source_refs"][-1].pop("extent_note")
    with pytest.raises(ValueError, match="citation_outside_topic"):
        validate_batch(bad)
    bad = deepcopy(doc)
    ref = bad["lessons"][3]["source_refs"][-1]
    # Even a valid-looking continuation note does not license another topic.
    ref["topic_id"] = "physics-8-section-38"
    with pytest.raises(ValueError, match="citation_outside_topic"):
        validate_batch(bad)
