"""Source-literal second-book oracles and real cross-book prerequisites."""

import json
from uuid import uuid4

import pytest
import test_mathematics_preview as first
from test_mathematics_batch7 import complete_first_thirty_five
from test_mathematics_batch8 import finish_first_book

from services import tokens
from services.mathematics_curriculum import ROOT, validate_document
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    42: ["13", "2", "12", "2", "b", "14", "15", "20"],
    43: ["1", "7", "12", "a", "b", "17", "18", "a"],
    44: ["4", "3", "12", "8", "b", "16", "11", "10"],
    45: ["13", "14", "6", "14", "a", "5", "b", "9"],
    46: ["15", "16", "9", ["a", "b", "c"], "b", "16", "b", "9"],
}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from first.preview.__wrapped__(tmp_path, monkeypatch)


def complete_part1(client):
    complete_first_thirty_five(client)
    for number in range(36, 42):
        assert finish_first_book(client, number)[-1]["xp_awarded"] == 10


def finish_second(client, number):
    response = client.post(
        first.P + f"/lessons/math-1-2-{number - 41}-r1/start",
        json={"assessment_version": 1, "request_id": str(uuid4())},
    )
    assert response.status_code == 200, response.text
    row = response.json()
    feedback = []
    for q, literal in zip(row["questions"], ANSWERS[number]):
        field = {"choice": "choice_id", "ordering": "order"}.get(
            q["response_kind"], "value"
        )
        payload = {
            "assessment_version": 1,
            "request_id": str(uuid4()),
            "question_id": q["id"],
            "answer": {field: literal},
        }
        result = client.post(
            first.P + f"/attempts/{row['attempt_id']}/answers", json=payload
        )
        assert result.status_code == 200 and result.json()["is_correct"], result.text
        assert (
            client.post(
                first.P + f"/attempts/{row['attempt_id']}/answers", json=payload
            ).json()
            == result.json()
        )
        feedback.append(result.json())
    result = client.post(
        first.P + f"/attempts/{row['attempt_id']}/complete",
        json={"assessment_version": 1, "request_id": str(uuid4())},
    )
    assert result.status_code == 200, result.text
    return row, feedback, result.json()


def test_cross_book_prerequisites_then_all_five_progress_replay_and_account_isolation(
    preview,
):
    client, factory = preview
    cat = client.get(first.P + "/catalog", params={"grade": 1, "part": 2}).json()
    assert not cat["previous_book_complete"] and len(cat["available_books"]) == 2
    assert all(l["state"] == "locked" for l in cat["lessons"])
    blocked = client.post(
        first.P + "/lessons/math-1-2-1-r1/start",
        json={"assessment_version": 1, "request_id": str(uuid4())},
    )
    assert (
        blocked.status_code == 403
        and blocked.json()["detail"] == "finish_previous_book"
    )
    complete_part1(client)
    cat = client.get(first.P + "/catalog", params={"grade": 1, "part": 2}).json()
    assert cat["previous_book_complete"] and [
        l["source_number"] for l in cat["lessons"]
    ] == list(range(42, 47))
    assert cat["lessons"][0]["state"] == "available"
    for number in range(42, 47):
        assert finish_second(client, number)[-1]["xp_awarded"] == 10
    assert finish_second(client, 46)[-1]["xp_awarded"] == 0
    oldcat = client.get(first.P + "/catalog").json()
    assert len(oldcat["lessons"]) == 41 and all(
        l["state"] == "completed" for l in oldcat["lessons"]
    )
    second = client.get(
        first.P + "/catalog",
        params={"part": 2},
        headers={"Authorization": "Bearer " + tokens.create_access_token(2)},
    ).json()
    assert not second["previous_book_complete"] and all(
        l["state"] == "locked" for l in second["lessons"]
    )
    with factory() as db:
        assert db.get(User, 1).xp_total == 597 and db.get(User, 2).xp_total == 0
        assert db.query(MathProgress).count() == 46


def test_second_book_equations_are_not_mistaken_for_first_ten_concept_topics():
    doc = json.loads((ROOT / "grade1_part2_batch1.json").read_text())
    review = json.loads((ROOT / "grade1_part2_batch1_review.json").read_text())
    assert len(validate_document(doc, review)) == 5
    assert (
        doc["lessons"][0]["sequence"] == 1 and doc["lessons"][0]["source_number"] == 42
    )
    assert doc["lessons"][0]["formulas"][0]["expression"] == "10 + 3 = 13"
    assert (
        review["topics"][0]["pdf_pages"] == [5, 6]
        and review["book_id"] == "math-uz-g1-p2"
    )
