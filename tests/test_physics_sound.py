"""Original PDF156–167 conceptual answer keys and independent numeric probes."""

from copy import deepcopy

import pytest
from test_physics_course import ORACLES_BATCH9, new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    57: [
        "Shoxchalarning tebranishi",
        "Mikrofon",
        "Ultratovush",
        "Yo‘q, eshitish sezgirligi farq qiladi",
    ],
    58: [
        "Tebranishni uzatuvchi moddiy muhit yo‘q",
        "Yorug‘lik havodagi tovushdan ancha tezroq",
        "Qattiq jism ham tovush tebranishini uzatadi",
        "20°C havo uchun berilgan model sifatida",
    ],
    59: [
        "Amplituda",
        "Ingichkaroq bo‘ladi",
        "Tembr",
        "Tovushni yo‘naltirish",
        "Qattiqlik va ton balandligi alohida xususiyatlar",
    ],
    60: [
        "Borish va qaytishning jami yo‘liga",
        "Exolot",
        "Bu vaziyatda bir tomon kelish vaqti berilgani uchun",
    ],
    61: [
        "Tarang membrana",
        "Juda qattiq tovush ham salbiy ta’sir qilishi mumkin",
        "Ko‘rsatilgan chastota va material sharoiti uchun",
        "Tovush tarqalishi, qaytishi va yutilishi",
    ],
}


@pytest.mark.parametrize("seq", range(57, 62))
def test_sound_concept_keys_and_all_wrong_choices(seq):
    l = load_batch("grade6_batch9")["lessons"][seq - 57]
    qs = [q for q in l["assessments"] if q["response_kind"] == "concept_selection"]
    assert len(qs) == len(KEYS[seq])
    for q, meaning in zip(qs, KEYS[seq]):
        assert meaning in [o["label"] for o in q["public"]["options"]]
        for o in q["public"]["options"]:
            assert grade_answer(q["grading_spec"], {"choice_id": o["id"]}) == (
                "correct" if o["label"] == meaning else "incorrect_concept"
            )
    if seq == 59:
        assert not l["formulas"]


def test_sound_numeric_oracles_and_physical_domains():
    doc = load_batch("grade6_batch9")
    assert validate_batch(doc) == {
        "lessons": 5,
        "cards": 20,
        "formulas": 6,
        "worked_examples": 5,
        "assessments": 29,
        "frq": 9,
    }
    seen = set()
    for l in doc["lessons"]:
        for q in l["assessments"]:
            spec = q["grading_spec"]
            if spec["kind"] != "numeric_quantity":
                continue
            seen.add((l["sequence"], int(q["key"].rsplit("q", 1)[1])))
            answer = new_answer(l, q)
            for f in spec["formula"]["equivalents"]:
                assert grade_answer(spec, {**answer, "formula": f}) == "correct"
            assert (
                grade_answer(spec, {**answer, "value": "999999999"})
                == "out_of_tolerance"
            )
            assert grade_answer(spec, {**answer, "unit": "kg"}) == "dimension_mismatch"
            assert grade_answer(spec, {**answer, "formula": "1"}) == "wrong_formula"
    assert seen == set(ORACLES_BATCH9)
    frequency = doc["lessons"][0]["assessments"][4]
    for field, bad in [("value", "2.5"), ("unit", "%")]:
        q = deepcopy(frequency)
        q["public"]["givens"][0][field] = bad
        with pytest.raises(ValueError):
            calculation_value(q)
    q = deepcopy(frequency)
    q["public"]["givens"][1]["value"] = "0"
    with pytest.raises(ValueError):
        calculation_value(q)
    absorption = deepcopy(doc["lessons"][4]["assessments"][4])
    absorption["public"]["givens"][0]["value"] = "41"
    with pytest.raises(ValueError, match="absorption_energy_domain"):
        calculation_value(absorption)
