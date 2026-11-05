"""All remaining available grade2I bodies;26practical adaptations are one lesson."""

from copy import deepcopy
from uuid import uuid4

import pytest
import test_mathematics_grade2_part1_batch7 as previous
import test_mathematics_preview as first
from test_mathematics_grade2_part1_batch6 import FLAG, start

from services import tokens
from services.mathematics_curriculum import ROOT, load_course, validate_document
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathLesson, MathProgress
from services.models import User

ANSWERS = {
    37: ["45", "27", "27", "11", "b", "27", "33", "c"],
    38: ["30", "12", "5", "20", "b", "15", "47", "7"],
    39: ["25", "43", "8", "64", "c", "38", "12", "33"],
    40: ["60", "37", "12", "38", "b", "41", "15", "7"],
    41: ["4", "9", "7", "6", "b", "13", "16", "2"],
    42: ["36", "0", "29", "12", "b", "78", "12", "c"],
    43: ["37", "22", "25", "65", "a", "23", ["a", "b", "c"], "c"],
    44: [
        "b",
        ["a", "d", "c", "b"],
        "6",
        "5",
        "a",
        ["a", "b", "c", "d"],
        "b",
        "18",
        "6",
        "3",
        "a",
        "4",
        "c",
        "15",
        "27",
        "ikki rangli",
        "15",
        "2",
        "b",
        "o‘ngda",
        "28",
        "12",
        "13",
        "34",
        "7",
        "34",
    ],
}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from previous.preview.__wrapped__(tmp_path, monkeypatch)


def complete_previous(client):
    previous.complete_previous(client)
    for n in previous.ANSWERS:
        assert previous.finish_new(client, n)[-1]["xp_awarded"] == 10


def finish_new(client, n):
    response = start(client, n)
    assert response.status_code == 200, response.text
    row = response.json()
    feedback = []
    for q, literal in zip(row["questions"], ANSWERS[n], strict=True):
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
    path = first.P + f"/attempts/{row['attempt_id']}/complete"
    payload = {"assessment_version": 1, "request_id": str(uuid4())}
    response = client.post(path, json=payload)
    assert response.status_code == 200, response.text
    assert client.post(path, json=payload).json() == response.json()
    return row, feedback, response.json()


@pytest.mark.parametrize("n", ANSWERS)
def test_source_independent_literal_keys_and_wrong_answers(n):
    l = next(l for l in load_course() if l["key"] == f"math-2-1-{n}-r1")
    assert l["sequence"] == n
    expected_source = {
        37: 36,
        38: 37,
        39: 38,
        40: 39,
        41: None,
        42: 40,
        43: 41,
        44: None,
    }[n]
    assert l["source_number"] == expected_source
    pages = list(range(89, 96)) if n == 44 else [2 * n + 1, 2 * n + 2]
    assert l["source_refs"][0]["pdf_pages"] == pages
    assert l["source_refs"][0]["printed_pages"] == [p + 1 for p in pages]
    for q, literal in zip(l["questions"], ANSWERS[n], strict=True):
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
    if n != 44:
        alt = {
            37: "88-(26+35)",
            38: "46-(7+18+6)",
            39: "(28+28)-(6+6+6)",
            40: "53+16-28",
            41: "5+2+6",
            42: "24+28+33-7",
            43: "64-(23+18)",
        }[n]
        assert grade_answer(l["questions"][5]["grading"], {"value": alt}) == "correct"
    assert 72 - 18 - 27 == 27 and 17 - 6 - 6 == 5 and 46 - 7 - 18 - 6 == 15
    assert 28 + 28 - 6 - 6 - 6 == 38 and 53 + 16 - 28 == 41 and 24 + 28 + 33 - 7 == 78
    assert len("kitob") + len("daftar") + len("qalam") == 16


def test_practical_real26mapping_and_tamper_rejection():
    import json

    doc = json.loads((ROOT / "grade2_part1_batch8.json").read_text())
    review = json.loads((ROOT / "grade2_part1_batch8_review.json").read_text())
    l = doc["lessons"][-1]
    assert l["sequence"] == 44 and l["source_number"] is None
    assert len(l["cards"]) == len(l["questions"]) == 26
    expected = (
        [89] * 4 + [90] * 4 + [91] * 4 + [92] * 4 + [93] * 4 + [94] * 3 + [95] * 3
    )
    assert [q["public"]["source_activity"]["number"] for q in l["questions"]] == list(
        range(1, 27)
    )
    assert [
        q["public"]["source_activity"]["pdf_pages"][0] for q in l["questions"]
    ] == expected
    for mutation in ["omit", "duplicate", "page", "card", "disable"]:
        altered = deepcopy(doc)
        if mutation == "omit":
            altered["lessons"][-1]["questions"].pop()
        if mutation == "duplicate":
            altered["lessons"][-1]["questions"][1]["public"]["source_activity"] = (
                deepcopy(l["questions"][0]["public"]["source_activity"])
            )
        if mutation == "page":
            altered["lessons"][-1]["questions"][0]["public"]["source_activity"][
                "pdf_pages"
            ] = [90]
        if mutation == "card":
            altered["lessons"][-1]["cards"][0].pop("source_activity")
        if mutation == "disable":
            altered["lessons"][-1]["cards"][0]["show_explorer"] = "false"
        with pytest.raises(
            ValueError,
            match="math_practical_activity_coverage_mismatch|math_invalid_card_explorer_visibility",
        ):
            validate_document(altered, review)
    # Independent enumeration/calculation checks of the new adapted worksheet.
    from itertools import combinations

    assert len(list(combinations("ABCD", 2))) == 6
    assert 13 + 18 - 24 == 7 and 43 + 5 - 14 == 34 and 19 + 14 - 5 == 28
    assert 9 + 2 + 4 == 15 and 1 + 6 + 8 == 2 + 5 + 8 == 3 + 4 + 8 == 15


def test_available_body_completion_missing_source_not_rewarded_and_revocation(
    preview, monkeypatch
):
    client, factory = preview
    monkeypatch.setenv(FLAG, "true")
    complete_previous(client)
    assert start(client, 38).status_code == 403
    for n in ANSWERS:
        assert finish_new(client, n)[-1]["xp_awarded"] == 10
    initial, _, result = finish_new(client, 44)
    assert result["xp_awarded"] == 0
    cat = client.get(first.P + "/catalog", params={"grade": 2}).json()
    assert len(cat["lessons"]) == 43 and cat["book"]["source_topic_count"] == 44
    assert all(l["state"] == "completed" for l in cat["lessons"])
    assert not cat["course_ready"] and cat["source_sequence_gap_bridge"][
        "missing_source_numbers"
    ] == [25]
    assert len({l["key"] for l in cat["lessons"]}) == 43
    assert (
        cat["lessons"][-4]["source_number"] is None
        and cat["lessons"][-1]["source_number"] is None
    )
    with factory() as db:
        assert db.query(MathProgress).filter_by(user_id=1).count() == 43
        assert db.get(MathLesson, "math-2-1-26-r1") is None
        assert db.get(User, 1).xp_total == 567 and db.get(User, 1).streak_days == 3
        assert db.get(User, 2).xp_total == 0
    other = {"Authorization": "Bearer " + tokens.create_access_token(2)}
    assert (
        client.post(
            first.P + f"/attempts/{initial['attempt_id']}/complete",
            headers=other,
            json={"assessment_version": 1, "request_id": str(uuid4())},
        ).status_code
        == 404
    )
    monkeypatch.setenv(FLAG, "false")
    assert start(client, 44).status_code == 403
    assert (
        start(client, 44, request_id=initial["attempt_id"].rsplit(":", 1)[1]).json()[
            "result"
        ]
        == result
    )
