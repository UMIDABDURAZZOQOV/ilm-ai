"""Ten, number properties and introductory geometry: independent answer oracles."""

import json
from uuid import uuid4

import pytest
import test_mathematics_preview as first
from test_mathematics_batch5 import complete_first_twenty_five

from services.mathematics_curriculum import ROOT, validate_document
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    26: ["10", "2", "3", "10", "a", "6", "b", "10"],
    27: [
        [f"n{i}" for i in range(1, 11)],
        "8",
        "4",
        "5",
        "a",
        "5",
        ["t", "e", "f", "w"],
        "b",
    ],
    28: ["a", "1", "2", "b", "b", "2", "a", "ha"],
    29: ["toq", "juft", "juft", "2", "b", "10", "5", "b"],
    30: ["a", "ha", "egri", "a", "b", "nuqta", "b", "a"],
}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from first.preview.__wrapped__(tmp_path, monkeypatch)


def finish_properties(client, number):
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


def complete_first_thirty(client):
    complete_first_twenty_five(client)
    for n in range(26, 31):
        assert finish_properties(client, n)[-1]["xp_awarded"] == 10


def test_all_thirty_additive_lessons_reopen_and_replay(preview):
    client, factory = preview
    complete_first_thirty(client)
    assert finish_properties(client, 30)[-1]["xp_awarded"] == 0
    with factory() as db:
        assert db.get(User, 1).xp_total == 437 and db.get(User, 2).xp_total == 0
        assert db.query(MathProgress).count() == 30
    assert all(
        r["state"] == "completed"
        for r in client.get(first.P + "/catalog").json()["lessons"][:30]
    )


def test_duplicate_aware_source_mapping_and_fail_closed_unknown_model():
    doc = json.loads((ROOT / "grade1_part1_batch6.json").read_text())
    review = json.loads((ROOT / "grade1_part1_batch6_review.json").read_text())
    assert doc["lessons"][0]["source_refs"][0]["pdf_pages"] == [57, 58]
    assert doc["lessons"][0]["source_refs"][0]["printed_pages"] == [54, 55]
    doc["lessons"][0]["explorer"]["type"] = "not_implemented"
    with pytest.raises(ValueError, match="unsupported_math_explorer"):
        validate_document(doc, review)


def test_ten_item_order_checks_all_items_and_wrong_direction(preview):
    client, _ = preview
    complete_first_twenty_five(client)
    finish_properties(client, 26)
    row = first.start(client, 27)

    def send(order):
        return client.post(
            f"{first.P}/attempts/{row['attempt_id']}/answers",
            json={
                "assessment_version": 1,
                "request_id": str(uuid4()),
                "question_id": row["questions"][0]["id"],
                "answer": {"order": order},
            },
        )

    assert send(["n1"] * 10).status_code == 422
    wrong = send([f"n{i}" for i in range(10, 0, -1)])
    assert not wrong.json()["is_correct"] and wrong.json()["hint_level"] == 1
    assert send([f"n{i}" for i in range(1, 11)]).json()["is_correct"]
