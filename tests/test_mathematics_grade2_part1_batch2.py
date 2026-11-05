"""Grade2I1–5: verified review, source gap and independent grade progress."""

from uuid import uuid4

import pytest
import test_mathematics_grade2_part1 as previous
import test_mathematics_preview as first

from services import tokens
from services.mathematics_curriculum import load_course
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    6: ["29", "46", "36", "68", "b", "35", "8", "3"],
    7: ["47", "69", "43", "11", "c", "19", "3", "14"],
    8: ["53", "3", "26", "48", "b", "22", "3", "a"],
    9: ["77", "7", "52", "18", "a", "66", "60", "5"],
    10: ["27", "18", "23", "5", "a", "28", "17", "50"],
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
    if n == 6:
        assert 93 - (27 + (27 + 4)) == 35 and 43 + 25 == 68
    if n == 7:
        assert 3 * 5 - 3 * 4 == 3
    if n == 8:
        assert 9 + 13 + (9 + 13 + 4) == 48
        assert (
            grade_answer(l["questions"][5]["grading"], {"value": "52-(14+16)"})
            == "correct"
        )
    if n == 9:
        assert 27 + (27 + 12) == 66
    if n == 10:
        assert [x for x in range(101) if 24 + x + 9 == 61] == [28]
        assert 6 * 2 + (6 - 1) * 1 == 17


def test_grade_choice_prerequisites_progress_replay_and_uid_isolation(preview):
    client, factory = preview
    complete_previous(client)
    cat = client.get(first.P + "/catalog", params={"grade": 2}).json()
    assert cat["grade"] == 2 and cat["previous_book_complete"]
    assert cat["book"]["source_topic_count"] == 44
    assert cat["book"]["implemented_sections"] == 10
    assert cat["book"]["source_gaps"][0]["missing_printed_pages"] == [54, 55]
    assert [l["state"] for l in cat["lessons"]] == ["completed"] * 5 + ["available"] + [
        "locked"
    ] * 4
    assert (
        client.post(
            first.P + "/lessons/math-2-1-7-r1/start",
            json={"assessment_version": 1, "request_id": str(uuid4())},
        ).status_code
        == 403
    )
    for n in ANSWERS:
        assert finish_new(client, n)[-1]["xp_awarded"] == 10
    assert finish_new(client, 10)[-1]["xp_awarded"] == 0
    complete = client.get(first.P + "/catalog", params={"grade": 2}).json()
    assert {l["key"] for l in complete["lessons"] if l["state"] == "completed"} == {
        f"math-2-1-{i}-r1" for i in range(1, 11)
    }
    assert not complete["course_ready"]
    first_grade = client.get(first.P + "/catalog").json()
    assert all(l["state"] != "completed" for l in first_grade["lessons"])
    other = client.get(
        first.P + "/catalog",
        params={"grade": 2},
        headers={"Authorization": "Bearer " + tokens.create_access_token(2)},
    ).json()
    assert [l["state"] for l in other["lessons"]] == ["available"] + ["locked"] * 9
    with factory() as db:
        assert db.query(MathProgress).filter_by(user_id=1).count() == 10
        assert db.get(User, 1).xp_total == 237 and db.get(User, 2).xp_total == 0
        assert db.get(User, 1).streak_days == 3


def complete_previous(client):
    for n in previous.ANSWERS:
        assert previous.finish_new(client, n)[-1]["xp_awarded"] == 10
