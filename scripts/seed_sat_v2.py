"""Seed the skill-tagged SAT question bank (v2).

Run from the ilm-ai/ directory:
    python scripts/seed_sat_v2.py

Delete data/sat_v2_seeded.flag to re-seed.
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.db import SessionLocal, engine, Base
from services.question_bank import validate_question, add_question

Base.metadata.create_all(bind=engine)

FLAG_FILE = "data/sat_v2_seeded.flag"
SEED_FILE = "scripts/seeds/sat_questions_v2.json"


def seed():
    if os.path.exists(FLAG_FILE):
        print("Already seeded. Delete data/sat_v2_seeded.flag to re-seed.")
        return

    with open(SEED_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)

    db = SessionLocal()
    inserted = skipped = 0
    try:
        for q in questions:
            ok, err = validate_question(q)
            if not ok:
                print(f"SKIP: {err} — {q.get('question_text', '')[:60]}")
                skipped += 1
                continue
            add_question(db, q)
            inserted += 1
    finally:
        db.close()

    with open(FLAG_FILE, "w") as f:
        f.write("done")
    print(f"Inserted {inserted}, skipped {skipped}.")


if __name__ == "__main__":
    seed()
