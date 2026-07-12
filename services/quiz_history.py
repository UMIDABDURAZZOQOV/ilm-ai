import json
import os
from datetime import datetime
from typing import Any

from services.users import USE_DB
from services.db import SessionLocal
from services.models import QuizSession

DATA_DIR = "data/quiz_history"
os.makedirs(DATA_DIR, exist_ok=True)


def _path(user_id: int) -> str:
    return f"{DATA_DIR}/user_{user_id}.json"


def _row_to_dict(row: QuizSession) -> dict[str, Any]:
    return {
        "id": row.id,
        "completed_at": row.completed_at.isoformat() + "Z" if row.completed_at else "",
        "score": row.score,
        "total": row.total,
        "difficulty": row.difficulty,
        "results": row.results,
    }


def load_sessions(user_id: int) -> list[dict[str, Any]]:
    if USE_DB:
        db = SessionLocal()
        try:
            rows = (
                db.query(QuizSession)
                .filter(QuizSession.user_id == user_id)
                .order_by(QuizSession.id.asc())
                .all()
            )
            return [_row_to_dict(r) for r in rows]
        finally:
            db.close()

    path = _path(user_id)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)


def save_sessions(user_id: int, sessions: list[dict[str, Any]]) -> None:
    """Only used by the JSON fallback path; DB path persists per-session in add_session."""
    with open(_path(user_id), "w", encoding="utf-8") as f:
        json.dump(sessions, f, ensure_ascii=False, indent=2)


def add_session(
    user_id: int,
    score: int,
    total: int,
    difficulty: str,
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    if USE_DB:
        db = SessionLocal()
        try:
            row = QuizSession(
                user_id=user_id,
                score=score,
                total=total,
                difficulty=difficulty,
                results=results,
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            return _row_to_dict(row)
        finally:
            db.close()

    sessions = load_sessions(user_id)
    session = {
        "id": len(sessions) + 1,
        "completed_at": datetime.utcnow().isoformat() + "Z",
        "score": score,
        "total": total,
        "difficulty": difficulty,
        "results": results,
    }
    sessions.append(session)
    save_sessions(user_id, sessions)
    return session
