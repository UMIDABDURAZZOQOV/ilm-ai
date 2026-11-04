"""Independent literal arithmetic/source oracles for book II topics69–73."""

import pytest
import test_mathematics_part2 as earlier
import test_mathematics_part2_batch5 as previous

from services.mathematics_curriculum import load_course
from services.mathematics_grading import grade_answer
from services.mathematics_models import MathProgress
from services.models import User

ANSWERS = {
    69: ["64", "43", "21", "b", "a", "23", "100", ["b", "a", "c"]],
    70: ["3", "2", "35", "49", "b", "48", "25", "49"],
    71: ["17", "8", "20", "a", "b", "19", "57", ["b", "a", "c"]],
    72: ["17", "39", "26", "58", "b", "32", "5", "38"],
    73: ["a", "33", "21", "63", "b", "30", "40", "b"],
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
    for n in range(62, 69):
        assert previous.finish_new(client, n)[-1]["xp_awarded"] == 10


def test_all_thirty_two_available_second_book_lessons_preserve_first_book_rewards_and_replay(
    preview,
):
    client, factory = preview
    complete_previous(client)
    for n in range(69, 74):
        assert finish_new(client, n)[-1]["xp_awarded"] == 10
    assert finish_new(client, 73)[-1]["xp_awarded"] == 0
    catalog = client.get(earlier.first.P + "/catalog", params={"part": 2}).json()
    assert catalog["book"]["implemented_sections"] == 32
    assert catalog["book"]["source_topic_count"] == 33
    assert catalog["book"]["source_gaps"][0]["topic_source_number"] == 74
    assert not catalog["course_ready"]
    assert [l["source_number"] for l in catalog["lessons"][:32]] == list(range(42, 74))
    assert all(l["state"] == "completed" for l in catalog["lessons"][:32])
    with factory() as db:
        assert db.get(User, 1).xp_total == 867 and db.get(User, 2).xp_total == 0
        assert db.query(MathProgress).count() == 73
        from services.mathematics_runtime import previous_book_complete

        completed = {p.lesson_key for p in db.query(MathProgress).filter_by(user_id=1)}
        assert not previous_book_complete(db, completed, 1, 3)


@pytest.mark.parametrize("number", range(69, 74))
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
