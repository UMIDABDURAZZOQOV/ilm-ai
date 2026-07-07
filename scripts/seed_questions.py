"""Seed the SAT/IELTS question bank.

Run once from the ilm-ai/ directory:
    python scripts/seed_questions.py

Delete data/sat_ielts_seeded.flag to re-seed.
"""

import os
import sys
import json

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.db import SessionLocal, engine, Base
from services.models import SatIeltsQuestion
from services.question_bank import validate_question, add_question

# Auto-create tables if they don't exist yet
Base.metadata.create_all(bind=engine)

FLAG_FILE = "data/sat_ielts_seeded.flag"

SEED_FILES = [
    "scripts/seeds/sat_questions.json",
    "scripts/seeds/ielts_questions.json",
]


def seed():
    if os.path.exists(FLAG_FILE):
        print("Already seeded. Delete data/sat_ielts_seeded.flag to re-seed.")
        return

    db = SessionLocal()
    try:
        for fname in SEED_FILES:
            if not os.path.exists(fname):
                print(f"Seed file not found: {fname}")
                continue

            with open(fname, "r", encoding="utf-8") as f:
                questions = json.load(f)

            inserted = 0
            skipped = 0

            for q in questions:
                ok, err = validate_question(q)
                if not ok:
                    print(f"  [INVALID] {err} — {q.get('question_text', '')[:60]}")
                    skipped += 1
                    continue

                # Idempotency: skip if already in DB (match on exam_type + domain + first 200 chars)
                existing = (
                    db.query(SatIeltsQuestion)
                    .filter(
                        SatIeltsQuestion.exam_type == q["exam_type"],
                        SatIeltsQuestion.domain == q["domain"],
                        SatIeltsQuestion.question_text.startswith(
                            q["question_text"][:200]
                        ),
                    )
                    .first()
                )
                if existing:
                    skipped += 1
                    continue

                try:
                    add_question(db, q)
                    inserted += 1
                except Exception as exc:
                    print(f"  [ERROR] {exc}")
                    skipped += 1

            print(f"{fname}: inserted={inserted}, skipped={skipped}")

        # Write flag file to prevent double-seeding
        os.makedirs("data", exist_ok=True)
        open(FLAG_FILE, "w").close()
        print("\nSeeding complete!")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
