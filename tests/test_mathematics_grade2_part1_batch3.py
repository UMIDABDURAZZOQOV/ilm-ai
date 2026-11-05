"""Grade2I1–5: verified review, source gap and independent grade progress."""

from uuid import uuid4

import pytest
import test_mathematics_grade2_part1_batch2 as previous
import test_mathematics_preview as first

from services import tokens
from services.mathematics_curriculum import load_course
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    11: ["30", "1", "40", "50", "c", "70", "20", "52"],
    12: ["80", "30", "40", "20", "b", "18", "36", "60"],
    13: ["43", "10", "66", "50", "b", "74", "8", "62"],
    14: ["52", "75", "53", "23", "b", "54", "26", "b"],
    15: ["60", "70", "100", "60", "b", "68", "32", "34"],
}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from first.preview.__wrapped__(tmp_path, monkeypatch)


def finish_new(client, n):
    response = client.post(
        first.P + f"/lessons/math-2-1-{n}-r1/start",
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
    l = next(l for l in load_course() if l["key"] == f"math-2-1-{n}-r1")
    assert l["source_number"] == n and l["sequence"] == n
    assert l["source_refs"][0]["pdf_pages"] == [2 * n + 3, 2 * n + 4]
    assert l["source_refs"][0]["printed_pages"] == [
        2 * n + 2,
        2 * n + 3,
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
    if n == 11:
        assert 6 + (6 + 3) + 5 == 20
        assert (
            grade_answer(l["questions"][5]["grading"], {"value": "67+3"}) == "correct"
        )
    if n == 12:
        assert 5 + (5 + 2) + (5 + 2 - 1) == 18
    if n == 13:
        assert 70 - (24 + 18 + 12 + 8) == 8
        assert (
            grade_answer(l["questions"][5]["grading"], {"value": "80-6"}) == "correct"
        )
    if n == 14:
        assert (30 - 1) % 7 == 1 and 60 - 6 == 54 and (40 - 7) - 7 == 26
    if n == 15:
        assert 74 + 26 == 100 and 28 + (28 + 12) == 68
        assert [x for x in range(101) if x + 26 == 60] == [34]


def test_grade_choice_prerequisites_progress_replay_and_uid_isolation(preview):
    client, factory = preview
    complete_previous(client)
    cat = client.get(first.P + "/catalog", params={"grade": 2}).json()
    assert cat["grade"] == 2 and cat["previous_book_complete"]
    assert cat["book"]["source_topic_count"] == 44
    assert cat["book"]["implemented_sections"] == len(cat["lessons"])
    assert cat["book"]["source_gaps"][0]["missing_printed_pages"] == [54, 55]
    assert [l["state"] for l in cat["lessons"]] == ["completed"] * 10 + [
        "available"
    ] + ["locked"] * (len(cat["lessons"]) - 11)
    assert (
        client.post(
            first.P + "/lessons/math-2-1-12-r1/start",
            json={"assessment_version": 1, "request_id": str(uuid4())},
        ).status_code
        == 403
    )
    for n in ANSWERS:
        assert finish_new(client, n)[-1]["xp_awarded"] == 10
    assert finish_new(client, 15)[-1]["xp_awarded"] == 0
    complete = client.get(first.P + "/catalog", params={"grade": 2}).json()
    assert {l["key"] for l in complete["lessons"] if l["state"] == "completed"} == {
        f"math-2-1-{i}-r1" for i in range(1, 16)
    }
    assert not complete["course_ready"]
    first_grade = client.get(first.P + "/catalog").json()
    assert all(l["state"] != "completed" for l in first_grade["lessons"])
    other = client.get(
        first.P + "/catalog",
        params={"grade": 2},
        headers={"Authorization": "Bearer " + tokens.create_access_token(2)},
    ).json()
    assert [l["state"] for l in other["lessons"]] == ["available"] + ["locked"] * (
        len(other["lessons"]) - 1
    )
    with factory() as db:
        assert db.query(MathProgress).filter_by(user_id=1).count() == 15
        assert db.get(User, 1).xp_total == 287 and db.get(User, 2).xp_total == 0
        assert db.get(User, 1).streak_days == 3


def complete_previous(client):
    previous.complete_previous(client)
    for n in previous.ANSWERS:
        assert previous.finish_new(client, n)[-1]["xp_awarded"] == 10
