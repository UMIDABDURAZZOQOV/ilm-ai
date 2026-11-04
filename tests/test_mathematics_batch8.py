"""First-book completion and inverse/comparison/table objectives: literal keys."""

import json
from uuid import uuid4

import pytest
import test_mathematics_preview as first
from test_mathematics_batch7 import complete_first_thirty_five

from services.mathematics_curriculum import ROOT, load_course, validate_document
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    36: ["b", "a", "5", "0", "b", "6", "5", "6"],
    37: ["7", "5", "2", "7", "a", "8", "3", "b"],
    38: ["a", "b", "5", "7", "b", "6", "b", "5"],
    39: ["7", "7", "7", "a", "b", "9", "b", "3"],
    40: ["2", "8", "5", "a", "a", "8", "b", "4"],
    41: ["a", "7", "6", "9", "b", "5", "b", "1"],
}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from first.preview.__wrapped__(tmp_path, monkeypatch)


def finish_first_book(client, number):
    row = first.start(client, number)
    feedback = []
    for q, literal in zip(row["questions"], ANSWERS[number]):
        field = "choice_id" if q["response_kind"] == "choice" else "value"
        data = {
            "assessment_version": 1,
            "request_id": str(uuid4()),
            "question_id": q["id"],
            "answer": {field: literal},
        }
        response = client.post(
            f"{first.P}/attempts/{row['attempt_id']}/answers", json=data
        )
        assert response.status_code == 200 and response.json()["is_correct"], (
            response.text
        )
        assert (
            client.post(
                f"{first.P}/attempts/{row['attempt_id']}/answers", json=data
            ).json()
            == response.json()
        )
        feedback.append(response.json())
    result = client.post(
        f"{first.P}/attempts/{row['attempt_id']}/complete",
        json={"assessment_version": 1, "request_id": str(uuid4())},
    )
    assert result.status_code == 200, result.text
    return row, feedback, result.json()


def test_first_book_all_forty_one_results_and_replay(preview):
    client, factory = preview
    complete_first_thirty_five(client)
    for n in range(36, 42):
        assert finish_first_book(client, n)[-1]["xp_awarded"] == 10
    assert finish_first_book(client, 41)[-1]["xp_awarded"] == 0
    assert all(
        r["state"] == "completed"
        for r in client.get(first.P + "/catalog").json()["lessons"]
    )
    with factory() as db:
        assert db.get(User, 1).xp_total == 547 and db.get(User, 2).xp_total == 0
        assert db.query(MathProgress).count() == 41


def test_first_book_has_exact_source_order_and_no_duplicate_scan_lessons():
    lessons = [l for l in load_course() if (l["grade"], l["part"]) == (1, 1)]
    assert [l["sequence"] for l in lessons] == list(range(1, 42))
    assert lessons[-1]["title"] == "Ifodalar"
    cited = {p for l in lessons for p in l["source_refs"][0]["pdf_pages"]}
    assert len(cited) == 82 and cited == set(range(5, 55)) | set(range(57, 89))
    assert all(
        l["source_refs"][0]["printed_pages"]
        == [2 * l["sequence"] + 2, 2 * l["sequence"] + 3]
        for l in lessons
    )


def test_fact_cannot_silently_cite_unreviewed_duplicate_or_wrong_book_pages():
    document = json.loads((ROOT / "grade1_part1_batch8.json").read_text())
    review = json.loads((ROOT / "grade1_part1_batch8_review.json").read_text())
    review["topics"][0]["facts"][0]["pdf_pages"] = [55, 56]
    with pytest.raises(ValueError, match="math_fact_pages_outside_review"):
        validate_document(document, review)
