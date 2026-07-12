"""Auto-seed the SAT/IELTS question bank on startup.

Production (Render Postgres) starts with an empty database, so the Question Bank
would show 0 questions. This loads the bundled fixture (exported from the curated
local bank — 900+ questions across every SAT domain and the IELTS skills) the
first time the table is empty. It's a no-op on every subsequent boot and on any
environment that already has questions, so it's safe to call unconditionally.
"""
import json
import logging
import os

from services.db import SessionLocal
from services.models import SatIeltsQuestion

logger = logging.getLogger(__name__)

_SEED_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "seeds", "sat_bank_full.json")


def seed_question_bank_if_empty() -> None:
    """Bulk-insert the fixture questions when the bank is empty. Best-effort."""
    db = SessionLocal()
    try:
        existing = db.query(SatIeltsQuestion).count()
        if existing > 0:
            return  # already populated — nothing to do
        if not os.path.exists(_SEED_FILE):
            logger.warning("Question bank empty but seed fixture missing at %s", _SEED_FILE)
            return

        with open(_SEED_FILE, "r", encoding="utf-8") as f:
            questions = json.load(f)

        mappings = [
            {
                "exam_type": q.get("exam_type"),
                "domain": q.get("domain"),
                "skill": q.get("skill"),
                "difficulty": q.get("difficulty"),
                "question_type": q.get("question_type"),
                "question_text": q.get("question_text"),
                "options": q.get("options"),
                "correct_answer": q.get("correct_answer"),
                "rubric": q.get("rubric"),
                "source_filename": q.get("source_filename"),
                "tags": q.get("tags") or [],
            }
            for q in questions
            if q.get("exam_type") and q.get("question_text")
        ]
        db.bulk_insert_mappings(SatIeltsQuestion, mappings)
        db.commit()
        logger.info("Seeded question bank with %d questions.", len(mappings))
    except Exception as e:  # noqa: BLE001 — never block startup on seeding
        db.rollback()
        logger.warning("Question bank auto-seed failed: %s", e)
    finally:
        db.close()
