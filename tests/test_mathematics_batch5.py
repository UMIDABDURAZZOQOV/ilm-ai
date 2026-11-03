"""Six to nine and zero, with book-grounded independent literal keys."""

from uuid import uuid4

import pytest
import test_mathematics_preview as first
from test_mathematics_batch4 import complete_until

from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    21: ["1", "2", "4", "6", "b", "6", "a", "6"],
    22: ["2", "3", "a", "3", "b", "7", "5", "c"],
    23: ["5", "8", "4", "a", "b", "3", "b", "5"],
    24: ["2", "3", "c", "8", "a", "8", "1", "a"],
    25: ["0", "3", "4", "0", "b", "0", "0", "a"],
}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from first.preview.__wrapped__(tmp_path, monkeypatch)


def finish_to_zero(client, number):
    row = first.start(client, number)
    feedback = []
    for q, literal in zip(row["questions"], ANSWERS[number]):
        field = "choice_id" if q["response_kind"] == "choice" else "value"
        data = {
            "assessment_version": 1,
            "request_id": str(uuid4()),
            "question_id": q["id"],
            "answer": {field: literal},
        }
        response = client.post(
            f"{first.P}/attempts/{row['attempt_id']}/answers", json=data
        )
        assert response.status_code == 200 and response.json()["is_correct"], (
            response.text
        )
        assert (
            client.post(
                f"{first.P}/attempts/{row['attempt_id']}/answers", json=data
            ).json()
            == response.json()
        )
        feedback.append(response.json())
    result = client.post(
        f"{first.P}/attempts/{row['attempt_id']}/complete",
        json={"assessment_version": 1, "request_id": str(uuid4())},
    )
    assert result.status_code == 200, result.text
    return row, feedback, result.json()


def complete_first_twenty_five(client):
    complete_until(client, 20)
    for number in range(21, 26):
        assert finish_to_zero(client, number)[-1]["xp_awarded"] == 10


def test_twenty_five_lesson_progress_and_zero_answers_survive_reopen(preview):
    client, factory = preview
    complete_first_twenty_five(client)
    assert finish_to_zero(client, 25)[-1]["xp_awarded"] == 0
    assert all(
        r["state"] == "completed"
        for r in client.get(first.P + "/catalog").json()["lessons"]
    )
    with factory() as db:
        assert db.get(User, 1).xp_total == 387 and db.get(User, 2).xp_total == 0
        assert db.query(MathProgress).count() == 25


def test_blank_is_not_zero_and_wrong_one_gets_hint(preview):
    client, _ = preview
    complete_until(client, 20)
    for number in range(21, 25):
        finish_to_zero(client, number)
    row = first.start(client, 25)

    def send(value):
        return client.post(
            f"{first.P}/attempts/{row['attempt_id']}/answers",
            json={
                "assessment_version": 1,
                "request_id": str(uuid4()),
                "question_id": row["questions"][0]["id"],
                "answer": {"value": value},
            },
        )

    assert send("").status_code == 422
    wrong = send("1")
    assert not wrong.json()["is_correct"] and wrong.json()["hint_level"] == 1
    assert send("0").json()["is_correct"]
