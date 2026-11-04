"""Independent literal arithmetic/source oracles for book II topics47–51."""

import pytest
import test_mathematics_part2 as earlier

from services.mathematics_curriculum import load_course
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    47: ["17", "6", "18", "b", "a", "18", "17", "14"],
    48: ["20", "2", "0", "a", "b", "20", "6", "19"],
    49: ["a", "b", ["b", "c", "a"], "c", "b", "18", "a", "c"],
    50: ["b", "9", "13", "15", "b", "8", "12", "13"],
    51: ["9", "3", "6", ["a", "b", "c"], "b", "14", "14", "b"],
}


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from earlier.preview.__wrapped__(tmp_path, monkeypatch)


def finish_new(client, number):
    # finish_second reads only this literal answer map, never private grading keys.
    with pytest.MonkeyPatch.context() as patch:
        patch.setitem(earlier.ANSWERS, number, ANSWERS[number])
        return earlier.finish_second(client, number)


def complete_first_second_batch(client):
    earlier.complete_part1(client)
    for n in range(42, 47):
        assert earlier.finish_second(client, n)[-1]["xp_awarded"] == 10


def test_ten_second_book_lessons_preserve_first_book_rewards_and_replay(preview):
    client, factory = preview
    complete_first_second_batch(client)
    for n in range(47, 52):
        assert finish_new(client, n)[-1]["xp_awarded"] == 10
    assert finish_new(client, 51)[-1]["xp_awarded"] == 0
    catalog = client.get(earlier.first.P + "/catalog", params={"part": 2}).json()
    assert [l["source_number"] for l in catalog["lessons"]] == list(range(42, 52))
    assert all(l["state"] == "completed" for l in catalog["lessons"])
    with factory() as db:
        assert db.get(User, 1).xp_total == 647 and db.get(User, 2).xp_total == 0
        assert db.query(MathProgress).count() == 51


@pytest.mark.parametrize("number", range(47, 52))
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


def test_bracket_equivalent_input_and_wrong_precedence_are_distinguished():
    lessons = {l["source_number"]: l for l in load_course() if l["part"] == 2}
    spec = lessons[50]["questions"][5]["grading"]
    assert grade_answer(spec, {"value": "15 - (3 + 4)"}) == "correct"
    assert grade_answer(spec, {"value": "15 - 3 + 4"}) == "incorrect"
    double = lessons[51]["questions"][5]["grading"]
    assert grade_answer(double, {"value": "(12 - 4)+(9-3)"}) == "correct"
    assert grade_answer(double, {"value": "14,0"}) == "correct"
