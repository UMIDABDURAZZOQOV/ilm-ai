"""Completion must cover source identities, not inflate counts with copies."""

from copy import deepcopy
import json

import pytest

from scripts.audit_biology_completion import completion_audit
from services.curriculum_validation import CATALOG_PATH, load_documents, load_lesson_set


def test_final_audit_matches_all_355_topics_51_activities_and_47_source_units():
    report = completion_audit(load_documents()[0], load_lesson_set())
    saved = json.loads(CATALOG_PATH.with_name("biology_completion_audit.json").read_text())
    assert saved == report, "Regenerate the final audit after reviewed content changes"
    assert report["complete"]
    assert report["totals"] == {
        "books": 7, "chapters": 46, "introductions": 1,
        "theory_lessons": 355, "digital_activities": 51,
        "cards": 2527, "questions": 2609,
    }
    assert len(report["chapters"]) == 47
    assert all(chapter["complete"] for chapter in report["chapters"])


def test_renaming_a_duplicate_lesson_does_not_complete_a_missing_topic():
    lessons = load_lesson_set()
    copy = deepcopy(lessons[0])
    copy["key"] = "renamed-copy-must-not-count"
    with pytest.raises(ValueError, match="duplicate_source_topic_lesson"):
        completion_audit(load_documents()[0], lessons + [copy])


@pytest.mark.parametrize("activity", [False, True])
def test_missing_final_topic_or_lab_keeps_grade_and_chapter_incomplete(activity):
    lessons = load_lesson_set()
    key = "biology-11-" + ("laboratory-5" if activity else "paragraph-44") + "-v1"
    removed = next(l for l in lessons if l["key"] == key)
    report = completion_audit(
        load_documents()[0], [l for l in lessons if l["key"] != key]
    )
    assert not report["complete"]
    assert not report["grades"][-1]["course_ready"]
    missing = [c for c in report["chapters"] if not c["complete"]]
    assert len(missing) == 1
    assert missing[0]["missing_record_ids"] == [removed["topic_id"]]
