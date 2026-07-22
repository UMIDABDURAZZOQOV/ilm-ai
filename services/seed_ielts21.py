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
from services.models import IeltsListening, IeltsQuestion, IeltsReading

logger = logging.getLogger(__name__)

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SEED_FILE = os.path.join(_ROOT, "scripts", "seeds", "ielts21.json")
_EXPECTED_QUESTIONS = 320          # 4 tests × (40 listening + 40 reading)
_EXPECTED_AUDIO_PARTS = 16         # 4 tests × 4 listening parts
_EXPECTED_TABLES = 3               # the book prints three: L1P1, L2P1 and R2P1


def _fixture_differs(db) -> bool:
    """True when the fixture's question text is not what the database holds.

    Counting rows is not enough: a parser fix changes the *wording* of questions
    without changing how many there are, and that is exactly what happened — a note
    that wrapped mid-sentence lost its tail, and every count stayed green. Sampling a
    handful of texts catches it for the price of one query.
    """
    import json

    with open(_SEED_FILE, encoding="utf-8") as fh:
        data = json.load(fh)

    sample: list[str] = []
    for test in data.get("tests", []):
        for section in test.get("reading", []) + test.get("listening", []):
            for q in section.get("questions", [])[:2]:
                if q.get("question_text"):
                    sample.append(q["question_text"])
    sample = sample[:24]
    if not sample:
        return False

    found = {
        t for (t,) in db.query(IeltsQuestion.question_text)
        .filter(IeltsQuestion.question_text.in_(sample)).all()
    }
    return len(found) < len(set(sample))


def seed_ielts21_if_needed() -> None:
    """Load the fixture unless the database already holds exactly this content."""
    if not os.path.exists(_SEED_FILE):
        logger.warning("Cambridge 21 fixture missing at %s", _SEED_FILE)
        return

    db = SessionLocal()
    try:
        existing = db.query(IeltsQuestion).count()
        # An earlier fixture resolved the mp3 paths from the local filesystem, so a
        # production seed left every audio_url NULL even though the questions were fine.
        with_audio = db.query(IeltsListening).filter(IeltsListening.audio_url.isnot(None)).count()
        stale = _fixture_differs(db)
        # Counting rows and sampling question text both miss a field that is new —
        # the printed tables arrived without a single question changing, so neither
        # check fired and production kept serving sections with no table at all.
        with_tables = (
            db.query(IeltsListening).filter(IeltsListening.tables.isnot(None)).count()
            + db.query(IeltsReading).filter(IeltsReading.tables.isnot(None)).count()
        )
    except Exception as exc:                       # table may not exist on a cold DB
        logger.warning("Cambridge 21 seed check failed: %s", exc)
        return
    finally:
        db.close()

    if (existing == _EXPECTED_QUESTIONS and with_audio >= _EXPECTED_AUDIO_PARTS
            and with_tables >= _EXPECTED_TABLES and not stale):
        return

    logger.info("Seeding Cambridge 21 (found %s questions / %s with audio / %s with "
                "tables; expected %s / %s / %s)", existing, with_audio, with_tables,
                _EXPECTED_QUESTIONS, _EXPECTED_AUDIO_PARTS, _EXPECTED_TABLES)
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
