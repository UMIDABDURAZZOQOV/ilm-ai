"""Disposable SQLite/API, source lineage and closed deterministic grading tests."""

import importlib.util
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import pytest
from alembic.migration import MigrationContext
from alembic.operations import Operations
from fastapi import HTTPException
from sqlalchemy import inspect
from sqlalchemy.engine import make_url
from test_release_hardening import setup as setup  # noqa: PLC0414 - pytest fixture export

from routers.physics_preview import router
from scripts.import_physics_preview import safe_url
from services import assessment_runtime as runtime
from services import tokens
from services.assessment_grading import AnswerError, formula_ast, grade_answer, numeric
from services.assessment_models import (
    AssessmentBase,
    AssessmentV2Answer,
    AssessmentV2Progress,
    CurriculumAssessment,
    CurriculumLessonV2,
)
from services.models import (
    Base,
    SkillQuestion,
    StudyEvent,
    StudySession,
    User,
    UserLessonProgress,
)
from services.physics_curriculum import (
    import_batch,
    load_batch,
    validate_batch,
)

PREFIX = "/preview/physics/v2"


@pytest.fixture
def preview(setup, monkeypatch):
    client, factory = setup
    with factory() as db:
        AssessmentBase.metadata.create_all(db.get_bind())
        import_batch(db, load_batch())
        db.commit()
    monkeypatch.setenv("PHYSICS_PREVIEW_ENABLED", "true")
    monkeypatch.setenv("ENVIRONMENT", "test")
    client.app.include_router(router)
    return client, factory


def start(client, n=1, request=None):
    return client.post(
        f"{PREFIX}/lessons/physics-6-section-{n}-r1/start",
        json={"assessment_version": 2, "request_id": request or str(uuid4())},
    )


def correct(q):
    spec = q["grading_spec"]
    if spec["kind"] == "concept_selection":
        return {"choice_id": spec["expected_choice"]}
    if spec["kind"] == "ordering":
        return {"order": spec["expected_order"]}
    # Independent arithmetic oracles for the original five numeric exercises.
    data = {
        "m_to_cm": ("170", "cm", "y=x*100"),
        "mm_to_m": ("0,46", "m", "x/1000"),
        "scale": ("2", "cm", "(b-a)/n"),
        "mean2": ("14.4", "cm", "(x2+x1)/2"),
        "half_division": ("2", "mm", "0.5*d"),
    }
    value, unit, formula = data[spec["rule"]]
    return {"value": value, "unit": unit, "formula": formula}


def submit(client, attempt, key, answer):
    return client.post(
        f"{PREFIX}/attempts/{attempt['attempt_id']}/answers",
        json={"assessment_version": 2, "assessment_key": key, "answer": answer},
    )


def finish(client, attempt):
    return client.post(
        f"{PREFIX}/attempts/{attempt['attempt_id']}/complete",
        json={"assessment_version": 2},
    )


def answer_all(client, attempt, n=1, wrong=False):
    for q in load_batch()["lessons"][n - 1]["assessments"]:
        answer = correct(q)
        if wrong:
            if q["response_kind"] == "concept_selection":
                answer = {
                    "choice_id": next(
                        i
                        for i in q["grading_spec"]["choice_ids"]
                        if i != answer["choice_id"]
                    )
                }
            elif q["response_kind"] == "ordering":
                answer = {"order": list(reversed(answer["order"]))}
            else:
                answer = {**answer, "value": "999999"}
        result = submit(client, attempt, q["key"], answer)
        assert result.status_code == 200, result.text
        assert result.json()["is_correct"] is not wrong


def assert_private_absent(payload):
    if isinstance(payload, dict):
        assert not (
            {
                "grading_spec",
                "expected_si",
                "expected_choice",
                "expected_order",
                "choice_ids",
                "equivalents",
                "abs_tol_si",
                "rel_tol",
                "rounding_increment_si",
            }
            & payload.keys()
        )
        for value in payload.values():
            assert_private_absent(value)
    if isinstance(payload, list):
        for value in payload:
            assert_private_absent(value)


def test_sources_content_counts_and_every_numeric_oracle():
    doc = load_batch()
    assert validate_batch(doc) == {
        "lessons": 7,
        "cards": 31,
        "formulas": 5,
        "worked_examples": 8,
        "assessments": 43,
        "frq": 5,
    }
    assert [len(l["assessments"]) for l in doc["lessons"]] == [6, 5, 5, 6, 6, 7, 8]
    assert [l["source_refs"][0]["pdf_pages"] for l in doc["lessons"]] == [
        [3, 4, 5],
        [6, 7, 8],
        [8, 9],
        [9, 10],
        [10, 11, 12],
        [12, 13, 14],
        [14, 15, 16],
    ]
    prompts = [q["public"]["prompt"] for l in doc["lessons"] for q in l["assessments"]]
    assert len(prompts) == len(set(prompts))
    for lesson in doc["lessons"]:
        for q in lesson["assessments"]:
            assert grade_answer(q["grading_spec"], correct(q)) == "correct"
    assert not any(l["formulas"] for l in doc["lessons"][:5])


@pytest.mark.parametrize(
    "tamper", ["page", "answer", "private", "formula", "fact", "publication", "expert"]
)
def test_content_validator_rejects_unreviewed_mutations(tamper):
    doc = load_batch()
    lesson = doc["lessons"][-1]
    if tamper == "page":
        lesson["source_refs"][0]["pdf_pages"][0] = 99
    if tamper == "answer":
        lesson["assessments"][0]["grading_spec"]["expected_si"] = "200"
    if tamper == "private":
        lesson["assessments"][0]["public"]["expected_si"] = "0.02"
    if tamper == "formula":
        lesson["assessments"][0]["grading_spec"]["formula"]["equivalents"] = ["b+a"]
    if tamper == "fact":
        lesson["assessments"][0]["fact_ids"] = ["unreviewed_fact"]
    if tamper == "publication":
        doc["publication"] = "public"
    if tamper == "expert":
        lesson["review"]["independent_subject_expert"] = "approved"
    with pytest.raises(ValueError):
        validate_batch(doc)


@pytest.mark.parametrize(
    "text,expected",
    [
        ("1,25", "1.25"),
        ("2*(3+4)", "14"),
        ("1e-3", "0.001"),
        ("10^2", "100"),
        ("2/5", "0.4"),
        ("−3", "-3"),
    ],
)
def test_exact_decimal_arithmetic(text, expected):
    assert numeric(text) == numeric(expected)


@pytest.mark.parametrize(
    "text",
    [
        '__import__("os")',
        "x.__class__",
        "[1]",
        "True",
        "NaN",
        "inf",
        "1e999999",
        "9" * 129,
        "2^999999",
        "1/0",
        "1,2,3",
        "1;2",
        "2x",
        "2**(2**20)",
    ],
)
def test_unsafe_unbounded_or_ambiguous_expressions_rejected(text):
    with pytest.raises(AnswerError):
        numeric(text)


def numeric_spec():
    return load_batch()["lessons"][6]["assessments"][0]["grading_spec"]


@pytest.mark.parametrize(
    "answer,code",
    [
        ({"formula": "d=(b-a)/n", "value": "2", "unit": "cm"}, "correct"),
        ({"formula": "b/n-a/n", "value": "20", "unit": "mm"}, "correct"),
        ({"formula": "(b-a)/n", "value": "0.02", "unit": "metr"}, "correct"),
        ({"formula": "(b-a)/n", "value": "-2", "unit": "cm"}, "sign_error"),
        ({"formula": "(b-a)/n", "value": "2", "unit": "m"}, "out_of_tolerance"),
        ({"formula": "(b-a)/n", "value": "2", "unit": "kg"}, "dimension_mismatch"),
        ({"formula": "(b-a)/n", "value": "2", "unit": "CM"}, "unknown_unit"),
        ({"formula": "b-a/n", "value": "2", "unit": "cm"}, "wrong_formula"),
        ({"formula": "(b-a)/z", "value": "2", "unit": "cm"}, "unknown_symbol"),
        ({"formula": "(b-a)/n", "value": "2"}, "answer_required"),
        (
            {"formula": "(b-a)/n", "value": "2", "unit": "cm", "is_correct": True},
            "answer_required",
        ),
    ],
)
def test_unit_formula_and_error_feedback_codes(answer, code):
    assert grade_answer(numeric_spec(), answer) == code


def test_reviewed_equivalence_and_rounding_tolerances():
    spec = numeric_spec()
    assert formula_ast("d = ( b - a ) / n", spec["formula"]) == formula_ast(
        "(b-a)/n", spec["formula"]
    )
    assert formula_ast("(b+a)/n", spec["formula"]) != formula_ast(
        "(b-a)/n", spec["formula"]
    )
    spec.update(
        expected_si="0.0204",
        abs_tol_si="0.0005",
        rel_tol="0",
        rounding_increment_si="0.001",
    )
    assert (
        grade_answer(spec, {"formula": "(b-a)/n", "value": "2", "unit": "cm"})
        == "correct"
    )
    assert (
        grade_answer(spec, {"formula": "(b-a)/n", "value": "2.04", "unit": "cm"})
        == "rounding_requirement"
    )
    assert (
        grade_answer(spec, {"formula": "(b-a)/n", "value": "2.1", "unit": "cm"})
        == "out_of_tolerance"
    )
    spec.pop("rounding_increment_si")
    spec.update(abs_tol_si="0", rel_tol="0.02")
    assert (
        grade_answer(spec, {"formula": "(b-a)/n", "value": "2", "unit": "cm"})
        == "correct"
    )


@pytest.mark.parametrize(
    "environment,flag,url",
    [
        ("production", "true", "sqlite:///:memory:"),
        ("staging", "true", "sqlite:///:memory:"),
        ("test", "false", "sqlite:///:memory:"),
        ("test", "true", "postgresql://remote.example/test"),
    ],
)
def test_preview_gate_cannot_publish(environment, flag, url, monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", environment)
    monkeypatch.setenv("PHYSICS_PREVIEW_ENABLED", flag)
    db = SimpleNamespace(get_bind=lambda: SimpleNamespace(url=make_url(url)))
    with pytest.raises(HTTPException) as caught:
        runtime.preview_gate(db)
    assert caught.value.status_code == 404


@pytest.mark.parametrize(
    "url,env",
    [
        (None, "test"),
        ("sqlite:///test.db", "production"),
        ("postgresql://prod.example/staging", "test"),
        ("postgresql://localhost/production", "test"),
    ],
)
def test_import_rejects_production_and_implicit_databases(url, env):
    from sqlalchemy import create_engine

    # Plain PostgreSQL URLs must select the installed requirements driver.
    engine = create_engine(safe_url("postgresql://qa@localhost/ilm_staging", "test"))
    assert engine.dialect.dbapi.__name__ == "psycopg2"
    engine.dispose()
    with pytest.raises(ValueError):
        safe_url(url, env)


def test_namespace_disabled_by_default_and_no_private_fields(preview, monkeypatch):
    client, _ = preview
    monkeypatch.delenv("PHYSICS_PREVIEW_ENABLED")
    assert client.get(PREFIX + "/catalog").status_code == 404
    monkeypatch.setenv("PHYSICS_PREVIEW_ENABLED", "true")
    cat = client.get(PREFIX + "/catalog").json()
    assert cat["implemented_sections"] == 7 and cat["course_complete"] is False
    assert [l["state"] for l in cat["lessons"]] == ["available"] + ["locked"] * 6
    assert start(client, 2).status_code == 403
    result = start(client).json()
    assert_private_absent(result)
    assert "solution" not in json.dumps(result)
    assert start(client, request=str(uuid4())).status_code == 200
    assert (
        client.get(PREFIX + "/catalog", headers={"Authorization": ""}).status_code
        == 401
    )


def test_all_seven_lessons_server_grading_xp_progress_and_legacy_isolation(preview):
    client, factory = preview
    with factory() as db:
        baseline = (
            db.query(SkillQuestion).count(),
            db.query(UserLessonProgress).count(),
        )
        user2xp = db.get(User, 2).xp_total
    for n in range(1, 8):
        rid = str(uuid4())
        issued = start(client, n, rid).json()
        assert start(client, n, rid).json() == issued
        assert finish(client, issued).status_code == 409
        answer_all(client, issued, n)
        resumed = start(client, n, rid).json()
        assert len(resumed["answers"]) == len(issued["questions"])
        assert_private_absent(resumed)
        result = finish(client, issued)
        assert result.status_code == 200, result.text
        assert result.json()["xp_awarded"] == 10 and result.json()["xp_total"] == 10 * n
        assert result.json()["passed"] and result.json()["streak_days"] == 1
        assert finish(client, issued).json() == result.json()
        # Completed answers/attempts replay unchanged; a new attempt earns no XP.
        replay = start(client, n).json()
        answer_all(client, replay, n)
        assert finish(client, replay).json()["xp_awarded"] == 0
    with factory() as db:
        assert db.get(User, 1).xp_total == 70 and db.get(User, 2).xp_total == user2xp
        assert db.query(AssessmentV2Progress).count() == 7
        assert all(
            p.attempts == 2 and p.xp_earned == 10
            for p in db.query(AssessmentV2Progress)
        )
        assert sum(e.xp for e in db.query(StudyEvent)) == 70
        assert (
            db.query(SkillQuestion).count(),
            db.query(UserLessonProgress).count(),
        ) == baseline


def test_order_auth_tamper_retry_and_answer_replay(preview):
    client, factory = preview
    issued = start(client).json()
    q1, q2 = load_batch()["lessons"][0]["assessments"][:2]
    assert submit(client, issued, q2["key"], correct(q2)).status_code == 409
    forged = {**correct(q1), "is_correct": True}
    assert submit(client, issued, q1["key"], forged).status_code == 422
    other = {"Authorization": f"Bearer {tokens.create_access_token(2)}"}
    assert (
        client.post(
            f"{PREFIX}/attempts/{issued['attempt_id']}/complete",
            json={"assessment_version": 2},
            headers=other,
        ).status_code
        == 404
    )
    result = submit(client, issued, q1["key"], correct(q1))
    assert result.status_code == 200 and result.json()["is_correct"]
    assert submit(client, issued, q1["key"], correct(q1)).json() == result.json()
    assert submit(client, issued, q1["key"], {"choice_id": "o3"}).status_code == 409
    with factory() as db:
        assert (
            db.query(AssessmentV2Answer).count() == 1 and db.get(User, 1).xp_total == 0
        )


def test_failed_attempt_does_not_unlock_or_award_xp(preview):
    client, factory = preview
    issued = start(client).json()
    answer_all(client, issued, wrong=True)
    result = finish(client, issued).json()
    assert result["xp_awarded"] == 0 and not result["passed"]
    assert start(client, 2).status_code == 403
    again = start(client).json()
    answer_all(client, again)
    assert finish(client, again).json()["xp_awarded"] == 10
    with factory() as db:
        p = db.get(AssessmentV2Progress, (1, issued["lesson_key"]))
        assert p.attempts == 2 and p.completed_at is not None


def test_expired_session_and_parallel_answer_completion_are_safe(preview):
    client, factory = preview
    issued = start(client).json()
    q = load_batch()["lessons"][0]["assessments"][0]
    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(
            pool.map(lambda _: submit(client, issued, q["key"], correct(q)), range(2))
        )
    assert all(r.status_code == 200 for r in responses)
    assert responses[0].json() == responses[1].json()
    answer_all(client, issued)
    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(lambda _: finish(client, issued), range(2)))
    assert all(r.status_code == 200 for r in responses)
    assert responses[0].json() == responses[1].json()
    with factory.begin() as db:
        assert db.get(User, 1).xp_total == 10 and db.query(StudyEvent).count() == 1
        db.get(StudySession, issued["attempt_id"]).started_at -= timedelta(days=2)
    assert finish(client, issued).json() == responses[0].json()
    pending = start(client).json()
    with factory.begin() as db:
        db.get(StudySession, pending["attempt_id"]).started_at -= timedelta(days=2)
    assert finish(client, pending).status_code == 409


def test_import_immutable_and_no_new_tables_in_legacy_metadata(preview):
    _, factory = preview
    doc = load_batch()
    assert not (set(AssessmentBase.metadata.tables) & set(Base.metadata.tables))
    with factory.begin() as db:
        import_batch(db, doc)
        assert db.query(CurriculumLessonV2).count() == 7
        assert db.query(CurriculumAssessment).count() == 43
        doc["lessons"][0]["cards"][0]["title"] = "Changed content"
        with pytest.raises(ValueError, match="changed_content"):
            import_batch(db, doc)


def migration(connection):
    path = (
        Path(__file__).resolve().parents[1]
        / "alembic/versions/0013_add_assessment_v2.py"
    )
    spec = importlib.util.spec_from_file_location("physics_migration", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    ctx = MigrationContext.configure(connection)
    with Operations.context(ctx):
        module.upgrade()
    return module


def test_additive_sqlite_migration_retains_legacy_users_progress(setup):
    _, factory = setup
    engine = factory.kw["bind"]
    with engine.begin() as conn:
        migration(conn)
    with factory.begin() as db:
        assert db.get(User, 1).name == "Learner 1"
        assert db.query(SkillQuestion).count() == 6
        import_batch(db, load_batch())
        assert db.query(CurriculumAssessment).count() == 43
    names = set(inspect(engine).get_table_names())
    assert set(AssessmentBase.metadata.tables) <= names


def test_local_sandbox_creates_only_private_test_data_and_resume_preserves_it(tmp_path):
    import os
    import subprocess
    import sys

    from sqlalchemy import create_engine, text

    from services.physics_curriculum import load_course

    path = tmp_path / "preview"
    command = [
        sys.executable,
        "-m",
        "scripts.serve_physics_preview",
        "--directory",
        str(path),
        "--create-only",
    ]
    env = {**os.environ, "ENVIRONMENT": "test"}
    result = subprocess.run(
        command, env=env, text=True, capture_output=True, timeout=30, check=False
    )
    assert result.returncode == 0, result.stderr
    config = json.loads((path / "flutter-defines.json").read_text())
    assert (
        config["PHYSICS_PREVIEW"] is True and config["PHYSICS_TEST_USER_ID"] == 900002
    )
    assert config["PHYSICS_TEST_TOKEN"] not in result.stdout
    engine = create_engine(f"sqlite:///{path / 'preview.db'}")
    with engine.begin() as conn:
        assert conn.execute(
            text("SELECT COUNT(*) FROM curriculum_v2_lessons")
        ).scalar() == sum(len(d["lessons"]) for d in load_course())
        assert (
            conn.execute(text("SELECT COUNT(*) FROM skilltree_lessons")).scalar() == 0
        )
        conn.execute(text("UPDATE users SET xp_total=137 WHERE id=900002"))
    assert (
        subprocess.run(command, env=env, capture_output=True, check=False).returncode
        != 0
    )
    resumed = subprocess.run(
        [*command, "--resume"],
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert resumed.returncode == 0, resumed.stderr
    with engine.connect() as conn:
        assert (
            conn.execute(text("SELECT xp_total FROM users WHERE id=900002")).scalar()
            == 137
        )
    engine.dispose()


def test_sandbox_cannot_write_inside_a_git_repository_or_resume_arbitrary_directory(
    tmp_path,
):
    from scripts.serve_physics_preview import sandbox_path

    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    with pytest.raises(ValueError, match="outside_all_git"):
        sandbox_path(str(repo / "qa"), False)
    with pytest.raises(ValueError):
        sandbox_path(str(tmp_path), False)
    with pytest.raises(ValueError):
        sandbox_path(str(tmp_path / "missing"), True)


def test_autogenerate_preserves_v2_metadata_and_review_evidence(preview):
    from alembic.autogenerate import compare_metadata

    from services.physics_curriculum import validate_review_evidence

    _, factory = preview
    with factory().get_bind().connect() as conn:
        changes = compare_metadata(
            MigrationContext.configure(conn), [Base.metadata, AssessmentBase.metadata]
        )
        assert not [
            d
            for d in changes
            if d[0] in {"remove_table", "add_table"}
            and getattr(d[1], "name", "") in AssessmentBase.metadata.tables
        ]
    changed = load_batch()
    changed["lessons"][0]["title"] = "Unreviewed title"
    with pytest.raises(ValueError, match="new_reviewed_revision"):
        validate_review_evidence(changed)


def test_numeric_api_format_error_is_editable_and_wrong_unit_is_authoritative(preview):
    client, factory = preview
    with factory.begin() as db:
        for n in range(1, 6):
            db.add(
                AssessmentV2Progress(
                    user_id=1,
                    lesson_key=f"physics-6-section-{n}-r1",
                    completed_at=runtime.utcnow(),
                    attempts=1,
                    best_score_pct=100,
                    xp_earned=0,
                )
            )
    issued = start(client, 6).json()
    questions = load_batch()["lessons"][5]["assessments"]
    for q in questions[:2]:
        assert submit(client, issued, q["key"], correct(q)).status_code == 200
    q = questions[2]
    invalid = submit(
        client,
        issued,
        q["key"],
        {"formula": "100*x", "value": '__import__("os")', "unit": "cm"},
    )
    assert invalid.status_code == 422 and "solution" not in invalid.text
    with factory() as db:
        assert db.query(AssessmentV2Answer).count() == 2
    wrong = submit(
        client, issued, q["key"], {"formula": "100*x", "value": "170", "unit": "kg"}
    )
    assert wrong.status_code == 200 and wrong.json()["code"] == "dimension_mismatch"
    assert_private_absent(wrong.json())
    assert wrong.json()["solution"]
    assert submit(client, issued, q["key"], correct(q)).status_code == 409


def test_importer_never_loads_legacy_database_hooks_or_alters_user_schema(tmp_path):
    import os
    import subprocess
    import sys

    from sqlalchemy import create_engine, text

    path = tmp_path / "minimal-legacy.db"
    engine = create_engine(f"sqlite:///{path}")
    with engine.begin() as conn:
        conn.execute(
            text("CREATE TABLE users (id INTEGER PRIMARY KEY, sentinel TEXT NOT NULL)")
        )
        conn.execute(text("INSERT INTO users VALUES (1, 'preserve')"))
        migration(conn)
    trap = tmp_path / "must-not-be-created.db"
    code = """
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from services.physics_curriculum import import_batch, load_batch
engine=create_engine(sys.argv[1])
with Session(engine) as db, db.begin():
    import_batch(db,load_batch())
assert 'services.db' not in sys.modules
assert 'services.models' not in sys.modules
engine.dispose()
"""
    result = subprocess.run(
        [sys.executable, "-c", code, f"sqlite:///{path}"],
        env={**os.environ, "ENVIRONMENT": "test", "DATABASE_URL": f"sqlite:///{trap}"},
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert not trap.exists()
    with engine.connect() as conn:
        assert conn.execute(text("SELECT sentinel FROM users")).scalar() == "preserve"
        assert [c["name"] for c in inspect(conn).get_columns("users")] == [
            "id",
            "sentinel",
        ]
        assert (
            conn.execute(text("SELECT COUNT(*) FROM curriculum_v2_lessons")).scalar()
            == 7
        )
    engine.dispose()
