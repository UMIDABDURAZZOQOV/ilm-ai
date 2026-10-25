"""Electrostatic conductor scope, recorded lightning and current-source concepts."""

from copy import deepcopy

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    6: [
        "Sirtida",
        "Ortiqcha hajm zaryadi haqida, elektron va protonlar saqlanadi",
        "Notekis, uchlarda zichroq",
        "Ichki bo‘shliqni ekranlaydi",
        "Tayyor tasvirdagi kuzatuvni izohlash",
    ],
    7: ["Zaryad modulini", "Birliksiz", "Og‘irlik kuchiga qarshi yuqoriga"],
    8: [
        "Yorug‘lik tovushdan tezroq keladi",
        "Havoning tez qizishi va bosim o‘zgarishi",
        "Berilgan tovush modeli bo‘yicha taxmin",
        "Yerga ulangan himoya tizimining qismi",
    ],
    9: [
        "Zaryadli zarralarning tartibli harakati",
        "Elektr maydon",
        "Qisqa muddatli zaryad oqimi bo‘lishi mumkin",
        "Zaryad ajratish va maydon ta’minoti",
        "Issiqlik,kimyoviy va magnit",
    ],
    10: [
        "Kimyoviydan elektrga",
        "Mos asbob bilan qayta zaryadlab ishlatish mumkin",
        "Manba,simlar,iste’molchi va kalit",
        "O‘tkazuvchi yo‘l uziladi",
        "Boshqa energiya hisobiga zaryadlarni ajratadi",
        "Ulangan nuqta bilan ulanmagan kesishish belgilarini ajratamiz",
    ],
}


@pytest.mark.parametrize("seq", range(6, 11))
def test_conductor_current_source_semantic_answers_and_wrong_options(seq):
    l = load_batch("grade8_batch2")["lessons"][seq - 6]
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
    if seq in [6, 9, 10]:
        assert not l["formulas"]
        assert not any(
            q["response_kind"] == "numeric_quantity" for q in l["assessments"]
        )


def test_practice_independent_oracles_counts_medium_equilibrium_and_sound_domains():
    doc = load_batch("grade8_batch2")
    assert validate_batch(doc) == {
        "lessons": 5,
        "cards": 22,
        "formulas": 5,
        "worked_examples": 7,
        "assessments": 34,
        "frq": 6,
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
    assert count == 6
    for li, qi, gi, bad in [
        (1, 4, 1, "0"),
        (1, 5, 0, "1"),
        (1, 6, 2, "3000"),
        (1, 7, 1, "9.8"),
        (2, 5, 0, "343"),
        (2, 6, 1, "-1"),
    ]:
        q = deepcopy(doc["lessons"][li]["assessments"][qi])
        q["public"]["givens"][gi]["value"] = bad
        with pytest.raises(ValueError):
            calculation_value(q)
    # The source's next voltage heading is on inclusive page39; it is not lesson10 teaching.
    l = doc["lessons"][4]
    assert all(
        39 not in r["pdf_pages"]
        for fact in l["facts"].values()
        for r in fact["source_refs"]
    )
    assert doc["lessons"][1]["review"]["physical_experiment_completed"] is False
