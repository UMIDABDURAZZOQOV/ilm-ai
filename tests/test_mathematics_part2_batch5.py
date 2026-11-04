"""Independent literal arithmetic/source oracles for book II topics62–68."""

import pytest
import test_mathematics_part2 as earlier
import test_mathematics_part2_batch4 as previous

from services.mathematics_curriculum import load_course
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    62: ["a", "b", "c", ["b", "a", "c"], "b", "76", "a", "79"],
    63: ["9", "5", "59", "a", "b", "58", "64", "60"],
    64: ["13", "24", "37", ["b", "c", "a"], "a", "77", "39", "1"],
    65: ["37", "46", "53", "3", "b", "33", "8", "c"],
    66: ["86", "2", "5", "52", "a", "52", "4", "55"],
    67: ["2", "50", "52", "64", "b", "62", "24", "13"],
    68: ["33", "68", "45", "23", "a", "45", "0", "70"],
}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from earlier.preview.__wrapped__(tmp_path, monkeypatch)


def finish_new(client, number):
    # finish_second reads only this literal answer map, never private grading keys.
    with pytest.MonkeyPatch.context() as patch:
        patch.setitem(earlier.ANSWERS, number, ANSWERS[number])
        return earlier.finish_second(client, number)


def complete_previous(client):
    previous.complete_previous(client)
    for n in range(57, 62):
        assert previous.finish_new(client, n)[-1]["xp_awarded"] == 10


def test_twenty_seven_second_book_lessons_preserve_first_book_rewards_and_replay(
    preview,
):
    client, factory = preview
    complete_previous(client)
    for n in range(62, 69):
        assert finish_new(client, n)[-1]["xp_awarded"] == 10
    assert finish_new(client, 68)[-1]["xp_awarded"] == 0
    catalog = client.get(earlier.first.P + "/catalog", params={"part": 2}).json()
    assert [l["source_number"] for l in catalog["lessons"][:27]] == list(range(42, 69))
    assert all(l["state"] == "completed" for l in catalog["lessons"][:27])
    with factory() as db:
        assert db.get(User, 1).xp_total == 817 and db.get(User, 2).xp_total == 0
        assert db.query(MathProgress).count() == 68


@pytest.mark.parametrize("number", range(62, 69))
def test_all_literal_answers_and_wrong_alternatives(number):
    lesson = next(l for l in load_course() if l["key"] == f"math-1-2-{number - 41}-r1")
    assert lesson["source_refs"][0]["pdf_pages"] == [2 * number - 79, 2 * number - 78]
    assert lesson["source_refs"][0]["printed_pages"] == [
        2 * number - 80,
        2 * number - 79,
    ]
    assert len(lesson["questions"]) == len(ANSWERS[number]) == 8
    for q, value in zip(lesson["questions"], ANSWERS[number]):
        kind = q["public"]["response_kind"]
        field = {"choice": "choice_id", "ordering": "order"}.get(kind, "value")
        assert grade_answer(q["grading"], {field: value}) == "correct"
        if kind == "exact_number":
            wrong = str(int(value) + 1)
        elif kind == "ordering":
            wrong = list(reversed(value))
        else:
            wrong = next(c["id"] for c in q["public"]["choices"] if c["id"] != value)
        assert grade_answer(q["grading"], {field: wrong}) == "incorrect"
