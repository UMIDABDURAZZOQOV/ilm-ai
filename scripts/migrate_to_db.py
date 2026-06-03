"""Run this script to create DB tables and import existing JSON data into Postgres.

Usage:
  python scripts/migrate_to_db.py

It reads `users.json`, `data/quiz_history/user_{id}.json` and `vectors/*.json` and inserts them into the new database.

Make sure `DATABASE_URL` is set in .env or environment.
"""
import json
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from services.db import engine
from services.models import Base, User, VectorEntry, QuizSession
from services.users import load_users

load_dotenv()

print("Creating tables...")
Base.metadata.create_all(bind=engine)

print("Loading users.json and inserting into DB...")
users = load_users()

with Session(engine) as sess:
    for u in users:
        exists = sess.query(User).filter(User.id == u["id"]).first()
        if exists:
            continue
        user = User(
            id=u["id"],
            name=u.get("name", ""),
            email=u.get("email", ""),
            password=u.get("password", ""),
            telegram_chat_id=u.get("telegram_chat_id"),
            reminder_time=u.get("reminder_time", "09:00"),
            streak_days=u.get("streak_days", 0),
            last_study_date=u.get("last_study_date"),
            subscription_tier=u.get("subscription_tier", "free"),
            uploads_count=u.get("uploads_count", 0),
            quiz_count_today=u.get("quiz_count_today", 0),
            quiz_count_date=u.get("quiz_count_date"),
            chat_count_today=u.get("chat_count_today", 0),
            chat_count_date=u.get("chat_count_date"),
        )
        sess.add(user)
    sess.commit()

print("Importing quiz history...")
quiz_dir = Path("data/quiz_history")
with Session(engine) as sess:
    for f in quiz_dir.glob("user_*.json"):
        uid = int(f.stem.split("_")[1])
        try:
            arr = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for s in arr:
            exists = sess.query(QuizSession).filter(QuizSession.id == s.get("id")).first()
            if exists:
                continue
            qs = QuizSession(
                id=s.get("id"),
                user_id=uid,
                completed_at=s.get("completed_at"),
                score=s.get("score"),
                total=s.get("total"),
                difficulty=s.get("difficulty"),
                results=s.get("results"),
            )
            sess.add(qs)
    sess.commit()

print("Importing vectors...")
vec_dir = Path("vectors")
with Session(engine) as sess:
    for f in vec_dir.glob("user_*.json"):
        try:
            arr = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for v in arr:
            # v expected to have id or filename::chunk
            chunk_id = v.get("id") or v.get("chunk_id")
            exists = sess.query(VectorEntry).filter(VectorEntry.chunk_id == chunk_id).first()
            if exists:
                continue
            ve = VectorEntry(
                user_id=int(f.stem.split("_")[1]),
                filename=v.get("filename"),
                chunk_id=chunk_id,
                text=v.get("text"),
                embedding=v.get("embedding"),
            )
            sess.add(ve)
    sess.commit()

print("Migration complete. Review DB contents.")
