"""Request-scoped publication policy; legacy website sessions are unaffected.

The mobile namespace exposes reviewed, explicitly indexed curriculum content.
No subject, lesson, progress, or historical XP row is changed by this policy.
"""

from functools import lru_cache
import hashlib
import json
import os

from fastapi import Depends, HTTPException, Request
from sqlalchemy import event, select, tuple_
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.orm import with_loader_criteria

from services.db import get_db
from services.models import (
    CurriculumChapter, CurriculumCourse, CurriculumLessonSource, CurriculumTopic,
    SkillLesson, SkillMistake, SkillQuestion, SkillSubject, SkillUnit,
)
from services.curriculum_validation import load_lesson_set


def published_subjects():
    return frozenset(s.strip() for s in os.getenv(
        "MOBILE_PUBLISHED_SUBJECTS", "biologiya"
    ).split(",") if s.strip())


@lru_cache(maxsize=1)
def reviewed_content():
    return tuple((lesson["key"], hashlib.sha256(json.dumps(
        lesson, sort_keys=True, ensure_ascii=False
    ).encode()).hexdigest()) for lesson in load_lesson_set())


def ensure_mobile_questions(db, questions):
    if not db.info.get("mobile_publication") or not questions:
        return
    ids = {q["id"] for q in questions}
    visible = {row[0] for row in db.query(SkillQuestion.id).filter(
        SkillQuestion.id.in_(ids)
    )}
    if visible != ids:
        raise HTTPException(409, "mobile_attempt_unavailable")


async def mobile_publication(request: Request, db=Depends(get_db)):
    """Apply one policy to catalogue, direct IDs, practice pools and statistics.

    Loader criteria apply before LIMIT/sample/aggregate queries. Raw publication
    tables deliberately avoid recursively applying criteria inside the policy.
    The listener is removed after this request; web queries use normal sessions.
    """
    slugs = published_subjects()
    path = request.url.path
    if any(part in path for part in (
        "/level-test", "/pronunciation", "/written-exam", "/cron/",
    )):
        raise HTTPException(404, "mobile_feature_not_published")
    if path.endswith("/tree") and request.query_params.get("grade") is None:
        raise HTTPException(422, "mobile_grade_required")
    for field in ("subject", "subject_slug"):
        value = request.query_params.get(field) or request.path_params.get(field)
        if value is not None and value not in slugs:
            raise HTTPException(404, "mobile_subject_not_published")
    if request.method == "POST":
        try:
            body = await request.json()
        except ValueError:
            raise HTTPException(422, "invalid_request_body") from None
        if isinstance(body, dict):
            for field in ("subject", "subject_slug"):
                if body.get(field) is not None and (
                    not isinstance(body[field], str) or body[field] not in slugs
                ):
                    raise HTTPException(404, "mobile_subject_not_published")
            if path.endswith("/preferences") and body.get("grade") is not None:
                if body["grade"] not in [str(g) for g in range(5, 12)]:
                    raise HTTPException(422, "mobile_grade_out_of_range")
    source = CurriculumLessonSource.__table__
    lesson, unit, subject = SkillLesson.__table__, SkillUnit.__table__, SkillSubject.__table__
    topic, chapter, course = CurriculumTopic.__table__, CurriculumChapter.__table__, CurriculumCourse.__table__
    statement = select(source.c.lesson_id, unit.c.id, subject.c.id, chapter.c.id, course.c.id).select_from(
        source.join(lesson, lesson.c.id == source.c.lesson_id)
        .join(unit, unit.c.id == lesson.c.unit_id)
        .join(subject, subject.c.id == unit.c.subject_id)
        .join(topic, topic.c.id == source.c.topic_id)
        .join(chapter, chapter.c.id == topic.c.chapter_id)
        .join(course, course.c.id == chapter.c.course_id)
    ).where(
        subject.c.slug.in_(slugs), subject.c.is_active.is_(True),
        course.c.status == "mapped", course.c.grade.between(5, 11),
        chapter.c.unit_id == unit.c.id, course.c.subject_id == subject.c.id,
        tuple_(source.c.content_key, source.c.content_sha256).in_(reviewed_content()),
    )
    try:
        rows = db.execute(statement).all()
    except (OperationalError, ProgrammingError):
        db.rollback()
        raise HTTPException(503, "mobile_schema_not_ready") from None
    lesson_ids, unit_ids, subject_ids, chapter_ids, course_ids = (
        tuple({r[i] for r in rows}) for i in range(5)
    )
    if path.endswith("/subjects") and slugs and not lesson_ids:
        raise HTTPException(503, "mobile_curriculum_not_imported")
    # Keep every mapped chapter/topic of the visible course, including content
    # gaps. Filtering out empty chapters would falsely mark a partial course
    # completed and bypass its existing prerequisite checks.
    mapped = db.execute(select(chapter.c.id, chapter.c.unit_id).where(
        chapter.c.course_id.in_(course_ids)
    )).all()
    chapter_ids = tuple(r[0] for r in mapped)
    unit_ids = tuple(r[1] for r in mapped)
    criteria = [
        with_loader_criteria(SkillSubject, SkillSubject.id.in_(subject_ids), include_aliases=True),
        with_loader_criteria(SkillUnit, SkillUnit.id.in_(unit_ids), include_aliases=True),
        with_loader_criteria(SkillLesson, SkillLesson.id.in_(lesson_ids), include_aliases=True),
        with_loader_criteria(SkillQuestion, SkillQuestion.lesson_id.in_(lesson_ids), include_aliases=True),
        with_loader_criteria(SkillMistake, SkillMistake.question_id.in_(
            select(SkillQuestion.__table__.c.id).where(SkillQuestion.__table__.c.lesson_id.in_(lesson_ids))
        ), include_aliases=True),
        with_loader_criteria(CurriculumCourse, CurriculumCourse.id.in_(course_ids), include_aliases=True),
        with_loader_criteria(CurriculumChapter, CurriculumChapter.id.in_(chapter_ids), include_aliases=True),
        with_loader_criteria(CurriculumTopic, CurriculumTopic.chapter_id.in_(chapter_ids), include_aliases=True),
        with_loader_criteria(CurriculumLessonSource, CurriculumLessonSource.lesson_id.in_(lesson_ids), include_aliases=True),
    ]

    def scope_queries(execute_state):
        if execute_state.is_select:
            execute_state.statement = execute_state.statement.options(*criteria)

    event.listen(db, "do_orm_execute", scope_queries)
    db.info["mobile_publication"] = True
    try:
        yield
    finally:
        db.info.pop("mobile_publication", None)
        event.remove(db, "do_orm_execute", scope_queries)
