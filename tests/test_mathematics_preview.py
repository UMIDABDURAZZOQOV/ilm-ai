"""Independent source answers through authenticated API; local databases only."""

import json
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import timedelta
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from routers.mathematics_preview import router
from services import db as database
from services import mathematics_runtime as runtime
from services import tokens
from services.mathematics_curriculum import (
    import_course,
    load_course,
    model_answer,
)
from services.mathematics_models import MathAttempt, MathBase, MathLesson, MathProgress
from services.models import Base, StudyEvent, User
from services.study import utcnow

P = "/preview/mathematics/v1"
# Typed from the visually reviewed source and the original activities. Never
# read expected keys/aliases/model_rule to construct a submitted test answer.
ANSWERS = {
    1: ["c", "b", "O’LCHAM", "b", "shakl", "c"],
    2: ["b", "a", "b", "b", "uzunlik", "b"],
    3: ["a", "doira", "o’ngda", "b", "doira", "b"],
    4: ["3", "b", "b", "b", "2", "4"],
    5: ["b", "yassi", "b", "a", "shar", "a"],
}


def make_preview(engine, monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("MATHEMATICS_PREVIEW_ENABLED", "true")
    monkeypatch.setattr(
        tokens,
        "JWT_SECRET",
        "mathematics-local-test-only-signature-not-a-production-secret",
    )
    Base.metadata.create_all(engine)
    MathBase.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    with factory.begin() as db:
        db.add_all(
            [
                User(
                    id=1,
                    email="math1@example.test",
                    name="Math QA",
                    xp_total=137,
                    streak_days=3,
                    last_study_date=utcnow().date().isoformat(),
                ),
                User(id=2, email="math2@example.test", name="Other QA", xp_total=0),
            ]
        )
        db.flush()
        assert import_course(db) == {"created": 5, "skipped": 0}
    app = FastAPI()
    app.include_router(router)

    def get_db():
        with factory() as db:
            yield db

    app.dependency_overrides[database.get_db] = get_db
    return TestClient(
        app, headers={"Authorization": "Bearer " + tokens.create_access_token(1)}
    ), factory


@pytest.fixture
def preview(tmp_path, monkeypatch):
    engine = create_engine(
        f"sqlite:///{tmp_path}/mathematics_staging.db",
        connect_args={"check_same_thread": False, "timeout": 30},
    )

    @event.listens_for(engine, "connect")
    def foreign_keys(connection, _):
        connection.execute("PRAGMA foreign_keys=ON")

    client, factory = make_preview(engine, monkeypatch)
    with client:
        yield client, factory
    engine.dispose()


def start(client, number, request=None):
    response = client.post(
        f"{P}/lessons/math-1-1-{number}-r1/start",
        json={"assessment_version": 1, "request_id": request or str(uuid4())},
    )
    assert response.status_code == 200, response.text
    return response.json()


def finish(client, number):
    attempt = start(client, number)
    feedback = []
    for q, literal in zip(attempt["questions"], ANSWERS[number]):
        answer = {"choice_id" if q["response_kind"] == "choice" else "value": literal}
        payload = {
            "assessment_version": 1,
            "request_id": str(uuid4()),
            "question_id": q["id"],
            "answer": answer,
        }
        response = client.post(
            f"{P}/attempts/{attempt['attempt_id']}/answers", json=payload
        )
        assert response.status_code == 200 and response.json()["is_correct"], (
            response.text
        )
        assert (
            client.post(
                f"{P}/attempts/{attempt['attempt_id']}/answers", json=payload
            ).json()
            == response.json()
        )
        feedback.append(response.json())
    body = {"assessment_version": 1, "request_id": str(uuid4())}
    result = client.post(f"{P}/attempts/{attempt['attempt_id']}/complete", json=body)
    assert result.status_code == 200, result.text
    assert (
        client.post(f"{P}/attempts/{attempt['attempt_id']}/complete", json=body).json()
        == result.json()
    )
    return attempt, feedback, result.json()


def test_five_lessons_literal_keys_preserve_balance_streak_reopen_and_replay(
    preview, monkeypatch
):
    client, factory = preview
    now = utcnow()
    monkeypatch.setattr(runtime, "utcnow", lambda: now)
    cat = client.get(P + "/catalog").json()
    assert [l["state"] for l in cat["lessons"]] == ["available"] + ["locked"] * 4
    assert not cat["course_ready"] and cat["full_topic_count"] is None
    assert (
        client.post(
            P + "/lessons/math-1-1-2-r1/start",
            json={"assessment_version": 1, "request_id": str(uuid4())},
        ).status_code
        == 403
    )
    for number in range(1, 6):
        initial, _, result = finish(client, number)
        assert result["xp_awarded"] == 10 and result["streak_days"] == 3
        assert result["first_try_correct"] == 6 and result["support_uses"] == 0
        assert result["educational_effectiveness"] == "not_verified"
        raw = json.dumps(initial)
        assert all(
            key not in raw
            for key in [
                '"grading"',
                '"expected"',
                '"aliases"',
                '"model_rule"',
                '"feedback_incorrect"',
            ]
        )
    with factory() as db:
        assert db.get(User, 1).xp_total == 187
        assert db.get(User, 2).xp_total == 0
        assert db.query(MathProgress).count() == 5
        assert (
            sum(e.xp for e in db.query(StudyEvent).filter_by(kind=runtime.KIND)) == 50
        )
    with TestClient(client.app, headers=dict(client.headers)) as reopened:
        assert all(
            l["state"] == "completed"
            for l in reopened.get(P + "/catalog").json()["lessons"]
        )
        assert finish(reopened, 5)[-1]["xp_awarded"] == 0
    with factory() as db:
        assert db.get(User, 1).xp_total == 187


def test_guided_hints_real_retry_resumes_idempotently_without_early_solution(preview):
    client, _ = preview
    request = str(uuid4())
    attempt = start(client, 1, request)
    sid = attempt["attempt_id"]
    payload = {
        "assessment_version": 1,
        "request_id": str(uuid4()),
        "question_id": attempt["questions"][0]["id"],
        "answer": {"choice_id": "b"},
    }
    response = client.post(f"{P}/attempts/{sid}/answers", json=payload)
    assert response.status_code == 200 and not response.json()["is_correct"]
    assert response.json()["hint_level"] == 1
    assert "solution" not in response.json() and "correct_answer" not in response.json()
    assert (
        client.post(f"{P}/attempts/{sid}/answers", json=payload).json()
        == response.json()
    )

    resumed = start(client, 1, request)
    assert len(resumed["answers"]) == 1 and resumed["answers"][0] == response.json()
    changed = deepcopy(payload)
    changed["answer"] = {"choice_id": "c"}
    assert client.post(f"{P}/attempts/{sid}/answers", json=changed).status_code == 409
    changed["request_id"] = str(uuid4())
    assert client.post(f"{P}/attempts/{sid}/answers", json=changed).json()["is_correct"]
    assert (
        client.post(
            f"{P}/attempts/{sid}/complete",
            json={"assessment_version": 1, "request_id": str(uuid4())},
        ).status_code
        == 409
    )


def test_retry_order_is_stable_with_identical_clock_and_reversed_request_uuids(
    preview, monkeypatch
):
    client, _ = preview
    now = utcnow()
    monkeypatch.setattr(runtime, "utcnow", lambda: now)
    row = start(client, 1)
    sid = row["attempt_id"]
    first = row["questions"][0]
    bad = {
        "assessment_version": 1,
        "request_id": "ffffffff-ffff-4fff-8fff-ffffffffffff",
        "question_id": first["id"],
        "answer": {"choice_id": "b"},
    }
    assert not client.post(f"{P}/attempts/{sid}/answers", json=bad).json()["is_correct"]
    for index, (q, literal) in enumerate(zip(row["questions"], ANSWERS[1]), 1):
        payload = {
            "assessment_version": 1,
            "request_id": f"00000000-0000-4000-8000-{index:012d}",
            "question_id": q["id"],
            "answer": {
                "choice_id" if q["response_kind"] == "choice" else "value": literal
            },
        }
        assert client.post(f"{P}/attempts/{sid}/answers", json=payload).json()[
            "is_correct"
        ]
    result = client.post(
        f"{P}/attempts/{sid}/complete",
        json={"assessment_version": 1, "request_id": str(uuid4())},
    ).json()
    assert result["first_try_correct"] == 5 and result["support_uses"] == 1


def test_auth_forgery_order_expiry_and_disabled_preview(preview, monkeypatch):
    client, factory = preview
    assert client.get(P + "/catalog", headers={"Authorization": ""}).status_code == 401
    initial = start(client, 1)
    sid = initial["attempt_id"]
    payload = {
        "assessment_version": 1,
        "request_id": str(uuid4()),
        "question_id": initial["questions"][1]["id"],
        "answer": {"choice_id": "b"},
    }
    assert client.post(f"{P}/attempts/{sid}/answers", json=payload).status_code == 409
    payload["question_id"] = initial["questions"][0]["id"]
    assert (
        client.post(
            f"{P}/attempts/{sid}/answers",
            json=payload,
            headers={"Authorization": "Bearer " + tokens.create_access_token(2)},
        ).status_code
        == 404
    )
    payload["answer"]["is_correct"] = True
    assert client.post(f"{P}/attempts/{sid}/answers", json=payload).status_code == 422
    with factory.begin() as db:
        db.get(MathAttempt, sid).started_at = utcnow() - timedelta(hours=25)
    assert (
        client.post(
            f"{P}/attempts/{sid}/answers",
            json={**payload, "answer": {"choice_id": "c"}},
        ).status_code
        == 409
    )
    monkeypatch.setenv("ENVIRONMENT", "production")
    assert client.get(P + "/catalog").status_code == 404
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("MATHEMATICS_PREVIEW_ENABLED", "false")
    assert client.get(P + "/catalog").status_code == 404


def test_immutable_import_and_model_mismatch(preview):
    _, factory = preview
    with factory.begin() as db:
        assert import_course(db) == {"created": 0, "skipped": 5}
        db.get(MathLesson, "math-1-1-1-r1").sha256 = "0" * 64
    with factory.begin() as db, pytest.raises(ValueError, match="revision_change"):
        import_course(db)
    course = load_course()
    assert len(course) == 5 and sum(len(l["questions"]) for l in course) == 30
    q = deepcopy(course[3]["questions"][-1])
    assert model_answer(q["public"], q["grading"]["model_rule"]) == "4"
    q["public"]["visual"]["items"].pop()
    assert model_answer(q["public"], q["grading"]["model_rule"]) == "3"


def test_parallel_first_completions_award_only_once(preview):
    client, factory = preview
    attempts = [start(client, 1), start(client, 1)]
    for row in attempts:
        for q, literal in zip(row["questions"], ANSWERS[1]):
            response = client.post(
                f"{P}/attempts/{row['attempt_id']}/answers",
                json={
                    "assessment_version": 1,
                    "request_id": str(uuid4()),
                    "question_id": q["id"],
                    "answer": {
                        "choice_id"
                        if q["response_kind"] == "choice"
                        else "value": literal
                    },
                },
            )
            assert response.status_code == 200 and response.json()["is_correct"]

    def run(row):
        with TestClient(client.app, headers=dict(client.headers)) as c:
            result = c.post(
                f"{P}/attempts/{row['attempt_id']}/complete",
                json={"assessment_version": 1, "request_id": str(uuid4())},
            )
            assert result.status_code == 200, result.text
            return result.json()["xp_awarded"]

    with ThreadPoolExecutor(2) as pool:
        assert sorted(pool.map(run, attempts)) == [0, 10]
    with factory() as db:
        assert db.get(User, 1).xp_total == 147 and db.query(MathProgress).count() == 1
