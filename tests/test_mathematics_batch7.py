"""Segments, operation terms and missing operands: literal independent keys."""

from uuid import uuid4

import pytest
import test_mathematics_preview as first
from test_mathematics_batch6 import complete_first_thirty

from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    31: ["kesma", "2", "2", "1", "a", "3", "b", "3"],
    32: ["a", "yig‘indi", "8", "3", "b", "5", "6", "a"],
    33: ["8", "3", "5", "ayirma", "b", "4", "4", "a"],
    34: ["8", "a", "5", "5", "b", "8", "8", "0"],
    35: ["a", "b", "7", "3", "a", "8", "7", "b"],
}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from first.preview.__wrapped__(tmp_path, monkeypatch)


def finish_unknowns(client, number):
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


def complete_first_thirty_five(client):
    complete_first_thirty(client)
    for n in range(31, 36):
        assert finish_unknowns(client, n)[-1]["xp_awarded"] == 10


def test_all_thirty_five_additive_lesson_results_and_replay(preview):
    client, factory = preview
    complete_first_thirty_five(client)
    assert finish_unknowns(client, 35)[-1]["xp_awarded"] == 0
    with factory() as db:
        assert db.get(User, 1).xp_total == 487 and db.get(User, 2).xp_total == 0
        assert db.query(MathProgress).count() == 35
    assert all(
        r["state"] == "completed"
        for r in client.get(first.P + "/catalog").json()["lessons"][:35]
    )
