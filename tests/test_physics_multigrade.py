"""Grade identity is explicit before any new grade content is imported."""

from copy import deepcopy

import pytest
from test_physics_course import NUMERIC_ORACLES, new_answer
from test_physics_v2 import PREFIX
from test_physics_v2 import preview as preview  # noqa: PLC0414
from test_release_hardening import setup as setup  # noqa: PLC0414

from services.physics_curriculum import load_batch, public_book


def test_numeric_oracle_does_not_fall_back_to_another_grade(monkeypatch):
    lesson = deepcopy(load_batch("grade6_batch2")["lessons"][1])
    q = lesson["assessments"][5]
    old = new_answer(lesson, q)
    lesson["topic_id"] = "physics-8-section-9"
    with pytest.raises(KeyError):
        new_answer(lesson, q)
    monkeypatch.setitem(NUMERIC_ORACLES, (8, 9, 6), ("123", "m", "s"))
    assert new_answer(lesson, q) == {"value": "123", "unit": "m", "formula": "s"}
    assert old["value"] == "0.0000000003"


@pytest.mark.parametrize("grade", range(6, 12))
def test_public_bibliography_is_source_catalogue_metadata_only(grade):
    book = public_book(grade)
    assert set(book) == {"id", "grade", "title", "authors", "publisher", "year"}
    assert book["grade"] == grade and book["authors"] and book["year"]
    if grade == 7:
        assert book["authors"][0] == "P. Q. Habibullayev"


def test_catalog_grade_default_and_explicit_metadata_do_not_unlock_missing_grade(
    preview,
):
    client, _ = preview
    default = client.get(f"{PREFIX}/catalog").json()
    assert default["grade"] == default["book"]["grade"] == 6
    other = client.get(f"{PREFIX}/catalog?grade=7").json()
    assert other["grade"] == other["book"]["grade"] == 7
    assert other["book"]["authors"][0] == "P. Q. Habibullayev"
    assert other["lessons"] == [] and not other["grade_content_complete"]
    assert other["available_grades"] == [6]
    assert not other["course_complete"]
