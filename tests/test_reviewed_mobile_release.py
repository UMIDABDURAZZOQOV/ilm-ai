"""Release publication on disposable reviewed fixtures; no hosted DB or OAuth."""

from uuid import uuid4

from fastapi import FastAPI
from starlette.testclient import TestClient
import pytest

from tests.test_integrated_beta import beta_api, correct_answer  # noqa: F401


@pytest.fixture
def released(beta_api, monkeypatch):  # noqa: F811
    from services.db import get_db
    from routers.reviewed_mobile import router
    from routers import (
        physics_preview,
        chemistry_preview,
        world_history_preview,
        uzbekistan_history_preview,
    )

    _, factory, account, _ = beta_api
    monkeypatch.setenv("MOBILE_REVIEWED_RELEASE", "true")
    monkeypatch.setenv(
        "MOBILE_PUBLICATION_REVIEW_REFERENCE",
        "automated technical fixture; not expert signoff",
    )
    for flag in [
        "PHYSICS_PREVIEW_ENABLED",
        "CHEMISTRY_PREVIEW_ENABLED",
        "WORLD_HISTORY_PREVIEW_ENABLED",
        "UZBEKISTAN_HISTORY_PREVIEW_ENABLED",
    ]:
        monkeypatch.setenv(flag, "false")
    app = FastAPI()
    app.include_router(router)
    for preview in [
        physics_preview,
        chemistry_preview,
        world_history_preview,
        uzbekistan_history_preview,
    ]:
        app.include_router(preview.router)

    def database():
        with factory() as db:
            yield db

    app.dependency_overrides[get_db] = database
    with TestClient(app) as client:
        client.headers["Authorization"] = "Bearer " + account["access_token"]
        yield client, factory, account


def test_release_all_five_catalogues_and_owner_scoped_engines(released):
    from services.models import StudySession

    client, factory, account = released
    response = client.get("/mobile/skills/config")
    assert response.status_code == 200, response.text
    assert response.json()["mobile_curriculum_version"] == 2
    expected = {"biologiya", "fizika", "kimyo", "ozbekiston_tarixi", "jahon_tarixi"}
    response = client.get("/mobile/skills/subjects")
    assert response.status_code == 200, response.text
    assert {s["slug"] for s in response.json() if s["available"]} == expected
    for grade in range(5, 12):
        rows = client.get("/mobile/skills/subjects", params={"grade": grade}).json()
        selected = {s["slug"]: s for s in rows if s["slug"] in expected}
        assert set(selected) == expected
        assert all(s["available"] == (grade in s["grades"]) for s in selected.values())
    for slug, grade in [
        ("fizika", 6),
        ("kimyo", 7),
        ("jahon_tarixi", 6),
        ("ozbekiston_tarixi", 7),
    ]:
        response = client.get(f"/mobile/v2/{slug}/catalog", params={"grade": grade})
        assert response.status_code == 200, response.text
        key = response.json()["lessons"][0]["key"]
        issued = client.post(
            f"/mobile/v2/{slug}/lessons/{key}/start",
            json={"assessment_version": 2, "request_id": str(uuid4())},
        )
        assert issued.status_code == 200, issued.text
        payload = issued.json()
        assert "grading_spec" not in issued.text and '"expected"' not in issued.text
        with factory() as db:
            questions = db.get(StudySession, payload["attempt_id"]).questions[
                "assessments"
            ]
        for q in questions:
            answer = client.post(
                f"/mobile/v2/{slug}/attempts/{payload['attempt_id']}/answers",
                json={
                    "assessment_version": 2,
                    "assessment_key": q["key"],
                    "answer": correct_answer(q),
                },
            )
            assert answer.status_code == 200 and answer.json()["is_correct"] is True, (
                answer.text
            )
        result = client.post(
            f"/mobile/v2/{slug}/attempts/{payload['attempt_id']}/complete",
            json={"assessment_version": 2},
        )
        assert result.status_code == 200, result.text
        assert (
            client.post(
                f"/mobile/v2/{slug}/attempts/{payload['attempt_id']}/complete",
                json={"assessment_version": 2},
            ).json()
            == result.json()
        )
    assert (
        client.get(f"/mobile/skills/{account['user_id'] + 1}/profile").status_code
        == 403
    )
    assert client.post("/beta/auth/test-login", json={}).status_code == 404


def test_release_profile_uses_reviewed_authorization_with_preview_flags_off(released):
    from services.models import User
    from routers import physics_preview

    client, factory, account = released
    with factory() as db:
        existing_xp = db.get(User, account['user_id']).xp_total
    response = client.get(f"/mobile/skills/{account['user_id']}/profile")
    assert response.status_code == 200, response.text
    profile = response.json()
    assert {s['slug'] for s in profile['subjects']} == {
        'biologiya', 'fizika', 'kimyo', 'jahon_tarixi', 'ozbekiston_tarixi'
    }
    assert profile['xp_total'] == existing_xp
    assert profile['lessons_completed'] == sum(s['completed'] for s in profile['subjects'])
    with factory() as db:
        assert db.get(User, account['user_id']).xp_total == existing_xp
    assert client.get(f"/mobile/skills/{account['user_id'] + 1}/profile").status_code == 403
    assert client.get(physics_preview.router.prefix + '/catalog', params={'grade': 6}).status_code == 404


def test_missing_approval_disabled_feature_and_prod_sqlite_fail_closed(
    released, monkeypatch
):
    client, factory, _ = released
    monkeypatch.delenv("MOBILE_PUBLICATION_REVIEW_REFERENCE")
    assert client.get("/mobile/skills/config").status_code == 503
    monkeypatch.setenv("MOBILE_PUBLICATION_REVIEW_REFERENCE", "technical fixture")
    monkeypatch.setenv("ENVIRONMENT", "production")
    response = client.get("/mobile/skills/config")
    # Both SQLite and real PostgreSQL fixtures exercise this contract. Only
    # SQLite must be denied in production mode; reviewed PostgreSQL is valid.
    with factory() as db:
        backend = db.get_bind().url.get_backend_name()
    if backend == "postgresql":
        assert response.status_code == 200, response.text
    else:
        assert response.status_code == 503, response.text
        assert response.json()["detail"] == "persistent_release_database_required"
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("MOBILE_REVIEWED_RELEASE", "false")
    assert client.get("/mobile/skills/config").status_code == 404


def test_content_and_private_grader_drift_are_rejected(released):
    from services.chemistry_models import ChemistryLesson, ChemistryAssessment
    from services.reviewed_mobile_release import validate_object
    from fastapi import HTTPException

    client, factory, _ = released
    with factory() as db:
        row = db.query(ChemistryLesson).order_by(ChemistryLesson.sequence).first()
        validate_object(row)
        original = row.title
        row.title = "unreviewed title"
        with pytest.raises(HTTPException):
            validate_object(row)
        row.title = original
        question = db.query(ChemistryAssessment).filter_by(lesson_key=row.key).first()
        validate_object(question)
        question.grading_spec = {"injected": "unreviewed"}
        with pytest.raises(HTTPException):
            validate_object(question)
        db.rollback()
    assert client.get("/mobile/skills/config").status_code == 200


def test_preview_guard_unchanged_without_release_dependency(beta_api, monkeypatch):  # noqa: F811
    from services import beta_curriculum
    from fastapi import HTTPException

    _, factory, _, _ = beta_api
    monkeypatch.setenv("PHYSICS_PREVIEW_ENABLED", "false")
    monkeypatch.setenv("MOBILE_REVIEWED_RELEASE", "true")
    with factory() as db:
        with pytest.raises(HTTPException) as failure:
            beta_curriculum.adapter(db, "fizika")
        assert failure.value.status_code == 404
