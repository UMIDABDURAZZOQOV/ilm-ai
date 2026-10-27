"""Local Math v1: immutable attempts, guided retries, one-time account XP.

All answers are server graded. No existing subject router or schema is changed.
An answer request UUID is an idempotency key; a new UUID permits a real retry.
"""

import os
from copy import deepcopy
from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy import inspect, update
from sqlalchemy.exc import IntegrityError

from services.mathematics_curriculum import digest, manifest, staging_url
from services.mathematics_grading import MathInputError, grade_answer
from services.mathematics_models import (
    MathAnswer,
    MathAttempt,
    MathBase,
    MathLesson,
    MathProgress,
)
from services.models import StudyEvent, User
from services.study import aware, record_activity, utcnow

KIND = "math_assessment_v1"


def preview_gate(db):
    try:
        staging_url(db.get_bind().url)
    except ValueError:
        raise HTTPException(404, "mathematics_preview_disabled") from None
    if os.getenv("MATHEMATICS_PREVIEW_ENABLED", "").lower() != "true":
        raise HTTPException(404, "mathematics_preview_disabled")
    if not set(MathBase.metadata.tables) <= set(
        inspect(db.get_bind()).get_table_names()
    ):
        raise HTTPException(503, "mathematics_preview_schema_not_installed")


def catalog(db, uid, grade=1, part=1):
    rows = (
        db.query(MathLesson)
        .filter_by(grade=grade, part=part)
        .order_by(MathLesson.sequence)
        .all()
    )
    completed = {p.lesson_key for p in db.query(MathProgress).filter_by(user_id=uid)}
    ready = True
    lessons = []
    for index, lesson in enumerate(rows, 1):
        ready = ready and lesson.sequence == index
        done = lesson.key in completed
        lessons.append(
            {
                "key": lesson.key,
                "title": lesson.document["title"],
                "sequence": lesson.sequence,
                "state": "completed" if done else "available" if ready else "locked",
                "source_refs": lesson.document["source_refs"],
            }
        )
        ready = ready and done
    return {
        "assessment_version": 1,
        "subject": "mathematics",
        "grade": grade,
        "part": part,
        "publication": "local_test_preview_only",
        "course_ready": False,
        "full_topic_count": None,
        "implemented_sections": len(rows),
        "blocked_sources": manifest()["blocked_sources"],
        "lessons": lessons,
    }


def attempt(db, uid, sid, *, lock=False):
    if lock:
        db.execute(
            update(MathAttempt)
            .where(MathAttempt.id == sid, MathAttempt.user_id == uid)
            .values(started_at=MathAttempt.started_at)
            .execution_options(synchronize_session=False)
        )
    row = (
        db.query(MathAttempt).filter_by(id=sid, user_id=uid).populate_existing().first()
    )
    if not row:
        raise HTTPException(404, "attempt_not_found")
    if row.result is None and utcnow() - aware(row.started_at) > timedelta(hours=24):
        raise HTTPException(409, "attempt_expired")
    return row


def answer_rows(db, row):
    return (
        db.query(MathAnswer)
        .filter_by(attempt_id=row.id)
        .order_by(MathAnswer.sequence)
        .all()
    )


def public_attempt(db, row):
    doc = row.snapshot
    return {
        "assessment_version": 1,
        "attempt_id": row.id,
        "lesson_key": row.lesson_key,
        "expires_at": (aware(row.started_at) + timedelta(hours=24)).isoformat(),
        "title": doc["title"],
        "content": {
            k: deepcopy(doc[k])
            for k in ["cards", "examples", "explorer", "formulas", "source_refs"]
        },
        "questions": [
            dict(id=q["id"], source_refs=q["source_refs"], **deepcopy(q["public"]))
            for q in doc["questions"]
        ],
        "answers": [a.response for a in answer_rows(db, row)],
        "result": row.result,
    }


def start(db, uid, key, request_id):
    sid = f"mathv1:{uid}:{request_id}"
    old = db.get(MathAttempt, sid)
    if old:
        row = attempt(db, uid, sid)
        if row.lesson_key != key:
            raise HTTPException(409, "request_id_reused_for_different_lesson")
        return public_attempt(db, row)
    lesson = db.get(MathLesson, key)
    if not lesson or db.get(User, uid) is None:
        raise HTTPException(404, "lesson_or_user_not_found")
    state = next(
        (
            l["state"]
            for l in catalog(db, uid, lesson.grade, lesson.part)["lessons"]
            if l["key"] == key
        ),
        "locked",
    )
    if state == "locked":
        raise HTTPException(403, "finish_previous_lesson")
    row = MathAttempt(
        id=sid,
        user_id=uid,
        lesson_key=key,
        started_at=utcnow(),
        snapshot=deepcopy(lesson.document),
    )
    db.add(row)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        row = attempt(db, uid, sid)
        if row.lesson_key != key:
            raise HTTPException(409, "request_id_reused_for_different_lesson") from None
    return public_attempt(db, row)


def submit(db, uid, sid, request_id, qid, answer):
    row = attempt(db, uid, sid, lock=True)
    fingerprint = digest({"question": qid, "answer": answer})
    old = db.get(MathAnswer, (sid, request_id))
    if old:
        if old.fingerprint != fingerprint:
            raise HTTPException(409, "answer_request_id_conflict")
        db.commit()
        return old.response
    if row.result is not None:
        raise HTTPException(409, "attempt_already_completed")
    previous = answer_rows(db, row)
    if len(previous) >= 256:
        raise HTTPException(409, "support_limit_open_new_attempt")
    solved = {a.question_id for a in previous if a.response["is_correct"]}
    question = next(
        (q for q in row.snapshot["questions"] if q["id"] not in solved), None
    )
    if question is None or question["id"] != qid:
        raise HTTPException(409, "answer_questions_in_order")
    spec = question["grading"]
    try:
        code = grade_answer(spec, answer)
    except MathInputError as exc:
        raise HTTPException(
            422,
            {
                "code": str(exc),
                "feedback": "Yozuvni tekshir. Hozir bu javob shaklini baholay olmadim; qayta yozib ko‘r.",
            },
        ) from None
    wrong = sum(a.question_id == qid and not a.response["is_correct"] for a in previous)
    if code == "correct":
        feedback = spec["feedback_correct"]
    elif wrong < len(spec["hints"]):
        feedback = spec["hints"][wrong]
    else:
        feedback = spec[
            "solution"
        ]  # Last rung after staged hints, not initial disclosure.
    response = {
        "assessment_version": 1,
        "request_id": request_id,
        "question_id": qid,
        "is_correct": code == "correct",
        "code": code,
        "feedback": feedback,
        "hint_level": 0
        if code == "correct"
        else min(wrong + 1, len(spec["hints"]) + 1),
        "tries": wrong + 1,
        "source_refs": question["source_refs"],
    }
    db.add(
        MathAnswer(
            attempt_id=sid,
            request_id=request_id,
            question_id=qid,
            sequence=len(previous) + 1,
            fingerprint=fingerprint,
            created_at=utcnow(),
            response=response,
        )
    )
    db.commit()
    return response


def complete(db, uid, sid):
    row = attempt(db, uid, sid, lock=True)
    if row.result is not None:
        db.commit()
        return row.result
    answers = answer_rows(db, row)
    solved = {a.question_id for a in answers if a.response["is_correct"]}
    if solved != {q["id"] for q in row.snapshot["questions"]}:
        raise HTTPException(409, "finish_all_questions_with_support")
    # Same account lock serializes first rewards across distinct parallel attempts.
    db.execute(
        update(User)
        .where(User.id == uid)
        .values(xp_total=User.xp_total)
        .execution_options(synchronize_session=False)
    )
    user = db.query(User).filter_by(id=uid).populate_existing().with_for_update().one()
    progress = db.get(MathProgress, (uid, row.lesson_key))
    xp = row.snapshot["xp_reward"] if progress is None else 0
    now = utcnow()
    if progress is None:
        db.add(
            MathProgress(
                user_id=uid, lesson_key=row.lesson_key, completed_at=now, xp_earned=xp
            )
        )
    user.xp_total += xp
    record_activity(db, user, now)
    db.add(
        StudyEvent(
            source_key=f"mathv1:{sid}", user_id=uid, kind=KIND, xp=xp, created_at=now
        )
    )
    first = {}
    for a in answers:
        first.setdefault(a.question_id, a.response)
    # Completion measures supported practice, not durable learning or a pilot result.
    result = {
        "assessment_version": 1,
        "attempt_id": sid,
        "lesson_key": row.lesson_key,
        "passed": True,
        "completed_questions": len(solved),
        "first_try_correct": sum(a["is_correct"] for a in first.values()),
        "total": len(solved),
        "support_uses": sum(not a.response["is_correct"] for a in answers),
        "xp_awarded": xp,
        "xp_total": user.xp_total,
        "streak_days": user.streak_days,
        "mastery_rule": "all_authored_guided_mcq_frq_transfer_correct_with_retries",
        "educational_effectiveness": "not_verified",
    }
    row.result = result
    db.commit()
    return result
