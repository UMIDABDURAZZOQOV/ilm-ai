"""Source-reviewed conceptual keys, not inferred from the private answer rubric.

PDF/printed102–114, Turdiyev2017. Historical hypotheses, measurement conditions
and digital laboratory scope must not silently become incorrect physical rules.
"""

import pytest

from services.assessment_grading import grade_answer
from services.physics_curriculum import load_batch, validate_batch

# Each string identifies the scientific answer, independently of option ids and
# the stored key. Reordering options must preserve meaning; mis-keying must fail.
ANSWERS = {
    36: [
        "Manba — Quyosh; qabul qiluvchi — yo‘lak",
        "Ishqalanishda mexanik energiya ichki energiyaga aylanadi",
        "Temperatura",
        "Energiyaning bir qismi tuzilish o‘zgarishiga sarflanmoqda",
        "Joul",
        "Issiqlik — jismdan jismga oqadigan alohida modda",
    ],
    37: [
        "Kengayish xossalari turlicha",
        "Temperaturaga bog‘liq uzayish uchun joy qoldirishga",
        "Birlashtirilgan qatlamlarning turlicha uzayishi",
        "4°C",
        "Ortadi",
        "Qatlamlar notekis isib, turlicha kengayishi mumkin",
    ],
    38: [
        "Issiqlik o‘tkazuvchanlik",
        "Konveksiya",
        "Mis yog‘ochdan yaxshiroq issiqlik o‘tkazadi",
        "Suv yomon o‘tkazadi va issiq qatlam pastga kuchli oqmaydi",
        "Suyuqlik va gazda",
        [
            "Radiator yonidagi havo qizib kengayadi",
            "Zichligi kamaygan havo yuqoriga ko‘tariladi",
            "Bo‘shagan joyga sovuqroq havo keladi",
        ],
    ],
    39: [
        "Nurlanish",
        "Yuzaning nurlanishni yutish va qaytarishga ta’siri",
        "Gaz orqali o‘tkazuvchanlik va konveksiyani kamaytiradi",
        "Nurlanish orqali almashinuvni kamaytirishga",
        "Issiqlikni yaxshi uzatadigan material",
        "Bir necha usul bir vaqtda qatnashishi mumkin",
    ],
    40: [
        "Zarralarning harakatiga",
        "Taxminni kuzatuv bilan tekshirish",
        "Tarixiy, e’tiroz bildirilgan taxmin",
        "Issiq jism yaqinligi, ishqalanish, yoritilish",
        "Tashqaridan issiqlik kirishi sekinlashadi",
        [
            "Beruniy muzlagan suv idishni nega yorishini so‘raydi",
            "Ibn Sino havo bo‘laklari haqidagi taxminni taklif qiladi",
            "Beruniy tashqariga yorilish kuzatuvi bilan e’tiroz bildiradi",
        ],
    ],
    41: [
        "Termometr bilan o‘lchash",
        "Suyuqlik ustunining yuqoriga ko‘tarilishi",
        "Normal atmosfera bosimida toza suv 100°C",
        "1°C",
        "Suvda ko‘rsatish barqarorlashgach, asbob suvda turganida",
        "Bu asbob tuzilishiga bog‘liq alohida xususiyat",
    ],
    42: [
        "Quyosh nuri va isitkichdan uzoq, shkalasi ko‘rinadigan joyda",
        "Barqarorlashishini kutamiz",
        "t3",
        "Namuna nomi, son va temperatura birligi",
        "Berilgan termometriya qaydlari va reja tahlil qilindi",
        [
            "Dastlabki suvlar uchun t1 va t2 ni alohida yozish",
            "Namunalar birlashtirilib aralashtirilgan bosqichni belgilash",
            "Aralashma ko‘rsatishi t3 ni qayd etish",
        ],
    ],
}


@pytest.mark.parametrize("section", range(36, 43))
def test_thermal_answers_have_scientific_meaning_and_reject_distractors(section):
    lesson = next(
        l for l in load_batch("grade6_batch6")["lessons"] if l["sequence"] == section
    )
    assert not lesson["formulas"]  # No invented Q=cmΔt/expansion/mixture law.
    assert len(lesson["assessments"]) == len(ANSWERS[section])
    for q, meaning in zip(lesson["assessments"], ANSWERS[section]):
        public, spec = q["public"], q["grading_spec"]
        if isinstance(meaning, list):
            ids = {i["label"]: i["id"] for i in public["items"]}
            answer = {"order": [ids[s] for s in meaning]}
            assert grade_answer(spec, answer) == "correct"
            assert (
                grade_answer(spec, {"order": answer["order"][::-1]})
                == "incorrect_order"
            )
        else:
            ids = {o["label"]: o["id"] for o in public["options"]}
            assert grade_answer(spec, {"choice_id": ids[meaning]}) == "correct"
            for label, choice in ids.items():
                if label != meaning:
                    assert (
                        grade_answer(spec, {"choice_id": choice}) == "incorrect_concept"
                    )
        assert spec["feedback"]["incorrect"] and spec["solution"]


def test_thermal_coverage_and_digital_lab_claims_are_honest():
    doc = load_batch("grade6_batch6")
    assert validate_batch(doc) == {
        "lessons": 7,
        "cards": 29,
        "formulas": 0,
        "worked_examples": 7,
        "assessments": 42,
        "frq": 0,
    }
    assert {
        p for l in doc["lessons"] for r in l["source_refs"] for p in r["pdf_pages"]
    } == set(range(102, 115))
    lab = doc["lessons"][-1]
    assert lab["review"]["physical_experiment_completed"] is False
    assert lab["source_refs"][0]["pdf_pages"] == [114]
    assert "o‘rtacha formula" in lab["facts"]["record"]["claim"]
