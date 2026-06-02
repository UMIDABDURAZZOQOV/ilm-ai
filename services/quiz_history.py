import json
import os
from datetime import datetime
from typing import Any

DATA_DIR = "data/quiz_history"
os.makedirs(DATA_DIR, exist_ok=True)


def _path(user_id: int) -> str:
    return f"{DATA_DIR}/user_{user_id}.json"


def load_sessions(user_id: int) -> list[dict[str, Any]]:
    path = _path(user_id)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_sessions(user_id: int, sessions: list[dict[str, Any]]) -> None:
    with open(_path(user_id), "w", encoding="utf-8") as f:
        json.dump(sessions, f, ensure_ascii=False, indent=2)


def add_session(
    user_id: int,
    score: int,
    total: int,
    difficulty: str,
    results: list[dict[str, Any]],
) -> dict[str, Any]:
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
