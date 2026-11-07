"""Independent grade2II literal, ordering, carry and real API/XP regressions."""

import json
from copy import deepcopy
from uuid import uuid4

import pytest
import test_mathematics_grade2_part2 as first
import test_mathematics_grade2_part2_batch4 as previous
import test_mathematics_preview as root
from test_mathematics_grade2_part1_batch6 import FLAG as PART1_FLAG

from services.mathematics_curriculum import ROOT, load_course, validate_document
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    21: ["10", "100", "341", "0", "b", "752", "45", "90"],
    22: ["276", "348", "624", "4", "b", "354", "35", "37"],
    23: ["3", "4", "80", "100", "b", "87", "230", "4"],
    24: ["408", "264", "426", "4", "a", "332", "327", "12"],
    25: ["407", "262", "145", ["b", "c", "a"], "b", "145", "50", "256"],
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
    assert lesson["source_number"] == 40 + n
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
        21: 700 + 50 + 2,
        22: 632 - 278,
        23: 28 + 33 + 26,
        24: 412 - 80,
        25: 240 + 167 - (500 - 238),
    }
    assert (
        grade_answer(lesson["questions"][5]["grading"], {"value": str(independent[n])})
        == "correct"
    )


def test_mm_geometry_operation_and_brackets_independent_results():
    assert 3 * 100 + 4 * 10 + 1 == 341 and 1 * 100 + 0 * 10 + 1 == 101
    assert 30 + 20 + 30 == 80 and 30 + 20 + 30 + 20 == 100
    assert 600 - 125 - 85 - 160 == 230 and 28 + 33 + 26 == 87
    assert int("400"[::-1]) == 4 and 246 + 327 == 573 and 573 - 246 == 327
    assert 240 + 167 - (500 - 238) == 145 and 240 + 167 - 500 - 238 != 145
    d = json.loads((ROOT / "grade2_part2_batch5.json").read_text())
    review = json.loads((ROOT / "grade2_part2_batch5_review.json").read_text())
    altered = deepcopy(d)
    altered["lessons"][0]["source_number"] = 62
    with pytest.raises(ValueError, match="math_topic_source_identity_mismatch"):
        validate_document(altered, review)
    spec = d["lessons"][-1]["questions"][5]["grading"]
    assert grade_answer(spec, {"value": "407-262"}) == "correct"
    assert grade_answer(spec, {"value": "240+167-500-238"}) == "incorrect"


def test_real_chain_ordering_resume_wrong_feedback_and_replay(preview, monkeypatch):
    client, factory = preview
    monkeypatch.setenv(first.FLAG, "true")
    monkeypatch.setenv(PART1_FLAG, "true")
    assert first.start(client, 21).status_code == 403
    complete_previous(client)
    assert first.start(client, 22).status_code == 403
    pending = first.start(client, 21).json()
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
        client, 21, request_id=pending["attempt_id"].rsplit(":", 1)[1]
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
    assert all(l["state"] == "completed" for l in cat["lessons"][:25])
    assert not cat["previous_book_complete"] and cat["source_gap_bridge"][
        "missing_source_numbers"
    ] == [25]
    with factory() as db:
        assert db.query(MathProgress).filter_by(user_id=1).count() == 68
        assert not db.query(MathProgress).filter_by(lesson_key="math-2-1-26-r1").first()
        assert db.get(User, 1).xp_total == 817 and db.get(User, 2).xp_total == 0
        assert db.get(User, 1).streak_days == 3
