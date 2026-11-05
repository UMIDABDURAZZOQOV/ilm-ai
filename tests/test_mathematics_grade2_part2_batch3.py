"""Independent grade2II literal, ordering, carry and real API/XP regressions."""

import json
from copy import deepcopy
from uuid import uuid4

import pytest
import test_mathematics_grade2_part2 as first
import test_mathematics_grade2_part2_batch2 as previous
import test_mathematics_preview as root
from test_mathematics_grade2_part1_batch6 import FLAG as PART1_FLAG

from services.mathematics_curriculum import ROOT, load_course, validate_document
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    11: ["10", "5", "13", "305", "b", "338", "435", "43"],
    12: ["14", "2", "12", "356", "a", "359", "485", "120"],
    13: ["10", "9", "4", "414", "b", "443", "20", "150"],
    14: ["635", "428", "422", ["c", "b", "a"], "a", "532", "115", ["b", "c", "a"]],
    15: ["21", "2", "11", "511", "b", "510", "360", "6"],
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
    previous.complete_previous(client)
    for n in previous.ANSWERS:
        assert previous.finish_new(client, n)[-1]["xp_awarded"] == 10


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
        11: 574 - 236,
        12: 745 - 386,
        13: 800 - 357,
        14: 900 - 368,
        15: 215 + 167 + 128,
    }
    assert (
        grade_answer(lesson["questions"][5]["grading"], {"value": str(independent[n])})
        == "correct"
    )


def test_donor_places_zero_and_multi_carry_are_independently_verified():
    assert 400 + 50 + 13 == 463 and 463 - 158 == 305 and 305 + 158 == 463
    assert 500 + 120 + 14 == 634 and 634 - 278 == 356
    assert 600 + 90 + 10 == 700 and 700 - 286 == 414
    assert 126 + 238 + 147 == 511 and divmod(6 + 8 + 7, 10) == (2, 1)
    assert divmod(2 + 3 + 4 + 2, 10) == (1, 1) and 1 + 2 + 1 + 1 == 5
    assert 215 + 167 + 128 == 510 and 154 + 168 + 213 - 420 == 115
    l = next(l for l in load_course() if l["key"] == "math-2-2-15-r1")
    assert grade_answer(l["questions"][5]["grading"], {"value": "500+10"}) == "correct"
    assert grade_answer(l["questions"][5]["grading"], {"value": "500"}) == "incorrect"
    d = json.loads((ROOT / "grade2_part2_batch3.json").read_text())
    review = json.loads((ROOT / "grade2_part2_batch3_review.json").read_text())
    altered = deepcopy(d)
    altered["lessons"][0]["source_number"] = 53
    with pytest.raises(ValueError, match="math_topic_source_identity_mismatch"):
        validate_document(altered, review)


def test_real_chain_ordering_resume_wrong_feedback_and_replay(preview, monkeypatch):
    client, factory = preview
    monkeypatch.setenv(first.FLAG, "true")
    monkeypatch.setenv(PART1_FLAG, "true")
    assert first.start(client, 11).status_code == 403
    complete_previous(client)
    assert first.start(client, 12).status_code == 403
    pending = first.start(client, 11).json()
    path = root.P + f"/attempts/{pending['attempt_id']}"
    response = client.post(
        path + "/answers",
        json={
            "assessment_version": 1,
            "request_id": str(uuid4()),
            "question_id": pending["questions"][0]["id"],
            "answer": {"value": "999"},
        },
    )
    assert response.status_code == 200 and not response.json()["is_correct"]
    assert response.json()["feedback"]
    resumed = first.start(
        client, 11, request_id=pending["attempt_id"].rsplit(":", 1)[1]
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
        assert db.query(MathProgress).filter_by(user_id=1).count() == 58
        assert not db.query(MathProgress).filter_by(lesson_key="math-2-1-26-r1").first()
        assert db.get(User, 1).xp_total == 717 and db.get(User, 2).xp_total == 0
        assert db.get(User, 1).streak_days == 3
