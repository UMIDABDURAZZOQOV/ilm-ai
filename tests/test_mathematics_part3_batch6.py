"""Textbook III31–35: literal arithmetic, whole/part, criteria and API replay."""

from uuid import uuid4

import pytest
import test_mathematics_part3_batch5 as previous
import test_mathematics_preview as first

from services.mathematics_curriculum import load_course
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    31: ["b", "7", "2", "12", "b", "28", "14", "a"],
    32: ["10", "14", "1", "10", "b", "16", "24", "7"],
    33: ["40", "27", "3", "6", "b", "16", "93", "a"],
    34: ["4", "a", "43", "22", "b", "13", ["b", "c", "a"], "21"],
    35: ["b", "9", "8", "a", "b", "12", "2", "8"],
}
SEQUENCES = {31: 26, 32: 27, 33: 28, 34: 29, 35: 30}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from first.preview.__wrapped__(tmp_path, monkeypatch)


def complete_previous(client, monkeypatch):
    previous.complete_previous(client, monkeypatch)
    monkeypatch.setenv("MATHEMATICS_QA_SOURCE_GAP_BRIDGE", "true")
    for n in previous.ANSWERS:
        assert previous.finish_new(client, n)[-1]["xp_awarded"] == 10


def finish_new(client, n):
    response = client.post(
        first.P + f"/lessons/math-1-3-{SEQUENCES[n]}-r1/start",
        json={"assessment_version": 1, "request_id": str(uuid4())},
    )
    assert response.status_code == 200, response.text
    row = response.json()
    feedback = []
    for q, value in zip(row["questions"], ANSWERS[n]):
        field = {"choice": "choice_id", "ordering": "order"}.get(
            q["response_kind"], "value"
        )
        payload = {
            "assessment_version": 1,
            "request_id": str(uuid4()),
            "question_id": q["id"],
            "answer": {field: value},
        }
        response = client.post(
            first.P + f"/attempts/{row['attempt_id']}/answers", json=payload
        )
        assert response.status_code == 200 and response.json()["is_correct"], (
            response.text
        )
        assert (
            client.post(
                first.P + f"/attempts/{row['attempt_id']}/answers", json=payload
            ).json()
            == response.json()
        )
        feedback.append(response.json())
    payload = {"assessment_version": 1, "request_id": str(uuid4())}
    path = first.P + f"/attempts/{row['attempt_id']}/complete"
    response = client.post(path, json=payload)
    assert response.status_code == 200, response.text
    assert client.post(path, json=payload).json() == response.json()
    return row, feedback, response.json()


@pytest.mark.parametrize("number", list(ANSWERS))
def test_source_literal_answers_wrong_answers_and_no_synthetic_formulas(number):
    lesson = next(
        l for l in load_course() if l["key"] == f"math-1-3-{SEQUENCES[number]}-r1"
    )
    ref = lesson["source_refs"][0]
    assert ref["pdf_pages"] == [2 * SEQUENCES[number] + 4, 2 * SEQUENCES[number] + 5]
    assert ref["printed_pages"] == [
        2 * SEQUENCES[number] + 2,
        2 * SEQUENCES[number] + 3,
    ]
    assert lesson["source_number"] == number and lesson["sequence"] == SEQUENCES[number]
    assert len(lesson["cards"]) == 6 and len(lesson["questions"]) == 8
    for q, literal in zip(lesson["questions"], ANSWERS[number]):
        kind = q["public"]["response_kind"]
        field = {"choice": "choice_id", "ordering": "order"}.get(kind, "value")
        assert grade_answer(q["grading"], {field: literal}) == "correct", (
            number,
            q["id"],
            literal,
        )
        if kind == "choice":
            wrong = next(c["id"] for c in q["public"]["choices"] if c["id"] != literal)
        elif kind == "ordering":
            wrong = list(reversed(literal))
        else:
            wrong = "999"
        assert grade_answer(q["grading"], {field: wrong}) == "incorrect"
        assert all(
            r["pdf_pages"] == ref["pdf_pages"]
            and r["printed_pages"] == ref["printed_pages"]
            for r in q["source_refs"]
        )
    if number == 33:
        assert (
            grade_answer(lesson["questions"][5]["grading"], {"value": "36-20"})
            == "correct"
        )
        assert (
            grade_answer(lesson["questions"][5]["grading"], {"value": "36-2"})
            == "incorrect"
        )
    if number == 35:
        assert (
            grade_answer(lesson["questions"][2]["grading"], {"value": "11-3"})
            == "correct"
        )


def test_all103_local_api_progress_order_and_replay_without_fake_missing74(
    preview, monkeypatch
):
    client, factory = preview
    complete_previous(client, monkeypatch)
    blocked = client.post(
        first.P + "/lessons/math-1-3-27-r1/start",
        json={"assessment_version": 1, "request_id": str(uuid4())},
    )
    assert (
        blocked.status_code == 403
        and blocked.json()["detail"] == "finish_previous_lesson"
    )
    for n in ANSWERS:
        initial, feedback, result = finish_new(client, n)
        assert result["xp_awarded"] == 10
        assert initial["source_gap_bridge"]["missing_source_numbers"] == [74]
        assert len(feedback) == 8
    assert finish_new(client, 35)[-1]["xp_awarded"] == 0
    catalog = client.get(first.P + "/catalog", params={"part": 3}).json()
    assert {l["key"] for l in catalog["lessons"] if l["state"] == "completed"} == {
        f"math-1-3-{n}-r1" for n in range(1, 31)
    }
    assert catalog["book"]["source_body_topic_count"] == 37
    assert not catalog["previous_book_complete"]
    with factory() as db:
        assert db.get(User, 1).xp_total == 1167
        assert db.get(User, 1).streak_days == 3 and db.get(User, 2).xp_total == 0
        assert db.query(MathProgress).count() == 103
        assert not db.query(MathProgress).filter_by(lesson_key="math-1-2-33-r1").first()
