"""Grade2I1–5: verified review, source gap and independent grade progress."""

from uuid import uuid4

import pytest
import test_mathematics_preview as first

from services import tokens
from services.mathematics_curriculum import load_course
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    1: ["14", "7", ["a", "b", "c"], "4", "b", "7", "11", "a"],
    2: ["64", "10", "40", "59", "b", "88", "50", "100"],
    3: ["31", "15", "53", "52", "b", "21", "21", "b"],
    4: ["30", "85", "22", "12", "b", "50", "1", "18"],
    5: ["8", "19", "4", "13", "b", "6", "4", "15"],
}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from first.preview.__wrapped__(tmp_path, monkeypatch)


def finish_new(client, n):
    response = client.post(
        first.P + f"/lessons/math-2-1-{n}-r1/start",
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
    l = next(l for l in load_course() if l["key"] == f"math-2-1-{n}-r1")
    assert l["source_number"] == n and l["sequence"] == n
    assert l["source_refs"][0]["pdf_pages"] == [2 * n + 3, 2 * n + 4]
    assert l["source_refs"][0]["printed_pages"] == [
        2 * n + 2,
        2 * n + 3,
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
    if n == 1:
        assert [20 - i for i in range(7)][-1] == 14
        assert 20 - (8 + 5 + 3) == 4
    if n == 2:
        assert 7 * 10 + 2 + 1 * 10 + 6 == 88
        assert (
            grade_answer(l["questions"][5]["grading"], {"value": "72+16"}) == "correct"
        )
    if n == 3:
        assert [x for x in range(101) if x - 12 == 41] == [53]
    if n == 4:
        assert 4 + 7 + 4 + 7 == 22 and 30 + (30 - 10) == 50
    if n == 5:
        assert [(a, b) for a in [7, 8] for b in [2, 5]] == [
            (7, 2),
            (7, 5),
            (8, 2),
            (8, 5),
        ]
        assert sum([3] * 4) == 12 and sum([3] * 6) == 18
        assert (
            grade_answer(l["questions"][5]["grading"], {"value": "15-(5+4)"})
            == "correct"
        )


def test_grade_choice_prerequisites_progress_replay_and_uid_isolation(preview):
    client, factory = preview
    cat = client.get(first.P + "/catalog", params={"grade": 2}).json()
    assert cat["grade"] == 2 and cat["previous_book_complete"]
    assert cat["book"]["source_topic_count"] == 44
    assert cat["book"]["implemented_sections"] == len(cat["lessons"])
    assert cat["book"]["source_gaps"][0]["missing_printed_pages"] == [54, 55]
    assert [l["state"] for l in cat["lessons"]] == ["available"] + ["locked"] * (
        len(cat["lessons"]) - 1
    )
    assert (
        client.post(
            first.P + "/lessons/math-2-1-2-r1/start",
            json={"assessment_version": 1, "request_id": str(uuid4())},
        ).status_code
        == 403
    )
    for n in ANSWERS:
        assert finish_new(client, n)[-1]["xp_awarded"] == 10
    assert finish_new(client, 5)[-1]["xp_awarded"] == 0
    complete = client.get(first.P + "/catalog", params={"grade": 2}).json()
    assert {l["key"] for l in complete["lessons"] if l["state"] == "completed"} == {
        f"math-2-1-{i}-r1" for i in range(1, 6)
    }
    assert not complete["course_ready"]
    first_grade = client.get(first.P + "/catalog").json()
    assert all(l["state"] != "completed" for l in first_grade["lessons"])
    other = client.get(
        first.P + "/catalog",
        params={"grade": 2},
        headers={"Authorization": "Bearer " + tokens.create_access_token(2)},
    ).json()
    assert [l["state"] for l in other["lessons"]] == ["available"] + ["locked"] * (
        len(cat["lessons"]) - 1
    )
    with factory() as db:
        assert db.query(MathProgress).filter_by(user_id=1).count() == 5
        assert db.get(User, 1).xp_total == 187 and db.get(User, 2).xp_total == 0
        assert db.get(User, 1).streak_days == 3


def test_grade2_map_keeps_missing25_and_actual_unnumbered_bodies():
    import json
    from copy import deepcopy

    from services.mathematics_curriculum import ROOT, validate_document

    m = json.loads((ROOT / "grade2_part1_map.json").read_text())
    assert len(m["topics"]) == 44 and m["authored_lessons"] == 43
    assert [t["source_number"] for t in m["topics"] if t["source_number"]] == list(
        range(1, 42)
    )
    assert [p for t in m["topics"] for p in (t["body_pdf_locator"] or [])] == list(
        range(5, 96)
    )
    gap = next(t for t in m["topics"] if t["source_number"] == 25)
    assert gap["body_pdf_locator"] is None and gap["printed_pages"] == [54, 55]
    assert not gap["interactive_lesson_created"]
    assert [
        (t["printed_pages"], t["body_pdf_locator"])
        for t in m["topics"]
        if t["source_number"] is None
    ] == [
        ([40, 41], [41, 42]),
        ([84, 85], [83, 84]),
        (list(range(90, 97)), list(range(89, 96))),
    ]
    assert not m["all_body_content_reviewed"] and not m["full_map_verified"]
    doc = json.loads((ROOT / "grade2_part1_batch1.json").read_text())
    review = json.loads((ROOT / "grade2_part1_batch1_review.json").read_text())
    altered = deepcopy(doc)
    altered["lessons"][0]["source_number"] = 2
    with pytest.raises(ValueError, match="math_topic_source_identity_mismatch"):
        validate_document(altered, review)
