"""
routers/mock_exam.py -- Milliy Sertifikat mock exam (Sinov imtihoni) + AI-style
score prediction. A timed, server-graded block of questions for one subject,
producing a DTM-style certificate grade and a predicted real-exam grade blended
from the learner's lesson mastery and past mock results.

All endpoints live under /skills (same prefix family as the skill tree).
"""
from __future__ import annotations

import random
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func as sa_func
from sqlalchemy.orm import Session

from services.auth_deps import ensure_own_user, get_authenticated_user_id, verify_user_access
from services.db import get_db
from services.models import (
    SkillLesson,
    SkillMockExam,
    SkillQuestion,
    SkillSubject,
    SkillUnit,
    User,
    UserLessonProgress,
)
from services.users import record_study_activity

router = APIRouter(prefix="/skills", tags=["mock-exam"])

MOCK_EXAM_SIZE = 30
MOCK_EXAM_DURATION_SECONDS = 30 * 60  # 30 minutes

# DTM-style certificate bands (percentage of the exam). A learner earns a
# certificate at 60%+; below that is "Sertifikatsiz" (no certificate). These are
# a clearly-labelled mock scale, not an official DTM table.
GRADE_BANDS = [
    (93, "A+"),
    (85, "A"),
    (78, "B+"),
    (70, "B"),
    (65, "C+"),
    (60, "C"),
]


def grade_for(pct: float) -> str:
    for threshold, label in GRADE_BANDS:
        if pct >= threshold:
            return label
    return "Sertifikatsiz"


def _subject_question_ids(db: Session, subject_slug: str) -> tuple[SkillSubject | None, list[int]]:
    s = db.query(SkillSubject).filter(SkillSubject.slug == subject_slug).first()
    if not s:
        return None, []
    unit_ids = [u.id for u in db.query(SkillUnit).filter(SkillUnit.subject_id == s.id).all()]
    lesson_ids = (
        [l.id for l in db.query(SkillLesson).filter(SkillLesson.unit_id.in_(unit_ids)).all()]
        if unit_ids else []
    )
    ids = (
        [row[0] for row in db.query(SkillQuestion.id).filter(SkillQuestion.lesson_id.in_(lesson_ids)).all()]
        if lesson_ids else []
    )
    return s, ids


def _subject_mastery_pct(db: Session, user_id: int, subject: SkillSubject) -> float | None:
    """Average best-score across the subject's completed lessons (0-100), or
    None if the learner hasn't finished any lesson in this subject yet."""
    unit_ids = [u.id for u in db.query(SkillUnit).filter(SkillUnit.subject_id == subject.id).all()]
    lesson_ids = (
        [l.id for l in db.query(SkillLesson).filter(SkillLesson.unit_id.in_(unit_ids)).all()]
        if unit_ids else []
    )
    if not lesson_ids:
        return None
    avg = (
        db.query(sa_func.avg(UserLessonProgress.best_score_pct))
        .filter(
            UserLessonProgress.user_id == user_id,
            UserLessonProgress.lesson_id.in_(lesson_ids),
            UserLessonProgress.completed_at.isnot(None),
        )
        .scalar()
    )
    return float(avg) if avg is not None else None


def _prediction(db: Session, user_id: int, subject: SkillSubject, latest_pct: float | None) -> dict | None:
    """Blend the latest mock %, the average of past mocks, and lesson mastery
    into a single predicted real-exam %. Confidence rises with more evidence."""
    past = (
        db.query(SkillMockExam.percentage)
        .filter(
            SkillMockExam.user_id == user_id,
            SkillMockExam.subject_slug == subject.slug,
            SkillMockExam.status == "completed",
            SkillMockExam.percentage.isnot(None),
        )
        .all()
    )
    past_pcts = [float(p[0]) for p in past if p[0] is not None]
    mastery = _subject_mastery_pct(db, user_id, subject)

    signals: list[tuple[float, float]] = []  # (value, weight)
    if latest_pct is not None:
        signals.append((latest_pct, 0.5))
    if past_pcts:
        signals.append((sum(past_pcts) / len(past_pcts), 0.3))
    if mastery is not None:
        signals.append((mastery, 0.2))

    if not signals:
        return None

    total_w = sum(w for _, w in signals)
    predicted = sum(v * w for v, w in signals) / total_w
    predicted = round(max(0.0, min(100.0, predicted)), 1)

    evidence = len(past_pcts) + (1 if mastery is not None else 0)
    confidence = "low" if evidence <= 1 else "medium" if evidence <= 3 else "high"

    return {
        "predicted_pct": predicted,
        "predicted_grade": grade_for(predicted),
        "confidence": confidence,
        "based_on_exams": len(past_pcts),
        "used_mastery": mastery is not None,
    }


@router.get("/{user_id}/mock-exam")
def mock_exam_overview(subject: str, user_id: int = Depends(verify_user_access), db: Session = Depends(get_db)):
    s, ids = _subject_question_ids(db, subject)
    if not s:
        raise HTTPException(status_code=404, detail="Subject not found")

    attempts = (
        db.query(SkillMockExam)
        .filter(
            SkillMockExam.user_id == user_id,
            SkillMockExam.subject_slug == subject,
            SkillMockExam.status == "completed",
        )
        .order_by(SkillMockExam.completed_at.desc())
        .limit(10)
        .all()
    )
    best = None
    for a in attempts:
        if a.percentage is not None and (best is None or a.percentage > best["percentage"]):
            best = {"percentage": round(a.percentage, 1), "grade": a.grade}

    return {
        "subject_slug": s.slug,
        "subject_name_uz": s.name_uz,
        "subject_name_ru": s.name_ru,
        "subject_name_en": s.name_en,
        "color": s.color,
        "available_questions": len(ids),
        "size": min(MOCK_EXAM_SIZE, len(ids)),
        "duration_seconds": MOCK_EXAM_DURATION_SECONDS,
        "best": best,
        "attempts": [
            {
                "id": a.id,
                "percentage": round(a.percentage, 1) if a.percentage is not None else None,
                "grade": a.grade,
                "score": a.score,
                "total": a.total,
                "completed_at": a.completed_at.isoformat() if a.completed_at else None,
            }
            for a in attempts
        ],
        "prediction": _prediction(db, user_id, s, best["percentage"] if best else None),
    }


class StartMockRequest(BaseModel):
    user_id: int
    subject: str


@router.post("/mock-exam/start")
def start_mock_exam(
    data: StartMockRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    ensure_own_user(data.user_id, auth_user_id)
    s, ids = _subject_question_ids(db, data.subject)
    if not s:
        raise HTTPException(status_code=404, detail="Subject not found")
    if not ids:
        raise HTTPException(status_code=400, detail="No questions for this subject")

    chosen = random.sample(ids, min(MOCK_EXAM_SIZE, len(ids)))
    exam = SkillMockExam(
        user_id=data.user_id,
        subject_slug=data.subject,
        status="in_progress",
        question_ids=chosen,
        duration_seconds=MOCK_EXAM_DURATION_SECONDS,
    )
    db.add(exam)
    db.commit()
    db.refresh(exam)

    q_map = {q.id: q for q in db.query(SkillQuestion).filter(SkillQuestion.id.in_(chosen)).all()}
    # No correct_answer sent during the exam -- it's server-graded on complete.
    questions = [
        {"id": i, "question_text": q_map[i].question_text, "options": q_map[i].options}
        for i in chosen if i in q_map
    ]
    return {
        "exam_id": exam.id,
        "subject_name_uz": s.name_uz,
        "duration_seconds": MOCK_EXAM_DURATION_SECONDS,
        "questions": questions,
    }


class MockAnswerItem(BaseModel):
    question_id: int
    user_answer: str | None = None


class CompleteMockRequest(BaseModel):
    user_id: int
    answers: list[MockAnswerItem]


@router.post("/mock-exam/{exam_id}/complete")
def complete_mock_exam(
    exam_id: int,
    data: CompleteMockRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    ensure_own_user(data.user_id, auth_user_id)
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    exam = (
        db.query(SkillMockExam)
        .filter(SkillMockExam.id == exam_id, SkillMockExam.user_id == data.user_id)
        .first()
    )
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    q_ids = list(exam.question_ids or [])
    q_map = {q.id: q for q in db.query(SkillQuestion).filter(SkillQuestion.id.in_(q_ids)).all()}
    answers = {a.question_id: (a.user_answer or "") for a in data.answers}

    # Already-graded exam -> return idempotently (re-open the review, no re-award).
    if exam.status == "completed":
        return _exam_result_payload(db, user, exam, q_map)

    review = []
    score = 0
    for qid in q_ids:
        q = q_map.get(qid)
        if not q:
            continue
        ua = answers.get(qid, "")
        is_correct = bool(ua) and ua.strip() == (q.correct_answer or "").strip()
        if is_correct:
            score += 1
        review.append({"question_id": qid, "user_answer": ua, "is_correct": is_correct})

    total = len(q_ids)
    pct = round(score / total * 100, 1) if total else 0.0
    grade = grade_for(pct)

    s = db.query(SkillSubject).filter(SkillSubject.slug == exam.subject_slug).first()
    pred = _prediction(db, data.user_id, s, pct) if s else None

    now = datetime.now(timezone.utc)
    exam.status = "completed"
    exam.score = score
    exam.total = total
    exam.percentage = pct
    exam.grade = grade
    exam.predicted_grade = pred["predicted_grade"] if pred else grade
    exam.predicted_pct = pred["predicted_pct"] if pred else pct
    exam.results = review
    exam.completed_at = now
    db.add(exam)

    # A flat, modest XP reward so mock exams contribute to streak/goal without
    # becoming an XP farm (the per-question bank is finite).
    xp_awarded = min(score, 20)
    user.xp_total = (user.xp_total or 0) + xp_awarded
    db.add(user)
    db.commit()
    db.refresh(user)
    record_study_activity(data.user_id)

    return _exam_result_payload(db, user, exam, q_map, xp_awarded=xp_awarded)


def _exam_result_payload(db: Session, user: User, exam: SkillMockExam, q_map: dict, xp_awarded: int = 0) -> dict:
    review = exam.results or []
    ans_by_q = {r["question_id"]: r for r in review}
    detail = []
    for qid in (exam.question_ids or []):
        q = q_map.get(qid)
        if not q:
            continue
        r = ans_by_q.get(qid, {})
        detail.append({
            "question_text": q.question_text,
            "options": q.options,
            "correct_answer": q.correct_answer,
            "explanation": q.explanation,
            "user_answer": r.get("user_answer", ""),
            "is_correct": r.get("is_correct", False),
        })
    s = db.query(SkillSubject).filter(SkillSubject.slug == exam.subject_slug).first()
    return {
        "exam_id": exam.id,
        "score": exam.score,
        "total": exam.total,
        "percentage": round(exam.percentage, 1) if exam.percentage is not None else None,
        "grade": exam.grade,
        "certificate": exam.grade != "Sertifikatsiz",
        "predicted_grade": exam.predicted_grade,
        "predicted_pct": exam.predicted_pct,
        "prediction": _prediction(db, exam.user_id, s, exam.percentage) if s else None,
        "xp_awarded": xp_awarded,
        "xp_total": user.xp_total,
        "review": detail,
    }
