"""Faraday units, explicit empirical constants, exact fractions and coating geometry."""

from copy import deepcopy

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    41: [
        "Musbat ion",
        "Musbat va manfiy ionlar",
        "Manfiy katodga",
        "Tok aynan mutlaq nol ekanini",
        "Eritmada musbat va manfiy ionlarga ajralish",
    ],
    42: ["Bir kulonga to‘g‘ri kelgan massa", "Ikki marta ortadi", "1e-6kg/C"],
    43: [
        "kg/mol",
        "Faradey doimiysining berilgan yaqinlashuvi",
        "Musbat butun elektronlar soni",
    ],
    44: [
        "Yo‘q,jami yuza allaqachon berilgan",
        "2*a*b",
        "Berilgan nazariy model massasi",
    ],
    45: [
        "Galvanostegiya",
        "Galvanoplastika",
        "Mis o‘tirishi bilan qalinlashadi",
        "Qavariq",
        "Tayyor rasmlar va jarayon maqsadlarini tahlil qilish",
    ],
}


@pytest.mark.parametrize("sequence", range(41, 46))
def test_source_semantics_and_wrong_options(sequence):
    lesson = load_batch("grade8_batch9")["lessons"][sequence - 41]
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
                grade_answer(q["grading_spec"], {"order": ["s1", "s2", "s3"]})
                != "correct"
            )
    if sequence in [41, 45]:
        assert not lesson["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in lesson["assessments"]
        )
    assert lesson["review"]["physical_experiment_completed"] is False


def test_eleven_independent_numeric_oracles_and_all_alternatives():
    doc = load_batch("grade8_batch9")
    assert validate_batch(doc) == {
        "lessons": 5,
        "cards": 21,
        "formulas": 11,
        "worked_examples": 7,
        "assessments": 35,
        "frq": 11,
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
            assert grade_answer(spec, {**answer, "unit": "s"}) == "dimension_mismatch"
            assert (
                grade_answer(spec, {**answer, "value": "123456789"})
                == "out_of_tolerance"
            )
            assert grade_answer(spec, {**answer, "formula": "1"}) == "wrong_formula"
            assert (
                grade_answer(
                    spec,
                    {
                        **answer,
                        "expected_rational": {"numerator": "0", "denominator": "1"},
                    },
                )
                == "answer_required"
            )
    assert count == 11


@pytest.mark.parametrize(
    "li,qi,gi,bad",
    [
        (1, 6, 1, "0"),
        (1, 7, 2, "0"),
        (1, 8, 1, "0"),
        (2, 4, 1, "0.5"),
        (2, 4, 2, "96485"),
        (3, 4, 3, "0"),
        (3, 5, 3, "0"),
        (3, 6, 4, "0"),
    ],
)
def test_constants_valence_and_geometry_domains(li, qi, gi, bad):
    q = deepcopy(load_batch("grade8_batch9")["lessons"][li]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_rounding_is_stated_grid_and_exact_private_truth_matches_source_arithmetic():
    doc = load_batch("grade8_batch9")
    questions = [
        doc["lessons"][2]["assessments"][4],
        doc["lessons"][3]["assessments"][4],
        doc["lessons"][3]["assessments"][6],
    ]
    for q in questions:
        assert "qadamga" in q["public"]["prompt"]
        assert "expected_rational" not in q["public"]
        spec = q["grading_spec"]
        assert "expected_rational" in spec
        assert "rounding_requirement" in spec["feedback"]
    k = questions[0]["grading_spec"]
    answer = {"value": "1.119", "unit": "mg/C", "formula": "M/(Z*F)"}
    assert grade_answer(k, answer) == "correct"
    assert grade_answer(k, {**answer, "value": "1.120"}) == "out_of_tolerance"
    assert grade_answer(k, {**answer, "value": "1.1192"}) == "rounding_requirement"
    assert (
        grade_answer(k, {**answer, "value": "1.119", "unit": "kg/C"})
        == "out_of_tolerance"
    )
    thickness = questions[2]["grading_spec"]
    assert (
        grade_answer(
            thickness, {"value": "2.51", "unit": "µm", "formula": "k*I*t/(rho*a*b)"}
        )
        == "wrong_formula"
    )
    bad = deepcopy(doc)
    bad["lessons"][2]["assessments"][4]["grading_spec"]["expected_rational"][
        "numerator"
    ] = "109"
    with pytest.raises(ValueError, match="calculation_answer_mismatch"):
        validate_batch(bad)
