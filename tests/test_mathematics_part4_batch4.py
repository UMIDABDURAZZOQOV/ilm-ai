"""IV127–132: exact shape conditions, views, bounded variable substitution."""

from uuid import uuid4

import pytest
import test_mathematics_part4_batch3 as previous
import test_mathematics_preview as first

from services.mathematics_curriculum import load_course
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    127: ["4", "2", "b", "c", "b", "2", "4", "b"],
    128: ["b", "shar", "a", "b", "b", "12", "8", "silindr"],
    129: ["25", "9", "40", "a", "b", "7", "a", "a"],
    130: ["a", "b", "11", "9", "b", "12", "15", "b"],
    131: ["13", "11", "a", "b", "b", "9", "13", "b"],
    132: ["6", "10", "a", "8", "b", "6", "3", "b"],
}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from first.preview.__wrapped__(tmp_path, monkeypatch)


def complete_previous(client, monkeypatch):
    previous.complete_previous(client, monkeypatch)
    monkeypatch.setenv("MATHEMATICS_QA_PART3_SCHEDULE_BRIDGE", "true")
    for n in previous.ANSWERS:
        assert previous.finish_new(client, n)[-1]["xp_awarded"] == 10


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
    if n == 127:
        assert l["formulas"] == []
    if n == 128:
        assert (
            grade_answer(l["questions"][1]["grading"], {"value": "SHAR MODELI"})
            == "correct"
        )
        assert (
            grade_answer(l["questions"][7]["grading"], {"value": "Silindr"})
            == "correct"
        )
        assert (
            grade_answer(l["questions"][5]["grading"], {"value": "31-(12+7)"})
            == "correct"
        )
    if n == 132:
        assert [x for x in range(15) if x + 2 == 14 - x] == [6]
        assert grade_answer(l["questions"][5]["grading"], {"value": "6.0"}) == "correct"
        assert "s + 0 = s" in l["cards"][3]["body"]
        assert "qaysi kunlarda" in l["cards"][-1]["body"]


def test_all131_progress_xp_and_no_extra_reward_or_control_completion(
    preview, monkeypatch
):
    client, factory = preview
    complete_previous(client, monkeypatch)
    assert (
        client.post(
            first.P + "/lessons/math-1-4-17-r1/start",
            json={"assessment_version": 1, "request_id": str(uuid4())},
        ).status_code
        == 403
    )
    for n in ANSWERS:
        assert finish_new(client, n)[-1]["xp_awarded"] == 10
    assert finish_new(client, 132)[-1]["xp_awarded"] == 0
    cat = client.get(first.P + "/catalog", params={"part": 4}).json()
    assert len(cat["lessons"]) == 21 and all(
        l["state"] == "completed" for l in cat["lessons"]
    )
    assert not cat["previous_book_complete"] and not cat["course_ready"]
    assert cat["source_gap_bridge"]["schedule_only_rows_not_completed"] == 5
    with factory.begin() as db:
        assert db.query(MathProgress).filter_by(user_id=1).count() == 131
        assert db.get(User, 1).xp_total == 1447 and db.get(User, 2).xp_total == 0
        assert db.get(User, 1).streak_days == 3
