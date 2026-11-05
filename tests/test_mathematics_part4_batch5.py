"""IV133–138: numeric values, strict integer domains, Roman and equations."""

from uuid import uuid4

import pytest
import test_mathematics_part4_batch4 as previous
import test_mathematics_preview as first

from services.mathematics_curriculum import load_course
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    133: ["13", "20", "60", "9", "b", "25", "4", "18"],
    134: ["15", "6", "15", "15", "b", "18", "62", "b"],
    135: ["4", "26", "29", "5", "b", "4", "a", "b"],
    136: ["4", "9", "50", "90", "a", "XLIII", "60", "21"],
    137: ["15", "17", "23", "17", "b", "14", "26", "24"],
    138: ["b", "15", ["a", "b", "c", "d", "e", "f"], "23", "a", "17", "29", "9"],
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
        field = {"choice": "choice_id", "ordering": "order"}.get(
            q["response_kind"], "value"
        )
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
        field = {"choice": "choice_id", "ordering": "order"}.get(kind, "value")
        assert grade_answer(q["grading"], {field: literal}) == "correct"
        wrong = (
            next(c["id"] for c in q["public"]["choices"] if c["id"] != literal)
            if kind == "choice"
            else list(reversed(literal))
            if kind == "ordering"
            else "noma’lum"
            if kind == "short_text"
            else "999"
        )
        assert grade_answer(q["grading"], {field: wrong}) == "incorrect"
    if n == 135:
        assert l["formulas"] == []
        assert [x for x in range(10, 100) if 25 < x < 30] == [26, 27, 28, 29]
        assert [x for x in range(10, 100) if x < 15] == [10, 11, 12, 13, 14]
        assert [x for x in range(10, 100) if x > 95] == [96, 97, 98, 99]
    if n == 136:
        assert (
            grade_answer(l["questions"][5]["grading"], {"value": "xliii"}) == "correct"
        )
        assert (
            grade_answer(l["questions"][5]["grading"], {"value": "XLII"}) == "incorrect"
        )
    if n == 137:
        assert [x for x in range(101) if 18 + x == 32] == [14]
        assert [x for x in range(101) if 46 - x == 20] == [26]
    if n == 138:
        assert (
            grade_answer(l["questions"][5]["grading"], {"value": "35-18"}) == "correct"
        )
        assert (
            grade_answer(
                l["questions"][2]["grading"], {"order": ["a", "b", "c", "d", "f", "e"]}
            )
            == "incorrect"
        )


def test_all137_progress_xp_and_no_extra_reward_or_control_completion(
    preview, monkeypatch
):
    client, factory = preview
    complete_previous(client, monkeypatch)
    assert (
        client.post(
            first.P + "/lessons/math-1-4-23-r1/start",
            json={"assessment_version": 1, "request_id": str(uuid4())},
        ).status_code
        == 403
    )
    for n in ANSWERS:
        assert finish_new(client, n)[-1]["xp_awarded"] == 10
    assert finish_new(client, 138)[-1]["xp_awarded"] == 0
    cat = client.get(first.P + "/catalog", params={"part": 4}).json()
    assert {l["key"] for l in cat["lessons"] if l["state"] == "completed"} == {
        f"math-1-4-{i}-r1" for i in range(1, 28)
    }
    assert not cat["previous_book_complete"] and not cat["course_ready"]
    assert cat["source_gap_bridge"]["schedule_only_rows_not_completed"] == 5
    with factory.begin() as db:
        assert db.query(MathProgress).filter_by(user_id=1).count() == 137
        assert db.get(User, 1).xp_total == 1507 and db.get(User, 2).xp_total == 0
        assert db.get(User, 1).streak_days == 3
