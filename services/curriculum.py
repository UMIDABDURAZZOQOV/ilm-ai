"""Source-traceable, additive grade paths using existing lesson/progress APIs."""

from __future__ import annotations

import hashlib
import json

from fastapi import HTTPException
from sqlalchemy import func

from services.models import (
    CurriculumChapter,
    CurriculumCourse,
    CurriculumLessonSource,
    CurriculumTopic,
    SkillLesson,
    SkillQuestion,
    SkillSubject,
    SkillUnit,
    UserLessonProgress,
    UserUnitExam,
)

from services.curriculum_validation import (
    load_documents as load_documents,
    validate_catalog as validate_catalog,
    validate_lesson as validate_lesson,
)


def citation(book, topic, source):
    return {
        "book_id": book["id"],
        "book_title": book["title"],
        "authors": book["authors"],
        "year": book["year"],
        "file_name": book["file_name"],
        "sha256": book["sha256"],
        "chapter_id": topic["chapter_id"],
        "topic_id": topic["id"],
        **source,
    }


def import_curriculum(db, catalog, lesson):
    """Caller controls one transaction. Never deletes or rewrites legacy progress.

    Published lessons are immutable; changed content requires a new reviewed key.
    Startup never calls this function; the CLI only allows explicit local SQLite.
    """
    book, source_topic = validate_lesson(catalog, lesson)
    subject = db.query(SkillSubject).filter_by(slug="biologiya").first()
    if not subject:
        subject = SkillSubject(
            slug="biologiya",
            name_uz="Biologiya",
            name_ru="Биология",
            name_en="Biology",
            icon="biology",
            color="#2DD4BF",
            is_active=True,
            order_index=(db.query(func.max(SkillSubject.order_index)).scalar() or 0)
            + 1,
        )
        db.add(subject)
        db.flush()
    next_order = (
        db.query(func.max(SkillUnit.order_index))
        .filter_by(subject_id=subject.id)
        .scalar()
        or 0
    ) + 1
    chapter_map = {}
    for item in catalog["books"]:
        course = (
            db.query(CurriculumCourse)
            .filter_by(subject_id=subject.id, grade=item["grade"])
            .first()
        )
        if course and course.catalog != item:
            raise ValueError("catalog_changed_requires_reviewed_migration")
        if not course:
            course = CurriculumCourse(
                subject_id=subject.id,
                grade=item["grade"],
                title_uz=item["title"],
                source_book_id=item["id"],
                status=item["status"],
                catalog=item,
            )
            db.add(course)
            db.flush()
        for record in item["records"]:
            if record["kind"] != "chapter":
                continue
            chapter = (
                db.query(CurriculumChapter)
                .filter_by(course_id=course.id, source_key=record["id"])
                .first()
            )
            if not chapter:
                unit = SkillUnit(
                    subject_id=subject.id,
                    slug=f"bio-{item['grade']}-{record['id']}",
                    title_uz=record["title"],
                    title_ru=record["title"],
                    title_en=record["title"],
                    order_index=next_order,
                )
                next_order += 1
                db.add(unit)
                db.flush()
                chapter = CurriculumChapter(
                    course_id=course.id, source_key=record["id"], unit_id=unit.id
                )
                db.add(chapter)
                db.flush()
            chapter_map[record["id"]] = chapter
        for record in item["records"]:
            if record["kind"] not in {"topic", "laboratory", "practical"}:
                continue
            if not db.get(CurriculumTopic, record["id"]):
                chapter = chapter_map[record["chapter_id"]]
                db.add(
                    CurriculumTopic(
                        id=record["id"],
                        chapter_id=chapter.id,
                        kind=record["kind"],
                        title_uz=record["title"],
                        source={"book_id": item["id"], **record},
                    )
                )
    db.flush()
    checksum = hashlib.sha256(
        json.dumps(lesson, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()
    existing = (
        db.query(CurriculumLessonSource).filter_by(content_key=lesson["key"]).first()
    )
    if existing:
        if existing.content_sha256 != checksum:
            raise ValueError("published_content_is_immutable_use_new_reviewed_key")
        return {"lesson_id": existing.lesson_id, "created": False}
    chapter = chapter_map[source_topic["chapter_id"]]
    refs = [citation(book, source_topic, f["source"]) for f in lesson["facts"].values()]
    references = list({json.dumps(r, sort_keys=True): r for r in refs}.values())
    theory = []
    for card in lesson["theory"]:
        src = citation(
            book, source_topic, lesson["facts"][card["fact_ids"][0]]["source"]
        )
        theory.append({"title": card["title"], "body": card["body"], "source": src})
    row = SkillLesson(
        unit_id=chapter.unit_id,
        slug=lesson["key"],
        title_uz=lesson["title"],
        title_ru=lesson["title"],
        title_en=lesson["title"],
        order_index=(
            source_topic["paragraph"] * 1000
            + (
                db.query(func.count(CurriculumLessonSource.lesson_id))
                .filter_by(topic_id=source_topic["id"])
                .scalar()
                or 0
            )
        )
        + 1,
        xp_reward=lesson["xp_reward"],
        theory=theory,
    )
    db.add(row)
    db.flush()
    question_refs = {}
    for i, q in enumerate(lesson["questions"]):
        question = SkillQuestion(
            lesson_id=row.id,
            order_index=i,
            language="uz",
            question_type="mcq",
            question_text=q["question_text"],
            options=q["options"],
            correct_answer=q["correct_answer"],
            explanation=q["explanation"],
            difficulty="easy",
        )
        db.add(question)
        db.flush()
        question_refs[str(question.id)] = citation(
            book, source_topic, lesson["facts"][q["fact_id"]]["source"]
        )
    db.add(
        CurriculumLessonSource(
            lesson_id=row.id,
            topic_id=source_topic["id"],
            content_key=lesson["key"],
            content_sha256=checksum,
            references=references,
            question_references=question_refs,
        )
    )
    db.flush()
    return {"lesson_id": row.id, "created": True}


def grade_for_unit(db, unit_id):
    return (
        db.query(CurriculumCourse.grade)
        .join(CurriculumChapter, CurriculumChapter.course_id == CurriculumCourse.id)
        .filter(CurriculumChapter.unit_id == unit_id)
        .scalar()
    )


def question_sources(db, ids):
    lesson_ids = db.query(SkillQuestion.lesson_id).filter(SkillQuestion.id.in_(ids))
    rows = (
        db.query(CurriculumLessonSource)
        .filter(CurriculumLessonSource.lesson_id.in_(lesson_ids))
        .all()
    )
    return {
        int(qid): ref
        for row in rows
        for qid, ref in row.question_references.items()
        if int(qid) in ids
    }


def chapter_coverage_map(db, unit_ids):
    rows = (
        db.query(
            CurriculumChapter.unit_id,
            CurriculumTopic.id,
            CurriculumLessonSource.topic_id,
        )
        .outerjoin(
            CurriculumTopic,
            (CurriculumTopic.chapter_id == CurriculumChapter.id)
            & (CurriculumTopic.kind == "topic"),
        )
        .outerjoin(
            CurriculumLessonSource,
            CurriculumLessonSource.topic_id == CurriculumTopic.id,
        )
        .filter(CurriculumChapter.unit_id.in_(unit_ids))
        .all()
    )
    expected, ready = {}, {}
    for unit, topic, published in rows:
        expected.setdefault(unit, set())
        ready.setdefault(unit, set())
        if topic:
            expected[unit].add(topic)
        if published:
            ready[unit].add(published)
    return {
        unit: bool(topics) and topics == ready[unit]
        for unit, topics in expected.items()
    }


def chapter_coverage(db, unit_id):
    return chapter_coverage_map(db, [unit_id]).get(unit_id, True)


def grade_list(db, subject_slug):
    subject = db.query(SkillSubject).filter_by(slug=subject_slug).first()
    if not subject:
        raise HTTPException(404, "Subject not found")
    out = []
    for row in (
        db.query(CurriculumCourse)
        .filter_by(subject_id=subject.id)
        .order_by(CurriculumCourse.grade)
    ):
        ready = (
            db.query(CurriculumLessonSource)
            .join(CurriculumTopic)
            .join(CurriculumChapter)
            .filter(CurriculumChapter.course_id == row.id)
            .count()
        )
        out.append(
            {
                "grade": row.grade,
                "title_uz": row.title_uz,
                "status": row.status,
                "ready_lessons": ready,
                "book_id": row.source_book_id,
                "language": "uz",
            }
        )
    return {"subject": subject_slug, "grades": out}


def course_outline(db, user_id, subject_slug, grade):
    subject = db.query(SkillSubject).filter_by(slug=subject_slug).first()
    course = (
        db.query(CurriculumCourse).filter_by(subject_id=subject.id, grade=grade).first()
        if subject
        else None
    )
    if not course:
        raise HTTPException(404, "Grade path not found")
    chapter_rows = (
        db.query(CurriculumChapter)
        .filter_by(course_id=course.id)
        .order_by(CurriculumChapter.id)
        .all()
    )
    chapter_ids = [c.id for c in chapter_rows]
    unit_ids = [c.unit_id for c in chapter_rows]
    units = {u.id: u for u in db.query(SkillUnit).filter(SkillUnit.id.in_(unit_ids))}
    topic_rows = (
        db.query(CurriculumTopic)
        .filter(CurriculumTopic.chapter_id.in_(chapter_ids))
        .all()
    )
    topic_rows.sort(
        key=lambda topic: (
            topic.source["pdf_start"],
            topic.source["verification"].get("heading_offset", 0),
        )
    )
    topic_ids = [t.id for t in topic_rows]
    lessons = (
        db.query(CurriculumLessonSource, UserLessonProgress)
        .outerjoin(
            UserLessonProgress,
            (UserLessonProgress.lesson_id == CurriculumLessonSource.lesson_id)
            & (UserLessonProgress.user_id == user_id),
        )
        .filter(CurriculumLessonSource.topic_id.in_(topic_ids))
        .all()
    )
    by_topic = {}
    for row, progress in lessons:
        by_topic.setdefault(row.topic_id, []).append((row, progress))
    exams = {
        e.unit_id: e
        for e in db.query(UserUnitExam).filter(
            UserUnitExam.user_id == user_id, UserUnitExam.unit_id.in_(unit_ids)
        )
    }
    chapters = []
    all_complete = bool(chapter_rows)
    for chapter in chapter_rows:
        unit = units[chapter.unit_id]
        topics = []
        for topic in topic_rows:
            if topic.chapter_id != chapter.id:
                continue
            rows = by_topic.get(topic.id, [])
            completed = bool(rows) and all(p and p.completed_at for _, p in rows)
            topics.append(
                {
                    "id": topic.id,
                    "kind": topic.kind,
                    "title_uz": topic.title_uz,
                    "source": topic.source,
                    "lesson_ids": [r.lesson_id for r, _ in rows],
                    "ready": bool(rows),
                    "completed": bool(completed),
                }
            )
            if topic.kind == "topic" and not completed:
                all_complete = False
        exam = exams.get(unit.id)
        if not exam or not exam.passed:
            all_complete = False
        required = [t for t in topics if t["kind"] == "topic"]
        chapters.append(
            {
                "unit_id": unit.id,
                "title_uz": unit.title_uz,
                "topics": topics,
                "coverage_complete": bool(required)
                and all(t["ready"] for t in required),
                "checkpoint_passed": bool(exam and exam.passed),
            }
        )
    return {
        "subject": subject_slug,
        "grade": grade,
        "title_uz": course.title_uz,
        "status": course.status,
        "book": {k: v for k, v in course.catalog.items() if k != "records"},
        "chapters": chapters,
        "completed": all_complete,
        "next_grade": grade + 1 if all_complete and grade < 11 else None,
    }
