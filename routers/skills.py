"""
routers/skills.py -- Milliy Sertifikat Skill Tree (Duolingo-style) endpoints.
All endpoints live under the /skills prefix. JWT auth via the same
verify_user_access / ensure_own_user pattern used across the app.
"""
from __future__ import annotations

import random
from datetime import date, datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func as sa_func
from sqlalchemy.orm import Session

from services.auth_deps import ensure_own_user, get_authenticated_user_id, verify_user_access
from services.db import get_db
from services.models import (
    PlacementQuestion,
    SkillDailyChallenge,
    SkillLesson,
    SkillLessonAttempt,
    SkillMistake,
    SkillQuestion,
    SkillSubject,
    SkillUnit,
    User,
    UserLanguageLevel,
    UserLessonProgress,
    UserUnitExam,
)
from services.placement import (
    LANGUAGE_SUBJECT_SLUGS,
    QUESTIONS_PER_LEVEL,
    level_label,
    levels_for,
    score_placement,
)
from services.skill_tree import build_tree, lesson_status, newly_unlocked_lesson_ids
from services.users import record_study_activity

router = APIRouter(prefix="/skills", tags=["skills"])


DAILY_GOAL_XP = 20


def _gamification_block(user: User, db: Session | None = None) -> dict:
    block = {
        "xp_total": user.xp_total,
        "streak_days": user.streak_days or 0,
    }
    if db is not None:
        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        lesson_xp = (
            db.query(sa_func.coalesce(sa_func.sum(SkillLessonAttempt.xp_awarded), 0))
            .filter(SkillLessonAttempt.user_id == user.id, SkillLessonAttempt.completed_at >= today_start)
            .scalar()
        ) or 0
        daily = (
            db.query(SkillDailyChallenge)
            .filter(SkillDailyChallenge.user_id == user.id, SkillDailyChallenge.date == date.today().isoformat())
            .first()
        )
        block["today_xp"] = int(lesson_xp) + (daily.xp_awarded or 0 if daily else 0)
        block["daily_goal_xp"] = DAILY_GOAL_XP
    return block


@router.get("/subjects")
def list_subjects(db: Session = Depends(get_db)):
    subjects = db.query(SkillSubject).filter(SkillSubject.is_active.is_(True)).order_by(SkillSubject.order_index).all()
    return [
        {
            "id": s.id,
            "slug": s.slug,
            "name_uz": s.name_uz,
            "name_ru": s.name_ru,
            "name_en": s.name_en,
            "icon": s.icon,
            "color": s.color,
        }
        for s in subjects
    ]


@router.get("/{user_id}/summary")
def get_summary(user_id: int = Depends(verify_user_access), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _gamification_block(user, db)


@router.get("/{user_id}/tree")
def get_tree(
    subject: str,
    user_id: int = Depends(verify_user_access),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    tree = build_tree(db, user_id, subject)
    if not tree:
        raise HTTPException(status_code=404, detail="Subject not found")

    tree["user"] = _gamification_block(user, db)
    return tree


class StartLessonRequest(BaseModel):
    user_id: int


@router.post("/lessons/{lesson_id}/start")
def start_lesson(
    lesson_id: int,
    data: StartLessonRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    ensure_own_user(data.user_id, auth_user_id)
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    lesson = db.query(SkillLesson).filter(SkillLesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    status = lesson_status(db, data.user_id, lesson)
    if status == "locked":
        raise HTTPException(status_code=403, detail="locked")

    attempt = SkillLessonAttempt(user_id=data.user_id, lesson_id=lesson_id)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    questions = (
        db.query(SkillQuestion)
        .filter(SkillQuestion.lesson_id == lesson_id)
        .order_by(SkillQuestion.order_index)
        .all()
    )
    return {
        "attempt_id": attempt.id,
        # Duolingo-style: the client shows these teaching cards first, THEN the questions.
        "theory": lesson.theory or [],
        "questions": [
            {
                "id": q.id,
                "question_text": q.question_text,
                "options": q.options,
                "correct_answer": q.correct_answer,
                "explanation": q.explanation,
                "order_index": q.order_index,
            }
            for q in questions
        ],
    }


class LessonResultItem(BaseModel):
    question_id: int
    user_answer: str
    is_correct: bool


class CompleteLessonRequest(BaseModel):
    user_id: int
    attempt_id: int
    results: list[LessonResultItem]


# Star tiers, and the pass mark. Earning at least one star (>= 60%) completes the
# lesson and unlocks the next node; below that the learner is asked to study the
# topic again and retry. On a 10-question lesson:
#   10 or 9 correct -> 3 stars | 8 -> 2 stars | 7 or 6 -> 1 star | 5 or fewer -> fail.
STAR3_PCT = 90.0
STAR2_PCT = 80.0
STAR1_PCT = 60.0
PASS_THRESHOLD_PCT = STAR1_PCT


@router.post("/lessons/{lesson_id}/complete")
def complete_lesson(
    lesson_id: int,
    data: CompleteLessonRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    ensure_own_user(data.user_id, auth_user_id)
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    lesson = db.query(SkillLesson).filter(SkillLesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    attempt = (
        db.query(SkillLessonAttempt)
        .filter(
            SkillLessonAttempt.id == data.attempt_id,
            SkillLessonAttempt.user_id == data.user_id,
            SkillLessonAttempt.lesson_id == lesson_id,
        )
        .first()
    )
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    if attempt.completed_at is not None:
        # Already submitted -- return the original result idempotently rather
        # than re-awarding XP on a replayed request.
        prev_pct = (attempt.score / attempt.total * 100) if attempt.total else 0.0
        return {
            "passed": prev_pct >= PASS_THRESHOLD_PCT,
            "pass_threshold_pct": PASS_THRESHOLD_PCT,
            "stars": (
                db.query(UserLessonProgress)
                .filter(UserLessonProgress.user_id == data.user_id, UserLessonProgress.lesson_id == lesson_id)
                .first()
                .stars
            ),
            "score": attempt.score,
            "total": attempt.total,
            "xp_awarded": attempt.xp_awarded,
            "xp_total": user.xp_total,
            "streak_days": user.streak_days or 0,
            "newly_unlocked_lesson_ids": [],
        }

    # Server recomputes score from submitted results -- never trusts a client score.
    total = len(data.results)
    score = sum(1 for r in data.results if r.is_correct)
    score_pct = (score / total * 100) if total > 0 else 0.0

    if score_pct >= STAR3_PCT:
        stars = 3
    elif score_pct >= STAR2_PCT:
        stars = 2
    elif score_pct >= STAR1_PCT:
        stars = 1
    else:
        stars = 0

    progress = (
        db.query(UserLessonProgress)
        .filter(UserLessonProgress.user_id == data.user_id, UserLessonProgress.lesson_id == lesson_id)
        .first()
    )
    # Failing the threshold never completes the lesson (and so never unlocks the
    # next one). An already-completed lesson stays completed if a later replay
    # falls short -- we only ever move progress forward.
    passed = stars >= 1  # i.e. score_pct >= STAR1_PCT
    already_completed = bool(progress and progress.completed_at is not None)
    is_first_completion = passed and not already_completed
    xp_awarded = lesson.xp_reward if is_first_completion else 5

    now = datetime.now(timezone.utc)
    if not progress:
        progress = UserLessonProgress(user_id=data.user_id, lesson_id=lesson_id, stars=0, attempts=0)
        db.add(progress)

    progress.attempts = (progress.attempts or 0) + 1
    progress.stars = max(progress.stars or 0, stars)
    progress.best_score_pct = max(progress.best_score_pct or 0, score_pct)
    progress.xp_earned = (progress.xp_earned or 0) + xp_awarded
    progress.last_attempt_at = now
    if is_first_completion:
        progress.completed_at = now

    user.xp_total = (user.xp_total or 0) + xp_awarded
    db.add(user)

    attempt.completed_at = now
    attempt.score = score
    attempt.total = total
    attempt.xp_awarded = xp_awarded
    attempt.results = [r.model_dump() for r in data.results]
    db.add(attempt)
    db.commit()
    db.refresh(user)

    # Mistakes notebook: a wrong answer becomes (or refreshes) an unresolved
    # mistake; a correct answer resolves any previously recorded one.
    for r in data.results:
        m = db.query(SkillMistake).filter(SkillMistake.user_id == data.user_id, SkillMistake.question_id == r.question_id).first()
        if r.is_correct:
            if m and m.resolved_at is None:
                m.resolved_at = now
                db.add(m)
        else:
            if m:
                m.wrong_count = (m.wrong_count or 0) + 1
                m.last_wrong_at = now
                m.resolved_at = None
            else:
                m = SkillMistake(user_id=data.user_id, question_id=r.question_id, wrong_count=1, last_wrong_at=now)
            db.add(m)
    db.commit()

    unlocked_ids = newly_unlocked_lesson_ids(db, data.user_id, lesson) if is_first_completion else []

    streak = record_study_activity(data.user_id)

    return {
        "passed": passed,
        "pass_threshold_pct": PASS_THRESHOLD_PCT,
        "stars": stars,
        "score": score,
        "total": total,
        "xp_awarded": xp_awarded,
        "xp_total": user.xp_total,
        "streak_days": streak.get("streak_days", user.streak_days or 0),
        "newly_unlocked_lesson_ids": unlocked_ids,
    }


# ─── Leaderboard ───────────────────────────────────────────────────────────────

@router.get("/leaderboard/weekly")
def weekly_leaderboard(
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    """Top-20 users by XP earned in the last 7 days (skill-tree activity),
    plus the requesting user's own rank -- Duolingo-style weekly league."""
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    rows = (
        db.query(
            SkillLessonAttempt.user_id,
            sa_func.sum(SkillLessonAttempt.xp_awarded).label("xp"),
        )
        .filter(SkillLessonAttempt.completed_at >= week_ago)
        .group_by(SkillLessonAttempt.user_id)
        .order_by(sa_func.sum(SkillLessonAttempt.xp_awarded).desc())
        .all()
    )
    user_ids = [r.user_id for r in rows]
    users = {u.id: u for u in db.query(User).filter(User.id.in_(user_ids)).all()} if user_ids else {}

    entries = []
    own_rank = None
    for rank, r in enumerate(rows, start=1):
        u = users.get(r.user_id)
        if r.user_id == auth_user_id:
            own_rank = rank
        if rank <= 20:
            entries.append({
                "rank": rank,
                "user_id": r.user_id,
                "name": (u.name if u else "..."),
                "profile_picture": (u.profile_picture if u else None),
                "weekly_xp": int(r.xp or 0),
                "league": _league_for(int(r.xp or 0))["id"],
                "is_me": r.user_id == auth_user_id,
            })
    return {"entries": entries, "own_rank": own_rank, "total_participants": len(rows)}


# ─── Mistakes notebook (Xatolar daftari) ──────────────────────────────────────

@router.get("/{user_id}/mistakes")
def list_mistakes(user_id: int = Depends(verify_user_access), db: Session = Depends(get_db)):
    mistakes = (
        db.query(SkillMistake)
        .filter(SkillMistake.user_id == user_id, SkillMistake.resolved_at.is_(None))
        .order_by(SkillMistake.last_wrong_at.desc())
        .limit(20)
        .all()
    )
    q_ids = [m.question_id for m in mistakes]
    questions = {q.id: q for q in db.query(SkillQuestion).filter(SkillQuestion.id.in_(q_ids)).all()} if q_ids else {}
    out = []
    for m in mistakes:
        q = questions.get(m.question_id)
        if not q:
            continue
        out.append({
            "id": q.id,
            "question_text": q.question_text,
            "options": q.options,
            "correct_answer": q.correct_answer,
            "explanation": q.explanation,
            "wrong_count": m.wrong_count,
        })
    return {"questions": out, "count": len(out)}


class PracticeResultItem(BaseModel):
    question_id: int
    is_correct: bool


class PracticeCompleteRequest(BaseModel):
    user_id: int
    results: list[PracticeResultItem]


@router.post("/mistakes/complete")
def complete_mistakes_practice(
    data: PracticeCompleteRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    ensure_own_user(data.user_id, auth_user_id)
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    now = datetime.now(timezone.utc)
    correct = 0
    for r in data.results:
        m = db.query(SkillMistake).filter(SkillMistake.user_id == data.user_id, SkillMistake.question_id == r.question_id).first()
        if not m:
            continue
        if r.is_correct:
            m.resolved_at = now
            correct += 1
        else:
            m.wrong_count = (m.wrong_count or 0) + 1
            m.last_wrong_at = now
        db.add(m)

    xp_awarded = min(correct, 10)
    user.xp_total = (user.xp_total or 0) + xp_awarded
    db.add(user)
    db.commit()
    db.refresh(user)
    streak = record_study_activity(data.user_id)
    remaining = db.query(SkillMistake).filter(SkillMistake.user_id == data.user_id, SkillMistake.resolved_at.is_(None)).count()
    return {
        "resolved": correct,
        "remaining": remaining,
        "xp_awarded": xp_awarded,
        "xp_total": user.xp_total,
        "streak_days": streak.get("streak_days", user.streak_days or 0),
    }


# ─── Daily challenge (Kunlik sinov) ───────────────────────────────────────────

DAILY_CHALLENGE_SIZE = 10


def _daily_questions(db: Session, user_id: int) -> list[SkillQuestion]:
    """Deterministic per-(user, day) sample so refreshing the page never
    reshuffles today's challenge."""
    ids = [row[0] for row in db.query(SkillQuestion.id).order_by(SkillQuestion.id).all()]
    if not ids:
        return []
    rng = random.Random(f"{user_id}-{date.today().isoformat()}")
    chosen = rng.sample(ids, min(DAILY_CHALLENGE_SIZE, len(ids)))
    q_map = {q.id: q for q in db.query(SkillQuestion).filter(SkillQuestion.id.in_(chosen)).all()}
    return [q_map[i] for i in chosen if i in q_map]


@router.get("/{user_id}/daily-challenge")
def get_daily_challenge(user_id: int = Depends(verify_user_access), db: Session = Depends(get_db)):
    existing = (
        db.query(SkillDailyChallenge)
        .filter(SkillDailyChallenge.user_id == user_id, SkillDailyChallenge.date == date.today().isoformat())
        .first()
    )
    if existing and existing.completed_at is not None:
        return {
            "completed": True,
            "score": existing.score,
            "total": existing.total,
            "xp_awarded": existing.xp_awarded,
            "questions": [],
        }
    questions = _daily_questions(db, user_id)
    return {
        "completed": False,
        "questions": [
            {
                "id": q.id,
                "question_text": q.question_text,
                "options": q.options,
                "correct_answer": q.correct_answer,
                "explanation": q.explanation,
            }
            for q in questions
        ],
    }


class DailyCompleteRequest(BaseModel):
    user_id: int
    results: list[PracticeResultItem]


@router.post("/daily-challenge/complete")
def complete_daily_challenge(
    data: DailyCompleteRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    ensure_own_user(data.user_id, auth_user_id)
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    today = date.today().isoformat()
    existing = (
        db.query(SkillDailyChallenge)
        .filter(SkillDailyChallenge.user_id == data.user_id, SkillDailyChallenge.date == today)
        .first()
    )
    if existing and existing.completed_at is not None:
        return {
            "score": existing.score,
            "total": existing.total,
            "xp_awarded": existing.xp_awarded,
            "xp_total": user.xp_total,
            "already_completed": True,
        }

    # Server-side check: only questions actually in today's deterministic set count.
    valid_ids = {q.id for q in _daily_questions(db, data.user_id)}
    total = len(valid_ids)
    score = sum(1 for r in data.results if r.is_correct and r.question_id in valid_ids)
    xp_awarded = 10 + score  # base bonus + 1 XP per correct

    if not existing:
        existing = SkillDailyChallenge(user_id=data.user_id, date=today)
    existing.score = score
    existing.total = total
    existing.xp_awarded = xp_awarded
    existing.completed_at = datetime.now(timezone.utc)
    db.add(existing)

    user.xp_total = (user.xp_total or 0) + xp_awarded
    db.add(user)
    db.commit()
    db.refresh(user)
    streak = record_study_activity(data.user_id)
    return {
        "score": score,
        "total": total,
        "xp_awarded": xp_awarded,
        "xp_total": user.xp_total,
        "streak_days": streak.get("streak_days", user.streak_days or 0),
        "already_completed": False,
    }


# ─── Achievements (Yutuqlar) ──────────────────────────────────────────────────

@router.get("/{user_id}/achievements")
def get_achievements(user_id: int = Depends(verify_user_access), db: Session = Depends(get_db)):
    """Derived on the fly from existing stats -- no storage needed."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    lessons_completed = (
        db.query(UserLessonProgress)
        .filter(UserLessonProgress.user_id == user_id, UserLessonProgress.completed_at.isnot(None))
        .count()
    )
    perfect_lessons = (
        db.query(UserLessonProgress)
        .filter(UserLessonProgress.user_id == user_id, UserLessonProgress.stars == 3)
        .count()
    )
    questions_answered = (
        db.query(sa_func.coalesce(sa_func.sum(SkillLessonAttempt.total), 0))
        .filter(SkillLessonAttempt.user_id == user_id, SkillLessonAttempt.completed_at.isnot(None))
        .scalar()
    ) or 0
    streak = user.streak_days or 0
    xp = user.xp_total or 0

    def tiers(aid: str, value: int, targets: list[int]) -> list[dict]:
        return [
            {"id": f"{aid}_{t}", "group": aid, "target": t, "progress": min(value, t), "earned": value >= t}
            for t in targets
        ]

    achievements = (
        tiers("streak", streak, [3, 7, 30])
        + tiers("lessons", lessons_completed, [1, 10, 25, 50])
        + tiers("perfect", perfect_lessons, [1, 5, 15])
        + tiers("questions", int(questions_answered), [50, 200, 500])
        + tiers("xp", xp, [100, 500, 1000])
    )
    return {"achievements": achievements}


# ─── Lightning round (Tezlik raundi) ──────────────────────────────────────────

@router.get("/{user_id}/lightning")
def get_lightning_round(user_id: int = Depends(verify_user_access), db: Session = Depends(get_db)):
    """A fresh random batch from the whole bank -- the client runs a 60s timer."""
    ids = [row[0] for row in db.query(SkillQuestion.id).all()]
    if not ids:
        return {"questions": []}
    chosen = random.sample(ids, min(30, len(ids)))
    q_map = {q.id: q for q in db.query(SkillQuestion).filter(SkillQuestion.id.in_(chosen)).all()}
    out = []
    for i in chosen:
        q = q_map.get(i)
        if not q:
            continue
        out.append({
            "id": q.id,
            "question_text": q.question_text,
            "options": q.options,
            "correct_answer": q.correct_answer,
        })
    return {"questions": out}


class LightningCompleteRequest(BaseModel):
    user_id: int
    score: int
    total: int


@router.post("/lightning/complete")
def complete_lightning(
    data: LightningCompleteRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    ensure_own_user(data.user_id, auth_user_id)
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    xp_awarded = max(0, min(data.score, 15))  # capped -- lightning is for fun, not farming
    user.xp_total = (user.xp_total or 0) + xp_awarded
    db.add(user)
    db.commit()
    db.refresh(user)
    streak = record_study_activity(data.user_id)
    return {
        "xp_awarded": xp_awarded,
        "xp_total": user.xp_total,
        "streak_days": streak.get("streak_days", user.streak_days or 0),
    }


# ─── League tiers (derived from weekly XP — no cohort batching needed) ─────────

LEAGUE_TIERS = [
    {"id": "diamond", "name_uz": "Olmos", "name_ru": "Алмаз", "name_en": "Diamond", "min_xp": 600, "color": "#7DD3FC"},
    {"id": "gold", "name_uz": "Oltin", "name_ru": "Золото", "name_en": "Gold", "min_xp": 300, "color": "#FFC800"},
    {"id": "silver", "name_uz": "Kumush", "name_ru": "Серебро", "name_en": "Silver", "min_xp": 100, "color": "#C0C0C0"},
    {"id": "bronze", "name_uz": "Bronza", "name_ru": "Бронза", "name_en": "Bronze", "min_xp": 0, "color": "#CD7F32"},
]


def _league_for(weekly_xp: int) -> dict:
    for tier in LEAGUE_TIERS:
        if weekly_xp >= tier["min_xp"]:
            return tier
    return LEAGUE_TIERS[-1]


def _weekly_xp(db: Session, user_id: int) -> int:
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    return int(
        db.query(sa_func.coalesce(sa_func.sum(SkillLessonAttempt.xp_awarded), 0))
        .filter(SkillLessonAttempt.user_id == user_id, SkillLessonAttempt.completed_at >= week_ago)
        .scalar()
        or 0
    )


@router.get("/{user_id}/league")
def get_league(user_id: int = Depends(verify_user_access), db: Session = Depends(get_db)):
    weekly = _weekly_xp(db, user_id)
    tier = _league_for(weekly)
    idx = LEAGUE_TIERS.index(tier)
    next_tier = LEAGUE_TIERS[idx - 1] if idx > 0 else None
    return {
        "league": tier,
        "weekly_xp": weekly,
        "next_league": next_tier,
        "xp_to_next": (next_tier["min_xp"] - weekly) if next_tier else 0,
        "all_tiers": LEAGUE_TIERS,
    }


# ─── Referrals (Do'st taklif qilish) ──────────────────────────────────────────

def _ensure_referral_code(db: Session, user: User) -> str:
    if not user.referral_code:
        import secrets
        alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        for _ in range(6):
            code = "".join(secrets.choice(alphabet) for _ in range(6))
            if not db.query(User).filter(User.referral_code == code).first():
                user.referral_code = code
                db.add(user)
                db.commit()
                db.refresh(user)
                break
    return user.referral_code


REFERRAL_BONUS_XP = 50


@router.get("/{user_id}/referral")
def get_referral(user_id: int = Depends(verify_user_access), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    code = _ensure_referral_code(db, user)
    invited = db.query(User).filter(User.referred_by == user_id).count()
    return {
        "code": code,
        "invited_count": invited,
        "bonus_per_invite": REFERRAL_BONUS_XP,
        "bonus_earned": invited * REFERRAL_BONUS_XP,
    }


class ApplyReferralRequest(BaseModel):
    user_id: int
    code: str


@router.post("/referral/apply")
def apply_referral(
    data: ApplyReferralRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    ensure_own_user(data.user_id, auth_user_id)
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.referred_by is not None:
        raise HTTPException(status_code=400, detail="already_referred")

    inviter = db.query(User).filter(User.referral_code == data.code.strip().upper()).first()
    if not inviter:
        raise HTTPException(status_code=404, detail="invalid_code")
    if inviter.id == user.id:
        raise HTTPException(status_code=400, detail="self_referral")

    user.referred_by = inviter.id
    user.xp_total = (user.xp_total or 0) + REFERRAL_BONUS_XP
    inviter.xp_total = (inviter.xp_total or 0) + REFERRAL_BONUS_XP
    db.add(user)
    db.add(inviter)
    db.commit()
    db.refresh(user)
    return {"bonus_xp": REFERRAL_BONUS_XP, "xp_total": user.xp_total, "inviter_name": inviter.name}


# ─── Profile (statistika) ─────────────────────────────────────────────────────

@router.get("/{user_id}/profile")
def get_profile(user_id: int = Depends(verify_user_access), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    subjects = db.query(SkillSubject).filter(SkillSubject.is_active.is_(True)).order_by(SkillSubject.order_index).all()
    per_subject = []
    for s in subjects:
        unit_ids = [u.id for u in db.query(SkillUnit).filter(SkillUnit.subject_id == s.id).all()]
        lessons = db.query(SkillLesson).filter(SkillLesson.unit_id.in_(unit_ids)).all() if unit_ids else []
        lesson_ids = [l.id for l in lessons]
        completed = (
            db.query(UserLessonProgress)
            .filter(
                UserLessonProgress.user_id == user_id,
                UserLessonProgress.lesson_id.in_(lesson_ids),
                UserLessonProgress.completed_at.isnot(None),
            )
            .count()
        ) if lesson_ids else 0
        stars = (
            db.query(sa_func.coalesce(sa_func.sum(UserLessonProgress.stars), 0))
            .filter(UserLessonProgress.user_id == user_id, UserLessonProgress.lesson_id.in_(lesson_ids))
            .scalar()
        ) if lesson_ids else 0
        total = len(lessons)
        per_subject.append({
            "slug": s.slug,
            "name_uz": s.name_uz,
            "name_ru": s.name_ru,
            "name_en": s.name_en,
            "color": s.color,
            "completed": completed,
            "total": total,
            "stars": int(stars or 0),
            "pct": round(completed / total * 100) if total else 0,
        })

    done_subjects = [p for p in per_subject if p["completed"] > 0]
    strongest = max(done_subjects, key=lambda p: p["pct"], default=None)
    weakest = min(done_subjects, key=lambda p: p["pct"], default=None)

    # Activity calendar: attempts-per-day for the last 84 days.
    since = datetime.now(timezone.utc) - timedelta(days=84)
    rows = (
        db.query(SkillLessonAttempt.completed_at)
        .filter(SkillLessonAttempt.user_id == user_id, SkillLessonAttempt.completed_at >= since)
        .all()
    )
    activity: dict[str, int] = {}
    for (ts,) in rows:
        if ts:
            key = ts.date().isoformat()
            activity[key] = activity.get(key, 0) + 1

    total_lessons_completed = sum(p["completed"] for p in per_subject)

    return {
        "name": user.name,
        "profile_picture": user.profile_picture,
        "xp_total": user.xp_total,
        "streak_days": user.streak_days or 0,
        "lessons_completed": total_lessons_completed,
        "subjects": per_subject,
        "strongest": strongest,
        "weakest": weakest,
        "activity": activity,
        "league": _league_for(_weekly_xp(db, user_id)),
    }


# ─── Marathon / exam mode ─────────────────────────────────────────────────────

MARATHON_SIZE = 30


@router.get("/{user_id}/marathon")
def get_marathon(subject: str, user_id: int = Depends(verify_user_access), db: Session = Depends(get_db)):
    s = db.query(SkillSubject).filter(SkillSubject.slug == subject).first()
    if not s:
        raise HTTPException(status_code=404, detail="Subject not found")
    unit_ids = [u.id for u in db.query(SkillUnit).filter(SkillUnit.subject_id == s.id).all()]
    lesson_ids = [l.id for l in db.query(SkillLesson).filter(SkillLesson.unit_id.in_(unit_ids)).all()] if unit_ids else []
    ids = [row[0] for row in db.query(SkillQuestion.id).filter(SkillQuestion.lesson_id.in_(lesson_ids)).all()] if lesson_ids else []
    if not ids:
        return {"questions": []}
    chosen = random.sample(ids, min(MARATHON_SIZE, len(ids)))
    q_map = {q.id: q for q in db.query(SkillQuestion).filter(SkillQuestion.id.in_(chosen)).all()}
    out = []
    for i in chosen:
        q = q_map.get(i)
        if not q:
            continue
        out.append({
            "id": q.id,
            "question_text": q.question_text,
            "options": q.options,
            "correct_answer": q.correct_answer,
            "explanation": q.explanation,
        })
    return {"questions": out, "subject_name": s.name_uz}


class MarathonCompleteRequest(BaseModel):
    user_id: int
    score: int
    total: int


@router.post("/marathon/complete")
def complete_marathon(
    data: MarathonCompleteRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    ensure_own_user(data.user_id, auth_user_id)
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    xp_awarded = min(data.score, 30)  # 1 XP per correct, capped at the marathon size
    user.xp_total = (user.xp_total or 0) + xp_awarded
    db.add(user)
    db.commit()
    db.refresh(user)
    streak = record_study_activity(data.user_id)
    return {
        "score": data.score,
        "total": data.total,
        "xp_awarded": xp_awarded,
        "xp_total": user.xp_total,
        "streak_days": streak.get("streak_days", user.streak_days or 0),
    }


# ─── Placement test ──────────────────────────────────────────────────────────
# Offered when the learner opens a subject, so they know where they stand before
# starting the path. Languages are placed on CEFR, the academic subjects on the
# Milliy Sertifikat 1-5 scale.
#
# This used to draw 15 questions from the ordinary lesson bank and map the raw
# percentage onto a band. That was wrong twice over -- the lesson bank is not
# calibrated to CEFR (its easy/medium/hard is relative to each lesson), and a
# single percentage cannot tell "mastered A1, nothing above" from "half of
# everything". The result disagreed with other placement tests, which makes it
# worse than useless. It now draws from PlacementQuestion, whose rows are authored
# at a level, and scores by level mastery -- see services/placement.py.


def _level_row(db: Session, user_id: int, subject_slug: str) -> dict | None:
    row = (
        db.query(UserLanguageLevel)
        .filter(UserLanguageLevel.user_id == user_id, UserLanguageLevel.subject_slug == subject_slug)
        .first()
    )
    if not row:
        return None
    return {
        "level": row.level,
        "label": level_label(subject_slug, row.level),
        "score": row.score,
        "total": row.total,
        "score_pct": row.score_pct,
        "taken_at": row.taken_at.isoformat() if row.taken_at else None,
    }


@router.get("/{user_id}/level-test")
def get_level_test(
    subject: str,
    user_id: int = Depends(verify_user_access),
    db: Session = Depends(get_db),
):
    """The placement paper for a subject, plus any level the learner already has
    (so the UI can offer 'retake' instead of 'start').

    Questions are drawn evenly from every level, easiest first: the learner walks up
    the scale and the point where they stop being able to answer IS the result. The
    level of each question is sent back with it so the client can report per-level
    results, but it is never used for grading -- that happens server-side in
    /level-test/complete from the stored answers.
    """
    subject_row = db.query(SkillSubject).filter(SkillSubject.slug == subject).first()
    if not subject_row:
        raise HTTPException(status_code=404, detail="Subject not found")

    picked: list[PlacementQuestion] = []
    for level in levels_for(subject):
        rows = (
            db.query(PlacementQuestion)
            .filter(PlacementQuestion.subject_slug == subject, PlacementQuestion.level == level)
            .all()
        )
        random.shuffle(rows)
        # Spread each level's slots across its skills so a learner who is strong on
        # grammar but weak on reading cannot pass a level on grammar alone.
        by_skill: dict[str, list[PlacementQuestion]] = {}
        for r in rows:
            by_skill.setdefault(r.skill or "", []).append(r)
        chosen: list[PlacementQuestion] = []
        while len(chosen) < QUESTIONS_PER_LEVEL and any(by_skill.values()):
            for bucket in by_skill.values():
                if bucket and len(chosen) < QUESTIONS_PER_LEVEL:
                    chosen.append(bucket.pop())
        picked.extend(chosen)

    if not picked:
        raise HTTPException(status_code=404, detail="No placement questions available for this subject")

    return {
        "subject": {"slug": subject_row.slug, "name_uz": subject_row.name_uz, "color": subject_row.color},
        "scale": "cefr" if subject in LANGUAGE_SUBJECT_SLUGS else "milliy",
        "levels": [{"level": l, "label": level_label(subject, l)} for l in levels_for(subject)],
        "current_level": _level_row(db, user_id, subject),
        "questions": [
            {
                "id": p.id,
                "level": p.level,
                "skill": p.skill,
                "question_text": p.question_text,
                "options": p.options,
                "correct_answer": p.correct_answer,
                "explanation": p.explanation,
            }
            for p in picked
        ],
    }


class LevelTestResultItem(BaseModel):
    question_id: int
    is_correct: bool


class CompleteLevelTestRequest(BaseModel):
    user_id: int
    subject_slug: str
    results: list[LevelTestResultItem]


@router.post("/level-test/complete")
def complete_level_test(
    data: CompleteLevelTestRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    """Score the placement test server-side and store the resulting level.

    The client sends which questions it got right, not a level -- the level comes from
    each question's own `level` column, looked up here, so a tampered client cannot
    award itself C1.
    """
    ensure_own_user(data.user_id, auth_user_id)
    if not data.results:
        raise HTTPException(status_code=400, detail="No results submitted")

    rows = (
        db.query(PlacementQuestion)
        .filter(PlacementQuestion.id.in_([r.question_id for r in data.results]))
        .all()
    )
    level_of = {r.id: r.level for r in rows}
    if not level_of:
        raise HTTPException(status_code=400, detail="Unknown placement questions")

    per_level: dict[str, tuple[int, int]] = {}
    for r in data.results:
        lvl = level_of.get(r.question_id)
        if not lvl:
            continue
        correct, asked = per_level.get(lvl, (0, 0))
        per_level[lvl] = (correct + (1 if r.is_correct else 0), asked + 1)

    result = score_placement(data.subject_slug, per_level)
    now = datetime.now(timezone.utc)

    row = (
        db.query(UserLanguageLevel)
        .filter(UserLanguageLevel.user_id == data.user_id, UserLanguageLevel.subject_slug == data.subject_slug)
        .first()
    )
    if not row:
        row = UserLanguageLevel(user_id=data.user_id, subject_slug=data.subject_slug)
        db.add(row)
    row.level = result["level"]
    row.score = result["score"]
    row.total = result["total"]
    row.score_pct = result["score_pct"]
    row.taken_at = now
    db.commit()

    record_study_activity(data.user_id)

    return result


# ─── Unit checkpoint exam ────────────────────────────────────────────────────
# Taken at the end of a unit (bob), covering every lesson in it. Passing it is
# what unlocks the NEXT unit -- see services/skill_tree.py::build_tree. Applies
# to every subject, not just one.

UNIT_EXAM_QUESTION_COUNT = 15
UNIT_EXAM_XP = 50


def _unit_lesson_ids(db: Session, unit_id: int) -> list[int]:
    return [l.id for l in db.query(SkillLesson).filter(SkillLesson.unit_id == unit_id).all()]


@router.get("/{user_id}/unit-exam")
def get_unit_exam(
    unit_id: int,
    user_id: int = Depends(verify_user_access),
    db: Session = Depends(get_db),
):
    """Questions for a unit's checkpoint exam, drawn from every lesson in it.
    Only available once all of the unit's lessons are completed."""
    unit = db.query(SkillUnit).filter(SkillUnit.id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    lesson_ids = _unit_lesson_ids(db, unit_id)
    if not lesson_ids:
        raise HTTPException(status_code=404, detail="Unit has no lessons")

    done = (
        db.query(UserLessonProgress)
        .filter(
            UserLessonProgress.user_id == user_id,
            UserLessonProgress.lesson_id.in_(lesson_ids),
            UserLessonProgress.completed_at.isnot(None),
        )
        .count()
    )
    if done < len(lesson_ids):
        raise HTTPException(status_code=403, detail="Finish every lesson in this unit first")

    questions = db.query(SkillQuestion).filter(SkillQuestion.lesson_id.in_(lesson_ids)).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions available for this unit")
    random.shuffle(questions)
    picked = questions[:UNIT_EXAM_QUESTION_COUNT]

    prev = db.query(UserUnitExam).filter(UserUnitExam.user_id == user_id, UserUnitExam.unit_id == unit_id).first()
    return {
        "unit": {
            "id": unit.id,
            "title_uz": unit.title_uz,
            "title_ru": unit.title_ru,
            "title_en": unit.title_en,
        },
        "pass_threshold_pct": PASS_THRESHOLD_PCT,
        "previous": (
            {"passed": prev.passed, "best_score_pct": prev.best_score_pct, "attempts": prev.attempts}
            if prev
            else None
        ),
        "questions": [
            {
                "id": q.id,
                "question_text": q.question_text,
                "options": q.options,
                "correct_answer": q.correct_answer,
                "explanation": q.explanation,
            }
            for q in picked
        ],
    }


class CompleteUnitExamRequest(BaseModel):
    user_id: int
    unit_id: int
    results: list[LevelTestResultItem]


@router.post("/unit-exam/complete")
def complete_unit_exam(
    data: CompleteUnitExamRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    """Score the checkpoint server-side. Passing unlocks the next unit; failing
    leaves it locked and the learner retries."""
    ensure_own_user(data.user_id, auth_user_id)
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not data.results:
        raise HTTPException(status_code=400, detail="No results submitted")

    total = len(data.results)
    score = sum(1 for r in data.results if r.is_correct)
    score_pct = score / total * 100
    passed = score_pct >= PASS_THRESHOLD_PCT
    now = datetime.now(timezone.utc)

    row = (
        db.query(UserUnitExam)
        .filter(UserUnitExam.user_id == data.user_id, UserUnitExam.unit_id == data.unit_id)
        .first()
    )
    if not row:
        row = UserUnitExam(user_id=data.user_id, unit_id=data.unit_id, attempts=0)
        db.add(row)

    newly_passed = passed and not row.passed
    row.attempts = (row.attempts or 0) + 1
    row.score = score
    row.total = total
    row.best_score_pct = max(row.best_score_pct or 0.0, score_pct)
    row.last_attempt_at = now
    if newly_passed:
        row.passed = True            # never downgraded by a weaker retake
        row.passed_at = now

    xp_awarded = UNIT_EXAM_XP if newly_passed else 0
    if xp_awarded:
        user.xp_total = (user.xp_total or 0) + xp_awarded
        db.add(user)
    db.commit()
    db.refresh(user)

    streak = record_study_activity(data.user_id)

    return {
        "passed": passed,
        "pass_threshold_pct": PASS_THRESHOLD_PCT,
        "score": score,
        "total": total,
        "score_pct": score_pct,
        "xp_awarded": xp_awarded,
        "xp_total": user.xp_total,
        "streak_days": streak.get("streak_days", user.streak_days or 0),
    }
