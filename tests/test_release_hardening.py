"""Regression tests use a disposable database, never application/user data."""

import hashlib
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from routers import auth, notifications, skills
from services import db as database, mobile_oauth, tokens, users
from services.models import (
    SkillLesson,
    SkillQuestion,
    SkillSubject,
    SkillUnit,
    StudyEvent,
    StudySession,
    User,
    UserLessonProgress,
    SkillMistake,
    UserUnitExam,
)
from services.study import utcnow


@pytest.fixture
def setup(tmp_path, monkeypatch):
    engine = create_engine(
        f"sqlite:///{tmp_path / 'study.db'}",
        connect_args={"check_same_thread": False, "timeout": 30},
    )

    @event.listens_for(engine, "connect")
    def foreign_keys(conn, _):
        conn.execute("PRAGMA foreign_keys=ON")

    database.Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    for module in (database, mobile_oauth, tokens, users):
        monkeypatch.setattr(module, "SessionLocal", factory)
    monkeypatch.setattr(
        tokens, "JWT_SECRET", "release-tests-only-secret-at-least-32-characters"
    )
    monkeypatch.setattr(users, "USE_DB", True)
    monkeypatch.setattr(tokens, "USE_DB", True)
    with factory() as db:
        db.add_all(
            [
                User(
                    id=i,
                    name=f"Learner {i}",
                    email=f"learner{i}@example.test",
                    xp_total=0,
                )
                for i in (1, 2)
            ]
        )
        db.add(
            SkillSubject(
                id=1,
                slug="math",
                name_uz="Math",
                name_ru="Math",
                name_en="Math",
                is_active=True,
            )
        )
        db.flush()
        db.add_all(
            [
                SkillUnit(
                    id=i,
                    subject_id=1,
                    slug=f"unit{i}",
                    title_uz="Unit",
                    title_ru="Unit",
                    title_en="Unit",
                    order_index=i,
                )
                for i in (1, 2)
            ]
        )
        db.flush()
        db.add_all(
            [
                SkillLesson(
                    id=i,
                    unit_id=1 if i < 3 else 2,
                    slug=f"lesson{i}",
                    title_uz="Lesson",
                    title_ru="Lesson",
                    title_en="Lesson",
                    order_index=i,
                    xp_reward=20,
                )
                for i in (1, 2, 3)
            ]
        )
        db.flush()
        db.add_all(
            [
                SkillQuestion(
                    id=i * 10 + j,
                    lesson_id=i,
                    question_text="Test fixture",
                    language="uz",
                    options=["a", "b"],
                    correct_answer="a",
                    order_index=j,
                )
                for i in (1, 2, 3)
                for j in (0, 1)
            ]
        )
        db.commit()
    app = FastAPI()
    app.include_router(skills.router)
    app.include_router(auth.router)
    app.include_router(notifications.router)

    def get_db():
        with factory() as db:
            try:
                yield db
            except Exception:
                db.rollback()
                raise

    app.dependency_overrides[database.get_db] = get_db
    with TestClient(
        app, headers={"Authorization": f"Bearer {tokens.create_access_token(1)}"}
    ) as client:
        yield client, factory
    engine.dispose()


def answers(questions, *, correct=True):
    return [
        {
            "question_id": q["id"],
            "answer_index": q["options"].index(q["correct_answer"]) if correct else 1,
            "is_correct": not correct,
        }
        for q in questions
    ]


def start(client, lesson=1):
    r = client.post(f"/skills/lessons/{lesson}/start", json={"user_id": 1})
    assert r.status_code == 200
    return r.json()


def finish(client, issued, lesson=1, results=None):
    return client.post(
        f"/skills/lessons/{lesson}/complete",
        json={
            "user_id": 1,
            "attempt_id": issued["attempt_id"],
            "results": results if results is not None else answers(issued["questions"]),
        },
    )


def test_server_grades_answers_and_replays_exact_response(setup):
    client, factory = setup
    issued = start(client)
    r = finish(client, issued)
    assert r.status_code == 200
    assert r.json()["score"] == 2  # submitted is_correct=False is ignored
    assert r.json()["xp_awarded"] == 20
    assert r.json()["newly_unlocked_lesson_ids"] == [2]
    assert finish(client, issued).json() == r.json()
    with factory() as db:
        assert db.get(User, 1).xp_total == 20
        assert db.query(StudyEvent).count() == 1


@pytest.mark.parametrize(
    "variant", ["booleans", "duplicate", "foreign", "incomplete", "invalid_index"]
)
def test_invalid_answer_sets_cannot_award_xp(setup, variant):
    client, factory = setup
    issued = start(client)
    rows = answers(issued["questions"])
    if variant == "booleans":
        rows = [
            {"question_id": q["id"], "is_correct": True} for q in issued["questions"]
        ]
    elif variant == "duplicate":
        rows[1] = rows[0]
    elif variant == "foreign":
        rows[1]["question_id"] = 20
    elif variant == "incomplete":
        rows.pop()
    else:
        rows[0]["answer_index"] = 9
    assert finish(client, issued, results=rows).status_code == 422
    with factory() as db:
        assert db.get(User, 1).xp_total == 0
        assert db.query(StudyEvent).count() == 0


def test_client_cannot_claim_correct_for_wrong_answers(setup):
    client, _ = setup
    issued = start(client)
    response = finish(
        client, issued, results=answers(issued["questions"], correct=False)
    )
    assert response.status_code == 200
    assert response.json()["score"] == 0
    assert response.json()["passed"] is False
    assert (
        client.post("/skills/lessons/2/start", json={"user_id": 1}).status_code == 403
    )


def test_checkpoint_gate_matches_tree_and_start_api(setup):
    client, _ = setup
    finish(client, start(client))
    finish(client, start(client, 2), 2)
    tree = client.get("/skills/1/tree?subject=math").json()
    assert tree["units"][0]["exam"]["status"] == "unlocked"
    assert tree["units"][1]["lessons"][0]["status"] == "locked"
    assert (
        client.post("/skills/lessons/3/start", json={"user_id": 1}).status_code == 403
    )
    issued = client.get("/skills/1/unit-exam?unit_id=1").json()
    data = {
        "user_id": 1,
        "unit_id": 1,
        "attempt_id": issued["attempt_id"],
        "results": answers(issued["questions"]),
    }
    first = client.post("/skills/unit-exam/complete", json=data)
    assert first.status_code == 200
    assert first.json()["xp_awarded"] == 50
    assert client.post("/skills/unit-exam/complete", json=data).json() == first.json()
    assert (
        client.post("/skills/lessons/3/start", json={"user_id": 1}).status_code == 200
    )


def test_checkpoint_post_cannot_bypass_prerequisites(setup):
    client, factory = setup
    from services.study import issue

    with factory() as db:
        issue(
            db,
            1,
            "checkpoint",
            "1",
            [{"id": 10, "options": ["a", "b"], "correct_answer": "a"}],
            "known",
        )
    response = client.post(
        "/skills/unit-exam/complete",
        json={
            "user_id": 1,
            "unit_id": 1,
            "attempt_id": "known",
            "results": [{"question_id": 10, "user_answer": "a"}],
        },
    )
    assert response.status_code == 403
    with factory() as db:
        assert db.query(UserUnitExam).count() == 0


@pytest.mark.parametrize("kind", ["daily-challenge", "lightning", "mistakes"])
def test_practice_retry_does_not_duplicate_xp_or_srs(setup, kind):
    client, factory = setup
    if kind == "mistakes":
        with factory() as db:
            db.add(
                SkillMistake(
                    user_id=1,
                    question_id=10,
                    due_at=utcnow() - timedelta(days=1),
                    review_stage=0,
                )
            )
            db.commit()
    issued = client.get(f"/skills/1/{kind}").json()
    data = {
        "user_id": 1,
        "attempt_id": issued["attempt_id"],
        "results": answers(issued["questions"]),
    }
    r = client.post(f"/skills/{kind}/complete", json=data)
    assert r.status_code == 200
    assert client.post(f"/skills/{kind}/complete", json=data).json() == r.json()
    with factory() as db:
        assert db.get(User, 1).xp_total == r.json()["xp_awarded"]
        assert db.query(StudyEvent).count() == 1
        if kind == "mistakes":
            assert db.query(SkillMistake).first().review_stage == 1
    summary = client.get("/skills/1/summary").json()
    profile = client.get("/skills/1/profile").json()
    league = client.get("/skills/1/league").json()
    assert summary["today_xp"] == league["weekly_xp"] == r.json()["xp_awarded"]
    assert sum(profile["activity"].values()) == 1


def test_foreign_user_cannot_complete_issued_attempt(setup):
    client, _ = setup
    issued = start(client)
    response = client.post(
        "/skills/lessons/1/complete",
        json={
            "user_id": 2,
            "attempt_id": issued["attempt_id"],
            "results": answers(issued["questions"]),
        },
    )
    assert response.status_code == 403


def test_parallel_retries_award_once(setup):
    client, factory = setup
    issued = start(client)
    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(lambda _: finish(client, issued), range(2)))
    assert all(r.status_code == 200 for r in responses)
    assert responses[0].json() == responses[1].json()
    with factory() as db:
        assert db.get(User, 1).xp_total == 20


def test_pkce_code_is_bound_expiring_and_one_use(setup):
    client, factory = setup
    verifier = "a" * 64
    code = mobile_oauth.issue_grant(1, mobile_oauth.pkce_challenge(verifier))
    assert (
        client.post(
            "/auth/mobile/exchange", json={"code": code, "code_verifier": "b" * 64}
        ).status_code
        == 400
    )
    response = client.post(
        "/auth/mobile/exchange", json={"code": code, "code_verifier": verifier}
    )
    assert response.status_code == 200
    assert response.json()["needs_onboarding"] is True
    assert (
        client.post(
            "/auth/mobile/exchange", json={"code": code, "code_verifier": verifier}
        ).status_code
        == 400
    )
    from services.models import MobileLoginGrant

    expired = mobile_oauth.issue_grant(1, mobile_oauth.pkce_challenge(verifier))
    with factory() as db:
        db.get(
            MobileLoginGrant, hashlib.sha256(expired.encode()).hexdigest()
        ).expires_at = utcnow() - timedelta(seconds=1)
        db.commit()
    assert (
        client.post(
            "/auth/mobile/exchange", json={"code": expired, "code_verifier": verifier}
        ).status_code
        == 400
    )


def test_oauth_state_rejects_replay_wrong_redirect_and_expiry(setup):
    mobile_oauth.save_state("test-state", "https://example.test/callback", "a" * 43)
    with pytest.raises(Exception):
        mobile_oauth.consume_state("test-state", "https://attacker.test/callback")
    assert (
        mobile_oauth.consume_state("test-state", "https://example.test/callback")
        == "a" * 43
    )
    with pytest.raises(Exception):
        mobile_oauth.consume_state("test-state", "https://example.test/callback")


def test_refresh_rotation_consumes_old_token(setup):
    client, _ = setup
    token = tokens.create_refresh_token(1)
    first = client.post("/auth/refresh", json={"refresh_token": token})
    assert first.status_code == 200
    assert (
        client.post("/auth/refresh", json={"refresh_token": token}).status_code == 401
    )
    replacement = first.json()["refresh_token"]
    assert (
        client.post("/auth/logout", json={"refresh_token": replacement}).status_code
        == 200
    )
    assert (
        client.post("/auth/refresh", json={"refresh_token": replacement}).status_code
        == 401
    )


def test_push_binding_moves_between_accounts_and_unbind_is_conditional(setup):
    client, factory = setup
    assert (
        client.post(
            "/notifications/register-token", json={"user_id": 1, "token": "test-device"}
        ).status_code
        == 200
    )
    client.headers["Authorization"] = f"Bearer {tokens.create_access_token(2)}"
    assert (
        client.post(
            "/notifications/register-token", json={"user_id": 2, "token": "test-device"}
        ).status_code
        == 200
    )
    with factory() as db:
        assert db.get(User, 1).push_token is None
        assert db.get(User, 2).push_token == "test-device"
    client.post(
        "/notifications/unregister-token", json={"user_id": 2, "token": "old-device"}
    )
    with factory() as db:
        assert db.get(User, 2).push_token == "test-device"


def test_mobile_callback_never_places_credentials_in_uri(setup, monkeypatch):
    client, _ = setup
    monkeypatch.setattr(auth, "is_google_oauth_enabled", lambda: True)

    async def callback(*args, **kwargs):
        assert kwargs["mobile"] is True
        return {
            "code": "one-use-code",
            "access_token": "must-not-leak",
            "refresh_token": "must-not-leak",
        }

    monkeypatch.setattr(auth, "handle_google_callback", callback)
    response = client.get(
        "/auth/google-callback-mobile?code=google-code&state=state",
        follow_redirects=False,
    )
    assert response.status_code == 307
    assert (
        response.headers["location"]
        == "ilmai://auth/callback?code=one-use-code&state=state"
    )

    async def failure(*args, **kwargs):
        from fastapi import HTTPException

        raise HTTPException(400, "private-provider-detail")

    monkeypatch.setattr(auth, "handle_google_callback", failure)
    response = client.get(
        "/auth/google-callback-mobile?code=x&state=state", follow_redirects=False
    )
    assert "error=oauth_failed" in response.headers["location"]
    assert "private-provider-detail" not in response.headers["location"]


@pytest.mark.parametrize("bad", [True, 0.5, "0"])
def test_answer_indices_are_strict_integers(setup, bad):
    client, _ = setup
    issued = start(client)
    rows = answers(issued["questions"])
    rows[0]["answer_index"] = bad
    assert finish(client, issued, results=rows).status_code == 422


def test_changed_replay_is_rejected_without_side_effects(setup):
    client, factory = setup
    issued = start(client)
    assert finish(client, issued).status_code == 200
    assert (
        finish(
            client, issued, results=answers(issued["questions"], correct=False)
        ).status_code
        == 409
    )
    with factory() as db:
        assert db.get(User, 1).xp_total == 20
        assert db.query(StudyEvent).count() == 1


def test_repeated_daily_issue_preserves_snapshot(setup):
    client, _ = setup
    issued = client.get("/skills/1/daily-challenge").json()
    again = client.get("/skills/1/daily-challenge").json()
    assert issued["questions"] == again["questions"]
    assert issued["attempt_id"] == again["attempt_id"]


def test_profile_additive_user_id_and_no_password(setup):
    client, _ = setup
    profile = client.get("/auth/profile/1").json()
    assert profile["id"] == profile["user_id"] == 1
    assert "password" not in profile


def test_account_preferences_are_validated_and_used_in_summary(setup):
    client, _ = setup
    assert client.get("/skills/1/preferences").json()["preferences"] is None
    data = {"daily_goal_xp": 30, "subject": "math", "grade": "2", "level": 1}
    assert client.post("/skills/1/preferences", json=data).status_code == 200
    assert client.get("/skills/1/preferences").json()["preferences"]["grade"] == "2"
    assert client.get("/skills/1/summary").json()["daily_goal_xp"] == 30
    assert (
        client.post("/skills/1/preferences", json={"daily_goal_xp": 999}).status_code
        == 422
    )
    assert client.post("/skills/2/preferences", json=data).status_code == 403


def test_subject_exam_uses_actual_answers_and_retries_once(setup):
    client, factory = setup
    issued = client.get("/skills/1/subject-exam?subject=math").json()
    payload = {
        "user_id": 1,
        "subject": "math",
        "score": 999,
        "total": 999,
        "attempt_id": issued["attempt_id"],
        "results": answers(issued["questions"], correct=False),
    }
    response = client.post("/skills/subject-exam/complete", json=payload)
    assert response.status_code == 200
    assert response.json()["score"] == response.json()["xp_awarded"] == 0
    assert (
        client.post("/skills/subject-exam/complete", json=payload).json()
        == response.json()
    )
    with factory() as db:
        assert db.get(User, 1).xp_total == 0
        assert db.query(StudyEvent).count() == 1


def test_schema_is_additive_and_ddl_compiles_for_postgres(setup):
    from sqlalchemy import inspect
    from sqlalchemy.schema import CreateTable
    from sqlalchemy.dialects import postgresql

    client, factory = setup
    with factory() as db:
        existing = db.get(User, 1)
        existing.name = "Preserved learner"
        db.commit()
        database.Base.metadata.create_all(db.bind)
        assert db.get(User, 1).name == "Preserved learner"
        expected = {
            "study_sessions",
            "study_events",
            "oauth_states",
            "mobile_login_grants",
            "user_study_preferences",
        }
        assert expected.issubset(set(inspect(db.bind).get_table_names()))
    for name in expected:
        ddl = str(
            CreateTable(database.Base.metadata.tables[name]).compile(
                dialect=postgresql.dialect()
            )
        )
        assert "CREATE TABLE" in ddl
        assert "DROP" not in ddl


def test_failed_transaction_can_retry_without_partial_xp(setup, monkeypatch):
    client, factory = setup
    issued = start(client)
    from services import study

    real_activity = study.record_activity

    def fail(*args):
        raise RuntimeError("simulated transaction interruption")

    monkeypatch.setattr(study, "record_activity", fail)
    with pytest.raises(RuntimeError):
        finish(client, issued)
    with factory() as db:
        assert db.get(User, 1).xp_total == 0
        assert db.query(StudyEvent).count() == 0
        assert db.query(UserLessonProgress).count() == 0
    monkeypatch.setattr(study, "record_activity", real_activity)
    assert finish(client, issued).json()["xp_awarded"] == 20


def test_streak_and_legacy_history_survive_new_ledger(setup):
    client, factory = setup
    from services.models import SkillLessonAttempt
    from services.study import effective_streak

    now = utcnow()
    with factory() as db:
        user = db.get(User, 1)
        user.streak_days = 7
        user.last_study_date = (now.date() - timedelta(days=3)).isoformat()
        db.add(
            SkillLessonAttempt(
                user_id=1, lesson_id=1, started_at=now, completed_at=now, xp_awarded=9
            )
        )
        db.commit()
        assert effective_streak(db, user) == 0
    assert client.get("/skills/1/summary").json()["today_xp"] == 9
    finish(client, start(client))
    summary = client.get("/skills/1/summary").json()
    assert summary["today_xp"] == 29
    assert summary["streak_days"] == 1


def test_google_rejects_unverified_email_before_linking_account(setup, monkeypatch):
    client, _ = setup
    from services import google_oauth

    monkeypatch.setattr(
        auth, "handle_google_callback", google_oauth.handle_google_callback
    )
    monkeypatch.setattr(auth, "is_google_oauth_enabled", lambda: True)
    monkeypatch.setattr(google_oauth, "is_google_oauth_enabled", lambda: True)

    class Response:
        status_code = 200

        def __init__(self, data):
            self.data = data

        def json(self):
            return self.data

    monkeypatch.setattr(
        google_oauth.requests,
        "post",
        lambda *a, **kw: Response({"access_token": "test-provider-token"}),
    )
    monkeypatch.setattr(
        google_oauth.requests,
        "get",
        lambda *a, **kw: Response(
            {
                "email": "learner1@example.test",
                "email_verified": False,
                "sub": "test-provider-sub",
            }
        ),
    )
    mobile_oauth.save_state(
        "unverified-state", "http://testserver/auth/google-callback-mobile", "a" * 43
    )
    response = client.get(
        "/auth/google-callback-mobile?code=x&state=unverified-state",
        follow_redirects=False,
    )
    assert "error=oauth_failed" in response.headers["location"]


def test_password_hashes_are_salted_and_legacy_accounts_still_work(setup):
    _, factory = setup
    first = users.hash_password("test-password-only")
    second = users.hash_password("test-password-only")
    assert first != second
    assert users.password_matches("test-password-only", first)
    assert not users.password_matches("wrong", first)
    assert not users.password_matches("anything", None)
    legacy = hashlib.sha256(b"legacy-test-only").hexdigest()
    with factory() as db:
        db.get(User, 1).password = legacy
        db.commit()
    assert users.verify_login("learner1@example.test", "legacy-test-only")["id"] == 1
    assert users.verify_login("learner1@example.test", "wrong") is None
    # Verification deliberately does not rewrite an existing password row.
    with factory() as db:
        assert db.get(User, 1).password == legacy


def test_legacy_server_graded_activity_is_replay_safe(setup):
    _, factory = setup
    from services.study import award_verified_activity, xp_since

    with factory() as db:
        assert award_verified_activity(db, 1, "written", "written:test-id", 10)
        assert not award_verified_activity(db, 1, "written", "written:test-id", 10)
        assert db.get(User, 1).xp_total == 10
        assert xp_since(db, 1, utcnow() - timedelta(days=1)) == 10


def test_legacy_mock_exam_parallel_completion_awards_once(setup):
    client, factory = setup
    from routers import mock_exam
    from services.models import SkillMockExam

    client.app.include_router(mock_exam.router)
    with factory() as db:
        exam = SkillMockExam(
            user_id=1,
            subject_slug="math",
            question_ids=[10, 11],
            status="in_progress",
            started_at=utcnow(),
        )
        db.add(exam)
        db.commit()
        eid = exam.id
    payload = {
        "user_id": 1,
        "answers": [{"question_id": i, "user_answer": "a"} for i in (10, 11)],
    }
    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(
            pool.map(
                lambda _: client.post(
                    f"/skills/mock-exam/{eid}/complete", json=payload
                ),
                range(2),
            )
        )
    assert all(r.status_code == 200 for r in responses)
    assert all(r.json()["xp_awarded"] == 2 for r in responses)
    with factory() as db:
        assert db.get(User, 1).xp_total == 2
        assert db.query(StudyEvent).count() == 1


def test_profile_query_count_does_not_grow_per_subject(setup):
    client, factory = setup
    with factory() as db:
        engine = db.bind
    calls = []

    def count(*args):
        calls.append(1)

    event.listen(engine, "before_cursor_execute", count)
    try:
        first = client.get("/skills/1/profile")
        assert first.status_code == 200
        initial_count = len(calls)
        with factory() as db:
            db.add_all(
                [
                    SkillSubject(
                        slug=f"empty{i}",
                        name_uz="Empty fixture",
                        name_ru="Empty fixture",
                        name_en="Empty fixture",
                        is_active=True,
                    )
                    for i in range(5)
                ]
            )
            db.commit()
        calls.clear()
        response = client.get("/skills/1/profile")
        assert response.status_code == 200
        assert len(calls) == initial_count
        assert len(response.json()["subjects"]) == 6
        assert all(
            s["total"] == 0
            for s in response.json()["subjects"]
            if s["slug"].startswith("empty")
        )
    finally:
        event.remove(engine, "before_cursor_execute", count)


@pytest.mark.parametrize("value", ["", "   ", "dev_secret"])
def test_production_rejects_empty_or_default_signing_keys(monkeypatch, value):
    from services.security_config import require_production_secret

    monkeypatch.setenv("ENVIRONMENT", "production")
    with pytest.raises(RuntimeError):
        require_production_secret("JWT_SECRET", value, "dev_secret")
    require_production_secret("JWT_SECRET", "test-only-configured-secret", "dev_secret")


@pytest.mark.parametrize(
    "kind,path,extra,score_only",
    [
        ("daily", "/skills/daily-challenge/complete", {}, False),
        ("mistakes", "/skills/mistakes/complete", {}, False),
        ("lightning", "/skills/lightning/complete", {}, True),
        ("marathon", "/skills/marathon/complete", {}, True),
        ("checkpoint", "/skills/unit-exam/complete", {"unit_id": 1}, False),
        ("placement", "/skills/level-test/complete", {"subject_slug": "math"}, False),
        (
            "subject_exam",
            "/skills/subject-exam/complete",
            {"subject": "math", "per_unit": {}},
            True,
        ),
    ],
)
def test_unchanged_legacy_web_payload_requires_actual_answers(
    setup, kind, path, extra, score_only
):
    """Compatibility evidence: the existing website cannot securely supply a grade.

    Website source stays unchanged. These intentional 422s are a release blocker,
    not evidence that the old browser practice flow has passed integration.
    """
    client, factory = setup
    from services.study import issue

    scope = (
        "math"
        if kind in ("placement", "subject_exam")
        else "1"
        if kind == "checkpoint"
        else "all"
    )
    with factory() as db:
        issue(
            db,
            1,
            kind,
            scope,
            [{"id": 10, "options": ["a", "b"], "correct_answer": "a"}],
        )
    payload = {"user_id": 1, **extra}
    if score_only:
        payload.update(score=1, total=1)
    else:
        payload["results"] = [{"question_id": 10, "is_correct": True}]
    assert client.post(path, json=payload).status_code == 422
    with factory() as db:
        assert db.get(User, 1).xp_total == 0


def test_existing_browser_lesson_answer_contract_remains_compatible(setup):
    client, _ = setup
    issued = start(client)
    rows = [
        {
            "question_id": q["id"],
            "user_answer": q["correct_answer"],
            "is_correct": False,
        }
        for q in issued["questions"]
    ]
    response = finish(client, issued, results=rows)
    assert response.status_code == 200
    assert response.json()["score"] == len(rows)
