"""IV112–116 actual source identities, literal keys and opt-in QA navigation."""

import json
from copy import deepcopy
from uuid import uuid4

import pytest
import test_mathematics_part3_batch7 as previous
import test_mathematics_preview as first

from services import mathematics_runtime as runtime
from services import tokens
from services.mathematics_curriculum import ROOT, load_course
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    112: ["7", "3", "26", "10", "b", "17", "8", "15"],
    113: ["6", "8", "5", "16", "a", "9", ["a", "b", "c", "d"], "9"],
    114: ["8", "5", "34", "4", "b", "11", "9", "a"],
    115: ["3", "4", "9", "5", "b", "15", "12", "a"],
    116: ["3", "5", "6", "61", "b", "4", "17", "b"],
}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from first.preview.__wrapped__(tmp_path, monkeypatch)


def complete_previous(client, monkeypatch):
    previous.complete_previous(client, monkeypatch)
    for n in previous.ANSWERS:
        assert previous.finish_new(client, n)[-1]["xp_awarded"] == 10


def finish_fourth(client, n, request=None):
    response = client.post(
        first.P + f"/lessons/math-1-4-{n - 111}-r1/start",
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
        path = first.P + f"/attempts/{row['attempt_id']}/answers"
        response = client.post(path, json=payload)
        assert response.status_code == 200 and response.json()["is_correct"], (
            response.text
        )
        assert client.post(path, json=payload).json() == response.json()
        feedback.append(response.json())
    path = first.P + f"/attempts/{row['attempt_id']}/complete"
    payload = {"assessment_version": 1, "request_id": str(uuid4())}
    response = client.post(path, json=payload)
    assert response.status_code == 200, response.text
    assert client.post(path, json=payload).json() == response.json()
    return row, feedback, response.json()


@pytest.mark.parametrize("n", ANSWERS)
def test_independently_computed_source_aligned_answers_and_wrong_inputs(n):
    lesson = next(l for l in load_course() if l["key"] == f"math-1-4-{n - 111}-r1")
    assert lesson["source_number"] == n and lesson["sequence"] == n - 111
    assert lesson["source_refs"][0]["pdf_pages"] == [
        2 * (n - 111) + 3,
        2 * (n - 111) + 4,
    ]
    assert lesson["source_refs"][0]["printed_pages"] == [
        2 * (n - 111) + 2,
        2 * (n - 111) + 3,
    ]
    assert len(lesson["cards"]) == 6 and len(lesson["questions"]) == 8
    for q, literal in zip(lesson["questions"], ANSWERS[n]):
        kind = q["public"]["response_kind"]
        field = {"choice": "choice_id", "ordering": "order"}.get(kind, "value")
        assert grade_answer(q["grading"], {field: literal}) == "correct"
        wrong = (
            next(c["id"] for c in q["public"]["choices"] if c["id"] != literal)
            if kind == "choice"
            else list(reversed(literal))
            if kind == "ordering"
            else "999"
        )
        assert grade_answer(q["grading"], {field: wrong}) == "incorrect"
    if n == 112:
        assert (
            grade_answer(lesson["questions"][6]["grading"], {"value": "11-3"})
            == "correct"
        )
        assert (
            grade_answer(lesson["questions"][6]["grading"], {"value": "11"})
            == "incorrect"
        )
    if n == 116:
        assert (
            grade_answer(lesson["questions"][3]["grading"], {"value": "26+(26+9)"})
            == "correct"
        )
        assert (
            grade_answer(lesson["questions"][3]["grading"], {"value": "26+9"})
            == "incorrect"
        )


def test_33_map_rows_are_not_33_ready_lessons_or_invented_edition_gaps():
    m = json.loads((ROOT / "grade1_part4_map.json").read_text())
    assert [t["source_number"] for t in m["topics"]] == list(range(112, 145))
    assert [t["path_sequence"] for t in m["topics"]] == list(range(1, 34))
    assert (
        m["authored_lessons"] == 10
        and not m["full_map_verified"]
        and not m["all_body_content_reviewed"]
    )
    assert [
        t["source_number"] for t in m["topics"] if t["interactive_lesson_created"]
    ] == list(range(112, 122))
    assert all(
        t["verification"] == "header_footer_images_reviewed_body_pending"
        for t in m["topics"][10:]
    )
    assert (
        m["topics"][5]["title"] == m["topics"][6]["title"]
        and m["topics"][5]["topic_id"] != m["topics"][6]["topic_id"]
    )


def test_scoped_iv_flag_never_completes_gaps_or_skips_prerequisites(
    preview, monkeypatch
):
    client, factory = preview
    path = first.P + "/lessons/math-1-4-1-r1/start"
    payload = {"assessment_version": 1, "request_id": str(uuid4())}
    monkeypatch.setenv("MATHEMATICS_QA_PART3_SCHEDULE_BRIDGE", "true")
    monkeypatch.setenv("MATHEMATICS_QA_SOURCE_GAP_BRIDGE", "true")
    assert client.post(path, json=payload).status_code == 403
    assert (
        client.post(path, json={**payload, "allow_source_gap": True}).status_code == 422
    )
    complete_previous(client, monkeypatch)
    monkeypatch.setenv("MATHEMATICS_QA_PART3_SCHEDULE_BRIDGE", "false")
    assert client.post(path, json=payload).status_code == 403
    monkeypatch.setenv("MATHEMATICS_QA_PART3_SCHEDULE_BRIDGE", "true")
    monkeypatch.setenv("MATHEMATICS_QA_SOURCE_GAP_BRIDGE", "false")
    assert client.post(path, json=payload).status_code == 403
    monkeypatch.setenv("MATHEMATICS_QA_SOURCE_GAP_BRIDGE", "true")
    cat = client.get(first.P + "/catalog", params={"part": 4}).json()
    assert (
        cat["previous_book_complete"] is False
        and cat["previous_book_navigation_ready"] is True
    )
    assert (
        cat["book"]["source_topic_count"] == 33
        and cat["book"]["implemented_sections"] == 10
    )
    assert cat["source_gap_bridge"]["schedule_only_rows_not_completed"] == 5
    assert cat["source_gap_bridge"]["earlier_source_gap"]["missing_source_numbers"] == [
        74
    ]
    with factory.begin() as db:
        completed = {p.lesson_key for p in db.query(MathProgress).filter_by(user_id=1)}
        assert len(completed) == 110
        assert runtime.qa_navigation_bridge(db, completed, 2, 4) is None
        altered = deepcopy(runtime.manifest())
        altered["books"][3]["sha256"] = "0" * 64
        with monkeypatch.context() as scoped:
            scoped.setattr(runtime, "manifest", lambda: altered)
            assert runtime.qa_navigation_bridge(db, completed, 1, 4) is None
    other = {"Authorization": "Bearer " + tokens.create_access_token(2)}
    assert client.post(path, json=payload, headers=other).status_code == 403
    # An in-flight IV attempt is rechecked against the IV policy, not hardcodedIII.
    row = client.post(path, json=payload).json()
    sid = row["attempt_id"]
    monkeypatch.setenv("MATHEMATICS_QA_PART3_SCHEDULE_BRIDGE", "false")
    assert client.post(path, json=payload).status_code == 403
    assert (
        client.post(
            first.P + f"/attempts/{sid}/answers",
            json={
                "assessment_version": 1,
                "request_id": str(uuid4()),
                "question_id": row["questions"][0]["id"],
                "answer": {"value": "7"},
            },
        ).status_code
        == 403
    )
    monkeypatch.setenv("MATHEMATICS_QA_PART3_SCHEDULE_BRIDGE", "true")
    assert client.post(path, json=payload).status_code == 200
    assert (
        client.post(
            first.P + "/lessons/math-1-4-2-r1/start",
            json={"assessment_version": 1, "request_id": str(uuid4())},
        ).status_code
        == 403
    )
    assert finish_fourth(client, 112, payload["request_id"])[-1]["xp_awarded"] == 10
    for n in range(113, 117):
        assert finish_fourth(client, n)[-1]["xp_awarded"] == 10
    assert finish_fourth(client, 116)[-1]["xp_awarded"] == 0
    monkeypatch.setenv("MATHEMATICS_QA_PART3_SCHEDULE_BRIDGE", "false")
    assert client.post(path, json=payload).json()["result"]["xp_awarded"] == 10
    with factory.begin() as db:
        assert db.query(MathProgress).filter_by(user_id=1).count() == 115
        assert db.get(User, 1).xp_total == 1287 and db.get(User, 2).xp_total == 0
        assert db.get(User, 1).streak_days == 3
