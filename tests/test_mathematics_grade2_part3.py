"""Source73–77: geometry concepts, exact arithmetic and prerequisite/replay."""

import json
from copy import deepcopy
from uuid import uuid4

import pytest
import test_mathematics_grade2_part2 as first
import test_mathematics_grade2_part2_batch7 as previous
import test_mathematics_preview as root
from test_mathematics_grade2_part1_batch6 import FLAG as PART1_FLAG

from services.mathematics_curriculum import ROOT, load_course, validate_document
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    1: ["a", "1", "b", "b", "1", "360", "46", ["c", "b", "a"]],
    2: ["b", "a", "92", "8", "b", "56", "b", ["b", "a", "c"]],
    3: ["a", "2", "a", "b", "b", "24", "48", "591"],
    4: ["a", "4", "a", "a", "28", "196", "720", "b"],
    5: ["a", "1", "4", "b", "b", "38", "19", "45"],
}
body = previous.body


def start(client, n, request_id=None):
    return client.post(
        root.P + f"/lessons/math-2-3-{n}-r1/start",
        json={"assessment_version": 1, "request_id": request_id or str(uuid4())},
    )


def finish_new(client, n):
    response = start(client, n)
    assert response.status_code == 200, response.text
    row = response.json()
    feedback = []
    path = root.P + f"/attempts/{row['attempt_id']}"
    for q, literal in zip(row["questions"], ANSWERS[n], strict=True):
        data = {
            "assessment_version": 1,
            "request_id": str(uuid4()),
            "question_id": q["id"],
            "answer": body(q, literal),
        }
        reply = client.post(path + "/answers", json=data)
        assert reply.status_code == 200 and reply.json()["is_correct"], reply.text
        assert client.post(path + "/answers", json=data).json() == reply.json()
        feedback.append(reply.json())
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
def test_source_order_literal_answers_and_wrong_answers(n):
    l = next(l for l in load_course() if l["key"] == f"math-2-3-{n}-r1")
    assert l["source_number"] == 72 + n
    assert l["source_refs"][0]["pdf_pages"] == [2 * n + 3, 2 * n + 4]
    assert l["source_refs"][0]["printed_pages"] == [2 * n + 2, 2 * n + 3]
    for q, answer in zip(l["questions"], ANSWERS[n], strict=True):
        wrong = (
            list(reversed(answer))
            if isinstance(answer, list)
            else next(
                (c["id"] for c in q["public"].get("choices", []) if c["id"] != answer),
                "999",
            )
        )
        assert grade_answer(q["grading"], body(q["public"], answer)) == "correct"
        assert grade_answer(q["grading"], body(q["public"], wrong)) == "incorrect"


def test_geometry_arithmetic_and_source_identity_are_independent():
    assert (2 * 60 + 15) + (60 + 35) + (2 * 60 + 10) == 360
    assert 2 * (28 + 18) == 92 and 100 - 92 == 8 and 24 + (24 + 8) == 56
    assert 24 - 7 + 12 == 29 and 126 - 45 - (45 - 12) == 48
    assert 2 * (58 + (58 - 18)) == 196 and 720 + 110 - 430 == 170 + 230
    assert 2 * 4 + 2 * 14 + 2 == 38 and (8 * 10 + 3) - (3 * 10 + 8) == 45
    d = json.loads((ROOT / "grade2_part3_batch1.json").read_text())
    rev = json.loads((ROOT / "grade2_part3_batch1_review.json").read_text())
    altered = deepcopy(d)
    altered["lessons"][0]["source_number"] = 74
    with pytest.raises(ValueError, match="math_topic_source_identity_mismatch"):
        validate_document(altered, rev)
    altered = deepcopy(d)
    altered["lessons"][4]["formulas"][0]["expression"] = "4 + 14 + 2 + 14 + 4 = 36"
    with pytest.raises(ValueError, match="false_math_identity"):
        validate_document(altered, rev)


def test_real_34_to_part3_chain_resume_and_replay(preview, monkeypatch):
    client, factory = preview
    assert start(client, 1).status_code == 403
    monkeypatch.setenv(first.FLAG, "true")
    monkeypatch.setenv(PART1_FLAG, "true")
    complete_previous(client)
    assert start(client, 2).status_code == 403
    request = str(uuid4())
    pending = start(client, 1, request).json()
    assert start(client, 1, request).json()["attempt_id"] == pending["attempt_id"]
    for n in ANSWERS:
        initial, feedback, result = finish_new(client, n)
        assert result["xp_awarded"] == 10
        assert all(f["feedback"] for f in feedback)
        assert finish_new(client, n)[-1]["xp_awarded"] == 0
        assert not any(
            k in str(initial) for k in ["'grading':", "'expected':", "'aliases':"]
        )
    cat = client.get(root.P + "/catalog", params={"grade": 2, "part": 3}).json()
    assert cat["previous_book_complete"] and not cat["course_ready"]
    assert len(cat["lessons"]) == 5 and all(
        l["state"] == "completed" for l in cat["lessons"]
    )
    assert cat["source_gap_bridge"] is None
    with factory() as db:
        assert db.query(MathProgress).filter_by(user_id=1).count() == 82
        assert db.get(User, 1).xp_total == 957 and db.get(User, 2).xp_total == 0
        assert db.get(User, 1).streak_days == 3
        assert not db.query(MathProgress).filter_by(lesson_key="math-2-1-26-r1").first()


def test_inventory_printed_mapping_matches_every_reviewed_body_pin():
    from services.mathematics_curriculum import BATCHES

    inventory = json.loads((ROOT / "page_inventory.json").read_text())
    seen = set()
    for _, name in BATCHES:
        review = json.loads((ROOT / name).read_text())
        for topic in review["topics"]:
            for pin in topic["pages"]:
                row = inventory[review["book_id"]][pin["pdf_page"] - 1]
                assert row["printed_page"] == pin["printed_page"]
                assert row["native_text_sha256"] == pin["native_text_sha256"]
                assert (
                    row["mapping_status"]
                    == row["review_status"]
                    == "body_images_reviewed"
                )
                seen.add((review["book_id"], pin["pdf_page"]))
    assert len(seen) == 460
    assert inventory["math-uz-g2-p3"][14]["printed_page"] == 14
    assert (
        inventory["math-uz-g2-p3"][14]["mapping_status"]
        == "image_viewed_content_review_pending"
    )
