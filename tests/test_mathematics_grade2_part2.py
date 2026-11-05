"""Grade2II: real-source hundreds/zeros,43actual prerequisites and revocable QA."""

import json
from copy import deepcopy
from uuid import uuid4

import pytest
import test_mathematics_grade2_part1_batch8 as previous
import test_mathematics_preview as first
from test_mathematics_grade2_part1_batch6 import FLAG as PART1_FLAG

from services import mathematics_runtime as runtime
from services import tokens
from services.mathematics_curriculum import ROOT, load_course, validate_document
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathLesson, MathProgress
from services.models import User

FLAG = "MATHEMATICS_QA_GRADE2_PART2_PREVIEW"
ANSWERS = {
    1: ["100", "10", "700", "1 000", "b", "700", "5", "45"],
    2: ["536", "5", "53", "629", "b", "768", "100", "600"],
    3: ["206", "0", "260", "2", "b", "809", "500", "24"],
    4: ["340", "0", "604", "64", "c", "570", "7", "30"],
    5: ["3", "63", "6", "5", "b", "97", "17", "93"],
}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    monkeypatch.delenv(FLAG, raising=False)
    yield from previous.preview.__wrapped__(tmp_path, monkeypatch)


def complete_previous(client):
    previous.complete_previous(client)
    for n in previous.ANSWERS:
        assert previous.finish_new(client, n)[-1]["xp_awarded"] == 10


def start(client, n=1, **extra):
    return client.post(
        first.P + f"/lessons/math-2-2-{n}-r1/start",
        json={"assessment_version": 1, "request_id": str(uuid4()), **extra},
    )


def finish_new(client, n):
    response = start(client, n)
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
def test_independent_literal_answers_wrong_values_and_aliases(n):
    l = next(l for l in load_course() if l["key"] == f"math-2-2-{n}-r1")
    assert l["source_number"] == 41 + n
    assert l["source_refs"][0]["pdf_pages"] == [2 * n + 3, 2 * n + 4]
    assert l["source_refs"][0]["printed_pages"] == [2 * n + 2, 2 * n + 3]
    for q, literal in zip(l["questions"], ANSWERS[n], strict=True):
        field = "choice_id" if q["public"]["response_kind"] == "choice" else "value"
        wrong = (
            next(c["id"] for c in q["public"]["choices"] if c["id"] != literal)
            if field == "choice_id"
            else "999"
        )
        assert grade_answer(q["grading"], {field: literal}) == "correct"
        assert grade_answer(q["grading"], {field: wrong}) == "incorrect"
    alternate = {1: "500+(400-200)", 2: "700+60+8", 3: "800+9", 4: "500+70", 5: "90+7"}[
        n
    ]
    assert grade_answer(l["questions"][5]["grading"], {"value": alternate}) == "correct"
    assert 1000 == 10 * 100 == 100 * 10 and len(str(1000)) == 4
    assert divmod(536, 10) == (53, 6) and 800 + 9 == 809 and 500 + 70 == 570
    assert 20 + (30 + 15) == 78 - 13 and 35 + 35 - 29 - 24 == 17 and 26 + 30 + 37 == 93


def test_real_body_map_keeps_toc73_discrepancy_and_rejects_renumbering():
    m = json.loads((ROOT / "grade2_part2_map.json").read_text())
    assert len(m["topics"]) == 34 and m["authored_lessons"] == 15
    assert [
        t["source_number"] for t in m["topics"] if t["source_number"] is not None
    ] == list(range(42, 73))
    assert [p for t in m["topics"] for p in t["body_pdf_locator"]] == list(range(5, 78))
    assert sum(t["kind"] == "unnumbered_summary" for t in m["topics"]) == 2
    assert m["topics"][32]["source_number"] is None and m["topics"][32][
        "body_pdf_locator"
    ] == [69, 70]
    assert (
        m["source_gaps"][0]["toc_source_number"] == 73
        and not m["all_body_content_reviewed"]
    )
    doc = json.loads((ROOT / "grade2_part2_batch1.json").read_text())
    review = json.loads((ROOT / "grade2_part2_batch1_review.json").read_text())
    altered = deepcopy(doc)
    altered["lessons"][0]["source_number"] = 73
    with pytest.raises(ValueError, match="math_topic_source_identity_mismatch"):
        validate_document(altered, review)


def test_all43_real_predecessors_no_missing_progress_and_revocation(
    preview, monkeypatch, tmp_path
):
    client, factory = preview
    assert start(client).status_code == 403
    monkeypatch.setenv(FLAG, "true")
    monkeypatch.setenv(PART1_FLAG, "true")
    assert start(client).status_code == 403  # Flags do not replace real prerequisites.
    assert start(client, allow_known_source_gap=True).status_code == 422
    complete_previous(client)
    monkeypatch.setenv(FLAG, "false")
    assert start(client).status_code == 403
    monkeypatch.setenv(FLAG, "true")
    monkeypatch.setenv(PART1_FLAG, "false")
    assert start(client).status_code == 403
    monkeypatch.setenv(PART1_FLAG, "true")
    cat = client.get(first.P + "/catalog", params={"grade": 2, "part": 2}).json()
    assert not cat["previous_book_complete"] and cat["previous_book_navigation_ready"]
    assert cat["source_gap_bridge"]["completed_predecessor_lessons"] == 43
    assert cat["source_gap_bridge"]["missing_source_numbers"] == [25]
    assert cat["source_sequence_gap_bridge"] is None and not cat["course_ready"]
    assert [l["state"] for l in cat["lessons"]] == ["available"] + ["locked"] * 14
    assert start(client, 2).status_code == 403
    pending = start(client).json()
    sid = pending["attempt_id"]
    req = sid.rsplit(":", 1)[1]
    other = {"Authorization": "Bearer " + tokens.create_access_token(2)}
    assert (
        client.post(
            first.P + f"/attempts/{sid}/complete",
            headers=other,
            json={"assessment_version": 1, "request_id": str(uuid4())},
        ).status_code
        == 404
    )
    for disabled in [FLAG, PART1_FLAG]:
        monkeypatch.setenv(disabled, "false")
        assert start(client, request_id=req).status_code == 403
        assert (
            client.post(
                first.P + f"/attempts/{sid}/answers",
                json={
                    "assessment_version": 1,
                    "request_id": str(uuid4()),
                    "question_id": pending["questions"][0]["id"],
                    "answer": {"value": "100"},
                },
            ).status_code
            == 403
        )
        assert (
            client.post(
                first.P + f"/attempts/{sid}/complete",
                json={"assessment_version": 1, "request_id": str(uuid4())},
            ).status_code
            == 403
        )
        monkeypatch.setenv(disabled, "true")
    assert start(client, request_id=req).status_code == 200
    initial, _, result = finish_new(client, 1)
    assert result["xp_awarded"] == 10
    assert finish_new(client, 1)[-1]["xp_awarded"] == 0
    monkeypatch.setenv(FLAG, "false")
    assert (
        start(client, 1).status_code == 403
    )  # Completed badge is not a new authorization.
    assert (
        start(client, 1, request_id=initial["attempt_id"].rsplit(":", 1)[1]).json()[
            "result"
        ]
        == result
    )
    monkeypatch.setenv(FLAG, "true")
    for n in [2, 3, 4, 5]:
        assert finish_new(client, n)[-1]["xp_awarded"] == 10
    assert finish_new(client, 5)[-1]["xp_awarded"] == 0
    with factory() as db:
        completed = {p.lesson_key for p in db.query(MathProgress).filter_by(user_id=1)}
        assert len(completed) == 48 and "math-2-1-26-r1" not in completed
        assert db.get(MathLesson, "math-2-1-26-r1") is None
        assert db.get(User, 1).xp_total == 617 and db.get(User, 2).xp_total == 0
        assert db.get(User, 1).streak_days == 3
        assert (
            runtime.qa_grade2_previous_book_gap(
                db, completed - {"math-2-1-44-r1"}, 2, 2
            )
            is None
        )
        assert runtime.qa_grade2_previous_book_gap(db, completed, 1, 3) is None
        for field in ["sha256", "topic_count"]:
            altered = deepcopy(runtime.manifest())
            target = next(
                b for b in altered["books"] if b["book_id"] == "math-uz-g2-p2"
            )
            target[field] = "invalid"
            with monkeypatch.context() as mp:
                mp.setattr(runtime, "manifest", lambda altered=altered: altered)
                assert runtime.qa_grade2_previous_book_gap(db, completed, 2, 2) is None
        with monkeypatch.context() as mp:
            mp.setenv("ENVIRONMENT", "production")
            assert runtime.qa_grade2_previous_book_gap(db, completed, 2, 2) is None
        m = json.loads((ROOT / "grade2_part2_map.json").read_text())
        m["topics"][0]["verification"] = "body_pending"
        (tmp_path / "grade2_part2_map.json").write_text(json.dumps(m))
        (tmp_path / "grade2_part1_map.json").write_bytes(
            (ROOT / "grade2_part1_map.json").read_bytes()
        )
        with monkeypatch.context() as mp:
            mp.setattr(runtime, "ROOT", tmp_path)
            assert runtime.qa_grade2_previous_book_gap(db, completed, 2, 2) is None
    assert not client.get(first.P + "/catalog", params={"grade": 2, "part": 2}).json()[
        "previous_book_complete"
    ]


@pytest.mark.parametrize(
    "text", ["1 000", "1\u00a0000", "1\u202f000", "+1 000", " 1 000 "]
)
def test_standard_grouped_thousand_literal_is_server_correct(text):
    lesson = next(l for l in load_course() if l["key"] == "math-2-2-1-r1")
    assert grade_answer(lesson["questions"][3]["grading"], {"value": text}) == "correct"
