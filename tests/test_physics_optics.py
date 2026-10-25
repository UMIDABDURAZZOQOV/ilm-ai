"""Image-reviewed PDF132–151: optical keys, numerical oracles and model limits."""

from copy import deepcopy

import pytest
from test_physics_course import ORACLES_BATCH8, new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

MEANINGS = {
    47: [
        "Quyosh nurini qaytaruvchi",
        "Quyosh va yorug‘lik chiqaruvchi hasharot",
        "Yorug‘lik qabul qilgichga",
        "Stoldan qaytgan yorug‘lik ko‘zga keladi",
        "Sun’iy yorug‘lik manbaiga",
        "Barcha nur manbalari faqat kuchli qizigan jismlardir",
    ],
    48: [
        "To‘liq soya",
        "Yarim soya",
        "To‘g‘ri chiziq",
        "Yorug‘ dog‘",
        "Manbaning bir qismi to‘silib, bir qismi ko‘rinishi bilan",
        [
            "Manba, to‘siq va ekran joyini aniqlash",
            "To‘siq chetlaridan chegaraviy nurlarni o‘tkazish",
            "Nursiz, qisman va to‘liq yoritilgan sohalarni ajratish",
        ],
    ],
    49: [
        "Oy",
        "Yerning",
        "Quyoshning qisman tutilishini",
        "Yo‘q, fazani tutilish bilan almashtirmaslik kerak",
        "Yo‘q, soya va yarim soyadagi joyga bog‘liq",
        ["Quyosh", "Yer", "Oy"],
    ],
    50: [
        "Sirtga tik normaldan",
        "35°",
        "Chegarada yorug‘likning sinishi",
        "Shishada yorug‘lik sekinroq tarqaladi",
    ],
    51: [
        "Buyumlardan ko‘zga yorug‘lik kelishi",
        "Uni kuzatuv va dalil bilan solishtirish",
        "Oyning Yer soyasiga kirishi",
        "Nurlarning to‘planishi",
        "Tayyor chizma va izohlarni solishtirish",
        [
            "Ko‘z atrofni o‘zi yoritadi degan taxminni ajratish",
            "Qorong‘ida nega ko‘rmaymiz degan kuzatuv savolini berish",
            "Buyumdan ko‘zga keladigan nur izohini solishtirish",
        ],
    ],
    52: [
        "Buyum o‘lchamiga teng",
        "Haqiqiy nurlar emas, orqaga davomlari kesishgani uchun",
        "To‘nkarilgan, kattalashgan haqiqiy tasvir",
        "To‘g‘ri, kichiklashgan, mavhum",
    ],
    53: [
        "Yig‘uvchi qavariq linza",
        "Tarqalgan nurlarning orqaga davomlaridan",
        "Manfiy",
        "Metrda",
    ],
    54: [
        "Tarkibiy ranglarni turlicha og‘dirib ajratish",
        "Qizil",
        "Noto‘g‘ri, yetti nom shartli va ranglar asta o‘tadi",
        "Tomchilarda yorug‘lik sinishi, qaytishi va ranglarga ajralishi",
        "Barcha yetti rangning yo‘qdan to‘liq paydo bo‘lishi",
        ["Qizil", "Sariq", "Yashil", "Binafsha"],
    ],
    55: [
        "Tushish nuqtasidagi normaldan",
        "20°→20°",
        "0°",
        "Bir tekislikda",
        "Berilgan qayd va sxema tahlil qilindi",
        [
            "Normalni sxemada aniqlash",
            "Ikkala nur burchagini normaldan qayd qilish",
            "Juft burchaklarni tenglik bilan solishtirish",
        ],
    ],
    56: [
        "Tor oq nur—prizma—ekran",
        "Ingichka nur hosil qilish",
        "Boshqa sharoitlarni imkon qadar bir xil saqlash",
        "Berilgan sharoitda B qaydi kengroq",
        "Berilgan sxema va shartli o‘lchovlar tahlil qilindi",
        [
            "Qurilma va taqqoslanayotgan omilni aniqlash",
            "Har prizma uchun berilgan kenglik qaydini yozish",
            "Farqni nazorat qilingan sharoitlar bilan izohlash",
        ],
    ],
}


@pytest.mark.parametrize("sequence", range(47, 57))
def test_optical_concepts_reject_every_other_choice_and_reversed_order(sequence):
    lesson = load_batch("grade6_batch8")["lessons"][sequence - 47]
    questions = [
        q for q in lesson["assessments"] if q["response_kind"] != "numeric_quantity"
    ]
    assert len(questions) == len(MEANINGS[sequence])
    for q, meaning in zip(questions, MEANINGS[sequence]):
        public, spec = q["public"], q["grading_spec"]
        if isinstance(meaning, list):
            ids = {i["label"]: i["id"] for i in public["items"]}
            answer = [ids[m] for m in meaning]
            assert grade_answer(spec, {"order": answer}) == "correct"
            assert grade_answer(spec, {"order": answer[::-1]}) == "incorrect_order"
        else:
            assert meaning in [o["label"] for o in public["options"]]
            for option in public["options"]:
                assert grade_answer(spec, {"choice_id": option["id"]}) == (
                    "correct" if option["label"] == meaning else "incorrect_concept"
                )
    if sequence not in {50, 52, 53}:
        assert not lesson["formulas"]


def test_optical_numeric_oracles_alternatives_and_zero_or_virtual_domains():
    doc = load_batch("grade6_batch8")
    assert validate_batch(doc) == {
        "lessons": 10,
        "cards": 42,
        "formulas": 7,
        "worked_examples": 10,
        "assessments": 63,
        "frq": 9,
    }
    seen = set()
    for lesson in doc["lessons"]:
        for q in lesson["assessments"]:
            spec = q["grading_spec"]
            if spec["kind"] != "numeric_quantity":
                continue
            seen.add((lesson["sequence"], int(q["key"].rsplit("q", 1)[1])))
            answer = new_answer(lesson, q)
            for expression in spec["formula"]["equivalents"]:
                assert (
                    grade_answer(spec, {**answer, "formula": expression}) == "correct"
                )
            bad_unit = "kg" if spec["dimension"] == "time" else "s"
            assert (
                grade_answer(spec, {**answer, "unit": bad_unit}) == "dimension_mismatch"
            )
            assert grade_answer(spec, {**answer, "formula": "1"}) == "wrong_formula"
            assert (
                grade_answer(spec, {**answer, "value": "999999999999"})
                == "out_of_tolerance"
            )
            if spec["rule"] in {
                "spherical_focus",
                "concave_image",
                "lens_power",
                "lens_focal",
            }:
                changed = deepcopy(q)
                changed["public"]["givens"][0]["value"] = "0"
                with pytest.raises(ValueError):
                    calculation_value(changed)
    assert seen == set(ORACLES_BATCH8)
    # Independently probe singular and virtual-image input against real-only rule.
    mirror = doc["lessons"][5]["assessments"][6]
    for distance in ["15", "10"]:
        changed = deepcopy(mirror)
        changed["public"]["givens"][1]["value"] = distance
        with pytest.raises(ValueError, match="real_concave_image_domain"):
            calculation_value(changed)
    assert all(
        l["review"]["physical_experiment_completed"] is False
        for l in doc["lessons"][-2:]
    )
