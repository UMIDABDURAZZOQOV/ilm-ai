"""Independent grade2II literal, ordering, carry and real API/XP regressions."""

import json
from copy import deepcopy
from uuid import uuid4

import pytest
import test_mathematics_grade2_part2 as first
import test_mathematics_grade2_part2_batch3 as previous
import test_mathematics_preview as root
from test_mathematics_grade2_part1_batch6 import FLAG as PART1_FLAG

from services.mathematics_curriculum import ROOT, load_course, validate_document
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    16: ["565", "564", "15", "400", "b", "800", "556", "96"],
    17: ["400", "100", "26", ["b", "a", "c"], "b", "3", "414", "100"],
    18: ["10", "100", "30", "300", "b", "46", "42", "210"],
    19: ["127", "2", "0", "308", "b", "542", "18", "13"],
    20: ["542", "54", "276", "624", "a", "354", "5", "410"],
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
    assert lesson["source_number"] == {16: 57, 17: None, 18: 58, 19: 59, 20: 60}[n]
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
        16: 214 + 186 + 225 + 175,
        17: 74 + 86 + 63 - 55 - 68 - 45 - 52,
        18: 460 // 10,
        19: 500 + 40 + 2,
        20: 632 - 278,
    }
    assert (
        grade_answer(lesson["questions"][5]["grading"], {"value": str(independent[n])})
        == "correct"
    )


def test_lengths_equal_units_strict_threshold_and_summary_identity():
    assert 1 * 100 == 10 * 10 and 4 * 100 + 6 * 10 == 46 * 10
    assert 1 * 100 + 2 * 10 + 7 == 127 and divmod(208, 100) == (2, 8)
    assert 276 + 348 == 624 and 632 - 278 == 354
    low, high = 95, 140
    assert [low < v < high for v in [95, 96, 139, 140]] == [False, True, True, False]
    assert 168 - 150 == 18 and 135 - 122 == 13
    d = json.loads((ROOT / "grade2_part2_batch4.json").read_text())
    review = json.loads((ROOT / "grade2_part2_batch4_review.json").read_text())
    summary = d["lessons"][1]
    assert summary["source_number"] is None and summary["sequence"] == 17
    altered = deepcopy(d)
    altered["lessons"][1]["source_number"] = 58
    with pytest.raises(ValueError, match="math_topic_source_identity_mismatch"):
        validate_document(altered, review)
    spec = d["lessons"][4]["questions"][5]["grading"]
    assert grade_answer(spec, {"value": "600+32-278"}) == "correct"
    assert grade_answer(spec, {"value": "364"}) == "incorrect"


def test_real_chain_ordering_resume_wrong_feedback_and_replay(preview, monkeypatch):
    client, factory = preview
    monkeypatch.setenv(first.FLAG, "true")
    monkeypatch.setenv(PART1_FLAG, "true")
    assert first.start(client, 16).status_code == 403
    complete_previous(client)
    assert first.start(client, 17).status_code == 403
    pending = first.start(client, 16).json()
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
        client, 16, request_id=pending["attempt_id"].rsplit(":", 1)[1]
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
        assert db.query(MathProgress).filter_by(user_id=1).count() == 63
        assert not db.query(MathProgress).filter_by(lesson_key="math-2-1-26-r1").first()
        assert db.get(User, 1).xp_total == 767 and db.get(User, 2).xp_total == 0
        assert db.get(User, 1).streak_days == 3
