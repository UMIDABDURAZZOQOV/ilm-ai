"""Independent elasticity, signed phase heat and source-rounded ice balance."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import new_answer
from test_physics_v2 import preview as preview  # noqa: PLC0414 - fixture export
from test_release_hardening import setup as setup  # noqa: PLC0414 - fixture export

from services.assessment_grading import grade_answer
from services.physics_curriculum import (
    calculation_value,
    import_batch,
    load_batch,
    validate_batch,
)

KEYS = {
    36: ["Elastik", "Pa", "Kichik chiziqli elastik sterjen modeli uchun"],
    37: [
        "0,003",
        "Ideal modeldagi eng katta chegaraviy uzunlikni",
        "Haqiqiy tajriba bajarilganini",
    ],
    38: [
        "Qattiqdan suyuqqa",
        "Yo‘q,erish uchun energiya olinadi",
        "Temperaturaning albatta pasayishini",
    ],
    39: [
        "Erish temperaturasidagi faza o‘zgarishini",
        "Manfiy",
        "Erish temperaturasida bo‘lishi",
    ],
    40: [
        "Kondensatsiya",
        "Bug‘lanish va kondensatsiya tezliklari",
        "Yo‘q,qaynash temperaturasi bosimga bog‘liq",
    ],
}


@pytest.mark.parametrize("seq", range(36, 41))
def test_semantic_all_options_and_order(seq):
    l = load_batch("grade9_batch8")["lessons"][seq - 36]
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


def test_literal_numeric_oracles_prefixes_equivalent_formulas_and_wrong_answers():
    d = load_batch("grade9_batch8")
    assert validate_batch(d) == {
        "lessons": 5,
        "cards": 24,
        "formulas": 21,
        "worked_examples": 5,
        "assessments": 40,
        "frq": 20,
    }
    n = 0
    for l in d["lessons"]:
        for q in l["assessments"]:
            s = q["grading_spec"]
            if s["kind"] != "numeric_quantity":
                continue
            n += 1
            a = new_answer(l, q)
            assert grade_answer(s, a) == "correct", q["key"]
            for f in s["formula"]["equivalents"]:
                assert grade_answer(s, {**a, "formula": f}) == "correct"
            assert (
                grade_answer(
                    s, {**a, "unit": "J" if s["dimension"] == "mass" else "kg"}
                )
                == "dimension_mismatch"
            )
            assert grade_answer(s, {**a, "value": "999999"}) == "out_of_tolerance"
            assert grade_answer(s, {**a, "formula": "1"}) == "wrong_formula"
    assert n == 20


@pytest.mark.parametrize(
    "seq,qi,gi,bad",
    [
        (36, 4, 0, "0.5"),
        (36, 4, 1, "0"),
        (36, 5, 1, "0"),
        (36, 6, 1, "0"),
        (36, 7, 0, "0"),
        (36, 7, 1, "-0.1"),
        (36, 8, 3, "0"),
        (36, 9, 2, "0"),
        (37, 4, 1, "0"),
        (37, 5, 3, "0"),
        (37, 6, 1, "0"),
        (37, 6, 2, "9.81"),
        (37, 7, 3, "0"),
        (38, 4, 1, "0"),
        (39, 4, 0, "0"),
        (39, 5, 1, "0"),
        (39, 6, 1, "0"),
        (39, 7, 1, "-0.2"),
        (39, 8, 2, "273"),
        (39, 8, 4, "0"),
        (40, 4, 0, "0"),
        (40, 5, 1, "0"),
        (40, 6, 1, "-20"),
        (40, 7, 1, "0"),
    ],
)
def test_nonphysical_inputs_and_explicit_g10_family(seq, qi, gi, bad):
    q = deepcopy(load_batch("grade9_batch8")["lessons"][seq - 36]["assessments"][qi])
    q["public"]["givens"][gi]["value"] = bad
    with pytest.raises(ValueError):
        calculation_value(q)


def test_strain_fraction_stress_units_and_geometric_stiffness_are_distinct():
    l = load_batch("grade9_batch8")["lessons"][0]
    q = l["assessments"][5]
    assert calculation_value(q) == Fraction(1, 500)
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "DL/l0", "value": "0.2", "unit": "%"}
        )
        == "correct"
    )
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "DL/l0", "value": "0.2", "unit": "1"}
        )
        == "out_of_tolerance"
    )
    q = l["assessments"][6]
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "F/S", "value": "100", "unit": "MPa"}
        )
        == "correct"
    )
    for bad in ("V", "N/m"):
        assert (
            grade_answer(
                q["grading_spec"], {"formula": "F/S", "value": "100", "unit": bad}
            )
            == "dimension_mismatch"
        )
    q = l["assessments"][9]
    assert calculation_value(q) == 100000
    assert (
        grade_answer(
            q["grading_spec"], {"formula": "E*S/l0", "value": "100", "unit": "GPa"}
        )
        == "dimension_mismatch"
    )


def test_preheating_excludes_latent_heat_and_freezing_condensing_keep_signed_q():
    d = load_batch("grade9_batch8")
    assert calculation_value(d["lessons"][2]["assessments"][4]) == 7800
    for li, qi, f, value, wrong in [
        (3, 7, "-m*lam", "-66.8", "66.8"),
        (4, 6, "-m*r", "-46", "46"),
    ]:
        q = d["lessons"][li]["assessments"][qi]
        assert calculation_value(q) < 0
        assert (
            grade_answer(
                q["grading_spec"], {"formula": f, "value": value, "unit": "kJ"}
            )
            == "correct"
        )
        assert (
            grade_answer(
                q["grading_spec"], {"formula": f, "value": wrong, "unit": "kJ"}
            )
            == "sign_error"
        )
        assert (
            grade_answer(
                q["grading_spec"], {"formula": f[1:], "value": wrong, "unit": "kJ"}
            )
            == "wrong_formula"
        )


def test_ice_balance_exact_rational_truth_and_one_gram_rounding():
    q = load_batch("grade9_batch8")["lessons"][3]["assessments"][8]
    assert calculation_value(q) == Fraction(84, 167)
    f = "mw*c*(Tw-Tm)/lam"
    assert (
        grade_answer(q["grading_spec"], {"formula": f, "value": "503", "unit": "g"})
        == "correct"
    )
    assert (
        grade_answer(q["grading_spec"], {"formula": f, "value": "502", "unit": "g"})
        == "out_of_tolerance"
    )
    assert (
        grade_answer(q["grading_spec"], {"formula": f, "value": "502.99", "unit": "g"})
        == "rounding_requirement"
    )


@pytest.mark.parametrize(
    "qi,wrong,formula", [(4, "-400", "p*(V2-V1)"), (5, "300", "p*(V2-V1)")]
)
def test_existing_issued_signed_snapshots_get_correct_feedback_without_rewriting_replay(
    preview, qi, wrong, formula
):
    """Exercise positive and negative old rubrics through the HTTP endpoint."""
    from uuid import uuid4

    from test_physics_v2 import submit

    from services.models import StudySession, User
    from services.study import utcnow

    client, factory = preview
    q = deepcopy(load_batch("grade9_batch4")["lessons"][0]["assessments"][qi])
    old_spec = deepcopy(q["grading_spec"])
    assert (
        old_spec["feedback"]["sign_error"]
        == "Bu vaziyatda javob manfiy bo‘lishi mumkin emas."
    )
    sid = "v2:1:sign-" + str(uuid4())
    with factory.begin() as db:
        import_batch(db, load_batch("grade9_batch4"))
        before_xp = db.get(User, 1).xp_total
        db.add(
            StudySession(
                id=sid,
                user_id=1,
                kind="assessment_v2",
                scope="physics-9-section-16-r1",
                started_at=utcnow(),
                questions={
                    "title": "Previously issued signed-work snapshot",
                    "content": {},
                    "assessments": [
                        {
                            "key": q["key"],
                            "kind": q["response_kind"],
                            "public": q["public"],
                            "grading_spec": q["grading_spec"],
                            "source_refs": q["source_refs"],
                        }
                    ],
                },
            )
        )
    answer = {"formula": formula, "value": wrong, "unit": "J"}
    first = submit(client, {"attempt_id": sid}, q["key"], answer)
    assert first.status_code == 200
    result = first.json()
    assert result["code"] == "sign_error" and not result["is_correct"]
    assert "Javob ishorasi talabga mos emas" in result["feedback"]
    assert "manfiy bo‘lishi mumkin emas" not in result["feedback"]
    assert submit(client, {"attempt_id": sid}, q["key"], answer).json() == result
    with factory() as db:
        assert db.get(User, 1).xp_total == before_xp
        assert (
            db.get(StudySession, sid).questions["assessments"][0]["grading_spec"]
            == old_spec
        )
