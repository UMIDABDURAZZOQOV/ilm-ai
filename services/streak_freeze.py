"""
Streak freezes — small, self-contained helper the streak logic calls to protect a
streak across missed days. Backward compatible: a learner with zero freezes behaves
exactly as before (a gap resets the streak).
"""
from __future__ import annotations

from services.db import SessionLocal
from services.models import StreakFreeze

FREEZE_CAP = 3          # most a learner can hold
GRANT_EVERY = 7         # earn one freeze each time the streak crosses a 7-day mark


def get_count(user_id: int) -> int:
    db = SessionLocal()
    try:
        row = db.query(StreakFreeze).filter(StreakFreeze.user_id == user_id).first()
        return int(row.count) if row else 0
    finally:
        db.close()


def _row(db, user_id: int) -> StreakFreeze:
    row = db.query(StreakFreeze).filter(StreakFreeze.user_id == user_id).first()
    if not row:
        row = StreakFreeze(user_id=user_id, count=0)
        db.add(row)
    return row


def consume(user_id: int, needed: int) -> int:
    """Try to spend `needed` freezes; returns how many were actually consumed
    (0 if none available). Never goes negative."""
    if needed <= 0:
        return 0
    db = SessionLocal()
    try:
        row = _row(db, user_id)
        used = min(int(row.count or 0), needed)
        if used:
            row.count = int(row.count) - used
            db.commit()
        return used
    finally:
        db.close()


def grant(user_id: int, n: int = 1, cap: int = FREEZE_CAP) -> int:
    """Add freezes up to the cap; returns the new total."""
    db = SessionLocal()
    try:
        row = _row(db, user_id)
        row.count = min(cap, int(row.count or 0) + n)
        db.commit()
        return int(row.count)
    finally:
        db.close()
