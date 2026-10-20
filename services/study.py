"""Authoritative grading and transactional, replay-safe study progress.

Question/content tables are read only here. New tables are additive; legacy
attempts and daily rewards remain visible without a balance migration.
"""

from __future__ import annotations

import hashlib
import json
import secrets
from datetime import date, datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy import String, cast, exists, literal, select, update, union_all, func
from sqlalchemy.exc import IntegrityError

from services.models import (
    PlacementQuestion,
    SkillDailyChallenge,
    SkillLesson,
    SkillLessonAttempt,
    SkillMistake,
    SkillQuestion,
    SkillUnit,
    StreakFreeze,
    StudyEvent,
    StudySession,
    User,
    UserLanguageLevel,
    UserLessonProgress,
    UserUnitExam,
)
from services.placement import score_placement

SRS_INTERVALS = [1, 3, 7, 16, 35]


def utcnow():
    return datetime.now(timezone.utc)


def aware(value):
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value


def issue(db, user_id, kind, scope, questions, session_id=None):
    if not questions:
        return None
    session_id = session_id or secrets.token_urlsafe(32)
    existing = db.get(StudySession, session_id)
    if existing:
        if existing.user_id != user_id or existing.kind != kind:
            raise HTTPException(409, "study_session_conflict")
        return existing
    # Keep the exact issued options, including runtime translations, for grading.
    row = StudySession(
        id=session_id,
        user_id=user_id,
        kind=kind,
        scope=str(scope),
        questions=questions,
        started_at=utcnow(),
    )
    db.add(row)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = db.get(StudySession, session_id)
        if (
            existing
            and existing.user_id == user_id
            and existing.kind == kind
            and existing.scope == str(scope)
        ):
            return existing
        raise
    return row


def issued_payload(db, user_id, kind, scope, payload, session_id=None):
    row = issue(db, user_id, kind, scope, payload.get("questions", []), session_id)
    return {
        **payload,
        "questions": row.questions if row else [],
        "attempt_id": row.id if row else None,
    }


def checkpoint_ready(db, user_id, unit_id):
    unit = db.get(SkillUnit, unit_id)
    if not unit:
        raise HTTPException(404, "Unit not found")
    ids = [
        r[0] for r in db.query(SkillLesson.id).filter(SkillLesson.unit_id == unit_id)
    ]
    done = (
        db.query(UserLessonProgress)
        .filter(
            UserLessonProgress.user_id == user_id,
            UserLessonProgress.lesson_id.in_(ids),
            UserLessonProgress.completed_at.isnot(None),
        )
        .count()
    )
    if not ids or done != len(ids):
        raise HTTPException(403, "Finish every lesson in this unit first")


def resolve_session(db, user_id, kind, scope=None, attempt_id=None):
    query = db.query(StudySession).filter_by(user_id=user_id, kind=kind)
    if attempt_id:
        query = query.filter(StudySession.id == str(attempt_id))
    if scope is not None:
        query = query.filter(StudySession.scope == str(scope))
    row = query.order_by(StudySession.started_at.desc()).first()
    if not row:
        raise HTTPException(409, "study_session_required")
    if not row.completed_at and utcnow() - aware(row.started_at) > timedelta(hours=24):
        raise HTTPException(409, "study_session_expired")
    return row


def grade(row, submitted, partial=False):
    questions = {q["id"]: q for q in row.questions}
    if len(questions) != len(row.questions):
        raise HTTPException(409, "invalid_question_snapshot")
    seen, results = set(), []
    for result in submitted:
        r = result.model_dump() if hasattr(result, "model_dump") else result
        qid = r["question_id"]
        if qid in seen or qid not in questions:
            raise HTTPException(422, "duplicate_or_foreign_question")
        seen.add(qid)
        q = questions[qid]
        options = q.get("options") or []
        index = r.get("answer_index")
        answer = r.get("user_answer")
        if index is not None:
            if (
                isinstance(index, bool)
                or not isinstance(index, int)
                or not 0 <= index < len(options)
            ):
                raise HTTPException(422, "invalid_answer_index")
            answer = options[index]
        if answer is None or answer not in options:
            # is_correct remains accepted as an advisory field, never as evidence.
            raise HTTPException(422, "answer_required")
        results.append(
            {
                "question_id": qid,
                "user_answer": answer,
                "is_correct": answer == q["correct_answer"],
            }
        )
    if not partial and seen != set(questions):
        raise HTTPException(422, "incomplete_question_set")
    fingerprint = hashlib.sha256(
        json.dumps(
            sorted(results, key=lambda r: r["question_id"]), sort_keys=True
        ).encode()
    ).hexdigest()
    return results, fingerprint


def record_activity(db, user, now):
    today = now.date()
    last = date.fromisoformat(user.last_study_date) if user.last_study_date else None
    previous = int(user.streak_days or 0)
    if last == today:
        return
    gap = (today - last).days if last else 0
    freeze = db.query(StreakFreeze).filter_by(user_id=user.id).first()
    available = int(freeze.count or 0) if freeze else 0
    missed = max(0, gap - 1)
    protected = gap > 1 and available >= missed
    if protected:
        freeze.count -= missed
    user.streak_days = previous + 1 if gap == 1 or protected else 1
    user.last_study_date = today.isoformat()
    if user.streak_days > previous and user.streak_days % 7 == 0:
        if freeze is None:
            freeze = StreakFreeze(user_id=user.id, count=0)
            db.add(freeze)
        freeze.count = min(3, int(freeze.count or 0) + 1)


def effective_streak(db, user):
    if not user.last_study_date:
        return 0
    missed = max(
        0, (utcnow().date() - date.fromisoformat(user.last_study_date)).days - 1
    )
    freeze = db.query(StreakFreeze).filter_by(user_id=user.id).first()
    return (
        int(user.streak_days or 0)
        if missed <= (int(freeze.count or 0) if freeze else 0)
        else 0
    )


def complete(db, user_id, kind, submitted, scope=None, attempt_id=None):
    row = resolve_session(db, user_id, kind, scope, attempt_id)
    results, fingerprint = grade(
        row, submitted, partial=kind in {"lightning", "subject_exam"}
    )
    if row.response is not None:
        if row.fingerprint != fingerprint:
            raise HTTPException(409, "attempt_already_completed")
        return row.response
    if kind == "checkpoint":
        checkpoint_ready(db, user_id, int(row.scope))
    if kind == "daily" and row.scope != utcnow().date().isoformat():
        raise HTTPException(409, "daily_challenge_expired")
    now = utcnow()
    # An atomic conditional UPDATE serializes duplicate submissions on both
    # PostgreSQL and SQLite. All side effects and response share this transaction.
    claimed = db.execute(
        update(StudySession)
        .where(StudySession.id == row.id, StudySession.completed_at.is_(None))
        .values(completed_at=now)
        .execution_options(synchronize_session=False)
    ).rowcount
    if not claimed:
        db.rollback()
        saved = db.get(StudySession, row.id)
        if saved.response is not None and saved.fingerprint == fingerprint:
            return saved.response
        raise HTTPException(409, "attempt_already_completed")
    user = (
        db.query(User)
        .filter_by(id=user_id)
        .with_for_update()
        .populate_existing()
        .first()
    )
    if not user:
        raise HTTPException(404, "User not found")
    score, total = sum(r["is_correct"] for r in results), len(results)
    if kind == "subject_exam":
        total = len(row.questions)
    pct = 100 * score / total if total else 0
    response = {"score": score, "total": total, "score_pct": pct}
    xp, source = 0, f"{kind}:{row.id}"
    if kind == "lesson":
        lesson = db.get(SkillLesson, int(row.scope))
        attempt = db.get(SkillLessonAttempt, int(row.id.removeprefix("lesson:")))
        if (
            not lesson
            or not attempt
            or attempt.user_id != user_id
            or attempt.lesson_id != lesson.id
        ):
            raise HTTPException(404, "Attempt not found")
        from services.skill_tree import build_tree
        from services.models import SkillSubject

        unit = db.get(SkillUnit, lesson.unit_id)
        subject = db.get(SkillSubject, unit.subject_id)

        def unlocked():
            return {
                l["id"]
                for u in build_tree(db, user_id, subject.slug)["units"]
                for l in u["lessons"]
                if l["status"] == "unlocked"
            }

        previously_open = unlocked()
        stars = 3 if pct >= 90 else 2 if pct >= 80 else 1 if pct >= 60 else 0
        progress = (
            db.query(UserLessonProgress)
            .filter_by(user_id=user_id, lesson_id=lesson.id)
            .first()
        )
        if progress is None:
            progress = UserLessonProgress(
                user_id=user_id, lesson_id=lesson.id, stars=0, attempts=0
            )
            db.add(progress)
        first = stars > 0 and progress.completed_at is None
        xp = lesson.xp_reward if first else 5
        progress.attempts = (progress.attempts or 0) + 1
        progress.stars = max(progress.stars or 0, stars)
        progress.best_score_pct = max(progress.best_score_pct or 0, pct)
        progress.xp_earned = (progress.xp_earned or 0) + xp
        progress.last_attempt_at = now
        if first:
            progress.completed_at = now
        attempt.completed_at, attempt.score, attempt.total = now, score, total
        attempt.xp_awarded, attempt.results = xp, results
        for r in results:
            mistake = (
                db.query(SkillMistake)
                .filter_by(user_id=user_id, question_id=r["question_id"])
                .first()
            )
            if r["is_correct"]:
                if mistake and mistake.resolved_at is None:
                    mistake.resolved_at = now
            else:
                if mistake is None:
                    mistake = SkillMistake(
                        user_id=user_id, question_id=r["question_id"], wrong_count=0
                    )
                    db.add(mistake)
                mistake.wrong_count = (mistake.wrong_count or 0) + 1
                mistake.last_wrong_at, mistake.resolved_at = now, None
                mistake.review_stage, mistake.due_at = 0, now + timedelta(days=1)
        source = f"lesson:{attempt.id}"
        db.flush()
        response.update(
            passed=stars > 0,
            pass_threshold_pct=60,
            stars=stars,
            newly_unlocked_lesson_ids=sorted(unlocked() - previously_open),
        )
    elif kind == "checkpoint":
        exam = (
            db.query(UserUnitExam)
            .filter_by(user_id=user_id, unit_id=int(row.scope))
            .first()
        )
        if exam is None:
            exam = UserUnitExam(
                user_id=user_id, unit_id=int(row.scope), attempts=0, passed=False
            )
            db.add(exam)
        passed = pct >= 60
        xp = 50 if passed and not exam.passed else 0
        exam.attempts = (exam.attempts or 0) + 1
        exam.score, exam.total, exam.last_attempt_at = score, total, now
        exam.best_score_pct = max(exam.best_score_pct or 0, pct)
        if passed and not exam.passed:
            exam.passed, exam.passed_at = True, now
        response.update(passed=passed, pass_threshold_pct=60)
    elif kind == "placement":
        levels = {
            q.id: q.level
            for q in db.query(PlacementQuestion).filter(
                PlacementQuestion.subject_slug == row.scope,
                PlacementQuestion.id.in_([r["question_id"] for r in results]),
            )
        }
        if len(levels) != len(results):
            raise HTTPException(422, "foreign_placement_question")
        per_level = {}
        for r in results:
            level = levels[r["question_id"]]
            correct, count = per_level.get(level, (0, 0))
            per_level[level] = (correct + int(r["is_correct"]), count + 1)
        response = score_placement(row.scope, per_level)
        level_row = (
            db.query(UserLanguageLevel)
            .filter_by(user_id=user_id, subject_slug=row.scope)
            .first()
        )
        if level_row is None:
            level_row = UserLanguageLevel(user_id=user_id, subject_slug=row.scope)
            db.add(level_row)
        for field in ("level", "score", "total", "score_pct"):
            setattr(level_row, field, response[field])
        level_row.taken_at = now
    elif kind == "daily":
        daily = (
            db.query(SkillDailyChallenge)
            .filter_by(user_id=user_id, date=row.scope)
            .first()
        )
        if daily and daily.completed_at is not None:
            raise HTTPException(409, "daily_already_completed")
        if daily is None:
            daily = SkillDailyChallenge(user_id=user_id, date=row.scope)
            db.add(daily)
        xp = 10 + score
        daily.score, daily.total, daily.xp_awarded, daily.completed_at = (
            score,
            total,
            xp,
            now,
        )
        source = f"daily:{user_id}:{row.scope}"
        response["already_completed"] = False
    elif kind == "mistakes":
        graduated = eligible_correct = 0
        for r in results:
            mistake = (
                db.query(SkillMistake)
                .filter_by(user_id=user_id, question_id=r["question_id"])
                .first()
            )
            if (
                not mistake
                or mistake.resolved_at is not None
                or (mistake.due_at and aware(mistake.due_at) > now)
            ):
                continue
            if r["is_correct"]:
                eligible_correct += 1
                stage = (mistake.review_stage or 0) + 1
                mistake.review_stage = stage
                if stage >= len(SRS_INTERVALS):
                    mistake.resolved_at = now
                    graduated += 1
                else:
                    mistake.due_at = now + timedelta(days=SRS_INTERVALS[stage])
            else:
                mistake.wrong_count = (mistake.wrong_count or 0) + 1
                mistake.last_wrong_at = now
                mistake.review_stage, mistake.due_at = 0, now + timedelta(days=1)
        xp = min(eligible_correct, 10)
        db.flush()
        remaining = (
            db.query(SkillMistake)
            .filter(
                SkillMistake.user_id == user_id,
                SkillMistake.resolved_at.is_(None),
                (SkillMistake.due_at.is_(None)) | (SkillMistake.due_at <= now),
            )
            .count()
        )
        response.update(
            resolved=eligible_correct, graduated=graduated, remaining=remaining
        )
    elif kind == "subject_exam":
        xp = min(score, 40)
        by_id = {q["id"]: q for q in row.questions}
        correct_ids = {r["question_id"] for r in results if r["is_correct"]}
        units = {}
        for q in by_id.values():
            title = q.get("unit_title", "")
            c, t = units.get(title, (0, 0))
            units[title] = (c + int(q["id"] in correct_ids), t + 1)
        response.update(
            passed=pct >= 70,
            weak_units=sorted(
                [
                    {"title_uz": title, "pct": round(100 * c / t, 1)}
                    for title, (c, t) in units.items()
                ],
                key=lambda x: x["pct"],
            )[:3],
        )
    elif kind in {"lightning", "marathon"}:
        xp = min(score, 15 if kind == "lightning" else 30)
    else:
        raise HTTPException(422, "unknown_study_mode")
    if results:
        user.xp_total = (user.xp_total or 0) + xp
        record_activity(db, user, now)
        db.add(
            StudyEvent(
                user_id=user_id, source_key=source, kind=kind, xp=xp, created_at=now
            )
        )
    response.update(
        xp_awarded=xp, xp_total=user.xp_total or 0, streak_days=user.streak_days or 0
    )
    row.completed_at, row.fingerprint, row.response = now, fingerprint, response
    db.add(row)
    db.commit()
    return response


def activity_rows(db, user_id, since):
    events = [
        (e.created_at, e.xp)
        for e in db.query(StudyEvent).filter(
            StudyEvent.user_id == user_id, StudyEvent.created_at >= since
        )
    ]
    # Retain historical activity and avoid counting new ledger-backed rows twice.
    tracked_lesson = exists(
        select(StudyEvent.id).where(
            StudyEvent.source_key
            == literal("lesson:") + cast(SkillLessonAttempt.id, String)
        )
    )
    events += [
        (r.completed_at, r.xp_awarded or 0)
        for r in db.query(SkillLessonAttempt).filter(
            SkillLessonAttempt.user_id == user_id,
            SkillLessonAttempt.completed_at >= since,
            ~tracked_lesson,
        )
    ]
    tracked_daily = exists(
        select(StudyEvent.id).where(
            StudyEvent.source_key
            == literal(f"daily:{user_id}:") + SkillDailyChallenge.date
        )
    )
    events += [
        (r.completed_at, r.xp_awarded or 0)
        for r in db.query(SkillDailyChallenge).filter(
            SkillDailyChallenge.user_id == user_id,
            SkillDailyChallenge.completed_at >= since,
            ~tracked_daily,
        )
    ]
    return events


def xp_since(db, user_id, since):
    return sum(xp for _, xp in activity_rows(db, user_id, since))


def weekly_totals(db):
    """One aggregate query for the whole leaderboard, rather than N per learner."""
    since = utcnow() - timedelta(days=7)
    tracked_lesson = exists(
        select(StudyEvent.id).where(
            StudyEvent.source_key
            == literal("lesson:") + cast(SkillLessonAttempt.id, String)
        )
    )
    tracked_daily = exists(
        select(StudyEvent.id).where(
            StudyEvent.source_key
            == literal("daily:")
            + cast(SkillDailyChallenge.user_id, String)
            + literal(":")
            + SkillDailyChallenge.date
        )
    )
    sources = union_all(
        select(StudyEvent.user_id.label("uid"), StudyEvent.xp.label("xp")).where(
            StudyEvent.created_at >= since
        ),
        select(SkillLessonAttempt.user_id, SkillLessonAttempt.xp_awarded).where(
            SkillLessonAttempt.completed_at >= since, ~tracked_lesson
        ),
        select(SkillDailyChallenge.user_id, SkillDailyChallenge.xp_awarded).where(
            SkillDailyChallenge.completed_at >= since, ~tracked_daily
        ),
    ).subquery()
    return (
        db.query(sources.c.uid, func.sum(sources.c.xp))
        .group_by(sources.c.uid)
        .having(func.sum(sources.c.xp) > 0)
        .order_by(func.sum(sources.c.xp).desc(), sources.c.uid)
        .all()
    )


def award_verified_activity(db, user_id, kind, source_key, xp):
    """Replay-safe XP for existing server/AI graded legacy modes, no content edits."""
    now = utcnow()
    dialect = db.bind.dialect.name
    if dialect == "postgresql":
        from sqlalchemy.dialects.postgresql import insert
    elif dialect == "sqlite":
        from sqlalchemy.dialects.sqlite import insert
    else:
        raise HTTPException(503, "unsupported_study_database")
    claimed = db.execute(
        insert(StudyEvent)
        .values(
            user_id=user_id, kind=kind, source_key=source_key, xp=xp, created_at=now
        )
        .on_conflict_do_nothing(index_elements=["source_key"])
    ).rowcount
    if not claimed:
        db.rollback()
        return False
    user = (
        db.query(User)
        .filter_by(id=user_id)
        .with_for_update()
        .populate_existing()
        .first()
    )
    if not user:
        raise HTTPException(404, "user_not_found")
    user.xp_total = (user.xp_total or 0) + xp
    record_activity(db, user, now)
    db.commit()
    return True
