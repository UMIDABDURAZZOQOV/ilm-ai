"""
skill_tree.py -- lock/unlock/completed computation for the Milliy Sertifikat
skill tree. No "locked" state is stored anywhere; it's derived at read time
from completed UserLessonProgress rows + SkillLessonPrerequisite edges, the
same lazy-compute philosophy services/users.py already uses for streaks.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from services.models import (
    SkillLesson,
    SkillLessonPrerequisite,
    SkillSubject,
    SkillUnit,
    UserLessonProgress,
    UserUnitExam,
)


def get_subject_by_slug(db: Session, slug: str) -> SkillSubject | None:
    return db.query(SkillSubject).filter(SkillSubject.slug == slug).first()


def build_tree(db: Session, user_id: int, subject_slug: str) -> dict | None:
    """Returns {"subject": {...}, "units": [{...,"lessons":[{...,"status":...}]}]}
    or None if the subject doesn't exist."""
    subject = get_subject_by_slug(db, subject_slug)
    if not subject:
        return None

    units = (
        db.query(SkillUnit)
        .filter(SkillUnit.subject_id == subject.id)
        .order_by(SkillUnit.order_index)
        .all()
    )
    unit_ids = [u.id for u in units]
    lessons = (
        db.query(SkillLesson)
        .filter(SkillLesson.unit_id.in_(unit_ids))
        .order_by(SkillLesson.order_index)
        .all()
    ) if unit_ids else []
    lesson_ids = [l.id for l in lessons]

    prereqs = (
        db.query(SkillLessonPrerequisite)
        .filter(SkillLessonPrerequisite.lesson_id.in_(lesson_ids))
        .all()
    ) if lesson_ids else []
    prereq_map: dict[int, list[int]] = {}
    for p in prereqs:
        prereq_map.setdefault(p.lesson_id, []).append(p.requires_lesson_id)

    progress_rows = (
        db.query(UserLessonProgress)
        .filter(
            UserLessonProgress.user_id == user_id,
            UserLessonProgress.lesson_id.in_(lesson_ids),
        )
        .all()
    ) if lesson_ids else []
    progress_map = {p.lesson_id: p for p in progress_rows}

    completed_ids = {lid for lid, p in progress_map.items() if p.completed_at is not None}

    lessons_by_unit: dict[int, list[SkillLesson]] = {}
    for l in lessons:
        lessons_by_unit.setdefault(l.unit_id, []).append(l)

    exams = (
        db.query(UserUnitExam)
        .filter(UserUnitExam.user_id == user_id, UserUnitExam.unit_id.in_(unit_ids))
        .all()
    ) if unit_ids else []
    exam_map = {e.unit_id: e for e in exams}

    result_units = []
    # A unit's checkpoint exam gates the NEXT unit: you can't start a new bob
    # until the previous one's exam is passed. The first unit is never gated.
    gate_open = True
    for u in units:
        u_lessons = lessons_by_unit.get(u.id, [])
        # Don't retroactively lock people who were already working inside this
        # unit before checkpoints existed -- only block *entering* a fresh one.
        started_here = any(l.id in completed_ids for l in u_lessons)
        gated = (not gate_open) and not started_here

        unit_lessons = []
        for l in u_lessons:
            if l.id in completed_ids:
                status = "completed"
            elif gated:
                status = "locked"
            else:
                requires = prereq_map.get(l.id, [])
                status = "unlocked" if all(r in completed_ids for r in requires) else "locked"
            p = progress_map.get(l.id)
            unit_lessons.append({
                "id": l.id,
                "slug": l.slug,
                "title_uz": l.title_uz,
                "title_ru": l.title_ru,
                "title_en": l.title_en,
                "order_index": l.order_index,
                "xp_reward": l.xp_reward,
                "status": status,
                "stars": p.stars if p else 0,
                "best_score_pct": p.best_score_pct if p else None,
            })
        all_done = bool(u_lessons) and all(l.id in completed_ids for l in u_lessons)
        ex = exam_map.get(u.id)
        exam_passed = bool(ex and ex.passed)
        if not u_lessons:
            exam_state = "none"           # nothing to examine -- never gates
        elif exam_passed:
            exam_state = "passed"
        elif all_done and not gated:
            exam_state = "unlocked"       # every lesson done -> checkpoint opens
        else:
            exam_state = "locked"

        result_units.append({
            "id": u.id,
            "slug": u.slug,
            "title_uz": u.title_uz,
            "title_ru": u.title_ru,
            "title_en": u.title_en,
            "order_index": u.order_index,
            "lessons": unit_lessons,
            "exam": {
                "status": exam_state,
                "passed": exam_passed,
                "best_score_pct": ex.best_score_pct if ex else None,
                "attempts": ex.attempts if ex else 0,
            },
        })

        # The next unit only opens once this one's checkpoint is passed.
        gate_open = exam_passed or not u_lessons

    return {
        "subject": {
            "id": subject.id,
            "slug": subject.slug,
            "name_uz": subject.name_uz,
            "name_ru": subject.name_ru,
            "name_en": subject.name_en,
            "icon": subject.icon,
            "color": subject.color,
        },
        "units": result_units,
    }


def lesson_status(db: Session, user_id: int, lesson: SkillLesson) -> str:
    """Status for a single lesson (used by the start/complete endpoints to
    reject starting a locked lesson without pulling the whole tree)."""
    progress = (
        db.query(UserLessonProgress)
        .filter(UserLessonProgress.user_id == user_id, UserLessonProgress.lesson_id == lesson.id)
        .first()
    )
    if progress and progress.completed_at is not None:
        return "completed"

    requires = [
        p.requires_lesson_id
        for p in db.query(SkillLessonPrerequisite)
        .filter(SkillLessonPrerequisite.lesson_id == lesson.id)
        .all()
    ]
    if not requires:
        return "unlocked"

    completed_count = (
        db.query(UserLessonProgress)
        .filter(
            UserLessonProgress.user_id == user_id,
            UserLessonProgress.lesson_id.in_(requires),
            UserLessonProgress.completed_at.isnot(None),
        )
        .count()
    )
    return "unlocked" if completed_count == len(requires) else "locked"


def newly_unlocked_lesson_ids(db: Session, user_id: int, completed_lesson: SkillLesson) -> list[int]:
    """Lessons that require `completed_lesson` and now have every prerequisite
    satisfied -- used to drive the "next node unlocked" celebration on the client."""
    dependents = (
        db.query(SkillLessonPrerequisite)
        .filter(SkillLessonPrerequisite.requires_lesson_id == completed_lesson.id)
        .all()
    )
    unlocked = []
    for dep in dependents:
        lesson = db.query(SkillLesson).filter(SkillLesson.id == dep.lesson_id).first()
        if lesson and lesson_status(db, user_id, lesson) == "unlocked":
            unlocked.append(lesson.id)
    return unlocked
