"""Local Math v1: immutable attempts, guided retries, one-time account XP.

All answers are server graded. No existing subject router or schema is changed.
An answer request UUID is an idempotency key; a new UUID permits a real retry.
"""

import os
from copy import deepcopy
from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy import func, inspect, update
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


def available_books(db):
    """Only imported preview books; never expose unreviewed TOC-only courses."""
    sources = {(b["grade"], b["part"]): b for b in manifest()["books"]}
    result = []
    for grade, part, count in (
        db.query(MathLesson.grade, MathLesson.part, func.count(MathLesson.key))
        .group_by(MathLesson.grade, MathLesson.part)
        .order_by(MathLesson.grade, MathLesson.part)
    ):
        source = sources[(grade, part)]
        roman = {1: "I", 2: "II", 3: "III", 4: "IV"}.get(part, str(part))
        result.append(
            {
                "book_id": source["book_id"],
                "grade": grade,
                "part": part,
                "label": f"{grade}-sinf · {roman} qism",
                "bibliography": source.get("bibliography", {}),
                "implemented_sections": count,
                "source_topic_count": source.get("topic_count"),
                "source_body_topic_count": source.get("body_topic_count"),
                "source_gaps": source.get("source_gaps", []),
            }
        )
    return result


def previous_book_complete(db, completed, grade, part):
    if part == 1:
        return True
    source = next(
        (
            b
            for b in manifest()["books"]
            if (b["grade"], b["part"]) == (grade, part - 1)
        ),
        None,
    )
    expected = source.get("topic_count") if source else None
    if not expected:
        return False
    rows = db.query(MathLesson.key).filter_by(grade=grade, part=part - 1).all()
    return len(rows) == expected and all(key in completed for (key,) in rows)


def qa_source_gap_bridge(db, completed, grade, part):
    """One explicit local-QA exception; it never completes or rewards missing74.

    Keep the ordinary source-complete prerequisite. Only this reviewed pair of
    books may be exercised after all existing predecessor lessons are complete.
    Neither a learner request nor a generic missing-source entry grants access.
    """
    if (
        (grade, part) != (1, 3)
        or os.getenv("MATHEMATICS_QA_SOURCE_GAP_BRIDGE", "").lower() != "true"
        or os.getenv("MATHEMATICS_PREVIEW_ENABLED", "").lower() != "true"
    ):
        return None
    try:
        staging_url(db.get_bind().url)
    except ValueError:
        return None
    source = next(b for b in manifest()["books"] if b["book_id"] == "math-uz-g1-p2")
    target = next(b for b in manifest()["books"] if b["book_id"] == "math-uz-g1-p3")
    gaps = source.get("source_gaps", [])
    if (
        source["sha256"]
        != "b45a8a2927f087b976a4c7a0213a8c3ec3f968b736b2a9c057308a8892757c05"
        or target["sha256"]
        != "46183895898c54f0554bdc47238b2d9ae8312225712618f20d9a9c9c467b0adf"
        or source.get("topic_count") != 33
        or source.get("available_body_topics") != 32
        or len(gaps) != 1
        or gaps[0].get("topic_source_number") != 74
        or gaps[0].get("missing_printed_pages") != [68, 69]
    ):
        return None
    rows = (
        db.query(MathLesson.key, MathLesson.sequence)
        .filter_by(grade=1, part=2)
        .order_by(MathLesson.sequence)
        .all()
    )
    expected = [(f"math-1-2-{n}-r1", n) for n in range(1, 33)]
    if rows != expected or not all(key in completed for key, _ in rows):
        return None
    # The predecessor's own prerequisites remain mandatory too.
    if not previous_book_complete(db, completed, 1, 2):
        return None
    return {
        "kind": "local_qa_known_source_gap",
        "previous_book_id": source["book_id"],
        "missing_source_numbers": [74],
        "missing_printed_pages": [68, 69],
        "previous_book_complete": False,
        "teacher_review": "not_verified",
        "message": "Lokal sinov: II qismning mavjud 32 darsi bajarilgan. 74-mavzuning bosma 68–69-sahifalari yo‘q; bu mavzu bajarilgan deb belgilanmagan. III qismni sinash yoqilgan, kurs hali to‘liq emas.",
    }


def catalog(db, uid, grade=1, part=1):
    rows = (
        db.query(MathLesson)
        .filter_by(grade=grade, part=part)
        .order_by(MathLesson.sequence)
        .all()
    )
    completed = {p.lesson_key for p in db.query(MathProgress).filter_by(user_id=uid)}
    previous_ready = previous_book_complete(db, completed, grade, part)
    bridge = (
        None if previous_ready else qa_source_gap_bridge(db, completed, grade, part)
    )
    navigation_ready = previous_ready or bridge is not None
    ready = navigation_ready
    books = available_books(db)
    lessons = []
    for index, lesson in enumerate(rows, 1):
        ready = ready and lesson.sequence == index
        done = lesson.key in completed
        lessons.append(
            {
                "key": lesson.key,
                "title": lesson.document["title"],
                "sequence": lesson.sequence,
                "source_number": lesson.document.get("source_number", lesson.sequence),
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
        "available_books": books,
        "book": next(
            (b for b in books if (b["grade"], b["part"]) == (grade, part)), None
        ),
        "previous_book_complete": previous_ready,
        "previous_book_navigation_ready": navigation_ready,
        "source_gap_bridge": bridge,
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
    if row.result is None and row.snapshot.get("qa_source_gap_bridge"):
        completed = {
            p.lesson_key for p in db.query(MathProgress).filter_by(user_id=uid)
        }
        if not previous_book_complete(db, completed, 1, 3) and not qa_source_gap_bridge(
            db, completed, 1, 3
        ):
            raise HTTPException(403, "math_source_gap_preview_disabled")
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
        "source_gap_bridge": doc.get("qa_source_gap_bridge"),
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
    course = catalog(db, uid, lesson.grade, lesson.part)
    state = next(
        (l["state"] for l in course["lessons"] if l["key"] == key),
        "locked",
    )
    if state == "locked":
        raise HTTPException(
            403,
            "finish_previous_lesson"
            if course["previous_book_navigation_ready"]
            else "finish_previous_book",
        )
    snapshot = deepcopy(lesson.document)
    if course["source_gap_bridge"]:
        snapshot["qa_source_gap_bridge"] = course["source_gap_bridge"]
    row = MathAttempt(
        id=sid,
        user_id=uid,
        lesson_key=key,
        started_at=utcnow(),
        snapshot=snapshot,
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
        "source_gap_bridge": row.snapshot.get("qa_source_gap_bridge"),
    }
    row.result = result
    db.commit()
    return result
