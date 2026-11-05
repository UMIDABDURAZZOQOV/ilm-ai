"""Sources31–35: original literal keys, scientifically corrected borrowing."""

from uuid import uuid4

import pytest
import test_mathematics_grade2_part1_batch6 as previous
import test_mathematics_preview as first

from services.mathematics_curriculum import load_course
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    32: ["35", "35", "50", "67", "b", "66", "36", "yigindi"],
    33: ["14", "6", "36", "28", "a", "35", "46", "73"],
    34: ["16", "16", "54", "24", "c", "69", "20", "20"],
    35: ["45", "38", "10", "38", "b", "46", "34", "33"],
    36: ["59", "31", "81", "65", "b", "48", "2", "ha"],
}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from previous.preview.__wrapped__(tmp_path, monkeypatch)


def complete_previous(client):
    previous.complete_previous(client)
    for n in previous.ANSWERS:
        assert previous.finish_new(client, n)[-1]["xp_awarded"] == 10


def finish_new(client, n):
    response = previous.start(client, n)
    assert response.status_code == 200, response.text
    row = response.json()
    feedback = []
    for q, literal in zip(row["questions"], ANSWERS[n], strict=True):
        field = "choice_id" if q["response_kind"] == "choice" else "value"
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
    path = first.P + f"/attempts/{row['attempt_id']}/complete"
    payload = {"assessment_version": 1, "request_id": str(uuid4())}
    response = client.post(path, json=payload)
    assert response.status_code == 200, response.text
    assert client.post(path, json=payload).json() == response.json()
    return row, feedback, response.json()


@pytest.mark.parametrize("n", ANSWERS)
def test_independent_answers_and_original_source_mapping(n):
    l = next(l for l in load_course() if l["key"] == f"math-2-1-{n}-r1")
    assert l["source_number"] == n - 1 and l["sequence"] == n
    assert l["source_refs"][0]["pdf_pages"] == [2 * n + 1, 2 * n + 2]
    assert l["source_refs"][0]["printed_pages"] == [2 * n + 2, 2 * n + 3]
    for q, literal in zip(l["questions"], ANSWERS[n], strict=True):
        kind = q["public"]["response_kind"]
        field = "choice_id" if kind == "choice" else "value"
        assert grade_answer(q["grading"], {field: literal}) == "correct"
        wrong = (
            next(c["id"] for c in q["public"]["choices"] if c["id"] != literal)
            if kind == "choice"
            else "noma’lum"
            if kind == "short_text"
            else "999"
        )
        assert grade_answer(q["grading"], {field: wrong}) == "incorrect"
    alternate = {
        32: "23+16+27",
        33: "82-47",
        34: "36+19+14",
        35: "36+24-14",
        36: "36+29-17",
    }[n]
    assert grade_answer(l["questions"][5]["grading"], {"value": alternate}) == "correct"
    assert (
        23 + 16 + 27 == 66
        and 82 - 47 == 35
        and 36 + 19 + 14 == 69
        and 36 + 24 - 14 == 46
        and 36 + 29 - 17 == 48
    )
    assert 58 - 18 == 40 and 40 - 30 == 10 and 12 - 10 == 2
    if n == 33:
        assert "kamayuvchining" in l["cards"][0]["body"].lower()
        assert 74 == 60 + 14 and 38 == 30 + 8 and (60 - 30) + (14 - 8) == 36
    if n == 35:
        a, b, c = 18, 26, 20
        assert a + b - c == 24 and b >= c and a < c


def test_all_five_real_progress_and_sequential_gap_policy(preview, monkeypatch):
    client, factory = preview
    monkeypatch.setenv(previous.FLAG, "true")
    complete_previous(client)
    cat = client.get(first.P + "/catalog", params={"grade": 2}).json()
    assert [l["state"] for l in cat["lessons"]][:30] == ["completed"] * 30
    assert (
        cat["lessons"][30]["key"] == "math-2-1-32-r1"
        and cat["lessons"][30]["state"] == "available"
    )
    assert previous.start(client, 33).status_code == 403
    for n in ANSWERS:
        assert finish_new(client, n)[-1]["xp_awarded"] == 10
    assert finish_new(client, 36)[-1]["xp_awarded"] == 0
    with factory() as db:
        keys = {p.lesson_key for p in db.query(MathProgress).filter_by(user_id=1)}
        assert len(keys) == 35 and "math-2-1-26-r1" not in keys
        assert db.get(User, 1).xp_total == 487 and db.get(User, 2).xp_total == 0
        assert db.get(User, 1).streak_days == 3
    monkeypatch.setenv(previous.FLAG, "false")
    assert previous.start(client, 36).status_code == 403
