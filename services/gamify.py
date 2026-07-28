"""
Lightweight gamification for the Ilm AI core: studying with the companion / Studio
counts toward the same streak the rest of the app uses, and earns a little XP. Safe
and idempotent — if anything fails it never blocks the actual feature.
"""
from __future__ import annotations

from services.db import SessionLocal
from services.models import User
from services.users import record_study_activity

# Small, so it rewards engagement without trivialising the skill-tree XP economy.
DEFAULT_XP = 2


def award_study(user_id: int, xp: int = DEFAULT_XP) -> None:
    """Mark today's study activity (streak) and add a little XP. Best-effort."""
    try:
        record_study_activity(user_id)
    except Exception:
        pass
    if xp <= 0:
        return
    try:
        db = SessionLocal()
        try:
            u = db.query(User).filter(User.id == user_id).first()
            if u:
                u.xp_total = int(u.xp_total or 0) + xp
                db.add(u)
                db.commit()
        finally:
            db.close()
    except Exception:
        pass


def get_stats(user_id: int) -> dict:
    db = SessionLocal()
    try:
        u = db.query(User).filter(User.id == user_id).first()
        if not u:
            return {"xp_total": 0, "streak_days": 0}
        return {"xp_total": int(u.xp_total or 0), "streak_days": int(u.streak_days or 0)}
    finally:
        db.close()
