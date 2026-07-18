"""
skill_stats.py -- shared read-only student-progress summaries, reused by the
teacher/class roster and the parent dashboard so both show the same numbers as
the learner's own profile screen. Pure queries, no mutation.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from sqlalchemy import func as sa_func
from sqlalchemy.orm import Session

from services.models import (
    SkillLesson,
    SkillLessonAttempt,
    SkillSubject,
    SkillUnit,
    User,
    UserLessonProgress,
)


def _weekly_xp(db: Session, user_id: int) -> int:
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    return int(
        db.query(sa_func.coalesce(sa_func.sum(SkillLessonAttempt.xp_awarded), 0))
        .filter(SkillLessonAttempt.user_id == user_id, SkillLessonAttempt.completed_at >= week_ago)
        .scalar()
        or 0
    )


def _subject_progress(db: Session, user_id: int) -> list[dict]:
    subjects = (
        db.query(SkillSubject)
        .filter(SkillSubject.is_active.is_(True))
        .order_by(SkillSubject.order_index)
        .all()
    )
    out: list[dict] = []
    for s in subjects:
        unit_ids = [u.id for u in db.query(SkillUnit).filter(SkillUnit.subject_id == s.id).all()]
        lesson_ids = (
            [l.id for l in db.query(SkillLesson).filter(SkillLesson.unit_id.in_(unit_ids)).all()]
            if unit_ids else []
        )
        total = len(lesson_ids)
        completed = (
            db.query(UserLessonProgress)
            .filter(
                UserLessonProgress.user_id == user_id,
                UserLessonProgress.lesson_id.in_(lesson_ids),
                UserLessonProgress.completed_at.isnot(None),
            )
            .count()
        ) if lesson_ids else 0
        out.append({
            "slug": s.slug,
            "name_uz": s.name_uz,
            "name_ru": s.name_ru,
            "name_en": s.name_en,
            "color": s.color,
            "completed": completed,
            "total": total,
            "pct": round(completed / total * 100) if total else 0,
        })
    return out


def student_row(db: Session, user: User) -> dict:
    """Compact per-student stats for a teacher roster row."""
    lessons_completed = (
        db.query(UserLessonProgress)
        .filter(UserLessonProgress.user_id == user.id, UserLessonProgress.completed_at.isnot(None))
        .count()
    )
    last_attempt = (
        db.query(sa_func.max(SkillLessonAttempt.completed_at))
        .filter(SkillLessonAttempt.user_id == user.id, SkillLessonAttempt.completed_at.isnot(None))
        .scalar()
    )
    today = date.today().isoformat()
    active_today = bool(last_attempt and last_attempt.date().isoformat() == today)
    return {
        "user_id": user.id,
        "name": user.name,
        "profile_picture": user.profile_picture,
        "xp_total": user.xp_total or 0,
        "weekly_xp": _weekly_xp(db, user.id),
        "streak_days": user.streak_days or 0,
        "lessons_completed": lessons_completed,
        "last_active": last_attempt.date().isoformat() if last_attempt else None,
        "active_today": active_today,
    }


def student_detail(db: Session, user: User) -> dict:
    """Full read-only detail for a parent viewing their child."""
    row = student_row(db, user)
    subjects = _subject_progress(db, user.id)
    done = [s for s in subjects if s["completed"] > 0]
    strongest = max(done, key=lambda p: p["pct"], default=None)
    weakest = min(done, key=lambda p: p["pct"], default=None)

    since = datetime.now(timezone.utc) - timedelta(days=84)
    rows = (
        db.query(SkillLessonAttempt.completed_at)
        .filter(SkillLessonAttempt.user_id == user.id, SkillLessonAttempt.completed_at >= since)
        .all()
    )
    activity: dict[str, int] = {}
    for (ts,) in rows:
        if ts:
            key = ts.date().isoformat()
            activity[key] = activity.get(key, 0) + 1

    return {
        **row,
        "subjects": subjects,
        "strongest": strongest,
        "weakest": weakest,
        "activity": activity,
    }
