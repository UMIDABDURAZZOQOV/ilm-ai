"""Export the cleaned+retagged SAT question bank from local SQLite to a JSON file.

Reads the LOCAL SQLite DB directly (data/ilm_ai.db) — independent of DATABASE_URL —
and writes every SAT question to scripts/seeds/sat_bank_export.json. Safe, read-only,
no effect on any running service. Pair with sync_sat_bank_to_prod.py to load into
production Postgres.
"""
import json, os, sys

from sqlalchemy import create_engine, text

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SQLITE = os.path.join(ROOT, "data", "ilm_ai.db")
OUT = os.path.join(HERE, "seeds", "sat_bank_export.json")

engine = create_engine(f"sqlite:///{SQLITE}", future=True)
cols = ["exam_type", "domain", "skill", "difficulty", "question_type",
        "question_text", "options", "correct_answer", "rubric",
        "source_filename", "tags"]

rows = []
with engine.connect() as conn:
    res = conn.execute(text(
        f"SELECT {', '.join(cols)} FROM sat_ielts_questions WHERE exam_type='SAT'"
    ))
    for r in res.mappings():
        d = dict(r)
        # options/tags are stored as JSON text in SQLite — normalise to python objects
        for j in ("options", "tags"):
            v = d.get(j)
            if isinstance(v, str):
                try: d[j] = json.loads(v)
                except Exception: d[j] = None
        rows.append(d)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False)

print(f"Exported {len(rows)} SAT questions -> {OUT}")
print(f"File size: {os.path.getsize(OUT)/1024:.0f} KB")
