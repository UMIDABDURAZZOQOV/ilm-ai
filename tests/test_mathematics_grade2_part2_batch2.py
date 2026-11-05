"""Independent grade2II literal, ordering, carry and real API/XP regressions."""

import json
from copy import deepcopy
from uuid import uuid4

import pytest
import test_mathematics_grade2_part2 as first
import test_mathematics_preview as root
from test_mathematics_grade2_part1_batch6 import FLAG as PART1_FLAG

from services.mathematics_curriculum import ROOT, load_course, validate_document
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    6: ["a", "583", "672", "0", "a", "740", "5", "65"],
    7: ["103", "8", "a", "8", "a", "101", "4", "66"],
    8: [
        "73",
        "415",
        "462",
        ["b", "d", "a", "c"],
        "c",
        "28",
        "79",
        ["c", "a", "d", "b"],
    ],
    9: ["7", "7", "6", "677", "b", "514", "345", "7"],
    10: ["15", "5", "12", "425", "c", "571", "1", "390"],
}


def body(q, value):
    return {
        {"choice": "choice_id", "ordering": "order"}.get(
            q["response_kind"], "value"
        ): value
    }


def finish_new(client, n):
    response = first.start(client, n)
    assert response.status_code == 200, response.text
    row = response.json()
    feedback = []
    path = root.P + f"/attempts/{row['attempt_id']}"
    for q, literal in zip(row["questions"], ANSWERS[n], strict=True):
        payload = {
            "assessment_version": 1,
            "request_id": str(uuid4()),
            "question_id": q["id"],
            "answer": body(q, literal),
        }
        response = client.post(path + "/answers", json=payload)
        assert response.status_code == 200 and response.json()["is_correct"], (
            response.text
        )
        assert client.post(path + "/answers", json=payload).json() == response.json()
        feedback.append(response.json())
    payload = {"assessment_version": 1, "request_id": str(uuid4())}
    response = client.post(path + "/complete", json=payload)
    assert response.status_code == 200, response.text
    assert client.post(path + "/complete", json=payload).json() == response.json()
    return row, feedback, response.json()


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from first.preview.__wrapped__(tmp_path, monkeypatch)


def complete_previous(client):
    first.complete_previous(client)
    for n in first.ANSWERS:
        assert first.finish_new(client, n)[-1]["xp_awarded"] == 10


@pytest.mark.parametrize("n", ANSWERS)
def test_original_answers_wrong_steps_and_source_identity(n):
    lesson = next(l for l in load_course() if l["key"] == f"math-2-2-{n}-r1")
    assert lesson["source_number"] == 41 + n
    assert lesson["source_refs"][0]["pdf_pages"] == [2 * n + 3, 2 * n + 4]
    assert lesson["source_refs"][0]["printed_pages"] == [2 * n + 2, 2 * n + 3]
    for q, literal in zip(lesson["questions"], ANSWERS[n], strict=True):
        wrong = (
            list(reversed(literal))
            if isinstance(literal, list)
            else next(
                (v["id"] for v in q["public"].get("choices", []) if v["id"] != literal),
                "999",
            )
        )
        assert grade_answer(q["grading"], body(q["public"], literal)) == "correct"
        assert grade_answer(q["grading"], body(q["public"], wrong)) == "incorrect"
    independent = {
        6: 35 - 30,
        7: 58 - 54,
        8: 28 + 35 - 19 - 16,
        9: 304 + 210,
        10: 245 + 326,
    }
    index = {6: 6, 7: 6, 8: 5, 9: 5, 10: 5}[n]
    assert (
        grade_answer(
            lesson["questions"][index]["grading"], {"value": str(independent[n])}
        )
        == "correct"
    )


def test_carry_steps_checked_independently_and_no_keys_in_public():
    assert 268 + 157 == 425 and divmod(8 + 7, 10) == (1, 5)
    assert divmod(6 + 5 + 1, 10) == (1, 2) and 2 + 1 + 1 == 4
    assert 245 + 326 == 571 and 180 + (180 + 30) == 390
    assert 0 * 100 + 2 * 10 + 1 == 21 and 2 * 100 + 1 * 10 == 210
    assert sorted([308, 73, 415, 106]) == [73, 106, 308, 415]
    # A common mistake (carry omitted) is not accepted by the independent FRQ.
    l = next(l for l in load_course() if l["key"] == "math-2-2-10-r1")
    assert grade_answer(l["questions"][5]["grading"], {"value": "561"}) == "incorrect"
    assert (
        grade_answer(l["questions"][5]["grading"], {"value": "500+70+1"}) == "correct"
    )
    d = json.loads((ROOT / "grade2_part2_batch2.json").read_text())
    review = json.loads((ROOT / "grade2_part2_batch2_review.json").read_text())
    altered = deepcopy(d)
    altered["lessons"][0]["source_number"] = 48
    with pytest.raises(ValueError, match="math_topic_source_identity_mismatch"):
        validate_document(altered, review)


def test_real_chain_ordering_resume_wrong_feedback_and_replay(preview, monkeypatch):
    client, factory = preview
    monkeypatch.setenv(first.FLAG, "true")
    monkeypatch.setenv(PART1_FLAG, "true")
    assert first.start(client, 6).status_code == 403
    complete_previous(client)
    assert first.start(client, 7).status_code == 403
    pending = first.start(client, 6).json()
    path = root.P + f"/attempts/{pending['attempt_id']}"
    response = client.post(
        path + "/answers",
        json={
            "assessment_version": 1,
            "request_id": str(uuid4()),
            "question_id": pending["questions"][0]["id"],
            "answer": {"choice_id": "b"},
        },
    )
    assert response.status_code == 200 and not response.json()["is_correct"]
    assert response.json()["feedback"]
    resumed = first.start(
        client, 6, request_id=pending["attempt_id"].rsplit(":", 1)[1]
    ).json()
    assert resumed["attempt_id"] == pending["attempt_id"]
    assert (
        client.post(
            path + "/complete",
            json={"assessment_version": 1, "request_id": str(uuid4())},
        ).status_code
        == 409
    )
    for n in ANSWERS:
        initial, _feedback, result = finish_new(client, n)
        assert result["xp_awarded"] == 10
        assert not any(
            k in str(initial) for k in ["'grading':", "'expected':", "'aliases':"]
        )
        assert finish_new(client, n)[-1]["xp_awarded"] == 0
    cat = client.get(root.P + "/catalog", params={"grade": 2, "part": 2}).json()
    assert all(l["state"] == "completed" for l in cat["lessons"])
    assert not cat["previous_book_complete"] and cat["source_gap_bridge"][
        "missing_source_numbers"
    ] == [25]
    with factory() as db:
        assert db.query(MathProgress).filter_by(user_id=1).count() == 53
        assert not db.query(MathProgress).filter_by(lesson_key="math-2-1-26-r1").first()
        assert db.get(User, 1).xp_total == 667 and db.get(User, 2).xp_total == 0
        assert db.get(User, 1).streak_days == 3
