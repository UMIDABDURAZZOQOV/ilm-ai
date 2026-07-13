"""Load the exported SAT bank into a target Postgres, additively and safely.

Usage (run from the ilm-ai directory), passing the target DB URL via env var so
no password is hard-coded:

    TARGET_DATABASE_URL="postgresql://USER:PASS@HOST:5432/DBNAME" python scripts/sync_sat_bank_to_prod.py

What it does:
  • Reads scripts/seeds/sat_bank_export.json (produced by export_sat_bank.py).
  • Connects DIRECTLY to TARGET_DATABASE_URL (never touches local SQLite / services.db).
  • Skips any question whose exact question_text already exists in the target
    (dedupe) — so re-running is safe and existing users' data is untouched.
  • INSERTs only the new rows, in batches, inside a transaction.

It is purely additive: no schema change, no deletes, no restart needed. The live
API reads questions from the DB per-request, so new questions appear immediately.
"""
import json, os, sys

from sqlalchemy import create_engine, MetaData, Table, select, insert

HERE = os.path.dirname(os.path.abspath(__file__))
EXPORT = os.path.join(HERE, "seeds", "sat_bank_export.json")

url = os.environ.get("TARGET_DATABASE_URL", "").strip()
if not url:
    sys.exit("ERROR: set TARGET_DATABASE_URL to your production Postgres URL first.")
# Render/Heroku sometimes give postgres:// — SQLAlchemy needs postgresql://
if url.startswith("postgres://"):
    url = "postgresql://" + url[len("postgres://"):]

with open(EXPORT, encoding="utf-8") as f:
    questions = json.load(f)
print(f"Loaded {len(questions)} questions from export file.")

engine = create_engine(url, future=True)
md = MetaData()
tbl = Table("sat_ielts_questions", md, autoload_with=engine)

with engine.begin() as conn:
    existing = {
        row[0]
        for row in conn.execute(
            select(tbl.c.question_text).where(tbl.c.exam_type == "SAT")
        )
    }
    print(f"Target already has {len(existing)} SAT questions.")

    new_rows = [q for q in questions if q.get("question_text") not in existing]
    # de-dupe within the file itself too
    seen = set()
    deduped = []
    for q in new_rows:
        t = q.get("question_text")
        if t in seen:
            continue
        seen.add(t)
        deduped.append(q)

    print(f"Inserting {len(deduped)} new questions (skipping {len(questions) - len(deduped)} dupes)...")

    BATCH = 500
    inserted = 0
    for i in range(0, len(deduped), BATCH):
        chunk = deduped[i : i + BATCH]
        conn.execute(insert(tbl), chunk)
        inserted += len(chunk)
        print(f"  ...{inserted}/{len(deduped)}")

    total = conn.execute(
        select(tbl.c.id).where(tbl.c.exam_type == "SAT")
    ).rowcount

print(f"\nDone. Inserted {inserted} new SAT questions.")
print("No restart needed — the live API will serve them immediately.")
