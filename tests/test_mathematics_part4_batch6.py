"""IV139–144: roots, inverse stories, review and full source closure."""

from uuid import uuid4

import pytest
import test_mathematics_part4_batch5 as previous
import test_mathematics_preview as first

from services.mathematics_curriculum import load_course
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    139: ["19", "25", "14", "25", "b", "18", "17", "b"],
    140: ["21", "13", "8", "22", "a", "15", "18", "b"],
    141: ["17", "7", "24", "15", "a", "17", "31", "b"],
    142: ["23", "19", ["a", "b", "c"], "10", "b", "11", "b", "7"],
    143: ["60", ["b", "a", "c"], "11", "4", "a", "36", "15", "b"],
    144: ["26", "2", "33", "12", "b", "20", "6", "3"],
}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from first.preview.__wrapped__(tmp_path, monkeypatch)


def complete_previous(client, monkeypatch):
    previous.complete_previous(client, monkeypatch)
    monkeypatch.setenv("MATHEMATICS_QA_PART3_SCHEDULE_BRIDGE", "true")
    for n in previous.ANSWERS:
        assert previous.finish_new(client, n)[-1]["xp_awarded"] == 10


def finish_new(client, n):
    response = client.post(
        first.P + f"/lessons/math-1-4-{n - 111}-r1/start",
        json={"assessment_version": 1, "request_id": str(uuid4())},
    )
    assert response.status_code == 200, response.text
    row = response.json()
    feedback = []
    for q, literal in zip(row["questions"], ANSWERS[n]):
        field = {"choice": "choice_id", "ordering": "order"}.get(
            q["response_kind"], "value"
        )
        payload = {
            "assessment_version": 1,
            "request_id": str(uuid4()),
            "question_id": q["id"],
            "answer": {field: literal},
        }
        path = first.P + f"/attempts/{row['attempt_id']}/answers"
        response = client.post(path, json=payload)
        assert response.status_code == 200 and response.json()["is_correct"], (
            response.text
        )
        assert client.post(path, json=payload).json() == response.json()
        feedback.append(response.json())
    payload = {"assessment_version": 1, "request_id": str(uuid4())}
    path = first.P + f"/attempts/{row['attempt_id']}/complete"
    response = client.post(path, json=payload)
    assert response.status_code == 200, response.text
    assert client.post(path, json=payload).json() == response.json()
    return row, feedback, response.json()


@pytest.mark.parametrize("n", ANSWERS)
def test_source_independent_literal_answers_and_alternatives(n):
    l = next(l for l in load_course() if l["key"] == f"math-1-4-{n - 111}-r1")
    assert l["source_number"] == n and l["sequence"] == n - 111
    assert l["source_refs"][0]["pdf_pages"] == [2 * (n - 111) + 3, 2 * (n - 111) + 4]
    assert l["source_refs"][0]["printed_pages"] == [
        2 * (n - 111) + 2,
        2 * (n - 111) + 3,
    ]
    for q, literal in zip(l["questions"], ANSWERS[n]):
        kind = q["public"]["response_kind"]
        field = {"choice": "choice_id", "ordering": "order"}.get(kind, "value")
        assert grade_answer(q["grading"], {field: literal}) == "correct"
        wrong = (
            next(c["id"] for c in q["public"]["choices"] if c["id"] != literal)
            if kind == "choice"
            else list(reversed(literal))
            if kind == "ordering"
            else "noma’lum"
            if kind == "short_text"
            else "999"
        )
        assert grade_answer(q["grading"], {field: wrong}) == "incorrect"
    if n == 139:
        assert [x for x in range(101) if 34 - x == 16] == [18]
        assert (
            grade_answer(l["questions"][5]["grading"], {"value": "34-16"}) == "correct"
        )
    if n == 140:
        assert [x for x in range(101) if 4 + x + 9 == 28] == [15]
    if n == 141:
        assert l["title"] == "Kesma va uning uzunligi"
        assert [x for x in range(101) if 38 - x == 21] == [17]
    if n == 142:
        assert 68 - (18 + 27) == 23 and 18 - 7 == 11
    if n == 143:
        assert 40 - (12 - 8) == 36 and 40 - (12 + 8) == 20
        assert (
            grade_answer(l["questions"][5]["grading"], {"value": "40-(12-8)"})
            == "correct"
        )
        assert (
            grade_answer(l["questions"][5]["grading"], {"value": "20"}) == "incorrect"
        )
    if n == 144:
        from itertools import combinations

        assert len(list(combinations("ACDB", 2))) == 6
        assert 3 + 4 + 5 == 12 and (3 + 4) + (4 + 5) == 16


def test_all143_progress_xp_and_no_extra_reward_or_control_completion(
    preview, monkeypatch
):
    client, factory = preview
    complete_previous(client, monkeypatch)
    assert (
        client.post(
            first.P + "/lessons/math-1-4-29-r1/start",
            json={"assessment_version": 1, "request_id": str(uuid4())},
        ).status_code
        == 403
    )
    for n in ANSWERS:
        assert finish_new(client, n)[-1]["xp_awarded"] == 10
    assert finish_new(client, 144)[-1]["xp_awarded"] == 0
    cat = client.get(first.P + "/catalog", params={"part": 4}).json()
    assert {l["key"] for l in cat["lessons"] if l["state"] == "completed"} == {
        f"math-1-4-{i}-r1" for i in range(1, 34)
    }
    assert not cat["previous_book_complete"] and not cat["course_ready"]
    assert cat["source_gap_bridge"]["schedule_only_rows_not_completed"] == 5
    with factory.begin() as db:
        assert db.query(MathProgress).filter_by(user_id=1).count() == 143
        assert db.get(User, 1).xp_total == 1567 and db.get(User, 2).xp_total == 0
        assert db.get(User, 1).streak_days == 3


def test_whole_book_source_closure_preserves_prior_unready_items():
    import json

    from services.mathematics_curriculum import ROOT

    fourth = json.loads((ROOT / "grade1_part4_map.json").read_text())
    checks = fourth["additional_image_checks"] + [
        p for t in fourth["topics"] for p in t["boundary_pins"]
    ]
    assert len(checks) == 74
    assert {p["pdf_page"] for p in checks} == set(range(1, 75))
    assert fourth["full_file_reviewed_page_count"] == 74
    assert fourth["authored_lessons"] == 33 and fourth["all_body_content_reviewed"]
    assert [t["body_pdf_locator"] for t in fourth["topics"]] == [
        [p, p + 1] for p in range(5, 71, 2)
    ]
    assert all(len(p["image_sha256"]) == 64 for p in checks)
    second = json.loads((ROOT / "grade1_part2_map.json").read_text())
    third = json.loads((ROOT / "grade1_part3_map.json").read_text())
    assert second["topics"][-1]["body_pdf_locator"] is None
    assert len(third["scheduled_activities_without_body"]) == 5
    assert not any(row["ready"] for row in third["scheduled_activities_without_body"])
