"""Independent grade2II literal, ordering, carry and real API/XP regressions."""

import json
from copy import deepcopy
from uuid import uuid4

import pytest
import test_mathematics_grade2_part2 as first
import test_mathematics_grade2_part2_batch5 as previous
import test_mathematics_preview as root
from test_mathematics_grade2_part1_batch6 import FLAG as PART1_FLAG

from services.mathematics_curriculum import ROOT, load_course, validate_document
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    26: ["b", "3", "225", "11", "a", "230", "431", "c"],
    27: ["555", "0", "700", "520", "b", "410", "360", "460"],
    28: ["297", "240", "4", "400", "b", "315", "641", ["c", "b", "a"]],
    29: ["60", "20", "6", "b", "a", "35", "1", "4"],
    30: ["135", "110", "245", "5", "70", "b", "155", "145", "35", "1"],
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
    assert lesson["source_number"] == 40 + n
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
        26: 650 - (120 + 140 + 160),
        27: 800 - 230 - 160,
        28: 620 - 95 - 210,
        29: 35,
        30: 4 * 60 + 10 - (60 + 35),
    }
    index = 6 if n == 30 else 5
    assert (
        grade_answer(
            lesson["questions"][index]["grading"], {"value": str(independent[n])}
        )
        == "correct"
    )


def test_source_science_zero_inverse_width_and_base60_independently():
    assert (750 - 476) + (280 - 123) == 431
    assert 180 + (375 + 145) == 700 and 430 - 0 == 430
    fixed = "400"
    reversed_fixed = fixed[::-1]
    assert reversed_fixed == "004" and reversed_fixed[::-1] == fixed
    assert int(reversed_fixed) == 4 and str(int(reversed_fixed))[::-1] != "400"
    assert 2 * 60 + 15 + 60 + 50 == 245 and divmod(245, 60) == (4, 5)
    assert 3 * 60 + 70 == 4 * 60 + 10 and 3 * 60 + 70 - (60 + 35) == 155
    assert (10 * 60 + 45) - (8 * 60 + 20) == 145
    d = json.loads((ROOT / "grade2_part2_batch6.json").read_text())
    review = json.loads((ROOT / "grade2_part2_batch6_review.json").read_text())
    altered = deepcopy(d)
    altered["lessons"][0]["source_number"] = 67
    with pytest.raises(ValueError, match="math_topic_source_identity_mismatch"):
        validate_document(altered, review)
    spec = d["lessons"][0]["questions"][7]["grading"]
    assert grade_answer(spec, {"choice_id": "c"}) == "correct"
    assert grade_answer(spec, {"choice_id": "a"}) == "incorrect"
    spec = d["lessons"][-1]["questions"][6]["grading"]
    assert grade_answer(spec, {"value": "250-95"}) == "correct"
    assert grade_answer(spec, {"value": "175"}) == "incorrect"


def test_real_chain_ordering_resume_wrong_feedback_and_replay(preview, monkeypatch):
    client, factory = preview
    monkeypatch.setenv(first.FLAG, "true")
    monkeypatch.setenv(PART1_FLAG, "true")
    assert first.start(client, 26).status_code == 403
    complete_previous(client)
    assert first.start(client, 27).status_code == 403
    pending = first.start(client, 26).json()
    path = root.P + f"/attempts/{pending['attempt_id']}"
    response = client.post(
        path + "/answers",
        json={
            "assessment_version": 1,
            "request_id": str(uuid4()),
            "question_id": pending["questions"][0]["id"],
            "answer": {"choice_id": "a"},
        },
    )
    assert response.status_code == 200 and not response.json()["is_correct"]
    assert response.json()["feedback"]
    resumed = first.start(
        client, 26, request_id=pending["attempt_id"].rsplit(":", 1)[1]
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
        assert db.query(MathProgress).filter_by(user_id=1).count() == 73
        assert not db.query(MathProgress).filter_by(lesson_key="math-2-1-26-r1").first()
        assert db.get(User, 1).xp_total == 867 and db.get(User, 2).xp_total == 0
        assert db.get(User, 1).streak_days == 3


def test_readonly_logical_catalog_has32_real_source_activities_not_lessons():
    catalog = json.loads(
        (ROOT / "grade2_part2_logical_source_catalog.json").read_text()
    )
    mapping = json.loads((ROOT / "grade2_part2_map.json").read_text())
    expected_pages = (
        [71] * 5 + [72] * 6 + [73] * 5 + [74] * 5 + [75] * 4 + [76] * 3 + [77] * 4
    )
    assert catalog["numbered_activities"] == 32
    assert catalog["original_digital_adaptations"] == 0
    assert catalog["publication"] == "source_catalog_only"
    assert catalog["source_activities"] == mapping["topics"][-1]["source_activities"]
    assert not mapping["topics"][-1]["interactive_lesson_created"]
    for n, (a, p) in enumerate(
        zip(catalog["source_activities"], expected_pages, strict=True), 1
    ):
        assert a["number"] == n and a["book_id"] == "math-uz-g2-p2"
        assert (
            a["pdf_pages"] == [p] and a["printed_pages"] == [p - 1] and a["objective"]
        )
