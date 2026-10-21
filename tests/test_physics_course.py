"""Reviewed batches append to the original course without resetting any progress."""

import hashlib

import pytest
from test_physics_v2 import (
    PREFIX,
    answer_all,
    assert_private_absent,
    correct,
    finish,
    start,
    submit,
)
from test_physics_v2 import preview as preview  # noqa: PLC0414 - pytest fixture export
from test_release_hardening import setup as setup  # noqa: PLC0414 - pytest fixture export

from scripts.audit_physics_course import report
from services.assessment_grading import grade_answer
from services.assessment_models import CurriculumLessonV2
from services.models import User
from services.physics_curriculum import (
    DIRECTORY,
    import_batch,
    load_batch,
    load_course,
    validate_batch,
)

# Independent explicit numeric answer oracles. None reads expected_si or calls
# the production arithmetic calculator. Equivalent units and reciprocal powers
# deliberately differ from the content's stored canonical solution strings.
ORACLES = {
    (9, 6): ("0.0000000003", "m", "V/S"),
    (9, 7): ("0,3", "nm", "V*S^-1"),
    (13, 5): ("0.02", "mm/s", "h/t"),
    (13, 6): ("0.000015", "m/s", "h*t^-1"),
    (14, 5): ("850", "g", "1000*x"),
    (14, 6): ("0.375", "kg", "x/1000"),
    (14, 7): ("1600", "kg", "1000*x"),
    (15, 6): ("170", "g", "m3+m1+m2"),
    (15, 7): ("160", "g", "M-m0"),
    (16, 6): ("2.7", "g/cm³", "m/V"),
    (16, 7): ("20", "g", "V*rho"),
    (16, 8): ("30", "cm^3", "m*rho^-1"),
    (16, 9): ("15", "cm3", "V2-V1"),
    (17, 5): ("40", "cm³", "l3*l1*l2"),
    (17, 6): ("2700", "kg/m^3", "m*V^-1"),
    (17, 7): ("18", "cm3", "V2-V1"),
    (17, 8): ("2.5", "g/cm3", "m/V"),
}


ORACLES_BATCH3 = {
    (19, 5): ("2350", "m", "x*1000"),
    (19, 6): ("270", "s", "60*x"),
    (19, 7): ("4500", "s", "3600*x"),
    (19, 8): ("90", "m", "n*l"),
    (20, 5): ("6", "m/s", "s/t"),
    (20, 6): ("30", "m", "t*v"),
    (20, 7): ("12", "s", "s/v"),
    (20, 8): ("3", "m/s", "(s2+s1)/(t2+t1)"),
    (21, 5): ("4.905", "N", "g*m"),
    (21, 6): ("2", "kg", "F/g"),
    (23, 5): ("0.02", "m²", "b*a"),
    (23, 6): ("3", "kPa", "F/S"),
    (23, 7): ("0.1", "kN", "p*S"),
    (23, 8): ("300", "cm²", "F/p"),
    (24, 6): ("160", "N", "F1*(S2/S1)"),
    (24, 7): ("0.12", "kN", "S2/S1*F1"),
}


def new_answer(lesson, q):
    spec = q["grading_spec"]
    if spec["kind"] == "numeric_quantity":
        number = int(q["key"].rsplit("q", 1)[1])
        value, unit, formula = (ORACLES | ORACLES_BATCH3)[(lesson["sequence"], number)]
        return {"value": value, "unit": unit, "formula": formula}
    return correct(q)


def test_original_frozen_content_and_honest_course_coverage():
    assert (
        hashlib.sha256((DIRECTORY / "grade6_batch1.json").read_bytes()).hexdigest()
        == "8d13627ce9275bda5a402b86d4ea94d67b1892c1538189c88dcc51891a3c6a78"
    )
    data = report()
    assert (data["authored"], data["remaining"], data["source_total"]) == (24, 292, 316)
    assert [r["authored"] for r in data["grades"]] == [24, 0, 0, 0, 0, 0]
    row = data["grades"][0]
    assert (
        row["cards"],
        row["assessments"],
        row["frq"],
        row["laboratories"],
        row["practicals"],
    ) == (99, 158, 38, 3, 1)
    assert row["next_section"] == 25
    assert len(load_course()) == 3
    with pytest.raises(ValueError, match="batch_not_reviewed"):
        load_batch("arbitrary_unreviewed_file")


def test_batch_two_independent_calculation_and_wrong_answers():
    doc = load_batch("grade6_batch2")
    assert validate_batch(doc) == {
        "lessons": 10,
        "cards": 41,
        "formulas": 14,
        "worked_examples": 12,
        "assessments": 67,
        "frq": 17,
    }
    seen = set()
    for lesson in doc["lessons"]:
        for q in lesson["assessments"]:
            answer = new_answer(lesson, q)
            spec = q["grading_spec"]
            assert grade_answer(spec, answer) == "correct", q["key"]
            if spec["kind"] == "numeric_quantity":
                seen.add((lesson["sequence"], int(q["key"].rsplit("q", 1)[1])))
                assert (
                    grade_answer(spec, {**answer, "unit": "s"}) == "dimension_mismatch"
                )
                assert (
                    grade_answer(spec, {**answer, "value": "999999999"})
                    == "out_of_tolerance"
                )
                assert grade_answer(spec, {**answer, "formula": "1"}) == "wrong_formula"
                assert (
                    grade_answer(spec, {**answer, "formula": "V.__class__"})
                    != "correct"
                )
                assert grade_answer(spec, {**answer, "value": "1/0"}) == "domain_error"
    assert seen == set(ORACLES)


@pytest.mark.parametrize(
    "tamper",
    [
        "gap",
        "negative",
        "dimension",
        "units",
        "untaught",
        "source",
        "physical",
        "frozen",
    ],
)
def test_new_batch_review_rejects_unsupported_or_changed_content(tamper):
    doc = load_batch("grade6_batch2")
    q = doc["lessons"][-1]["assessments"][-1]
    if tamper == "gap":
        doc["lessons"].pop(2)
    if tamper == "negative":
        q["public"]["givens"][1]["value"] = "-1"
    if tamper == "dimension":
        q["grading_spec"]["dimension"] = "length"
    if tamper == "units":
        q["public"]["unit_choices"] = ["s"]
    if tamper == "untaught":
        doc["lessons"][-1]["formulas"] = []
    if tamper == "source":
        q["source_refs"][0]["page_text_sha256"][0] = "0" * 64
    if tamper == "physical":
        doc["lessons"][-1]["review"]["physical_experiment_completed"] = True
    if tamper == "frozen":
        doc["lessons"][-1]["cards"][0]["body"] += " Unreviewed addition."
    with pytest.raises(ValueError):
        validate_batch(doc)
        import_batch(None, doc)  # evidence check fails before opening any DB


def test_all_seventeen_http_lessons_replay_append_and_private_keys(preview):
    client, factory = preview
    original = load_batch()
    for n in range(1, 8):
        attempt = start(client, n).json()
        answer_all(client, attempt, n)
        assert finish(client, attempt).json()["xp_awarded"] == 10
    with factory.begin() as db:
        old_hashes = {l.key: l.content_sha256 for l in db.query(CurriculumLessonV2)}
        for _ in range(2):
            for document in load_course():
                import_batch(db, document)
        assert all(
            db.get(CurriculumLessonV2, key).content_sha256 == digest
            for key, digest in old_hashes.items()
        )
        assert db.get(User, 1).xp_total == 70
    cat = client.get(f"{PREFIX}/catalog").json()
    assert [r["state"] for r in cat["lessons"][:9]] == ["completed"] * 7 + [
        "available",
        "locked",
    ]
    assert not cat["course_complete"] and not cat["grade_content_complete"]
    assert client.get(f"{PREFIX}/catalog?grade=7").json()["lessons"] == []
    assert client.get(f"{PREFIX}/catalog?grade=12").status_code == 422
    for lesson in load_batch("grade6_batch2")["lessons"]:
        response = start(client, lesson["sequence"])
        assert response.status_code == 200, response.text
        attempt = response.json()
        assert_private_absent(attempt)
        for q in lesson["assessments"]:
            answer = new_answer(lesson, q)
            result = submit(client, attempt, q["key"], answer)
            assert result.status_code == 200 and result.json()["is_correct"], (
                q["key"],
                result.text,
            )
            assert submit(client, attempt, q["key"], answer).json() == result.json()
        result = finish(client, attempt)
        assert result.status_code == 200 and result.json()["xp_awarded"] == 10
        assert finish(client, attempt).json() == result.json()
    with factory() as db:
        assert db.get(User, 1).xp_total == 170
    assert load_batch() == original


def test_import_gap_does_not_unlock_next_section(preview):
    client, factory = preview
    with factory.begin() as db:
        import_batch(db, load_batch("grade6_batch2"))
        db.query(CurriculumLessonV2).filter_by(sequence=1).update({"sequence": 100})
    rows = client.get(f"{PREFIX}/catalog").json()["lessons"]
    assert rows and all(r["state"] == "locked" for r in rows)


def test_batch_three_independent_answers_and_every_reviewed_equivalent():
    document = load_batch("grade6_batch3")
    assert validate_batch(document) == {
        "lessons": 7,
        "cards": 27,
        "formulas": 15,
        "worked_examples": 8,
        "assessments": 48,
        "frq": 16,
    }
    seen = set()
    for lesson in document["lessons"]:
        for q in lesson["assessments"]:
            answer = new_answer(lesson, q)
            spec = q["grading_spec"]
            assert grade_answer(spec, answer) == "correct", q["key"]
            if spec["kind"] != "numeric_quantity":
                continue
            seen.add((lesson["sequence"], int(q["key"].rsplit("q", 1)[1])))
            for expression in spec["formula"]["equivalents"]:
                assert (
                    grade_answer(spec, {**answer, "formula": expression}) == "correct"
                )
            wrong_unit = "kg" if spec["dimension"] == "time" else "s"
            assert (
                grade_answer(spec, {**answer, "unit": wrong_unit})
                == "dimension_mismatch"
            )
            assert grade_answer(spec, {**answer, "formula": "1"}) == "wrong_formula"
            assert (
                grade_answer(spec, {**answer, "value": "999999999"})
                == "out_of_tolerance"
            )
    assert seen == set(ORACLES_BATCH3)


def test_all_reviewed_http_content_and_replay(preview):
    client, factory = preview
    with factory.begin() as db:
        for document in load_course():
            import_batch(db, document)
    for document in load_course():
        for lesson in document["lessons"]:
            issued = start(client, lesson["sequence"])
            assert issued.status_code == 200, issued.text
            attempt = issued.json()
            assert_private_absent(attempt)
            for q in lesson["assessments"]:
                answer = correct(q) if lesson["sequence"] < 8 else new_answer(lesson, q)
                graded = submit(client, attempt, q["key"], answer)
                assert graded.status_code == 200 and graded.json()["is_correct"], (
                    q["key"],
                    graded.text,
                )
                assert submit(client, attempt, q["key"], answer).json() == graded.json()
            result = finish(client, attempt)
            assert result.status_code == 200 and result.json()["xp_awarded"] == 10
            assert finish(client, attempt).json() == result.json()
    with factory() as db:
        assert db.get(User, 1).xp_total == 240


@pytest.mark.parametrize(
    "case", ["gravity", "zero_area", "fraction_steps", "mixed_areas", "zero_time"]
)
def test_source_domains_not_silently_relaxed(case):
    from copy import deepcopy

    document = deepcopy(load_batch("grade6_batch3"))
    locations = {
        "gravity": (3, 4, 1, "value", "10"),
        "zero_area": (5, 5, 1, "value", "0"),
        "fraction_steps": (1, 7, 1, "value", "2.5"),
        "mixed_areas": (6, 5, 2, "unit", "m2"),
        "zero_time": (2, 4, 1, "value", "0"),
    }
    li, qi, gi, key, bad = locations[case]
    document["lessons"][li]["assessments"][qi]["public"]["givens"][gi][key] = bad
    with pytest.raises(ValueError):
        validate_batch(document)
