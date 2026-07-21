"""Auto-seed the calibrated placement bank on startup, from the fixture that
scripts/seed_placement.py dumps. Production never calls Gemini live.

Incremental by (subject, level, skill): the bank is generated over several days
against the free tier's daily quota, so each deploy picks up whatever buckets have
been filled since the last one without duplicating what is already there.
"""
import json
import logging
import os

from services.db import SessionLocal
from services.models import PlacementQuestion

logger = logging.getLogger(__name__)

_SEED_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "scripts", "seeds", "placement_bank.json",
)


def seed_placement_if_needed() -> None:
    if not os.path.exists(_SEED_FILE):
        return

    db = SessionLocal()
    try:
        with open(_SEED_FILE, encoding="utf-8") as fh:
            rows = json.load(fh)

        # Question text is the natural identity here — the fixture has no ids, and
        # matching on it makes a re-run of the generator idempotent even when it
        # renumbers rows.
        existing = {t for (t,) in db.query(PlacementQuestion.question_text).all()}
        mappings = [
            {
                "subject_slug": r["subject_slug"],
                "level": r["level"],
                "skill": r.get("skill"),
                "question_text": r["question_text"],
                "options": r["options"],
                "correct_answer": r["correct_answer"],
                "explanation": r.get("explanation"),
            }
            for r in rows
            if r.get("question_text") and r["question_text"] not in existing
        ]
        if mappings:
            db.bulk_insert_mappings(PlacementQuestion, mappings)
            db.commit()
            logger.info("Seeded %s placement questions.", len(mappings))
    except Exception as e:  # noqa: BLE001 -- never block startup on seeding
        db.rollback()
        logger.warning("Placement bank auto-seed failed: %s", e)
    finally:
        db.close()
