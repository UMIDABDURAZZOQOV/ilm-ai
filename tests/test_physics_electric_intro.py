"""Source-reviewed charge signs, instruments/circuits and V↔mV boundary cases."""

from copy import deepcopy

import pytest

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

KEYS = {
    43: [
        "Itarilish",
        "Manfiy",
        "Musbat",
        "Elektr zaryadsiz",
        "Metall ichidagi zaryadlar qayta taqsimlanadi",
        "Bir-biriga tortiladi",
    ],
    44: [
        "Zaryadlangan zarralarning tartibli harakati",
        "Ikkinchi strelka ochilmagan",
        "Kimyoviy jarayonga",
        "Akkumulyator",
        "Voltmetrni parallel ulash",
        "Musbat zaryadning harakat yo‘nalishi",
    ],
    45: [
        "Berk tok yo‘li",
        "Ampermetrni ketma-ket ulash",
        "Parallel ulanish",
        [
            "Manba, lampochka, sim va kalit belgilarini aniqlash",
            "Ochiq kalitli sxemadagi ulanishlarni tekshirish",
            "Kalit yopilganda berk yo‘l hosil bo‘lishini tekshirish",
        ],
    ],
    46: [
        "Elektr hisoblagich",
        "Keraksiz energiya sarfini kamaytiradi",
        "Kerakli yoritishni kamroq elektr energiyasi bilan olish",
        "Tarmoqni ochmasdan, berilgan qurilmalar ishlash rejasini tahlil qilish",
        "Vazifalari turli, ikkalasi ham energiya sarflaydi",
        "Hisoblagich energiya sarfini, voltmetr kuchlanishni o‘lchaydi",
    ],
}


@pytest.mark.parametrize("sequence", range(43, 47))
def test_source_reviewed_electric_concepts_and_all_distractors(sequence):
    lesson = load_batch("grade6_batch7")["lessons"][sequence - 43]
    conceptual = [
        q for q in lesson["assessments"] if q["response_kind"] != "numeric_quantity"
    ]
    assert len(conceptual) == len(KEYS[sequence])
    for q, meaning in zip(conceptual, KEYS[sequence]):
        p, spec = q["public"], q["grading_spec"]
        if isinstance(meaning, list):
            ids = {i["label"]: i["id"] for i in p["items"]}
            answer = [ids[m] for m in meaning]
            assert grade_answer(spec, {"order": answer}) == "correct"
            assert grade_answer(spec, {"order": answer[::-1]}) == "incorrect_order"
        else:
            for option in p["options"]:
                result = grade_answer(spec, {"choice_id": option["id"]})
                assert result == (
                    "correct" if option["label"] == meaning else "incorrect_concept"
                )
            assert meaning in [o["label"] for o in p["options"]]
    if sequence != 45:
        assert not lesson["formulas"]


def test_voltage_calculations_accept_equivalent_units_not_wrong_quantity_or_case():
    doc = load_batch("grade6_batch7")
    assert validate_batch(doc) == {
        "lessons": 4,
        "cards": 18,
        "formulas": 1,
        "worked_examples": 4,
        "assessments": 24,
        "frq": 2,
    }
    qs = doc["lessons"][2]["assessments"][-2:]
    # Independently computed 3V=3000mV and1.8V=1800mV; alternative kV allowed.
    for q, volts, mv, kv in zip(
        qs, ["3", "1.8"], ["3000", "1800"], ["0.003", "0.0018"]
    ):
        spec = q["grading_spec"]
        for unit, value in [("V", volts), ("mV", mv), ("kV", kv)]:
            assert (
                grade_answer(
                    spec, {"formula": "y=x*1000", "value": value, "unit": unit}
                )
                == "correct"
            )
        assert (
            grade_answer(spec, {"formula": "1000*x", "value": volts, "unit": "mV"})
            == "out_of_tolerance"
        )
        assert (
            grade_answer(spec, {"formula": "x/1000", "value": mv, "unit": "mV"})
            == "wrong_formula"
        )
        assert (
            grade_answer(spec, {"formula": "1000*x", "value": mv, "unit": "mv"})
            == "unknown_unit"
        )
        assert (
            grade_answer(spec, {"formula": "1000*x", "value": mv, "unit": "W"})
            == "dimension_mismatch"
        )
        for key, bad in [("value", "-3"), ("unit", "mV"), ("unit", "kg")]:
            changed = deepcopy(q)
            changed["public"]["givens"][0][key] = bad
            with pytest.raises(ValueError):
                calculation_value(changed)
