"""Independent image-reviewed keys, signed acceleration and stop-domain probes."""

from copy import deepcopy

import pytest
from test_physics_course import new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    6: [
        "s yo‘l bosib o‘tilgan ayni oraliq",
        "Bir xil tezlik",
        "Tezlik",
        "O‘rtacha tezlik moduli kattaroq",
    ],
    7: [
        "Tezlik4m/s bo‘lib saqlanadi",
        "Kattaroq tezlikka",
        "Bosib o‘tilgan yo‘lga",
        "O‘qlar nomi, birligi va masshtabi",
    ],
    8: [
        "Jami yo‘lni jami vaqtga bo‘lish",
        "Jami vaqtga qo‘shamiz",
        "Buni o‘rtacha sonning o‘zidan bilib bo‘lmaydi",
        "O‘sha qisqa oraliqdagi taqribiy tezlik",
    ],
    9: ["Tekis o‘zgaruvchan harakatga", "m/s2", "Manfiy", "Ha, vektor o‘zgargan"],
    10: ["v0+a*t", "Manfiy", "Doimiy tezlanish va yo‘nalish almashmasligida", "v=a*t"],
}


@pytest.mark.parametrize("seq", range(6, 11))
def test_motion_keys_match_scientific_meaning_not_option_position(seq):
    l = load_batch("grade7_batch2")["lessons"][seq - 6]
    qs = [q for q in l["assessments"] if q["response_kind"] == "concept_selection"]
    assert len(qs) == len(KEYS[seq])
    for q, label in zip(qs, KEYS[seq]):
        assert label in [o["label"] for o in q["public"]["options"]]
        for o in q["public"]["options"]:
            assert grade_answer(q["grading_spec"], {"choice_id": o["id"]}) == (
                "correct" if label == o["label"] else "incorrect_concept"
            )


def test_motion_numeric_oracles_and_all_reviewed_alternatives():
    doc = load_batch("grade7_batch2")
    assert validate_batch(doc) == {
        "lessons": 5,
        "cards": 20,
        "formulas": 8,
        "worked_examples": 5,
        "assessments": 35,
        "frq": 15,
    }
    count = 0
    for l in doc["lessons"]:
        for q in l["assessments"]:
            spec = q["grading_spec"]
            if spec["kind"] != "numeric_quantity":
                continue
            a = new_answer(l, q)
            count += 1
            for f in spec["formula"]["equivalents"]:
                assert grade_answer(spec, {**a, "formula": f}) == "correct"
            assert grade_answer(spec, {**a, "unit": "kg"}) == "dimension_mismatch"
            assert grade_answer(spec, {**a, "formula": "1"}) == "wrong_formula"
            assert grade_answer(spec, {**a, "value": "123456789"}) == "out_of_tolerance"
    assert count == 15
    negative = doc["lessons"][3]["assessments"][5]["grading_spec"]
    assert (
        grade_answer(
            negative, {"formula": "(v-v0)/t", "value": "−300", "unit": "cm/s²"}
        )
        == "correct"
    )
    assert (
        grade_answer(negative, {"formula": "(v-v0)/t", "value": "3", "unit": "m/s2"})
        == "sign_error"
    )
    # Same initial motion and constant braking cannot use speed branch beyond stop.
    q = deepcopy(doc["lessons"][4]["assessments"][5])
    q["public"]["givens"][2]["value"] = "9"
    with pytest.raises(ValueError, match="before_stop_velocity_domain"):
        calculation_value(q)
    q = deepcopy(doc["lessons"][3]["assessments"][4])
    q["public"]["givens"][2]["value"] = "0"
    with pytest.raises(ValueError):
        calculation_value(q)
