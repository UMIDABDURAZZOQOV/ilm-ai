"""Source26/path27: real answers and a revocable, default-off local gap policy."""

import json
from copy import deepcopy
from uuid import uuid4

import pytest
import test_mathematics_grade2_part1_batch5 as previous
import test_mathematics_preview as first

from services import mathematics_runtime as runtime
from services import tokens
from services.mathematics_curriculum import ROOT, load_course
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathAttempt, MathLesson, MathProgress
from services.models import User

FLAG = "MATHEMATICS_QA_GRADE2_PART1_SOURCE_GAP"
ANSWERS = {
    27: ["14", "1", "74", "6", "a", "83", "35", "45"],
    28: ["55", "27", "57", "7", "b", "68", "52", "68"],
    29: ["12", "4", "25", "5", "a", "26", "29", "8"],
    30: ["34", "4", "26", "40", "c", "47", "15", "13"],
    31: ["15", "1", "75", "68", "b", "83", "9", "30"],
}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    monkeypatch.delenv(FLAG, raising=False)
    yield from first.preview.__wrapped__(tmp_path, monkeypatch)


def complete_previous(client):
    previous.complete_previous(client)
    for n in previous.ANSWERS:
        assert previous.finish_new(client, n)[-1]["xp_awarded"] == 10


def start(client, n=27, **extra):
    return client.post(
        first.P + f"/lessons/math-2-1-{n}-r1/start",
        json={
            "assessment_version": 1,
            "request_id": str(uuid4()),
            **extra,
        },
    )


def finish_new(client, n=27):
    response = start(client, n)
    assert response.status_code == 200, response.text
    row = response.json()
    feedback = []
    for q, literal in zip(row["questions"], ANSWERS[n], strict=True):
        field = "choice_id" if q["response_kind"] == "choice" else "value"
        payload = {
            "assessment_version": 1,
            "request_id": str(uuid4()),
            "question_id": q["id"],
            "answer": {field: literal},
        }
        path = first.P + f"/attempts/{row['attempt_id']}/answers"
        response = client.post(path, json=payload)
        assert response.status_code == 200 and response.json()["is_correct"], (
            response.text
        )
        assert client.post(path, json=payload).json() == response.json()
        feedback.append(response.json())
    path = first.P + f"/attempts/{row['attempt_id']}/complete"
    payload = {"assessment_version": 1, "request_id": str(uuid4())}
    response = client.post(path, json=payload)
    assert response.status_code == 200, response.text
    assert client.post(path, json=payload).json() == response.json()
    return row, feedback, response.json()


def test_independent_answers_wrong_answers_alternatives_and_source_boundary():
    lesson = next(l for l in load_course() if l["key"] == "math-2-1-27-r1")
    assert lesson["sequence"] == 27 and lesson["source_number"] == 26
    assert lesson["source_refs"][0]["pdf_pages"] == [55, 56]
    assert lesson["source_refs"][0]["printed_pages"] == [56, 57]
    assert 46 + 28 == 74 and 57 + 26 == 83
    assert 15 - (5 + 4) == 6 and 24 + 19 - 8 == 35 and 37 + 8 == 45
    for q, literal in zip(lesson["questions"], ANSWERS[27], strict=True):
        field = "choice_id" if q["public"]["response_kind"] == "choice" else "value"
        assert grade_answer(q["grading"], {field: literal}) == "correct"
        assert (
            grade_answer(q["grading"], {field: "b" if field == "choice_id" else "999"})
            == "incorrect"
        )
    assert (
        grade_answer(lesson["questions"][5]["grading"], {"value": "57+26"}) == "correct"
    )
    assert (
        grade_answer(lesson["questions"][5]["grading"], {"value": "83.0"}) == "correct"
    )
    assert "har safar1taga ortadi" in lesson["questions"][7]["public"]["prompt"]


def test_gap_policy_real_progress_authorization_revocation_and_replay(
    preview, monkeypatch, tmp_path
):
    client, factory = preview
    assert start(client).status_code == 403
    monkeypatch.setenv(FLAG, "true")
    assert start(client).status_code == 403  # No fabricated prerequisite bypass.
    assert start(client, source_sequence_gap_bridge=True).status_code == 422
    complete_previous(client)
    cat = client.get(first.P + "/catalog", params={"grade": 2}).json()
    bridge = cat["source_sequence_gap_bridge"]
    assert cat["previous_book_complete"] and cat["source_gap_bridge"] is None
    assert not cat["course_ready"] and bridge["missing_path_sequences"] == [26]
    assert (
        bridge["missing_source_numbers"] == [25]
        and not bridge["missing_topic_completed"]
    )
    assert [l["state"] for l in cat["lessons"]] == ["completed"] * 25 + [
        "available"
    ] + ["locked"] * (len(cat["lessons"]) - 26)
    assert [l["sequence"] for l in cat["lessons"]] == list(range(1, 26)) + list(
        range(27, len(cat["lessons"]) + 2)
    )
    pending = start(client).json()
    sid = pending["attempt_id"]
    answer_path = first.P + f"/attempts/{sid}/answers"
    hints = []
    for level in range(1, 5):
        wrong = {
            "assessment_version": 1,
            "request_id": str(uuid4()),
            "question_id": pending["questions"][0]["id"],
            "answer": {"value": "999"},
        }
        response = client.post(answer_path, json=wrong)
        assert response.status_code == 200 and not response.json()["is_correct"]
        assert response.json()["hint_level"] == level
        assert client.post(answer_path, json=wrong).json() == response.json()
        hints.append(response.json()["feedback"])
    assert len(set(hints)) == 4  # Targeted hints, then the full solution.
    other = {"Authorization": "Bearer " + tokens.create_access_token(2)}
    assert (
        client.post(
            first.P + f"/attempts/{sid}/complete",
            headers=other,
            json={"assessment_version": 1, "request_id": str(uuid4())},
        ).status_code
        == 404
    )
    monkeypatch.setenv(FLAG, "false")
    assert start(client).status_code == 403
    assert start(client, request_id=sid.rsplit(":", 1)[1]).status_code == 403
    assert (
        client.post(
            first.P + f"/attempts/{sid}/complete",
            json={"assessment_version": 1, "request_id": str(uuid4())},
        ).status_code
        == 403
    )
    assert (
        client.post(
            first.P + f"/attempts/{sid}/answers",
            json={
                "assessment_version": 1,
                "request_id": str(uuid4()),
                "question_id": pending["questions"][0]["id"],
                "answer": {"value": "14"},
            },
        ).status_code
        == 403
    )
    monkeypatch.setenv(FLAG, "true")
    assert start(client, request_id=sid.rsplit(":", 1)[1]).status_code == 200
    assert start(client, 28).status_code == 403
    initial, _, result = finish_new(client)
    assert result["xp_awarded"] == 10
    assert finish_new(client)[-1]["xp_awarded"] == 0
    for n in [28, 29, 30, 31]:
        assert finish_new(client, n)[-1]["xp_awarded"] == 10
    assert finish_new(client, 31)[-1]["xp_awarded"] == 0
    with factory() as db:
        completed = {p.lesson_key for p in db.query(MathProgress).filter_by(user_id=1)}
        assert len(completed) == 30 and "math-2-1-26-r1" not in completed
        assert db.get(MathLesson, "math-2-1-26-r1") is None
        assert not db.query(MathAttempt).filter_by(lesson_key="math-2-1-26-r1").count()
        assert db.get(User, 1).xp_total == 437 and db.get(User, 1).streak_days == 3
        assert db.get(User, 2).xp_total == 0
        assert (
            runtime.qa_grade2_source_sequence_gap(
                db, completed - {"math-2-1-25-r1"}, 2, 1
            )
            is None
        )
        assert runtime.qa_grade2_source_sequence_gap(db, completed, 1, 3) is None
        # Fail closed for altered source metadata, production, or an invented26.
        source = deepcopy(runtime.manifest())
        book = next(b for b in source["books"] if b["book_id"] == "math-uz-g2-p1")
        for field, value in [("sha256", "0" * 64), ("source_gaps", [])]:
            with monkeypatch.context() as mp:
                altered = deepcopy(source)
                next(b for b in altered["books"] if b["book_id"] == book["book_id"])[
                    field
                ] = value
                mp.setattr(runtime, "manifest", lambda altered=altered: altered)
                assert (
                    runtime.qa_grade2_source_sequence_gap(db, completed, 2, 1) is None
                )
        with monkeypatch.context() as mp:
            mp.setenv("ENVIRONMENT", "production")
            assert runtime.qa_grade2_source_sequence_gap(db, completed, 2, 1) is None
        mapping = json.loads((ROOT / "grade2_part1_map.json").read_text())
        mapping["topics"][25]["interactive_lesson_created"] = True
        (tmp_path / "grade2_part1_map.json").write_text(json.dumps(mapping))
        with monkeypatch.context() as mp:
            mp.setattr(runtime, "ROOT", tmp_path)
            assert runtime.qa_grade2_source_sequence_gap(db, completed, 2, 1) is None
        db.add(
            MathLesson(
                key="math-2-1-26-r1",
                grade=2,
                part=1,
                sequence=26,
                sha256="0" * 64,
                document={},
            )
        )
        db.flush()
        assert runtime.qa_grade2_source_sequence_gap(db, completed, 2, 1) is None
        db.rollback()
    monkeypatch.setenv(FLAG, "false")
    assert start(client).status_code == 403  # Even a previously completed lesson.
    assert (
        start(client, request_id=initial["attempt_id"].rsplit(":", 1)[1]).json()[
            "result"
        ]
        == result
    )
    assert start(client, request_id=sid.rsplit(":", 1)[1]).status_code == 403
    assert (
        client.get(first.P + "/catalog", params={"grade": 2}, headers=other).json()[
            "lessons"
        ][-1]["state"]
        == "locked"
    )
    assert (
        client.post(
            first.P + "/lessons/math-2-1-26-r1/start",
            json={"assessment_version": 1, "request_id": str(uuid4())},
        ).status_code
        == 404
    )


@pytest.mark.parametrize("n", [28, 29, 30, 31])
def test_remaining_batch_literal_keys_and_alternatives(n):
    lesson = next(l for l in load_course() if l["key"] == f"math-2-1-{n}-r1")
    assert lesson["source_number"] == n - 1
    assert lesson["source_refs"][0]["pdf_pages"] == [2 * n + 1, 2 * n + 2]
    assert lesson["source_refs"][0]["printed_pages"] == [2 * n + 2, 2 * n + 3]
    for q, literal in zip(lesson["questions"], ANSWERS[n], strict=True):
        field = "choice_id" if q["public"]["response_kind"] == "choice" else "value"
        assert grade_answer(q["grading"], {field: literal}) == "correct"
        wrong = (
            next(c["id"] for c in q["public"]["choices"] if c["id"] != literal)
            if field == "choice_id"
            else "999"
        )
        assert grade_answer(q["grading"], {field: wrong}) == "incorrect"
    alternative = {28: "43+25", 29: "64-38", 30: "73-26", 31: "56+27"}[n]
    assert (
        grade_answer(lesson["questions"][5]["grading"], {"value": alternative})
        == "correct"
    )
    assert 43 + 25 == 68 and 64 - 38 == 26 and 73 - 26 == 47 and 56 + 27 == 83
    assert 2 * (21 + 13) == 68 and 18 + 25 - 14 == 29 and 12 - 7 + 8 - 5 == 8
    assert 44 - 13 - 16 == 15 and 32 - 23 == 9 and 2 * (9 + 6) == 30
