from services.db import SessionLocal
from services.models import AssistantMessage

MAX_HISTORY_PAIRS = 10


def load_history(user_id: int) -> list[dict]:
    db = SessionLocal()
    try:
        rows = (
            db.query(AssistantMessage)
            .filter(AssistantMessage.user_id == user_id)
            .order_by(AssistantMessage.id.asc())
            .all()
        )
        return [{"role": r.role, "content": r.content} for r in rows[-MAX_HISTORY_PAIRS * 2:]]
    finally:
        db.close()


def append_message(user_id: int, role: str, content: str) -> None:
    db = SessionLocal()
    try:
        db.add(AssistantMessage(user_id=user_id, role=role, content=content))
        db.commit()
    finally:
        db.close()


def clear_history(user_id: int) -> None:
    db = SessionLocal()
    try:
        db.query(AssistantMessage).filter(AssistantMessage.user_id == user_id).delete()
        db.commit()
    finally:
        db.close()
