"""Mobile visibility, legacy web compatibility and preserved learner data."""

import pytest

from test_release_hardening import setup
from test_biology_segments import answers
from services.curriculum import import_curriculum, load_documents
from services.curriculum_validation import load_lesson_set
from services.models import SkillLesson, SkillQuestion, SkillSubject, SkillUnit, User
from services.models import UserStudyPreferences
from routers.mobile_skills import router


@pytest.fixture
def mobile(setup):
    client, factory = setup
    client.app.include_router(router)
    catalog, _ = load_documents()
    with factory.begin() as db:
        for lesson in load_lesson_set(batch="foundation-19"):
            import_curriculum(db, catalog, lesson)
        subject = db.query(SkillSubject).filter_by(slug="biologiya").one()
        unit = SkillUnit(subject_id=subject.id, slug="legacy-biology",
                         title_uz="Old AI biology", title_ru="Old AI biology",
                         title_en="Old AI biology", order_index=1000)
        db.add(unit)
        db.flush()
        lesson = SkillLesson(unit_id=unit.id, slug="legacy-ai",
                             title_uz="Unreviewed AI", title_ru="Unreviewed AI",
                             title_en="Unreviewed AI", order_index=1, xp_reward=20,
                             theory=[{"title": "Unreviewed AI", "body": "Must stay hidden"}])
        db.add(lesson)
        db.flush()
        db.add(SkillQuestion(lesson_id=lesson.id, question_text="Unreviewed AI",
                             language="uz", options=["yes", "no"], correct_answer="yes", order_index=1))
        db.get(User, 1).xp_total = 137
        legacy = lesson.id
    return client, factory, legacy


def test_only_reviewed_biology_is_mobile_published_and_web_catalogue_is_unchanged(mobile):
    client, factory, _ = mobile
    mobile_rows = client.get("/mobile/skills/subjects")
    assert mobile_rows.status_code == 200, mobile_rows.text
    assert [s["slug"] for s in mobile_rows.json()] == ["biologiya"]
    assert mobile_rows.json()[0]["ready_lessons"] == 19
    assert {s["slug"] for s in client.get("/skills/subjects").json()} == {"math", "biologiya"}
    assert client.get("/mobile/skills/1/summary").json()["xp_total"] == 137
    with factory() as db:
        assert db.get(User, 1).xp_total == 137
        assert db.query(SkillSubject).count() == 2


@pytest.mark.parametrize("route", [
    "/1/tree?subject=math&grade=5", "/subjects/math/grades",
    "/1/curriculum?subject=math&grade=5", "/1/marathon?subject=math",
    "/1/unit-exam?unit_id=1", "/1/level-test?subject=biologiya",
])
def test_hidden_subjects_and_unreviewed_placement_cannot_be_opened_directly(mobile, route):
    client, _, _ = mobile
    assert client.get("/mobile/skills" + route).status_code == 404


def test_legacy_ai_biology_lesson_and_grade_less_path_are_hidden(mobile):
    client, _, legacy = mobile
    for lid in (1, legacy):
        response = client.post(f"/mobile/skills/lessons/{lid}/start", json={"user_id": 1})
        assert response.status_code == 404, response.text
    assert client.get("/mobile/skills/1/tree?subject=biologiya").status_code == 422
    tree = client.get("/mobile/skills/1/tree?subject=biologiya&grade=5").json()
    assert all(l["id"] != legacy for u in tree["units"] for l in u["lessons"])
    outline = client.get("/mobile/skills/1/curriculum?subject=biologiya&grade=5").json()
    assert len(outline["chapters"]) == 3
    assert not outline["completed"]


@pytest.mark.parametrize("kind", ["daily-challenge", "lightning", "mistakes", "mixed-review"])
def test_practice_pools_never_return_hidden_questions_even_in_english_ui(mobile, kind):
    client, _, _ = mobile
    result = client.get(f"/mobile/skills/1/{kind}?language=en")
    assert result.status_code == 200, result.text
    for question in result.json()["questions"]:
        assert question["source"]["book_id"].startswith("biology-")
        assert question["question_text"] != "Unreviewed AI"
        assert question["question_text"] != "Test fixture"


def test_missing_import_is_an_explicit_503_not_a_fake_or_empty_course(setup):
    client, _ = setup
    client.app.include_router(router)
    response = client.get("/mobile/skills/subjects")
    assert response.status_code == 503
    assert response.json()["detail"] == "mobile_curriculum_not_imported"
    assert [r["slug"] for r in client.get("/skills/subjects").json()] == ["math"]


def test_mobile_daily_has_own_snapshot_but_shared_once_only_account_reward(mobile):
    client, factory, _ = mobile
    web = client.get("/skills/1/daily-challenge").json()
    issued = client.get("/mobile/skills/1/daily-challenge").json()
    assert issued["attempt_id"].startswith("mobile:daily:")
    assert issued["attempt_id"] != web["attempt_id"]
    body = {"user_id": 1, "attempt_id": issued["attempt_id"], "results": answers(issued)}
    result = client.post("/mobile/skills/daily-challenge/complete", json=body)
    assert result.status_code == 200, result.text
    assert client.post("/mobile/skills/daily-challenge/complete", json=body).json() == result.json()
    assert client.get("/skills/1/daily-challenge").json()["completed"]
    with factory() as db:
        assert db.get(User, 1).xp_total == 137 + result.json()["xp_awarded"]


def test_configuration_can_hide_without_deleting_any_subject(mobile, monkeypatch):
    client, factory, _ = mobile
    monkeypatch.setenv("MOBILE_PUBLISHED_SUBJECTS", "")
    assert client.get("/mobile/skills/subjects").json() == []
    with factory() as db:
        assert db.query(SkillSubject).count() == 2


def test_old_preferences_are_hidden_in_get_and_post_responses_but_not_erased(mobile):
    client, factory, _ = mobile
    with factory.begin() as db:
        db.add(UserStudyPreferences(user_id=1, subject="math", grade="1", daily_goal_xp=20))
    for response in [
        client.get("/mobile/skills/1/preferences"),
        client.post("/mobile/skills/1/preferences", json={"daily_goal_xp": 30}),
    ]:
        assert response.status_code == 200, response.text
        assert "subject" not in response.json()["preferences"]
        assert "grade" not in response.json()["preferences"]
    with factory() as db:
        old = db.get(UserStudyPreferences, 1)
        assert old.subject == "math" and old.grade == "1" and old.daily_goal_xp == 30


def test_complete_all_406_mobile_lessons_and_47_checkpoints(setup, tmp_path):
    from test_biology_continuation import test_complete_grades5_to11_api_once_only_xp as exercise
    client, factory = setup
    client.app.include_router(router)

    class MobileClient:
        def get(self, path, **kwargs):
            return client.get("/mobile" + path, **kwargs)

        def post(self, path, **kwargs):
            return client.post("/mobile" + path, **kwargs)

    exercise((MobileClient(), factory), tmp_path)
