"""Pinned scanned sources and the real first-chapter lesson set, in isolated QA DBs."""

from copy import deepcopy
import json
import pytest

from test_release_hardening import setup
from services.curriculum import citation, import_curriculum, load_documents
from services.curriculum_validation import (
    CATALOG_PATH,
    load_lesson_set,
    readiness_report,
    validate_catalog,
)
from services.models import (
    CurriculumChapter,
    CurriculumCourse,
    CurriculumLessonSource,
    StudyEvent,
    User,
    UserLessonProgress,
)


@pytest.fixture
def batch(setup):
    client, factory = setup
    catalog, _ = load_documents()
    with factory.begin() as db:
        for lesson in load_lesson_set():
            assert import_curriculum(db, catalog, lesson)["created"]
    return client, factory


def answers(issued):
    return [
        {
            "question_id": q["id"],
            "answer_index": q["options"].index(q["correct_answer"]),
            "is_correct": False,
        }
        for q in issued["questions"]
    ]


@pytest.mark.parametrize("grade", range(5, 12))
def test_real_chapter_flow_server_grading_sources_checkpoints_and_once_only_xp(
    batch, grade
):
    client, factory = batch
    tree = client.get(f"/skills/1/tree?subject=biologiya&grade={grade}").json()
    ready = tree["units"][: 2 if grade == 8 else 1]
    assert all(u["coverage_complete"] for u in ready)
    if grade == 8:
        second = ready[1]["lessons"][0]["id"]
        assert (
            client.post(
                f"/skills/lessons/{second}/start", json={"user_id": 1}
            ).status_code
            == 403
        )
    xp = lessons = 0
    for unit in ready:
        for lesson in unit["lessons"]:
            lid = lesson["id"]
            start = client.post(
                f"/skills/lessons/{lid}/start", json={"user_id": 1, "language": "en"}
            )
            assert start.status_code == 200, start.text
            data = start.json()
            assert data["content_language"] == "uz" and data["theory"]
            for q in data["questions"]:
                src = q["source"]
                assert src["pdf_pages"] and q["explanation"]
                if grade in (6, 8):
                    assert "sha256" not in src and src["source_set_sha256"]
                    assert src["source_segments"]
                    assert all(
                        1 <= p <= 48
                        for part in src["source_segments"]
                        for p in part["segment_pdf_pages"]
                    )
            body = {
                "user_id": 1,
                "attempt_id": data["attempt_id"],
                "results": answers(data),
            }
            response = client.post(f"/skills/lessons/{lid}/complete", json=body)
            assert response.status_code == 200, response.text
            assert response.json()["xp_awarded"] == 20 and response.json()[
                "score"
            ] == len(data["questions"])
            assert (
                client.post(f"/skills/lessons/{lid}/complete", json=body).json()
                == response.json()
            )
            lessons += 1
            xp += 20
        exam = client.get(f"/skills/1/unit-exam?unit_id={unit['id']}&language=ru")
        assert exam.status_code == 200, exam.text
        issued = exam.json()
        assert all(q["source"]["book_id"] for q in issued["questions"])
        body = {
            "user_id": 1,
            "unit_id": unit["id"],
            "attempt_id": issued["attempt_id"],
            "results": answers(issued),
        }
        result = client.post("/skills/unit-exam/complete", json=body)
        assert result.status_code == 200, result.text
        assert (
            client.post("/skills/unit-exam/complete", json=body).json() == result.json()
        )
        xp += result.json()["xp_awarded"]
    outline = client.get(f"/skills/1/curriculum?subject=biologiya&grade={grade}").json()
    assert not outline["completed"] and outline["next_grade"] is None
    assert all(not c["coverage_complete"] for c in outline["chapters"][len(ready) :])
    assert all(c["checkpoint_passed"] for c in outline["chapters"][: len(ready)])
    with factory.begin() as db:
        assert db.get(User, 1).xp_total == xp
        assert db.query(StudyEvent).count() == lessons + len(ready)
        assert db.query(UserLessonProgress).filter_by(user_id=1).count() == lessons
        catalog, _ = load_documents()
        for lesson in load_lesson_set():
            assert not import_curriculum(db, catalog, lesson)["created"]
        assert db.get(User, 1).xp_total == xp
        assert db.query(StudyEvent).count() == lessons + len(ready)


def test_explicit_blocked_source_upgrade_preserves_course_ids_content_and_progress(
    setup,
):
    _, factory = setup
    catalog, lesson = load_documents()
    old = deepcopy(catalog)
    for i, b in enumerate(old["books"]):
        if b["grade"] in (6, 8):
            old["books"][i] = {
                "id": f"biology-{b['grade']}-unavailable",
                "grade": b["grade"],
                "file_name": b["file_name"],
                "title": b["title"],
                "status": "blocked_transfer_limit_32_mib",
                "records": [],
            }
    with factory.begin() as db:
        prior = import_curriculum(db, old, lesson)
        lid = prior["lesson_id"]
        db.get(User, 1).xp_total = 73
        db.add(
            UserLessonProgress(
                user_id=1, lesson_id=lid, stars=2, attempts=1, xp_earned=20
            )
        )
        digest = db.get(CurriculumLessonSource, lid).content_sha256
        ids = {c.grade: c.id for c in db.query(CurriculumCourse)}
    with pytest.raises(ValueError, match="reviewed_migration"), factory.begin() as db:
        import_curriculum(db, catalog, lesson)
    with factory.begin() as db:
        assert not import_curriculum(db, catalog, lesson, allow_source_upgrade=True)[
            "created"
        ]
        assert {c.grade: c.id for c in db.query(CurriculumCourse)} == ids
        assert db.query(CurriculumChapter).count() == 47
        assert db.get(User, 1).xp_total == 73
        assert db.get(CurriculumLessonSource, lid).content_sha256 == digest
        assert db.query(UserLessonProgress).filter_by(lesson_id=lid).one().stars == 2
    changed = deepcopy(catalog)
    changed["books"][0]["title"] = "Unreviewed replacement"
    with pytest.raises(ValueError, match="reviewed_migration"), factory.begin() as db:
        import_curriculum(db, changed, lesson, allow_source_upgrade=True)


def test_unwritten_earlier_paragraph_blocks_later_lesson_in_tree_and_api(setup):
    client, factory = setup
    catalog, _ = load_documents()
    bykey = {l["key"]: l for l in load_lesson_set()}
    with factory.begin() as db:
        second = import_curriculum(db, catalog, bykey["biology-6-paragraph-2-v1"])[
            "lesson_id"
        ]
    tree = client.get("/skills/1/tree?subject=biologiya&grade=6").json()
    assert tree["units"][0]["lessons"][0]["status"] == "locked"
    assert (
        client.post(f"/skills/lessons/{second}/start", json={"user_id": 1}).status_code
        == 403
    )
    with factory.begin() as db:
        first = import_curriculum(db, catalog, bykey["biology-6-paragraph-1-v1"])[
            "lesson_id"
        ]
    tree = client.get("/skills/1/tree?subject=biologiya&grade=6").json()
    assert [l["id"] for l in tree["units"][0]["lessons"]] == [first, second]
    assert [l["status"] for l in tree["units"][0]["lessons"]] == ["unlocked", "locked"]


@pytest.mark.parametrize(
    "damage", ["gap", "overlap", "count", "digest", "whole_pdf_hash"]
)
def test_split_provenance_rejects_gaps_overlap_and_false_whole_pdf_hash(damage):
    catalog, _ = deepcopy(load_documents())
    book = catalog["books"][1]
    if damage == "gap":
        book["segments"][1]["start"] += 1
    elif damage == "overlap":
        book["segments"][1]["start"] -= 1
    elif damage == "count":
        book["segments"][0]["pages"] = 35
    elif damage == "whole_pdf_hash":
        book["sha256"] = "0" * 64
    else:
        book["source_set_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="source_"):
        validate_catalog(catalog)


def test_original_pdf_page_maps_to_local_segment_page_without_renumbering():
    catalog, _ = load_documents()
    book = catalog["books"][1]
    topic = next(r for r in book["records"] if r.get("paragraph") == 30)
    # Mapping only: no claim that this unwritten paragraph was fact-reviewed.
    ref = citation(
        book, topic, {"paragraph": 30, "pdf_pages": [73], "printed_pages": [73]}
    )
    assert ref["source_segments"][0]["file_name"].endswith("073-108.pdf")
    assert ref["source_segments"][0]["segment_pdf_pages"] == [1]
    assert ref["pdf_pages"] == [73] and "sha256" not in ref


def test_readiness_snapshot_counts_only_explicit_reviewed_lessons():
    catalog, _ = load_documents()
    lessons = load_lesson_set()
    report = readiness_report(catalog, lessons)
    assert (
        json.loads(CATALOG_PATH.with_name("biology_readiness.json").read_text())
        == report
    )
    assert [(r["grade"], r["ready_lessons"]) for r in report] == [
        (5, 4),
        (6, 3),
        (7, 2),
        (8, 4),
        (9, 2),
        (10, 2),
        (11, 2),
    ]
    assert len(lessons) == 19 and sum(len(l["questions"]) for l in lessons) == 140
    assert not any(r["course_ready"] for r in report)


def test_question_evidence_must_be_present_in_the_teaching_cards():
    from services.curriculum_validation import validate_lesson

    catalog, lesson = deepcopy(load_documents())
    assessed = lesson["questions"][0]["fact_id"]
    for card in lesson["theory"]:
        card["fact_ids"] = [f for f in card["fact_ids"] if f != assessed]
        # Preserve valid nonempty cards to isolate the assessment linkage.
        if not card["fact_ids"]:
            card["fact_ids"] = [next(f for f in lesson["facts"] if f != assessed)]
    with pytest.raises(ValueError, match="assessed_fact_must_be_taught"):
        validate_lesson(catalog, lesson)


def test_full_batch_dry_run_is_safe_with_a_production_database_url():
    import os
    import subprocess
    import sys

    result = subprocess.run(
        [
            sys.executable,
            str(CATALOG_PATH.parents[1] / "import_biology_curriculum.py"),
            "--all",
        ],
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
    assert "19 reviewed lesson(s)" in result.stdout
    assert "Grade 8: 13 chapters, 61 topics, 4 ready lessons" in result.stdout
    assert "Migration" not in result.stdout
