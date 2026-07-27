"""
send_streak_reminders.py — nudge learners whose streak is about to break.

A user with a live streak who has not studied today loses it at midnight. Once a day,
in the evening, we send them a push reminder (via the FCM/Expo path already used by the
mobile app) so the streak — the single biggest reason people come back — survives.

Run by the Render cron service defined in render.yaml; safe to run by hand too:

    python scripts/send_streak_reminders.py
"""
from __future__ import annotations

import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.db import SessionLocal              # noqa: E402
from services.models import User                  # noqa: E402
from services.push import send_push               # noqa: E402


def main() -> int:
    today = date.today().isoformat()
    db = SessionLocal()
    sent = 0
    try:
        # A streak worth protecting, a token to reach them on, and nothing studied today.
        users = (
            db.query(User)
            .filter(
                User.streak_days >= 1,
                User.push_token.isnot(None),
                (User.last_study_date.is_(None)) | (User.last_study_date != today),
            )
            .all()
        )
        for u in users:
            days = u.streak_days or 0
            title = f"🔥 {days} kunlik streak xavf ostida!"
            body = "Bugun hali mashq qilmadingiz. Streakni saqlab qolish uchun bitta dars yeching."
            try:
                if send_push(u.push_token, title, body, {"type": "streak_reminder"}):
                    sent += 1
            except Exception as exc:                # one bad token must not stop the run
                print(f"reminder to user {u.id} failed: {exc}", flush=True)
        print(f"streak reminders: {sent} sent / {len(users)} at risk", flush=True)
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
