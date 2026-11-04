"""BookIII literal source oracles and explicit, scoped local-QA source-gap bridge."""

import json
from copy import deepcopy
from uuid import uuid4

import pytest
import test_mathematics_part2_batch6 as last
import test_mathematics_preview as first

from services import mathematics_runtime as runtime
from services import tokens
from services.mathematics_curriculum import ROOT, load_course, validate_document
from services.mathematics_grading import grade_answer
from services.mathematics_models import (
    MathAnswer,
    MathAttempt,
    MathLesson,
    MathProgress,
)
from services.models import User

ANSWERS = {
    1: ["b", "a", "17", "a", "b", "17", "18", "c"],
    2: [["a", "b", "c", "d"], "37", "b", "47", "b", "62", "65", "b"],
    3: ["b", "56", "76", "22", "a", "22", "a", ["a", "b", "c", "d", "e"]],
    4: ["b", "a", "37", "b", "a", "33", "18", "23"],
    5: ["12", "11", "a", ["a", "b", "c"], "b", "57", "9", "22"],
}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from first.preview.__wrapped__(tmp_path, monkeypatch)


def complete_existing_73(client):
    last.complete_previous(client)
    for n in range(69, 74):
        assert last.finish_new(client, n)[-1]["xp_awarded"] == 10


def finish_third(client, n, request=None):
    response = client.post(
        first.P + f"/lessons/math-1-3-{n}-r1/start",
        json={"assessment_version": 1, "request_id": request or str(uuid4())},
    )
    assert response.status_code == 200, response.text
    row = response.json()
    feedback = []
    for q, value in zip(row["questions"], ANSWERS[n]):
        field = {"choice": "choice_id", "ordering": "order"}.get(
            q["response_kind"], "value"
        )
        payload = {
            "assessment_version": 1,
            "request_id": str(uuid4()),
            "question_id": q["id"],
            "answer": {field: value},
        }
        response = client.post(
            first.P + f"/attempts/{row['attempt_id']}/answers", json=payload
        )
        assert response.status_code == 200 and response.json()["is_correct"], (
            response.text
        )
        assert (
            client.post(
                first.P + f"/attempts/{row['attempt_id']}/answers", json=payload
            ).json()
            == response.json()
        )
        feedback.append(response.json())
    payload = {"assessment_version": 1, "request_id": str(uuid4())}
    path = first.P + f"/attempts/{row['attempt_id']}/complete"
    response = client.post(path, json=payload)
    assert response.status_code == 200, response.text
    assert client.post(path, json=payload).json() == response.json()
    return row, feedback, response.json()


def test_explicit_bridge_keeps_strict_prerequisites_progress_and_account_isolation(
    preview, monkeypatch
):
    client, factory = preview
    monkeypatch.delenv("MATHEMATICS_QA_SOURCE_GAP_BRIDGE", raising=False)
    path = first.P + "/lessons/math-1-3-1-r1/start"
    request = str(uuid4())
    start = {"assessment_version": 1, "request_id": request}
    assert (
        client.post(path, json={**start, "allow_source_gap": True}).status_code == 422
    )
    assert client.post(path, json=start).status_code == 403
    monkeypatch.setenv("MATHEMATICS_QA_SOURCE_GAP_BRIDGE", "true")
    # A flag never skips unfinished existing lessons.
    assert client.post(path, json=start).status_code == 403
    complete_existing_73(client)
    monkeypatch.delenv("MATHEMATICS_QA_SOURCE_GAP_BRIDGE")
    assert client.post(path, json=start).status_code == 403
    monkeypatch.setenv("MATHEMATICS_QA_SOURCE_GAP_BRIDGE", "true")
    cat = client.get(first.P + "/catalog", params={"part": 3}).json()
    assert not cat["previous_book_complete"] and cat["previous_book_navigation_ready"]
    assert cat["source_gap_bridge"]["missing_source_numbers"] == [74]
    assert cat["book"]["source_body_topic_count"] == 37
    assert cat["lessons"][0]["state"] == "available"
    assert all(l["state"] == "locked" for l in cat["lessons"][1:])
    blocked_next = client.post(
        first.P + "/lessons/math-1-3-2-r1/start",
        json={**start, "request_id": str(uuid4())},
    )
    assert (
        blocked_next.status_code == 403
        and blocked_next.json()["detail"] == "finish_previous_lesson"
    )
    row = client.post(path, json=start).json()
    assert row["source_gap_bridge"]["kind"] == "local_qa_known_source_gap"
    sid = row["attempt_id"]
    answer_path = first.P + f"/attempts/{sid}/answers"
    wrong = {
        "assessment_version": 1,
        "request_id": str(uuid4()),
        "question_id": row["questions"][0]["id"],
        "answer": {"choice_id": "a"},
    }
    result = client.post(answer_path, json=wrong)
    assert not result.json()["is_correct"] and result.json()["hint_level"] == 1
    assert client.post(answer_path, json=wrong).json() == result.json()
    assert (
        client.post(
            answer_path, json={**wrong, "answer": {"choice_id": "b"}}
        ).status_code
        == 409
    )
    monkeypatch.setenv("MATHEMATICS_QA_SOURCE_GAP_BRIDGE", "false")
    assert client.post(path, json=start).status_code == 403
    assert client.post(answer_path, json=wrong).status_code == 403
    assert (
        client.post(first.P + f"/attempts/{sid}/complete", json=start).status_code
        == 403
    )
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("MATHEMATICS_QA_SOURCE_GAP_BRIDGE", "true")
    assert client.get(first.P + "/catalog", params={"part": 3}).status_code == 404
    monkeypatch.setenv("ENVIRONMENT", "test")
    assert client.post(path, json=start).json()["attempt_id"] == sid
    for n in range(1, 6):
        result = finish_third(client, n, request if n == 1 else None)[-1]
        assert result["xp_awarded"] == 10
        assert result["source_gap_bridge"]["missing_source_numbers"] == [74]
    assert finish_third(client, 5)[-1]["xp_awarded"] == 0
    other = {"Authorization": "Bearer " + tokens.create_access_token(2)}
    othercat = client.get(
        first.P + "/catalog", params={"part": 3}, headers=other
    ).json()
    assert not othercat["previous_book_navigation_ready"]
    assert all(l["state"] == "locked" for l in othercat["lessons"])
    assert client.post(answer_path, json=wrong, headers=other).status_code == 404
    with factory() as db:
        assert db.get(User, 1).xp_total == 917 and db.get(User, 1).streak_days == 3
        assert db.get(User, 2).xp_total == 0
        assert db.query(MathProgress).count() == 78
        assert not db.get(MathLesson, "math-1-2-33-r1")
        assert (
            db.get(MathLesson, "math-1-3-1-r1").document.get("qa_source_gap_bridge")
            is None
        )
        assert db.get(MathAttempt, sid).snapshot["qa_source_gap_bridge"]
        assert db.query(MathAnswer).filter_by(attempt_id=sid).count() == 9
        completed = {p.lesson_key for p in db.query(MathProgress).filter_by(user_id=1)}
        assert runtime.qa_source_gap_bridge(db, completed, 2, 3) is None
        assert runtime.qa_source_gap_bridge(db, completed, 1, 4) is None
        original = runtime.manifest()
        changed = deepcopy(original)
        next(b for b in changed["books"] if b["book_id"] == "math-uz-g1-p2")[
            "sha256"
        ] = "0" * 64
        monkeypatch.setattr(runtime, "manifest", lambda: changed)
        assert runtime.qa_source_gap_bridge(db, completed, 1, 3) is None


@pytest.mark.parametrize("n", range(1, 6))
def test_third_book_literal_keys_wrong_answers_and_page_identity(n):
    lesson = next(l for l in load_course() if l["key"] == f"math-1-3-{n}-r1")
    assert lesson["source_number"] == n
    assert lesson["source_refs"][0]["pdf_pages"] == [2 * n + 4, 2 * n + 5]
    assert lesson["source_refs"][0]["printed_pages"] == [2 * n + 2, 2 * n + 3]
    assert len(lesson["questions"]) == len(ANSWERS[n]) == 8
    for q, literal in zip(lesson["questions"], ANSWERS[n]):
        kind = q["public"]["response_kind"]
        field = {"choice": "choice_id", "ordering": "order"}.get(kind, "value")
        assert grade_answer(q["grading"], {field: literal}) == "correct"
        wrong = (
            str(int(literal) + 1)
            if kind == "exact_number"
            else list(reversed(literal))
            if kind == "ordering"
            else next(c["id"] for c in q["public"]["choices"] if c["id"] != literal)
        )
        assert grade_answer(q["grading"], {field: wrong}) == "incorrect"


def test_third_book_cannot_invent_source75_or_turn_toc_only_schedule_into_a_lesson():
    doc = json.loads((ROOT / "grade1_part3_batch1.json").read_text())
    review = json.loads((ROOT / "grade1_part3_batch1_review.json").read_text())
    doc["lessons"][0]["source_number"] = 75
    with pytest.raises(ValueError, match="source_identity"):
        validate_document(doc, review)
    mapping = json.loads((ROOT / "grade1_part3_map.json").read_text())
    assert len(mapping["topics"]) == 37
    assert mapping["full_map_verified"] == mapping["all_body_content_reviewed"]
    assert all(
        not t["ready"] and t["body_pdf_locator"] is None
        for t in mapping["scheduled_activities_without_body"]
    )
