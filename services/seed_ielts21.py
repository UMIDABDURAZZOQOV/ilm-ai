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
_SEEDS_DIR = os.path.join(_ROOT, "scripts", "seeds")


def _fixtures() -> list[tuple[int, str]]:
    """Every Cambridge volume whose fixture is committed, as (book, path).

    Adding a book is dropping `ielts20.json` in beside `ielts21.json`; nothing here
    should need editing for it.
    """
    import glob
    import re as _re
    out = []
    for path in sorted(glob.glob(os.path.join(_SEEDS_DIR, "ielts*.json"))):
        m = _re.search(r"ielts(\d+)\.json$", os.path.basename(path))
        if m:
            out.append((int(m.group(1)), path))
    return out
_EXPECTED_QUESTIONS = 320          # 4 tests × (40 listening + 40 reading)
_EXPECTED_AUDIO_PARTS = 16         # 4 tests × 4 listening parts
_EXPECTED_TABLES = 3               # the book prints three: L1P1, L2P1 and R2P1


def _fixture_counts(path: str) -> tuple[int, int]:
    """(questions, sections with a table) that this fixture should produce.

    Read from the fixture rather than hard-coded: volumes differ, and a constant like
    "expect 3 tables" is only true of book 21. The first version compared against
    `>= 1`, which meant a book that lost two of its three tables still looked fine.
    """
    import json

    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    questions = tables = 0
    for test in data.get("tests", []):
        for section in test.get("listening", []) + test.get("reading", []):
            questions += len(section.get("questions", []))
            if section.get("tables"):
                tables += 1
    return questions, tables


def _fixture_differs(db, path: str) -> bool:
    """True when the fixture's question text is not what the database holds.

    Counting rows is not enough: a parser fix changes the *wording* of questions
    without changing how many there are, and that is exactly what happened — a note
    that wrapped mid-sentence lost its tail, and every count stayed green. Sampling a
    handful of texts catches it for the price of one query.
    """
    import json

    with open(path, encoding="utf-8") as fh:
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
    """Load every committed Cambridge fixture whose content is not already in place.

    Each volume is checked and seeded on its own, so buying Cambridge 20 is a matter of
    dropping `ielts20.json` into scripts/seeds — no code here changes.
    """
    fixtures = _fixtures()
    if not fixtures:
        logger.warning("No Cambridge fixtures found in %s", _SEEDS_DIR)
        return

    for book, path in fixtures:
        prefix = f"Cambridge {book} Test"
        db = SessionLocal()
        try:
            listening = db.query(IeltsListening).filter(IeltsListening.title.like(f"{prefix}%"))
            reading = db.query(IeltsReading).filter(IeltsReading.title.like(f"{prefix}%"))
            # Counted per skill. `parent_id` is only unique *within* a skill — listening
            # part 5 and reading passage 5 are both parent_id 5 — so matching on the ids
            # alone counts every reading question against the listening rows too. The
            # total came out larger than the fixture holds, and since the guard asks for
            # "at least as many", a book that had lost questions would still look whole.
            existing = sum(
                db.query(IeltsQuestion).filter(
                    IeltsQuestion.skill == skill_name,
                    IeltsQuestion.parent_id.in_(ids),
                ).count()
                for skill_name, ids in (
                    ("Listening", [r.id for r in listening.all()]),
                    ("Reading", [r.id for r in reading.all()]),
                ) if ids
            )
            with_audio = listening.filter(IeltsListening.audio_url.isnot(None)).count()
            # Counting rows and sampling question text both miss a field that is new —
            # the printed tables arrived without a single question changing, so neither
            # check fired and production kept serving sections with no table at all.
            #
            # Counted in Python on purpose: a JSON column stores Python None as the JSON
            # value `null`, not as SQL NULL, so `tables.isnot(None)` matches every row
            # and the guard silently passes for a database with no tables in it at all.
            with_tables = sum(
                1 for (t,) in listening.with_entities(IeltsListening.tables).all() if t
            ) + sum(
                1 for (t,) in reading.with_entities(IeltsReading.tables).all() if t
            )
            stale = _fixture_differs(db, path)
        except Exception as exc:                   # table may not exist on a cold DB
            logger.warning("Cambridge %s seed check failed: %s", book, exc)
            db.close()
            continue
        finally:
            db.close()

        want_questions, want_tables = _fixture_counts(path)
        if (existing >= want_questions and with_audio >= _EXPECTED_AUDIO_PARTS
                and with_tables >= want_tables and not stale):
            continue

        logger.info("Seeding Cambridge %s (have %s/%s questions, %s with audio, %s/%s "
                    "with tables)", book, existing, want_questions, with_audio,
                    with_tables, want_tables)
        sys.path.insert(0, os.path.join(_ROOT, "scripts"))
        os.environ["IELTS_BOOK"] = str(book)
        try:
            import importlib
            import seed_ielts21 as seeder            # noqa: PLC0415 — script-local
            importlib.reload(seeder)                 # picks up IELTS_BOOK
            argv, sys.argv = sys.argv, ["seed_ielts21.py"]
            try:
                seeder.main()
            finally:
                sys.argv = argv
        except Exception as exc:
            logger.exception("Cambridge %s seeding failed: %s", book, exc)
