"""Textbook III23–26/30: literal arithmetic, whole/part, criteria and API replay."""

from uuid import uuid4

import pytest
import test_mathematics_part3_batch4 as previous
import test_mathematics_preview as first

from services.mathematics_curriculum import load_course
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    23: ["b", "34", "8", "b", "b", "21", "7", "b"],
    24: ["b", "6", "c", "5", "b", "6", "4", "4"],
    25: ["17", "30", "b", "a", "b", "27", "34", "3"],
    26: ["b", "a", "c", "5", "b", "43", "8", "26"],
    30: ["a", "5", "b", "5", "b", "5", "4", "a"],
}
SEQUENCES = {23: 21, 24: 22, 25: 23, 26: 24, 30: 25}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from first.preview.__wrapped__(tmp_path, monkeypatch)


def complete_previous(client, monkeypatch):
    previous.complete_previous(client, monkeypatch)
    monkeypatch.setenv("MATHEMATICS_QA_SOURCE_GAP_BRIDGE", "true")
    for n in previous.ANSWERS:
        assert previous.finish_new(client, n)[-1]["xp_awarded"] == 10


def finish_new(client, n):
    response = client.post(
        first.P + f"/lessons/math-1-3-{SEQUENCES[n]}-r1/start",
        json={"assessment_version": 1, "request_id": str(uuid4())},
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


@pytest.mark.parametrize("number", list(ANSWERS))
def test_source_literal_answers_wrong_answers_and_no_synthetic_formulas(number):
    lesson = next(
        l for l in load_course() if l["key"] == f"math-1-3-{SEQUENCES[number]}-r1"
    )
    ref = lesson["source_refs"][0]
    assert ref["pdf_pages"] == [2 * SEQUENCES[number] + 4, 2 * SEQUENCES[number] + 5]
    assert ref["printed_pages"] == [
        2 * SEQUENCES[number] + 2,
        2 * SEQUENCES[number] + 3,
    ]
    assert lesson["source_number"] == number and lesson["sequence"] == SEQUENCES[number]
    assert len(lesson["cards"]) == 6 and len(lesson["questions"]) == 8
    for q, literal in zip(lesson["questions"], ANSWERS[number]):
        kind = q["public"]["response_kind"]
        field = {"choice": "choice_id", "ordering": "order"}.get(kind, "value")
        assert grade_answer(q["grading"], {field: literal}) == "correct", (
            number,
            q["id"],
            literal,
        )
        if kind == "choice":
            wrong = next(c["id"] for c in q["public"]["choices"] if c["id"] != literal)
        elif kind == "ordering":
            wrong = list(reversed(literal))
        else:
            wrong = "999"
        assert grade_answer(q["grading"], {field: wrong}) == "incorrect"
        assert all(
            r["pdf_pages"] == ref["pdf_pages"]
            and r["printed_pages"] == ref["printed_pages"]
            for r in q["source_refs"]
        )
    if number == 25:
        assert (
            grade_answer(lesson["questions"][5]["grading"], {"value": "12+(12+3)"})
            == "correct"
        )
        assert (
            grade_answer(lesson["questions"][5]["grading"], {"value": "12+3"})
            == "incorrect"
        )
    if number == 30:
        # Numeric-only answer with cm fixed in the authored question, not
        # a claim to parse unrestricted physical unit expressions.
        assert "santimetr" in lesson["questions"][5]["public"]["prompt"]


def test_all98_local_api_progress_order_and_replay_without_fake_missing74(
    preview, monkeypatch
):
    client, factory = preview
    complete_previous(client, monkeypatch)
    blocked = client.post(
        first.P + "/lessons/math-1-3-22-r1/start",
        json={"assessment_version": 1, "request_id": str(uuid4())},
    )
    assert (
        blocked.status_code == 403
        and blocked.json()["detail"] == "finish_previous_lesson"
    )
    for n in ANSWERS:
        initial, feedback, result = finish_new(client, n)
        assert result["xp_awarded"] == 10
        assert initial["source_gap_bridge"]["missing_source_numbers"] == [74]
        assert len(feedback) == 8
    assert finish_new(client, 30)[-1]["xp_awarded"] == 0
    catalog = client.get(first.P + "/catalog", params={"part": 3}).json()
    assert {l["key"] for l in catalog["lessons"] if l["state"] == "completed"} == {
        f"math-1-3-{n}-r1" for n in range(1, 26)
    }
    assert catalog["book"]["source_body_topic_count"] == 37
    assert not catalog["previous_book_complete"]
    with factory() as db:
        assert db.get(User, 1).xp_total == 1117
        assert db.get(User, 1).streak_days == 3 and db.get(User, 2).xp_total == 0
        assert db.query(MathProgress).count() == 98
        assert not db.query(MathProgress).filter_by(lesson_key="math-1-2-33-r1").first()


def test_footer29_and_toc28_remain_explicit_unready_without_invented_lesson():
    import json

    from services.mathematics_curriculum import ROOT

    mapping = json.loads((ROOT / "grade1_part3_map.json").read_text())
    game = next(
        t
        for t in mapping["scheduled_activities_without_body"]
        if t["kind"] == "game" and t["source_numbers"] == [28]
    )
    assert game["body_footer_source_numbers"] == [29]
    assert game["body_footer_pdf_page"] == 53 and game["body_footer_printed_page"] == 51
    assert game["body_pdf_locator"] is None and not game["ready"]
    assert not any(
        l.get("source_number") == 29
        for l in load_course()
        if (l["grade"], l["part"]) == (1, 3)
    )
    title = next(l for l in load_course() if l["key"] == "math-1-3-21-r1")["title"]
    assert title == "Shartni yetishmayotgan ma’lumotlar bilan to‘ldirish"
