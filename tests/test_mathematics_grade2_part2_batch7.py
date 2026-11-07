"""Book II closure: independent answers, 32 exact activities and private grading."""

import json
from copy import deepcopy
from uuid import uuid4

import pytest
import test_mathematics_grade2_part2 as first
import test_mathematics_grade2_part2_batch6 as previous
import test_mathematics_preview as root
from test_mathematics_grade2_part1_batch6 import FLAG as PART1_FLAG

from services.mathematics_curriculum import ROOT, load_course, validate_document
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    31: ["3", "10", "35", "5", "a", "215", "95", "33"],
    32: ["37", "445", "49", "10", "b", "108", "100", "18"],
    33: ["369", "400", "67", ["b", "c", "a"], "b", "131", "b", "75"],
    34: [
        "10",
        "6",
        "a",
        "b",
        "22",
        "34",
        "52",
        "80",
        ["d", "b", "a", "c"],
        "9",
        "730",
        "8",
        "a",
        "a",
        "4",
        "4",
        "6",
        "1",
        "a",
        "20",
        "20",
        "3",
        "a",
        "12",
        "9",
        "971",
        "b",
        "a",
        "c",
        "7",
        "17",
        "42",
        "c",
        "4",
        "7",
        "2",
        "5",
        "6",
        "9",
        "4",
        "128",
        "35",
        "g",
    ],
}
body = previous.body


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
def test_original_literals_wrong_answers_and_exact_source_pages(n):
    lesson = next(l for l in load_course() if l["key"] == f"math-2-2-{n}-r1")
    assert lesson["source_refs"][0]["pdf_pages"] == (
        [71] if n == 34 else [2 * n + 3, 2 * n + 4]
    )
    assert lesson["source_refs"][0]["printed_pages"] == (
        [70] if n == 34 else [2 * n + 2, 2 * n + 3]
    )
    for q, literal in zip(lesson["questions"], ANSWERS[n], strict=True):
        wrong = (
            list(reversed(literal))
            if isinstance(literal, list)
            else next(
                (c["id"] for c in q["public"].get("choices", []) if c["id"] != literal),
                "999",
            )
        )
        assert grade_answer(q["grading"], body(q["public"], literal)) == "correct", q[
            "id"
        ]
        assert grade_answer(q["grading"], body(q["public"], wrong)) == "incorrect", q[
            "id"
        ]


def test_independent_duration_balances_partitions_and_rosette_orbits():
    assert 24 - 21 + 7 == 10
    assert 17 * 60 + 20 - (15 * 60 + 45) == 95
    assert 8 * 60 + 20 + 15 - (8 * 60 + 30) == 5
    assert 2 * 60 + 8 == 128 and 7 - 3 == 4 and 3 * 365 - 365 == 730
    assert 5 + 2 - 3 == 4 and 5 + 3 - 2 == 6 and 3 - 2 == 1
    groups = [[7], [1, 6], [2, 5], [3, 4]]
    assert sorted(v for g in groups for v in g) == list(range(1, 8))
    assert all(sum(g) == 7 for g in groups)
    lesson = load_course()[-1]
    patterns = lesson["questions"][-1]["public"]["visual"]["patterns"]
    orbits = {}
    for p in patterns:
        colors = p["colors"]
        canonical = min(tuple(colors[i:] + colors[:i]) for i in range(6))
        orbits.setdefault(canonical, []).append(p["id"])
    assert sorted(len(v) for v in orbits.values()) == [1, 2, 2, 2]
    assert next(v for v in orbits.values() if len(v) == 1) == ["g"]


def test_32_activities_have43_checks_with_exact_book_page_and_fact():
    lesson = load_course()[-1]
    assert lesson["key"] == "math-2-2-34-r1"
    cards = lesson["cards"]
    assert (
        len(cards) == 32
        and len(lesson["questions"]) == 43
        and len(lesson["examples"]) == 8
    )
    pages = [71] * 5 + [72] * 6 + [73] * 5 + [74] * 5 + [75] * 4 + [76] * 3 + [77] * 4
    for n, (card, page) in enumerate(zip(cards, pages, strict=True), 1):
        a = card["source_activity"]
        assert a["number"] == n and a["book_id"] == "math-uz-g2-p2"
        assert a["pdf_pages"] == [page] and a["printed_pages"] == [page - 1]
        questions = [
            q
            for q in lesson["questions"]
            if q["public"]["source_activity"]["number"] == n
        ]
        assert len(questions) == {6: 3, 14: 3, 21: 2, 26: 2, 28: 6}.get(n, 1)
        assert all(q["public"]["source_activity"] == a for q in questions)
    scene = lesson["questions"][-2]["public"]["visual"]
    assert set(scene) == {"type", "hour_hand", "minute_hand", "mirrored"}
    assert scene["mirrored"] is True
    assert not {"hour", "minute", "expected", "grading"}.intersection(scene)


@pytest.mark.parametrize("mutation", ["page", "activity", "clock", "rosette", "answer"])
def test_validator_rejects_wrong_pages_missing_activity_bad_visual_or_key(mutation):
    d = json.loads((ROOT / "grade2_part2_batch7.json").read_text())
    review = json.loads((ROOT / "grade2_part2_batch7_review.json").read_text())
    bad = deepcopy(d)
    lesson = bad["lessons"][-1]
    if mutation == "page":
        lesson["questions"][0]["public"]["source_activity"]["pdf_pages"] = [77]
    elif mutation == "activity":
        lesson["cards"][0]["source_activity"]["number"] = 32
    elif mutation == "clock":
        lesson["questions"][-2]["public"]["visual"]["minute_hand"] = [0, 0]
    elif mutation == "rosette":
        lesson["questions"][-1]["public"]["visual"]["patterns"][-1]["colors"] = lesson[
            "questions"
        ][-1]["public"]["visual"]["patterns"][0]["colors"][:]
    else:
        lesson["questions"][-1]["grading"]["expected"] = "a"
    with pytest.raises((ValueError, KeyError)):
        validate_document(bad, review)


def test_real_all34_chain_replay_identity_and_part3_prerequisite(preview, monkeypatch):
    client, factory = preview
    monkeypatch.setenv(first.FLAG, "true")
    monkeypatch.setenv(PART1_FLAG, "true")
    assert first.start(client, 31).status_code == 403
    complete_previous(client)
    for n in ANSWERS:
        initial, feedback, result = finish_new(client, n)
        assert result["xp_awarded"] == 10
        assert not any(
            k in str(initial) for k in ["'grading':", "'expected':", "'aliases':"]
        )
        assert all(f["feedback"] for f in feedback)
        assert finish_new(client, n)[-1]["xp_awarded"] == 0
    cat = client.get(root.P + "/catalog", params={"grade": 2, "part": 2}).json()
    assert len(cat["lessons"]) == 34 and all(
        l["state"] == "completed" for l in cat["lessons"]
    )
    assert not cat["previous_book_complete"] and cat["source_gap_bridge"][
        "missing_source_numbers"
    ] == [25]
    third = client.get(root.P + "/catalog", params={"grade": 2, "part": 3}).json()
    assert third["previous_book_complete"] and third["lessons"] == []
    with factory() as db:
        assert db.query(MathProgress).filter_by(user_id=1).count() == 77
        assert not db.query(MathProgress).filter_by(lesson_key="math-2-1-26-r1").first()
        assert db.get(User, 1).xp_total == 907 and db.get(User, 2).xp_total == 0
        assert db.get(User, 1).streak_days == 3
