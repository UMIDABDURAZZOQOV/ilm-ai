"""Whole/part and number-line objectives, with literal independent answers."""

from uuid import uuid4

import pytest
import test_mathematics_preview as first
from test_mathematics_batch2 import finish_new
from test_mathematics_batch3 import finish_arithmetic

from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    16: ["3", "2", "1", "b", "2", ["k", "d", "u"]],
    17: ["2", "1", "2", "a", "1", "4"],
    18: ["1", "2", "2", "b", "2", "4"],
    19: ["5", "3", "2", "b", "2", "a"],
    20: ["4", "3", "a", "b", "2", "a"],
}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from first.preview.__wrapped__(tmp_path, monkeypatch)


def finish_parts(client, number):
    row = first.start(client, number)
    feedback = []
    for q, literal in zip(row["questions"], ANSWERS[number]):
        field = {"choice": "choice_id", "ordering": "order"}.get(
            q["response_kind"], "value"
        )
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


def complete_until(client, count):
    for n in range(1, count + 1):
        result = (
            first.finish(client, n)
            if n <= 5
            else finish_new(client, n)
            if n <= 10
            else finish_arithmetic(client, n)
            if n <= 15
            else finish_parts(client, n)
        )
        assert result[-1]["xp_awarded"] == 10


def test_twenty_lessons_preserve_old_progress_and_xp(preview):
    client, factory = preview
    complete_until(client, 20)
    assert all(
        r["state"] == "completed"
        for r in client.get(first.P + "/catalog").json()["lessons"]
    )
    assert finish_parts(client, 20)[-1]["xp_awarded"] == 0
    with factory() as db:
        assert db.get(User, 1).xp_total == 337 and db.get(User, 2).xp_total == 0
        assert db.query(MathProgress).count() == 20


def test_wrong_step_count_receives_hint_then_alternative_numeric_form_is_accepted(
    preview,
):
    client, _ = preview
    complete_until(client, 19)
    row = first.start(client, 20)
    url = f"{first.P}/attempts/{row['attempt_id']}/answers"

    def send(value):
        return client.post(
            url,
            json={
                "assessment_version": 1,
                "request_id": str(uuid4()),
                "question_id": row["questions"][0]["id"],
                "answer": {"value": value},
            },
        )

    assert not send("3").json()["is_correct"]
    correct = send("2 + 2")
    assert correct.json()["is_correct"]
    assert not correct.json().get(
        "solution"
    )  # No private rule added to a successful answer.
