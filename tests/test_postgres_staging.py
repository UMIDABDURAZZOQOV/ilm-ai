"""Opt-in real PostgreSQL rehearsal, confined to a fresh schema in local staging.

ILM_TEST_POSTGRES_URL_FILE points to a private file, never a command-line secret.
No production URL, public host, existing schema, or SQLite fallback is accepted.
"""

from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import secrets
from urllib.parse import urlparse

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import Column, MetaData, Table, create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

from routers import auth, skills
from routers.mobile_skills import router as mobile_router
from services import db as database, mobile_oauth, tokens, users
from services.models import Base, User, UserLessonProgress, SkillSubject, SkillUnit, SkillLesson
from services.study import utcnow
from services.database_url import normalize_database_url


@pytest.fixture(scope="module")
def postgres_stage():
    filename = os.getenv("ILM_TEST_POSTGRES_URL_FILE")
    if not filename:
        pytest.skip("Set ILM_TEST_POSTGRES_URL_FILE for the opt-in local PostgreSQL rehearsal")
    url = Path(filename).read_text().strip()
    parsed = urlparse(url)
    if (parsed.scheme != "postgresql" or parsed.hostname not in {"localhost", "127.0.0.1"}
            or "staging" not in parsed.path or os.getenv("ENVIRONMENT") == "production"):
        pytest.fail("Only an explicit loopback PostgreSQL staging database is permitted")
    schema = "ilm_mobile_" + secrets.token_hex(8)
    url = normalize_database_url(url)
    admin = create_engine(url)
    with admin.begin() as conn:
        conn.execute(text(f'CREATE SCHEMA "{schema}"'))
    engine = create_engine(url, connect_args={"options": f"-csearch_path={schema}"})
    patch = pytest.MonkeyPatch()
    try:
        # Reproduce a pre-OAuth users table and pre-hardening/additive schema.
        legacy = Table("users", MetaData(), *[
            Column(c.name, c.type, primary_key=c.primary_key,
                   nullable=False if c.name == "password" else c.nullable)
            for c in User.__table__.columns
            if c.name not in {"oauth_provider", "oauth_provider_id", "email_verified", "age"}
        ])
        legacy.create(engine)
        additive = {"curriculum_courses", "curriculum_chapters", "curriculum_topics",
                    "curriculum_lesson_sources", "study_sessions", "study_events",
                    "oauth_states", "mobile_login_grants"}
        Base.metadata.create_all(engine, tables=[t for t in Base.metadata.sorted_tables
                                               if t.name != "users" and t.name not in additive])
        with engine.begin() as conn:
            for uid, xp in [(1, 0), (42, 137)]:
                conn.execute(legacy.insert().values(id=uid, name="Staging learner",
                    email=f"staging-{uid}@example.test", password="not-a-real-password",
                    xp_total=xp, streak_days=3 if uid == 42 else 0))
        factory = sessionmaker(bind=engine, expire_on_commit=False)
        with factory.begin() as db:
            subject = SkillSubject(slug="math", name_uz="Math", name_ru="Math", name_en="Math", is_active=True)
            db.add(subject); db.flush()
            unit = SkillUnit(subject_id=subject.id, slug="legacy", title_uz="Legacy", title_ru="Legacy", title_en="Legacy", order_index=1)
            db.add(unit); db.flush()
            lesson = SkillLesson(unit_id=unit.id, slug="legacy", title_uz="Legacy", title_ru="Legacy", title_en="Legacy", order_index=1, xp_reward=20)
            db.add(lesson); db.flush()
            db.add(UserLessonProgress(user_id=42, lesson_id=lesson.id, stars=2,
                                      attempts=1, xp_earned=137, completed_at=utcnow()))
        patch.setattr(database, "engine", engine)
        patch.setattr(database, "DATABASE_URL", url)
        database.migrate_postgres_columns()
        Base.metadata.create_all(engine)
        database.migrate_postgres_columns()
        for module in (database, mobile_oauth, tokens, users):
            patch.setattr(module, "SessionLocal", factory)
        patch.setattr(tokens, "JWT_SECRET", "postgres-rehearsal-only-at-least-32-characters")
        patch.setattr(users, "USE_DB", True)
        patch.setattr(tokens, "USE_DB", True)
        app = FastAPI()
        app.include_router(auth.router); app.include_router(skills.router); app.include_router(mobile_router)

        def get_db():
            with factory() as db:
                yield db

        app.dependency_overrides[database.get_db] = get_db
        with TestClient(app, headers={"Authorization": f"Bearer {tokens.create_access_token(1)}"}) as client:
            yield client, factory, engine
    finally:
        patch.undo()
        engine.dispose()
        admin.dispose()


def test_postgres_legacy_oauth_migration_is_additive_and_nullable(postgres_stage):
    client, factory, engine = postgres_stage
    columns = {c["name"]: c for c in inspect(engine).get_columns("users")}
    assert {"oauth_provider", "oauth_provider_id", "email_verified", "age"} <= set(columns)
    assert columns["password"]["nullable"]
    with factory.begin() as db:
        old = db.get(User, 42)
        assert old.xp_total == 137 and old.streak_days == 3
        assert db.query(UserLessonProgress).filter_by(user_id=42).one().stars == 2
        db.add(User(id=3, name="OAuth staging", email="oauth@example.test",
                    password=None, oauth_provider="google", oauth_provider_id="staging-only"))
    verifier = "v" * 64
    grant = mobile_oauth.issue_grant(3, mobile_oauth.pkce_challenge(verifier))
    exchange = client.post("/auth/mobile/exchange", json={"code": grant, "code_verifier": verifier})
    assert exchange.status_code == 200
    assert client.post("/auth/mobile/exchange", json={"code": grant, "code_verifier": verifier}).status_code == 400
    refreshed = client.post("/auth/refresh", json={"refresh_token": exchange.json()["refresh_token"]})
    assert refreshed.status_code == 200


def test_postgres_all_mobile_content_retry_import_and_parallel_completion(postgres_stage, tmp_path):
    from test_biology_continuation import test_complete_grades5_to11_api_once_only_xp as exercise
    from test_biology_segments import answers
    client, factory, _ = postgres_stage

    class MobileClient:
        def get(self, path, **kwargs):
            return client.get("/mobile" + path, **kwargs)

        def post(self, path, **kwargs):
            return client.post("/mobile" + path, **kwargs)

    exercise((MobileClient(), factory), tmp_path)
    tree = client.get("/mobile/skills/1/tree?subject=biologiya&grade=5").json()
    lid = tree["units"][0]["lessons"][0]["id"]
    start = client.post(f"/mobile/skills/lessons/{lid}/start", json={"user_id": 1}).json()
    body = {"user_id": 1, "attempt_id": start["attempt_id"], "results": answers(start)}
    with factory() as db:
        before = db.get(User, 1).xp_total
    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(lambda _: client.post(f"/mobile/skills/lessons/{lid}/complete", json=body), range(2)))
    assert all(r.status_code == 200 for r in responses), [r.status_code for r in responses]
    assert responses[0].json() == responses[1].json()
    with factory() as db:
        assert db.get(User, 1).xp_total == before + responses[0].json()["xp_awarded"]
        assert db.get(User, 42).xp_total == 137
        assert db.query(UserLessonProgress).filter_by(user_id=42).one().stars == 2
