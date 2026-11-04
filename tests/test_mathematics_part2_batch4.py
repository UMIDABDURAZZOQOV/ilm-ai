"""Independent literal arithmetic/source oracles for book II topics57–61."""

import pytest
import test_mathematics_part2 as earlier
import test_mathematics_part2_batch2 as second
import test_mathematics_part2_batch3 as previous

from services.mathematics_curriculum import load_course
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    57: ["4", "2", "6", "a", "b", "6", "9", "6"],
    58: ["4", "5", "50", "30", "b", "50", "50", "100"],
    59: ["3", "4", "41", "40", "b", "35", "30", "40"],
    60: ["40", "2", "64", "49", "b", "32", "40", "30"],
    61: ["42", "10", "60", "5", "a", "64", "34", "b"],
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
    earlier.complete_part1(client)
    for n in range(42, 47):
        assert earlier.finish_second(client, n)[-1]["xp_awarded"] == 10
    for n in range(47, 52):
        assert second.finish_new(client, n)[-1]["xp_awarded"] == 10
    for n in range(52, 57):
        assert previous.finish_new(client, n)[-1]["xp_awarded"] == 10


def test_twenty_second_book_lessons_preserve_first_book_rewards_and_replay(preview):
    client, factory = preview
    complete_previous(client)
    for n in range(57, 62):
        assert finish_new(client, n)[-1]["xp_awarded"] == 10
    assert finish_new(client, 61)[-1]["xp_awarded"] == 0
    catalog = client.get(earlier.first.P + "/catalog", params={"part": 2}).json()
    assert [l["source_number"] for l in catalog["lessons"][:20]] == list(range(42, 62))
    assert all(l["state"] == "completed" for l in catalog["lessons"][:20])
    with factory() as db:
        assert db.get(User, 1).xp_total == 747 and db.get(User, 2).xp_total == 0
        assert db.query(MathProgress).count() == 61


@pytest.mark.parametrize("number", range(57, 62))
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
