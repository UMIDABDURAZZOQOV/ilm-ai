"""Whole-course local QA: source coverage is separate from publication approval."""

from copy import deepcopy

import pytest
import test_uzbekistan_history_course as g7
import test_uzbekistan_history_grade8 as g8
import test_uzbekistan_history_grade9 as g9
import test_uzbekistan_history_grade10 as g10
import test_uzbekistan_history_grade11 as g11
from fastapi.testclient import TestClient

from services import uzbekistan_history_runtime as runtime
from services.models import StudyEvent, User
from services.study import utcnow
from services.uzbekistan_history_models import (
    HistoryAssessment,
    HistoryLesson,
    HistoryProgress,
)
from services.uzbekistan_history_validation import load_course


@pytest.fixture
def preview(tmp_path, monkeypatch):
    yield from g7.preview.__wrapped__(tmp_path, monkeypatch)


def test_all_172_lessons_one_account_sources_xp_replay_reopen_and_legacy_balance(
    preview, monkeypatch
):
    client, factory = preview
    expected = {7: 42, 8: 41, 9: 39, 10: 28, 11: 22}
    documents = load_course()
    grouped = {
        g: [l for d in documents if d["grade"] == g for l in d["lessons"]]
        for g in expected
    }
    assert {g: len(ls) for g, ls in grouped.items()} == expected
    assert sum(len(l["assessments"]) for ls in grouped.values() for l in ls) == 1027
    now = utcnow()
    monkeypatch.setattr(runtime, "utcnow", lambda: now)
    # The account already studied today: History must preserve this existing streak.
    with factory.begin() as db:
        db.get(User, 1).last_study_date = now.date().isoformat()
    for grade, lessons in grouped.items():
        cat = client.get(g7.P + f"/catalog?grade={grade}").json()
        assert cat["course_content_complete"] and cat["grade_content_complete"]
        assert not cat["course_complete"] and not cat["course_ready"]
        assert (
            cat["independent_review_pending"]
            and cat["publication"] == "local_test_preview_only"
        )
        for lesson in lessons:
            if grade == 7:
                _, result = g7.complete_lesson(client, lesson)
            elif grade == 8:
                _, result = g8.finish(client, lesson)
            else:
                result = {9: g9, 10: g10, 11: g11}[grade].finish(client, lesson)
            assert result["score_pct"] == 100 and result["xp_awarded"] == 10
            assert result["streak_days"] == 3
    with factory() as db:
        rows = db.query(HistoryProgress).filter_by(user_id=1).all()
        assert len(rows) == 172
        assert all(
            r.completed_at is not None and r.xp_earned == 10 and r.best_score_pct == 100
            for r in rows
        )
        assert db.get(User, 1).xp_total == 1857
        assert db.get(User, 1).streak_days == 3
        assert db.get(User, 2).xp_total == 0
        ledger = db.query(StudyEvent).filter_by(user_id=1, kind=runtime.KIND).all()
        assert len(ledger) == 172 and sum(e.xp for e in ledger) == 1720
    with TestClient(
        client.app, headers={"Authorization": client.headers["Authorization"]}
    ) as reopened:
        chapters = 0
        for grade, count in expected.items():
            cat = reopened.get(g7.P + f"/catalog?grade={grade}").json()
            assert len(cat["lessons"]) == count
            assert all(l["state"] == "completed" for l in cat["lessons"])
            assert all(c["checkpoint_state"] == "completed" for c in cat["chapters"])
            assert cat["course_content_complete"] and not cat["course_ready"]
            chapters += len(cat["chapters"])
        assert chapters == 34
        assert g11.finish(reopened, grouped[11][-1])["xp_awarded"] == 0
    with factory() as db:
        assert db.get(User, 1).xp_total == 1857
        assert (
            sum(
                e.xp
                for e in db.query(StudyEvent).filter_by(user_id=1, kind=runtime.KIND)
            )
            == 1720
        )


def test_coverage_flag_detects_missing_import_without_claiming_publication(preview):
    client, factory = preview
    assert client.get(g7.P + "/catalog?grade=11").json()["course_content_complete"]
    # Owned disposable test DB only, simulating an incomplete import.
    with factory.begin() as db:
        db.query(HistoryAssessment).filter_by(lesson_key="uzh-8-41-r1").delete()
        db.query(HistoryLesson).filter_by(key="uzh-8-41-r1").delete()
    cat = client.get(g7.P + "/catalog?grade=11").json()
    assert cat["grade_content_complete"] and not cat["course_content_complete"]
    assert not cat["course_complete"] and not cat["course_ready"]
    assert not client.get(g7.P + "/catalog?grade=8").json()["grade_content_complete"]
    with factory() as db:
        assert db.get(User, 1).xp_total == 137


def test_missing_source_never_reports_full_coverage(preview, monkeypatch):
    source = deepcopy(runtime.load_catalog())
    source["books"] = [b for b in source["books"] if b["grade"] != 8]
    source["blocked_books"] = [{"grade": 8}]
    monkeypatch.setattr(runtime, "load_catalog", lambda: source)
    client, _ = preview
    for grade in [7, 8, 11]:
        cat = client.get(g7.P + f"/catalog?grade={grade}").json()
        assert not cat["course_content_complete"] and not cat["course_ready"]
