"""
sat_subscription.py — SAT/IELTS-specific daily counter enforcement.

Uses SatIeltsUserPrefs (stored in DB) rather than the file-based subscriptions.py,
so no structural changes to the existing User model are needed.
"""
from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from services.models import SatIeltsUserPrefs, User

SAT_FREE_DAILY_QUESTIONS = 10
SAT_FREE_DAILY_AI_GENERATED = 10


def _get_or_create_prefs(user_id: int, db: Session) -> SatIeltsUserPrefs:
    prefs = db.query(SatIeltsUserPrefs).filter(SatIeltsUserPrefs.user_id == user_id).first()
    if not prefs:
        prefs = SatIeltsUserPrefs(user_id=user_id)
        db.add(prefs)
        db.commit()
        db.refresh(prefs)
    return prefs


def _reset_if_stale(prefs: SatIeltsUserPrefs, db: Session) -> None:
    """Reset questions_today if the stored date is not today (UTC)."""
    today = date.today().isoformat()
    if prefs.questions_date != today:
        prefs.questions_today = 0
        prefs.questions_date = today
        db.commit()


def _is_premium(user_id: int, db: Session) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    return getattr(user, "subscription_tier", "free") == "premium"


def can_attempt_sat_ielts(user_id: int, db: Session) -> tuple[bool, str]:
    """Check daily question limit.

    Free tier  : max SAT_FREE_DAILY_QUESTIONS per UTC calendar day.
    Premium    : unlimited.

    Resets the counter automatically on date roll-over.
    """
    if _is_premium(user_id, db):
        return True, ""

    prefs = _get_or_create_prefs(user_id, db)
    _reset_if_stale(prefs, db)

    if prefs.questions_today >= SAT_FREE_DAILY_QUESTIONS:
        return (
            False,
            f"Daily SAT/IELTS limit reached ({SAT_FREE_DAILY_QUESTIONS} questions). "
            "Upgrade to Premium for unlimited practice.",
        )
    return True, ""


def record_sat_ielts_attempt(user_id: int, count: int, db: Session) -> None:
    """Increment questions_today by *count*. Resets counter if date has changed."""
    prefs = _get_or_create_prefs(user_id, db)
    _reset_if_stale(prefs, db)
    prefs.questions_today = (prefs.questions_today or 0) + count
    db.commit()


def reset_daily_counters_utc(db: Session) -> int:
    """Reset questions_today for all users whose counter date is stale.

    Intended to be called at midnight UTC (e.g. from a scheduled job).
    Returns the number of rows updated.
    """
    today = date.today().isoformat()
    stale = (
        db.query(SatIeltsUserPrefs)
        .filter(SatIeltsUserPrefs.questions_date != today)
        .all()
    )
    count = 0
    for prefs in stale:
        prefs.questions_today = 0
        prefs.questions_date = today
        count += 1
    if count:
        db.commit()
    return count
