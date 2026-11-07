import json
import os
from pathlib import Path
from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/feedback", tags=["feedback"])

DATA_DIR = "data/feedback"
os.makedirs(DATA_DIR, exist_ok=True)


class FeedbackRequest(BaseModel):
    name: str
    email: str
    message: str
    rating: int | None = None


@router.post("/submit")
def submit_feedback(data: FeedbackRequest):
    entry = {
        "name": data.name.strip(),
        "email": data.email.strip().lower(),
        "message": data.message.strip(),
        "rating": data.rating,
        "submitted_at": datetime.utcnow().isoformat() + "Z",
    }
    path = f"{DATA_DIR}/feedback.jsonl"
    from services.private_file_lock import exclusive_file_lock
    with exclusive_file_lock(Path(path).with_suffix('.lock')):
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return {"message": "Thank you for your feedback!"}
