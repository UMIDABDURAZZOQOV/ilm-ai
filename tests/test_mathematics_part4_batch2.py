"""IV117–121: all edges, inverse sums, dimensional scope and text aliases."""

from uuid import uuid4

import pytest
import test_mathematics_part4 as previous
import test_mathematics_preview as first

from services.mathematics_curriculum import load_course
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    117: ["18", "20", "15", "6", "a", "20", "18", "12"],
    118: ["6", "20", "12", "4", "b", "7", "20", "a"],
    119: ["20", "16", "8", "6", "a", "24", "a", "4"],
    120: ["32", "20", "a", "b", "b", "32", "16", "b"],
    121: ["2", "1", "a", "c", "b", "o‘tkir", "o‘tmas", "b"],
}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from first.preview.__wrapped__(tmp_path, monkeypatch)


def complete_previous(client, monkeypatch):
    previous.complete_previous(client, monkeypatch)
    monkeypatch.setenv("MATHEMATICS_QA_PART3_SCHEDULE_BRIDGE", "true")
    for n in previous.ANSWERS:
        assert previous.finish_fourth(client, n)[-1]["xp_awarded"] == 10


def finish_new(client, n):
    response = client.post(
        first.P + f"/lessons/math-1-4-{n - 111}-r1/start",
        json={"assessment_version": 1, "request_id": str(uuid4())},
    )
    assert response.status_code == 200, response.text
    row = response.json()
    feedback = []
    for q, literal in zip(row["questions"], ANSWERS[n]):
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
    payload = {"assessment_version": 1, "request_id": str(uuid4())}
    path = first.P + f"/attempts/{row['attempt_id']}/complete"
    response = client.post(path, json=payload)
    assert response.status_code == 200, response.text
    assert client.post(path, json=payload).json() == response.json()
    return row, feedback, response.json()


@pytest.mark.parametrize("n", ANSWERS)
def test_source_independent_literal_answers_and_alternatives(n):
    l = next(l for l in load_course() if l["key"] == f"math-1-4-{n - 111}-r1")
    assert l["source_number"] == n and l["sequence"] == n - 111
    assert l["source_refs"][0]["pdf_pages"] == [2 * (n - 111) + 3, 2 * (n - 111) + 4]
    assert l["source_refs"][0]["printed_pages"] == [
        2 * (n - 111) + 2,
        2 * (n - 111) + 3,
    ]
    for q, literal in zip(l["questions"], ANSWERS[n]):
        kind = q["public"]["response_kind"]
        field = "choice_id" if kind == "choice" else "value"
        assert grade_answer(q["grading"], {field: literal}) == "correct"
        wrong = (
            next(c["id"] for c in q["public"]["choices"] if c["id"] != literal)
            if kind == "choice"
            else "noma’lum"
            if kind == "short_text"
            else "999"
        )
        assert grade_answer(q["grading"], {field: wrong}) == "incorrect"
    if n == 118:
        assert (
            grade_answer(l["questions"][0]["grading"], {"value": "18-(5+7)"})
            == "correct"
        )
        assert (
            grade_answer(l["questions"][0]["grading"], {"value": "18-5+7"})
            == "incorrect"
        )
    if n == 121:
        assert (
            l["formulas"] == []
        )  # Angle classification gets no artificial numeric formula.
        for alias in ["O'TKIR", "oʻtkir burchak", "  otkir  "]:
            assert (
                grade_answer(l["questions"][5]["grading"], {"value": alias})
                == "correct"
            )
        for alias in ["O'TMAS", "o‘tmas burchak", "  otmas "]:
            assert (
                grade_answer(l["questions"][6]["grading"], {"value": alias})
                == "correct"
            )
        assert "takrorlangan" in l["cards"][-1]["body"]


def test_all120_progress_xp_and_no_extra_reward_or_control_completion(
    preview, monkeypatch
):
    client, factory = preview
    complete_previous(client, monkeypatch)
    assert (
        client.post(
            first.P + "/lessons/math-1-4-7-r1/start",
            json={"assessment_version": 1, "request_id": str(uuid4())},
        ).status_code
        == 403
    )
    for n in ANSWERS:
        assert finish_new(client, n)[-1]["xp_awarded"] == 10
    assert finish_new(client, 121)[-1]["xp_awarded"] == 0
    cat = client.get(first.P + "/catalog", params={"part": 4}).json()
    assert {l["key"] for l in cat["lessons"] if l["state"] == "completed"} == {
        f"math-1-4-{i}-r1" for i in range(1, 11)
    }
    assert not cat["previous_book_complete"] and not cat["course_ready"]
    assert cat["source_gap_bridge"]["schedule_only_rows_not_completed"] == 5
    with factory.begin() as db:
        assert db.query(MathProgress).filter_by(user_id=1).count() == 120
        assert db.get(User, 1).xp_total == 1337 and db.get(User, 2).xp_total == 0
        assert db.get(User, 1).streak_days == 3
