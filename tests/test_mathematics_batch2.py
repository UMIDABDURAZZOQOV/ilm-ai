"""Source-reviewed sequence/group/number objectives; independent literal keys."""

from uuid import uuid4

import pytest
import test_mathematics_preview as first
from test_mathematics_preview import P, finish, start

from services.mathematics_grading import MathInputError, grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    6: [["s", "c"], "a", "keyin", "b", "payshanba", ["a", "b", "c"]],
    7: ["b", "a", "guruh", "b", "yo‘q", "a"],
    8: ["a", "1", "teng", "b", "2", "a"],
    9: ["5", "7", ["a", "b", "c"], "b", "10", ["a", "b", "c"]],
    10: ["4", "8", "5", "a", "7", "3"],
}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from first.preview.__wrapped__(tmp_path, monkeypatch)


def finish_new(client, number):
    row = start(client, number)
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
        response = client.post(f"{P}/attempts/{row['attempt_id']}/answers", json=data)
        assert response.status_code == 200 and response.json()["is_correct"], (
            response.text
        )
        assert (
            client.post(f"{P}/attempts/{row['attempt_id']}/answers", json=data).json()
            == response.json()
        )
        feedback.append(response.json())
    result = client.post(
        f"{P}/attempts/{row['attempt_id']}/complete",
        json={"assessment_version": 1, "request_id": str(uuid4())},
    )
    assert result.status_code == 200, result.text
    return row, feedback, result.json()


def test_all_ten_in_order_then_reopen_replay_no_lost_legacy_xp(preview):
    client, factory = preview
    for n in range(1, 11):
        result = (finish(client, n) if n <= 5 else finish_new(client, n))[-1]
        assert result["xp_awarded"] == 10
    assert all(
        l["state"] == "completed" for l in client.get(P + "/catalog").json()["lessons"]
    )
    assert finish_new(client, 10)[-1]["xp_awarded"] == 0
    with factory() as db:
        assert db.get(User, 1).xp_total == 237 and db.get(User, 2).xp_total == 0
        assert db.query(MathProgress).count() == 10


def test_ordering_is_a_permutation_not_fuzzy_or_unordered_set():
    spec = {"kind": "ordering", "expected": ["a", "b", "c"]}
    assert grade_answer(spec, {"order": ["a", "b", "c"]}) == "correct"
    assert grade_answer(spec, {"order": ["c", "b", "a"]}) == "incorrect"
    for value in [
        [],
        ["a", "a", "c"],
        ["a", "b", "d"],
        ["a", "b"],
        True,
        "abc",
        [1, 2, 3],
    ]:
        with pytest.raises(MathInputError):
            grade_answer(spec, {"order": value})


def test_ordering_invalid_can_be_fixed_and_real_wrong_order_gets_a_hint(preview):
    client, _ = preview
    for n in range(1, 6):
        finish(client, n)
    row = start(client, 6)
    url = f"{P}/attempts/{row['attempt_id']}/answers"

    def send(order):
        return client.post(
            url,
            json={
                "assessment_version": 1,
                "request_id": str(uuid4()),
                "question_id": row["questions"][0]["id"],
                "answer": {"order": order},
            },
        )

    assert send(["s", "s"]).status_code == 422
    wrong = send(["c", "s"])
    assert wrong.status_code == 200 and not wrong.json()["is_correct"]
    assert wrong.json()["hint_level"] == 1
    assert send(["s", "c"]).json()["is_correct"]
