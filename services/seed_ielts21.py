"""Auto-seed Cambridge IELTS 21 Academic on startup.

Production (Render Postgres) has no way to run `scripts/seed_ielts21.py`, and the very
first extraction left the IELTS tables holding 16 stub passages and *zero* questions —
so this reseeds whenever what's in the database doesn't match the bundled fixture.

Keyed on the question count rather than "is the table empty", because the broken rows
were not empty; they were wrong. The owner holds a licence for the book and its audio.
"""
import logging
import os
import sys

from services.db import SessionLocal
from services.models import IeltsQuestion

logger = logging.getLogger(__name__)

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SEED_FILE = os.path.join(_ROOT, "scripts", "seeds", "ielts21.json")
_EXPECTED_QUESTIONS = 320          # 4 tests × (40 listening + 40 reading)


def seed_ielts21_if_needed() -> None:
    """Load the fixture unless the database already holds exactly this content."""
    if not os.path.exists(_SEED_FILE):
        logger.warning("Cambridge 21 fixture missing at %s", _SEED_FILE)
        return

    db = SessionLocal()
    try:
        existing = db.query(IeltsQuestion).count()
    except Exception as exc:                       # table may not exist on a cold DB
        logger.warning("Cambridge 21 seed check failed: %s", exc)
        return
    finally:
        db.close()

    if existing == _EXPECTED_QUESTIONS:
        return

    logger.info("Seeding Cambridge 21 (found %s questions, expected %s)",
                existing, _EXPECTED_QUESTIONS)
    sys.path.insert(0, os.path.join(_ROOT, "scripts"))
    try:
        from seed_ielts21 import main as run_seed   # noqa: PLC0415 — optional, script-local
        argv, sys.argv = sys.argv, ["seed_ielts21.py", "--purge-legacy"]
        try:
            run_seed()
        finally:
            sys.argv = argv
    except Exception as exc:
        logger.exception("Cambridge 21 seeding failed: %s", exc)
