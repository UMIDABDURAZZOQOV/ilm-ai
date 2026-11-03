"""Original arithmetic examples with independent literal answer oracles."""

import json
from uuid import uuid4

import pytest
import test_mathematics_preview as first
from test_mathematics_batch2 import finish_new

from services.mathematics_curriculum import ROOT, load_course, validate_document
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    11: ["3", "b", "a", "b", "5", "5"],
    12: ["3", "a", "b", "a", "4", "7"],
    13: ["a", "c", "b", "a", "3", "b"],
    14: ["1", "a", "b", "b", "1", "1"],
    15: ["2", "1", "b", "a", "3", "b"],
}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from first.preview.__wrapped__(tmp_path, monkeypatch)


def finish_arithmetic(client, number):
    row = first.start(client, number)
    feedback = []
    for q, literal in zip(row["questions"], ANSWERS[number]):
        field = "choice_id" if q["response_kind"] == "choice" else "value"
        payload = {
            "assessment_version": 1,
            "request_id": str(uuid4()),
            "question_id": q["id"],
            "answer": {field: literal},
        }
        response = client.post(
            f"{first.P}/attempts/{row['attempt_id']}/answers", json=payload
        )
        assert response.status_code == 200 and response.json()["is_correct"], (
            response.text
        )
        assert (
            client.post(
                f"{first.P}/attempts/{row['attempt_id']}/answers", json=payload
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


def test_all_fifteen_in_sequence_progress_and_replay(preview):
    client, factory = preview
    for n in range(1, 16):
        completed = (
            first.finish(client, n)
            if n <= 5
            else finish_new(client, n)
            if n <= 10
            else finish_arithmetic(client, n)
        )
        assert completed[-1]["xp_awarded"] == 10
    assert finish_arithmetic(client, 15)[-1]["xp_awarded"] == 0
    with factory() as db:
        assert db.get(User, 1).xp_total == 287
        assert db.get(User, 2).xp_total == 0
        assert db.query(MathProgress).count() == 15
    assert all(
        r["state"] == "completed"
        for r in client.get(first.P + "/catalog").json()["lessons"]
    )


def test_notation_identity_is_validated_not_an_unchecked_display():
    document = json.loads((ROOT / "grade1_part1_batch3.json").read_text())
    review = json.loads((ROOT / "grade1_part1_batch3_review.json").read_text())
    document["lessons"][0]["formulas"][0]["expression"] = "2 + 1 = 4"
    with pytest.raises(ValueError, match="false_math_identity"):
        validate_document(document, review)
    document["lessons"][0]["formulas"][0]["expression"] = "__import__(os) = 3"
    with pytest.raises(ValueError, match="invalid_expression"):
        validate_document(document, review)


def test_all_written_equalities_are_true_with_independent_integer_arithmetic():
    # These four taught examples are authored independently of the parser.
    expected = {11: ["2 + 1 = 3"], 12: ["4 − 1 = 3"], 15: ["1 + 1 = 2", "2 − 1 = 1"]}
    for lesson in load_course():
        if lesson["sequence"] in expected:
            assert [f["expression"] for f in lesson["formulas"]] == expected[
                lesson["sequence"]
            ]
