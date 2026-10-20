"""Reviewed continuation, immutable foundation and real digital-activity flows."""

from copy import deepcopy
import hashlib
import json

import pytest

from test_release_hardening import setup
from test_biology_segments import answers
from services.curriculum import citation, import_curriculum, load_documents
from services.curriculum_validation import (
    CATALOG_PATH,
    load_lesson_set,
    readiness_report,
    validate_lesson,
)
from services.models import (
    SkillLesson,
    StudyEvent,
    User,
    UserLessonProgress,
    UserUnitExam,
)
from services.study import utcnow


def test_preserved_foundation_and_seven_source_catalogues_are_byte_identical():
    baseline = json.loads(
        CATALOG_PATH.with_name("biology_preserved_baseline.json").read_text()
    )
    assert (
        hashlib.sha256(CATALOG_PATH.read_bytes()).hexdigest()
        == baseline["catalog_sha256"]
    )
    for name, digest in baseline["files"].items():
        assert (
            hashlib.sha256(CATALOG_PATH.with_name(name).read_bytes()).hexdigest()
            == digest
        )
    old = load_lesson_set(batch="foundation-19")
    assert len(old) == 19
    assert sum(len(l["theory"]) for l in old) == baseline["cards"] == 72
    assert sum(len(l["questions"]) for l in old) == baseline["questions"] == 140


def test_all_209_previously_published_theory_lessons_and_activities_are_preserved():
    baseline = json.loads(
        CATALOG_PATH.with_name("biology_preserved_release09.json").read_text()
    )
    documents = []
    for name, digest in baseline["files"].items():
        path = CATALOG_PATH.with_name(name)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
        documents.append(json.loads(path.read_text()))
    assert len(documents) == 241
    assert sum("activity" not in d for d in documents) == 209
    assert sum(len(d["theory"]) for d in documents) == 1340
    assert sum(len(d["questions"]) for d in documents) == 1422


@pytest.mark.parametrize("damage", [None, "topic", "paragraph", "ocr", "pages", "mapping"])
def test_calculation_rules_have_separately_verified_supporting_paragraphs(damage):
    lesson = deepcopy(next(l for l in load_lesson_set() if l["key"] == "biology-9-paragraph-36-v1"))
    source = next(iter(lesson["facts"].values()))["source"]["supporting_sources"][0]
    if damage == "topic":
        source["topic_id"] = "missing-topic"
    elif damage == "paragraph":
        source["paragraph"] = 36
    elif damage == "ocr":
        source["verification"] = "ocr_only"
    elif damage == "pages":
        source["pdf_pages"] = source["printed_pages"] = [93]
    elif damage == "mapping":
        source["printed_pages"] = [81, 82]
    if damage:
        with pytest.raises(ValueError, match="supporting_source"):
            validate_lesson(load_documents()[0], lesson)
    else:
        validate_lesson(load_documents()[0], lesson)
        assert source["paragraph"] == 32
        assert source["pdf_pages"] == [82, 83]


@pytest.mark.parametrize("lesson", load_lesson_set(), ids=lambda l: l["key"])
def test_every_published_lesson_has_taught_answers_and_matching_source_pages(lesson):
    catalog, _ = load_documents()
    book, topic = validate_lesson(catalog, lesson)
    assert book["grade"] in range(5, 12)
    assert topic["id"] == lesson["topic_id"]
    for fact in lesson["facts"].values():
        assert fact["source"]["reviewed_on"]
        assert fact["claim"].strip()


def test_distinct_continuation_questions_and_honest_theory_activity_counts():
    catalog, _ = load_documents()
    lessons = load_lesson_set()
    texts = [
        q["question_text"].strip().casefold() for l in lessons for q in l["questions"]
    ]
    assert len(texts) == len(set(texts)), "Do not inflate counts with duplicate prompts"
    report = readiness_report(catalog, lessons)
    assert sum(r["topics"] for r in report) == 355
    assert sum(r["ready_theory_lessons"] for r in report) == 233
    assert sum(r["ready_activities"] for r in report) == 36
    assert all(r["course_ready"] for r in report[:4])
    assert not any(r["course_ready"] for r in report[4:])
    for row in report[:4]:
        assert row["remaining_topics"] == 0
        assert row["remaining_activity_ids"] == []


def test_release_batches_preserve_foundation_and_add_twenty_to_thirty_theory_topics():
    index = json.loads(CATALOG_PATH.with_name("biology_lessons.json").read_text())
    catalog, _ = load_documents()
    published = set(index["batches"]["foundation-19"])
    for name, filenames in index["batches"].items():
        if not name.startswith("continuation-"):
            continue
        assert not published.intersection(filenames), f"Republished lessons in {name}"
        documents = load_lesson_set(batch=name)
        records = [validate_lesson(catalog, document)[1] for document in documents]
        assert 20 <= sum(r["kind"] == "topic" for r in records) <= 30
        published.update(filenames)
    assert published == set(index["lessons"]), "Unreleased drafts must not enter import"


@pytest.mark.parametrize("damage", ["physical", "step", "source", "answer"])
def test_activity_cannot_claim_physical_execution_or_lose_evidence(damage):
    lesson = deepcopy(next(l for l in load_lesson_set() if "activity" in l))
    if damage == "physical":
        lesson["activity"]["physical_execution_required"] = True
    elif damage == "step":
        lesson["activity"]["steps"][0]["fact_ids"] = ["unverified"]
    elif damage == "source":
        next(iter(lesson["facts"].values()))["source"]["verification"] = "ocr_only"
    else:
        lesson["questions"][0]["correct_answer"] = "unverified"
    with pytest.raises(ValueError):
        validate_lesson(load_documents()[0], lesson)


@pytest.mark.parametrize(
    "grade,topic_id,number,paragraph",
    [
        (7, "bio-7-laboratory-8", 1, None),
        (7, "bio-7-laboratory-20", 2, None),
        (7, "bio-7-laboratory-34", 3, None),
        (7, "bio-7-laboratory-45", 4, None),
        (7, "bio-7-laboratory-62", 5, None),
        (9, "bio-9-laboratory-36", 4, 29),
        (9, "bio-9-practical-64", 1, 51),
        (10, "bio-10-laboratory-52", 4, None),
        (11, "bio-11-laboratory-53", 5, None),
    ],
)
def test_citation_uses_printed_activity_number_and_preserves_catalogue_id(
    grade, topic_id, number, paragraph
):
    book = next(b for b in load_documents()[0]["books"] if b["grade"] == grade)
    topic = next(r for r in book["records"] if r["id"] == topic_id)
    result = citation(
        book,
        topic,
        {
            "paragraph": topic["paragraph"],
            "pdf_pages": [topic["pdf_start"]],
            "printed_pages": [topic["printed_start"]],
        },
    )
    assert result["activity_number"] == number
    assert result["topic_id"] == topic_id
    assert result["paragraph"] == paragraph


def test_complete_grades5_to8_and_grade9_continuation_api_once_only_xp(setup, tmp_path):
    client, factory = setup
    catalog, _ = load_documents()
    lessons = load_lesson_set()
    bykey = {l["key"]: l for l in lessons}
    with factory.begin() as db:
        for lesson in lessons:
            import_curriculum(db, catalog, lesson)
    xp = events = checkpoints = 0
    for grade in (5, 6, 7, 8, 9):
        tree = client.get(f"/skills/1/tree?subject=biologiya&grade={grade}").json()
        units = tree["units"]
        for unit in units:
            if grade in (5, 6, 7, 8):
                assert unit["coverage_complete"]
            for row in unit["lessons"]:
                lid = row["id"]
                issued = client.post(
                    f"/skills/lessons/{lid}/start", json={"user_id": 1}
                )
                assert issued.status_code == 200, issued.text
                data = issued.json()
                for q in data["questions"]:
                    assert q["source"]["chapter_title"]
                    assert q["source"]["topic_title"]
                    if "activity" in bykey[row["slug"]]:
                        number = int(row["slug"].rsplit("-", 2)[1])
                        assert q["source"]["activity_number"] == number
                        first_fact = next(iter(bykey[row["slug"]]["facts"].values()))
                        assert q["source"]["paragraph"] == first_fact["source"]["paragraph"]
                reward = bykey[row["slug"]]["xp_reward"]
                body = {
                    "user_id": 1,
                    "attempt_id": data["attempt_id"],
                    "results": answers(data),
                }
                result = client.post(f"/skills/lessons/{lid}/complete", json=body)
                assert result.status_code == 200, result.text
                assert result.json()["xp_awarded"] == reward
                assert (
                    client.post(f"/skills/lessons/{lid}/complete", json=body).json()
                    == result.json()
                )
                xp += reward
                events += 1
                if "laboratory-1" in row["slug"] and grade == 5:
                    assert all(
                        q["source"]["paragraph"] is None for q in data["questions"]
                    )
                    (tmp_path / "biology_activity_lesson.json").write_text(
                        json.dumps(data, ensure_ascii=False, indent=2) + "\n"
                    )
                    (tmp_path / "biology_activity_row.json").write_text(
                        json.dumps(row, ensure_ascii=False, indent=2) + "\n"
                    )
                    (tmp_path / "biology_activity_result.json").write_text(
                        json.dumps(result.json(), ensure_ascii=False, indent=2) + "\n"
                    )
            exam = client.get(f"/skills/1/unit-exam?unit_id={unit['id']}")
            if not unit["coverage_complete"]:
                assert exam.status_code == 409
                break
            assert exam.status_code == 200, exam.text
            data = exam.json()
            body = {
                "user_id": 1,
                "unit_id": unit["id"],
                "attempt_id": data["attempt_id"],
                "results": answers(data),
            }
            result = client.post("/skills/unit-exam/complete", json=body)
            assert result.status_code == 200, result.text
            assert (
                client.post("/skills/unit-exam/complete", json=body).json()
                == result.json()
            )
            xp += result.json()["xp_awarded"]
            events += 1
            checkpoints += 1
        outline = client.get(
            f"/skills/1/curriculum?subject=biologiya&grade={grade}"
        ).json()
        assert outline["completed"] is (grade < 9)
        assert outline["next_grade"] == (grade + 1 if grade < 9 else None)
    with factory.begin() as db:
        assert db.get(User, 1).xp_total == xp
        assert db.query(StudyEvent).count() == events
        assert db.query(UserLessonProgress).count() == events - checkpoints
        for lesson in lessons:
            assert not import_curriculum(db, catalog, lesson)["created"]
        assert db.get(User, 1).xp_total == xp


def test_missing_activity_blocks_checkpoint_and_later_lesson_without_erasing_progress(
    setup,
):
    client, factory = setup
    catalog, _ = load_documents()
    lessons = {l["key"]: l for l in load_lesson_set()}
    with factory.begin() as db:
        ids = [
            import_curriculum(db, catalog, l)["lesson_id"]
            for l in load_lesson_set(batch="foundation-19")[:4]
        ]
        unit_id = db.get(SkillLesson, ids[0]).unit_id
        db.add(
            UserLessonProgress(
                user_id=1,
                lesson_id=ids[2],
                stars=2,
                attempts=1,
                xp_earned=20,
                completed_at=utcnow(),
            )
        )
        db.add(UserUnitExam(user_id=1, unit_id=unit_id, passed=True))
        db.get(User, 1).xp_total = 73
        import_curriculum(db, catalog, lessons["biology-5-laboratory-1-v1"])
    tree = client.get("/skills/1/tree?subject=biologiya&grade=5").json()
    assert not tree["units"][0]["coverage_complete"]
    last = next(l for l in tree["units"][0]["lessons"] if l["id"] == ids[3])
    assert last["status"] == "locked"
    assert (
        client.post(f"/skills/lessons/{ids[3]}/start", json={"user_id": 1}).status_code
        == 403
    )
    assert client.get(f"/skills/1/unit-exam?unit_id={unit_id}").status_code == 409
    with factory.begin() as db:
        assert db.get(User, 1).xp_total == 73
        assert db.query(UserLessonProgress).one().stars == 2
        assert db.query(UserUnitExam).one().passed
