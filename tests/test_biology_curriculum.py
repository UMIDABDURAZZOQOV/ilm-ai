"""Real source catalogue and first authored lesson, in disposable staging only."""

from copy import deepcopy
from pathlib import Path
import os
import subprocess
import sys

import pytest
from sqlalchemy import func
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable

from test_release_hardening import setup  # Reuse the isolated JWT/API fixture.
from services.curriculum import load_documents, validate_lesson, import_curriculum
from services.models import (
    CurriculumCourse,
    CurriculumChapter,
    CurriculumTopic,
    CurriculumLessonSource,
    SkillLesson,
    SkillQuestion,
    User,
    UserLessonProgress,
)


@pytest.fixture
def biology(setup):
    client, factory = setup
    with factory.begin() as db:
        imported = import_curriculum(db, *load_documents())
    return client, factory, imported["lesson_id"]


def test_real_catalog_covers_every_available_toc_paragraph_and_flags_missing_files():
    catalog, lesson = load_documents()
    validate_lesson(catalog, lesson)
    assert sum(len(b["records"]) for b in catalog["books"]) == 468
    assert sum(b.get("chapter_count", 0) for b in catalog["books"]) == 46
    assert sum(b.get("paragraph_count", 0) for b in catalog["books"]) == 366
    assert [
        b["grade"] for b in catalog["books"] if b["status"].startswith("blocked_")
    ] == []
    five = catalog["books"][0]
    assert five["duplicate_pdf_ranges"] == [[99, 195]]
    first = next(r for r in five["records"] if r.get("paragraph") == 1)
    assert (
        first["pdf_start"],
        first["pdf_end"],
        first["printed_start"],
        first["printed_end"],
    ) == (5, 8, 4, 7)
    seven = catalog["books"][2]
    forty = next(r for r in seven["records"] if r.get("paragraph") == 40)
    assert forty["toc_printed_start"] == 132 and forty["printed_start"] == 136
    # Part boundaries must not absorb later chapters through a stale parent ID.
    nine = catalog["books"][4]
    assert nine["records"][0]["pdf_end"] < 31


@pytest.mark.parametrize(
    "change",
    [
        "answer",
        "page",
        "page_offset",
        "verification",
        "duplicate_options",
        "card_fact",
        "missing_question",
    ],
)
def test_source_validator_rejects_unsubstantiated_or_inconsistent_payload(change):
    catalog, lesson = deepcopy(load_documents())
    if change == "answer":
        lesson["questions"][0]["correct_answer"] = "unsupported"
    elif change == "page":
        lesson["facts"]["biology"]["source"]["pdf_pages"] = [100]
    elif change == "page_offset":
        lesson["facts"]["biology"]["source"]["printed_pages"] = [5]
    elif change == "verification":
        lesson["facts"]["biology"]["source"]["verification"] = "not_read"
    elif change == "duplicate_options":
        lesson["questions"][0]["options"][1] = lesson["questions"][0]["options"][0]
    elif change == "card_fact":
        lesson["theory"][0]["fact_ids"] = ["unread_fact"]
    else:
        lesson["questions"] = []
    with pytest.raises(ValueError):
        validate_lesson(catalog, lesson)


def test_additive_import_is_idempotent_and_does_not_rewrite_progress(biology):
    _, factory, lesson_id = biology
    with factory.begin() as db:
        user = db.get(User, 1)
        user.xp_total = 73
        db.add(
            UserLessonProgress(
                user_id=1, lesson_id=1, stars=2, attempts=1, xp_earned=12
            )
        )
    with factory.begin() as db:
        before = db.query(func.count(SkillQuestion.id)).scalar()
        assert import_curriculum(db, *load_documents()) == {
            "lesson_id": lesson_id,
            "created": False,
        }
        assert db.query(func.count(SkillQuestion.id)).scalar() == before
        assert db.get(User, 1).xp_total == 73
        assert (
            db.query(UserLessonProgress).filter_by(user_id=1, lesson_id=1).one().stars
            == 2
        )
        assert db.query(CurriculumCourse).count() == 7
        assert db.query(CurriculumChapter).count() == 47
        assert db.query(CurriculumTopic).count() == 406


def test_published_source_and_lesson_are_immutable(biology):
    _, factory, _ = biology
    catalog, lesson = deepcopy(load_documents())
    lesson["theory"][0]["body"] += " O‘rganishda davom etamiz."
    with factory.begin() as db, pytest.raises(ValueError, match="immutable"):
        import_curriculum(db, catalog, lesson)


def test_backend_loaded_grade_paths_keep_legacy_path_and_grade_progress_separate(
    biology,
):
    client, factory, lesson_id = biology
    response = client.get("/skills/subjects/biologiya/grades")
    assert response.status_code == 200
    grades = response.json()["grades"]
    assert [g["grade"] for g in grades] == list(range(5, 12))
    assert [g["grade"] for g in grades if g["ready_lessons"]] == [5]
    assert client.get("/skills/1/tree?subject=biologiya").json()["units"] == []
    tree = client.get("/skills/1/tree?subject=biologiya&grade=5").json()
    assert len(tree["units"]) == 3
    assert tree["units"][0]["lessons"][0]["id"] == lesson_id
    assert tree["units"][0]["lessons"][0]["status"] == "unlocked"
    assert tree["units"][0]["exam"]["status"] == "locked"
    assert (
        client.get("/skills/1/tree?subject=biologiya&grade=7").json()["units"][0][
            "lessons"
        ]
        == []
    )
    assert client.get("/skills/1/tree?subject=biologiya&grade=4").status_code == 404
    assert (
        client.get("/skills/2/curriculum?subject=biologiya&grade=5").status_code == 403
    )
    # Other subjects still use their original ungraded path.
    assert len(client.get("/skills/1/tree?subject=math").json()["units"]) == 2


def test_first_real_lesson_sources_feedback_xp_retry_and_incomplete_chapter_gate(
    biology,
):
    client, factory, lesson_id = biology
    start = client.post(
        f"/skills/lessons/{lesson_id}/start", json={"user_id": 1, "language": "ru"}
    )
    assert start.status_code == 200
    data = start.json()
    assert len(data["questions"]) == 12 and data["content_language"] == "uz"
    assert all(c["source"]["printed_pages"] in ([4], [6]) for c in data["theory"])
    assert all(
        q["source"]["pdf_pages"] in ([5], [7]) and q["explanation"]
        for q in data["questions"]
    )
    payload = {
        "user_id": 1,
        "attempt_id": data["attempt_id"],
        "results": [
            {
                "question_id": q["id"],
                "answer_index": q["options"].index(q["correct_answer"]),
                "is_correct": False,
            }
            for q in data["questions"]
        ],
    }
    result = client.post(f"/skills/lessons/{lesson_id}/complete", json=payload)
    assert result.status_code == 200
    assert result.json()["score"] == 12 and result.json()["xp_awarded"] == 20
    assert (
        client.post(f"/skills/lessons/{lesson_id}/complete", json=payload).json()
        == result.json()
    )
    outline = client.get("/skills/1/curriculum?subject=biologiya&grade=5").json()
    assert outline["chapters"][0]["topics"][0]["completed"] is True
    assert outline["completed"] is False and outline["next_grade"] is None
    unit_id = outline["chapters"][0]["unit_id"]
    assert client.get(f"/skills/1/unit-exam?unit_id={unit_id}").status_code == 409
    other = client.get("/skills/1/curriculum?subject=biologiya&grade=7").json()
    assert all(not t["completed"] for c in other["chapters"] for t in c["topics"])
    with factory() as db:
        assert db.get(User, 1).xp_total == 20


def test_sourced_practice_questions_do_not_use_unreviewed_runtime_translation(biology):
    _, factory, lesson_id = biology
    from routers.skills import _translate_questions, _QUESTION_TX_CACHE

    with factory() as db:
        q = db.query(SkillQuestion).filter_by(lesson_id=lesson_id).first()
        _QUESTION_TX_CACHE[(q.id, "ru")] = {
            "id": q.id,
            "question_text": "unreviewed translation",
        }
        try:
            result = _translate_questions(
                [
                    {
                        "id": q.id,
                        "question_text": q.question_text,
                        "options": q.options,
                        "correct_answer": q.correct_answer,
                    }
                ],
                "ru",
                db,
            )
            assert result[0]["question_text"] == q.question_text
            assert result[0]["source"]["paragraph"] == 1
        finally:
            _QUESTION_TX_CACHE.pop((q.id, "ru"), None)


def test_grade_schema_is_additive_and_compiles_for_postgres():
    for model in [
        CurriculumCourse,
        CurriculumChapter,
        CurriculumTopic,
        CurriculumLessonSource,
    ]:
        assert str(CreateTable(model.__table__).compile(dialect=postgresql.dialect()))


def test_importer_refuses_production_before_connecting_to_database():
    command = [
        sys.executable,
        str(
            Path(__file__).resolve().parents[1] / "scripts/import_biology_curriculum.py"
        ),
        "--apply",
        "--database-url",
        "sqlite:////tmp/never-write-production.db",
    ]
    result = subprocess.run(
        command,
        env={**os.environ, "ENVIRONMENT": "production"},
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2 and "production is forbidden" in result.stderr


def test_dry_run_validates_without_importing_orm_or_touching_production_database():
    command = [
        sys.executable,
        str(
            Path(__file__).resolve().parents[1] / "scripts/import_biology_curriculum.py"
        ),
    ]
    result = subprocess.run(
        command,
        env={
            **os.environ,
            "ENVIRONMENT": "production",
            "DATABASE_URL": "postgresql://unreachable.invalid:1/must_not_connect",
        },
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
    assert "Sources and original lesson validated" in result.stdout
    assert "PostgreSQL" not in result.stdout and "Migration" not in result.stdout


def test_mobile_auth_version_is_discoverable_without_credentials(setup):
    client, _ = setup
    payload = client.get("/auth/mobile/config").json()
    assert payload["mobile_auth_version"] == 2
    assert payload["pkce_method"] == "S256"
    assert not any("secret" in key or "token" in key for key in payload)


def test_course_outline_uses_bounded_queries_for_a_whole_textbook(biology):
    _, factory, _ = biology
    from sqlalchemy import event
    from services.curriculum import course_outline

    calls = []
    engine = factory.kw["bind"]

    def record(*args):
        calls.append(args[2])

    event.listen(engine, "before_cursor_execute", record)
    try:
        with factory() as db:
            outline = course_outline(db, 1, "biologiya", 9)
        assert len(outline["chapters"]) == 8
        assert len(calls) <= 8
    finally:
        event.remove(engine, "before_cursor_execute", record)
