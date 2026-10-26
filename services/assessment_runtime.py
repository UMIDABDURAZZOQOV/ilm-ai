"""Opt-in v2 Physics preview: authoritative, immutable, transactional attempts.

Separate namespace and tables. Never invoked by legacy Biology/web endpoints.
The authenticated account, not a submitted user_id, owns every operation.
"""

import os
from copy import deepcopy
from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy import inspect, update
from sqlalchemy.exc import IntegrityError

from services.assessment_grading import grade_answer
from services.assessment_models import (
    AssessmentBase,
    AssessmentV2Answer,
    AssessmentV2Progress,
    CurriculumAssessment,
    CurriculumLessonV2,
)
from services.models import StudyEvent, StudySession, User
from services.physics_curriculum import fingerprint, public_book
from services.study import aware, record_activity, utcnow

KIND = "assessment_v2"
SOURCE_SECTIONS = {6: 61, 7: 46, 8: 60, 9: 59, 10: 45, 11: 45}


def preview_gate(db):
    url = db.get_bind().url
    local = url.get_backend_name() == "sqlite" or (
        url.get_backend_name() == "postgresql"
        and url.host in {"localhost", "127.0.0.1", "::1"}
        and "staging" in (url.database or "")
    )
    if (
        os.getenv("PHYSICS_PREVIEW_ENABLED", "").lower() != "true"
        or os.getenv("ENVIRONMENT", "development") not in {"development", "test"}
        or not local
    ):
        raise HTTPException(404, "physics_preview_disabled")
    if not set(AssessmentBase.metadata.tables) <= set(
        inspect(db.get_bind()).get_table_names()
    ):
        raise HTTPException(503, "physics_preview_schema_not_installed")


def lessons(db, grade=6):
    return (
        db.query(CurriculumLessonV2)
        .filter_by(subject="fizika", grade=grade)
        .order_by(CurriculumLessonV2.sequence)
        .all()
    )


def catalog(db, uid, grade=6):
    if grade not in SOURCE_SECTIONS:
        raise HTTPException(422, "unsupported_physics_grade")
    progress = {
        p.lesson_key: p for p in db.query(AssessmentV2Progress).filter_by(user_id=uid)
    }
    ready = True
    result = []
    for expected, lesson in enumerate(lessons(db, grade), start=1):
        # A missing imported prerequisite must never unlock a later section.
        ready = ready and lesson.sequence == expected
        done = bool(progress.get(lesson.key) and progress[lesson.key].completed_at)
        result.append(
            {
                "key": lesson.key,
                "sequence": lesson.sequence,
                "title": lesson.title,
                "state": "completed" if done else ("available" if ready else "locked"),
                "best_score_pct": progress[lesson.key].best_score_pct
                if lesson.key in progress
                else 0,
                "source_refs": lesson.content["source_refs"],
            }
        )
        ready = ready and done
    return {
        "assessment_version": 2,
        "subject": "fizika",
        "grade": grade,
        "book": public_book(grade),
        "language": "uz",
        "publication": "local_test_preview_only",
        "source_sections": SOURCE_SECTIONS[grade],
        "implemented_sections": len(result),
        "course_complete": False,
        "grade_content_complete": [r["sequence"] for r in result]
        == list(range(1, SOURCE_SECTIONS[grade] + 1)),
        "available_grades": [
            g
            for g in SOURCE_SECTIONS
            if db.query(CurriculumLessonV2.key)
            .filter_by(subject="fizika", grade=g, sequence=1)
            .first()
        ],
        "lessons": result,
    }


def get_session(db, uid, sid, lock=False):
    # A no-op UPDATE acquires a row/SQLite writer lock before reading answers.
    # Same ordering for answer/complete avoids a lost simultaneous submission.
    if lock:
        db.execute(
            update(StudySession)
            .where(
                StudySession.id == sid,
                StudySession.user_id == uid,
                StudySession.kind == KIND,
            )
            .values(started_at=StudySession.started_at)
            .execution_options(synchronize_session=False)
        )
    row = (
        db.query(StudySession)
        .filter_by(id=sid, user_id=uid, kind=KIND)
        .populate_existing()
        .first()
    )
    if not row:
        raise HTTPException(404, "attempt_not_found")
    if row.completed_at is None and utcnow() - aware(row.started_at) > timedelta(
        hours=24
    ):
        raise HTTPException(409, "attempt_expired")
    return row


def public_attempt(db, row):
    snap = row.questions
    answers = {
        a.assessment_key: a.response
        for a in db.query(AssessmentV2Answer).filter_by(session_id=row.id)
    }
    # Explicit allowlist: never serialize an ORM row, rubric, expected answer,
    # tolerance, or formula alternatives. Solutions only follow submitted answers.
    return {
        "assessment_version": 2,
        "attempt_id": row.id,
        "lesson_key": row.scope,
        "expires_at": (aware(row.started_at) + timedelta(hours=24)).isoformat(),
        "title": snap["title"],
        "content": deepcopy(snap["content"]),
        "questions": [
            dict(
                key=q["key"],
                response_kind=q["kind"],
                **deepcopy(q["public"]),
                source_refs=q["source_refs"],
            )
            for q in snap["assessments"]
        ],
        "answers": answers,
        "result": row.response,
    }


def start(db, uid, key, request_id):
    sid = f"v2:{uid}:{request_id}"
    existing = db.get(StudySession, sid)
    if existing:
        row = get_session(db, uid, sid)
        if row.scope != key:
            raise HTTPException(409, "request_id_reused_for_different_lesson")
        return public_attempt(db, row)
    lesson = db.get(CurriculumLessonV2, key)
    if not lesson or lesson.subject != "fizika" or lesson.grade not in SOURCE_SECTIONS:
        raise HTTPException(404, "lesson_not_found")
    state = next(
        (
            l["state"]
            for l in catalog(db, uid, lesson.grade)["lessons"]
            if l["key"] == key
        ),
        "locked",
    )
    if state == "locked":
        raise HTTPException(403, "finish_previous_lesson")
    if db.get(User, uid) is None:
        raise HTTPException(404, "user_not_found")
    questions = (
        db.query(CurriculumAssessment)
        .filter_by(lesson_key=key)
        .order_by(CurriculumAssessment.order_index)
        .all()
    )
    if not questions:
        raise HTTPException(409, "lesson_not_imported")
    row = StudySession(
        id=sid,
        user_id=uid,
        kind=KIND,
        scope=key,
        started_at=utcnow(),
        questions={
            "revision": lesson.revision,
            "content_sha256": lesson.content_sha256,
            "title": lesson.title,
            "content": deepcopy(lesson.content),
            "assessments": [
                {
                    "key": q.key,
                    "kind": q.response_kind,
                    "public": deepcopy(q.public_prompt),
                    "grading_spec": deepcopy(q.grading_spec),
                    "source_refs": q.source_refs,
                }
                for q in questions
            ],
        },
    )
    db.add(row)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        row = get_session(db, uid, sid)
        if row.scope != key:
            raise HTTPException(409, "request_id_reused_for_different_lesson")
    return public_attempt(db, row)


def submit(db, uid, sid, key, answer):
    row = get_session(db, uid, sid, lock=True)
    digest = fingerprint(answer)
    old = db.get(AssessmentV2Answer, (sid, key))
    if old:
        if old.fingerprint != digest:
            raise HTTPException(409, "answer_already_submitted")
        db.commit()  # release the writer lock even for a replay
        return old.response
    if row.completed_at:
        raise HTTPException(409, "attempt_already_completed")
    done = {
        a.assessment_key for a in db.query(AssessmentV2Answer).filter_by(session_id=sid)
    }
    q = next((q for q in row.questions["assessments"] if q["key"] not in done), None)
    if q is None or q["key"] != key:
        raise HTTPException(409, "answer_questions_in_order")
    spec = q["grading_spec"]
    code = grade_answer(spec, answer)
    feedback = spec["feedback"].get(code, spec["feedback"]["incorrect"])
    # Preserve immutable snapshots and stored replay responses. The original
    # generic template assumed unsigned answers; signed work/heat can be negative.
    if (
        code == "sign_error"
        and feedback == "Bu vaziyatda javob manfiy bo‘lishi mumkin emas."
    ):
        feedback = "Javob ishorasi talabga mos emas. Topshiriqdagi yo‘nalish va ishora konvensiyasini tekshir."
    if code in {
        "invalid_answer",
        "answer_required",
        "invalid_expression",
        "domain_error",
    }:
        # Format problems may be corrected. No solution/expected value disclosed.
        raise HTTPException(422, {"code": code, "feedback": feedback})
    result = {
        "assessment_version": 2,
        "assessment_key": key,
        "is_correct": code == "correct",
        "code": code,
        "feedback": feedback,
        "solution": deepcopy(spec["solution"]),
        "source_refs": q["source_refs"],
    }
    db.add(
        AssessmentV2Answer(
            session_id=sid, assessment_key=key, fingerprint=digest, response=result
        )
    )
    db.commit()
    return result


def complete(db, uid, sid):
    row = get_session(db, uid, sid, lock=True)
    if row.response is not None:
        db.commit()
        return row.response
    responses = db.query(AssessmentV2Answer).filter_by(session_id=sid).all()
    if len(responses) != len(row.questions["assessments"]):
        raise HTTPException(409, "finish_all_questions")
    # Row lock also serializes different attempts by the same learner, so two
    # successful parallel attempts cannot award the first-completion XP twice.
    user = db.query(User).filter_by(id=uid).with_for_update().populate_existing().one()
    score = sum(a.response["is_correct"] for a in responses)
    total = len(responses)
    passed = score * 100 >= total * 60
    progress = db.get(AssessmentV2Progress, (uid, row.scope))
    if progress is None:
        progress = AssessmentV2Progress(
            user_id=uid, lesson_key=row.scope, attempts=0, best_score_pct=0, xp_earned=0
        )
        db.add(progress)
    first_pass = passed and progress.completed_at is None
    now = utcnow()
    xp = int(row.questions["content"]["xp_reward"]) if first_pass else 0
    if first_pass:
        progress.completed_at = now
        progress.xp_earned += xp
    progress.attempts += 1
    pct = score * 100 / total
    progress.best_score_pct = max(progress.best_score_pct, pct)
    user.xp_total = int(user.xp_total or 0) + xp
    record_activity(db, user, now)
    db.add(
        StudyEvent(
            source_key=f"v2:{sid}", user_id=uid, kind=KIND, xp=xp, created_at=now
        )
    )
    result = {
        "assessment_version": 2,
        "attempt_id": sid,
        "lesson_key": row.scope,
        "score": score,
        "total": total,
        "score_pct": pct,
        "passed": passed,
        "xp_awarded": xp,
        "xp_total": user.xp_total,
        "streak_days": user.streak_days,
        "completion_threshold_pct": 60,
    }
    row.completed_at, row.response = now, result
    db.commit()
    return result
