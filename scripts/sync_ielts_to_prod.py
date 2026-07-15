"""Sync LOCAL sqlite IELTS content -> PROD Postgres, de-duplicated.

- Reads data/ilm_ai.db (local).
- Copies only UNIQUE parents (reading/listening/writing/speaking) by natural key.
- Copies Reading/Listening questions, remapping parent_id to the new prod ids.
- Idempotent: skips parents already present in prod (by natural key), so it is
  safe to re-run. Additive only (no deletes / no schema change).

Run:
  TARGET_DATABASE_URL="postgresql://.../ilm_ai_db" python scripts/sync_ielts_to_prod.py
"""
import os
import sqlite3
import json
from sqlalchemy import create_engine, MetaData, Table, select, insert
from sqlalchemy import JSON as SA_JSON

LOCAL_DB = os.path.join(os.path.dirname(__file__), "..", "data", "ilm_ai.db")

# parent table -> (columns to copy, natural-key columns for dedup)
PARENTS = {
    "ielts_reading":   (["section", "title", "passage_text", "difficulty", "word_count"], ["title", "passage_text"]),
    "ielts_listening": (["section", "title", "audio_url", "transcript", "difficulty", "duration_seconds"], ["title", "transcript"]),
    "ielts_writing":   (["task_type", "category", "prompt", "image_url", "min_words", "duration_minutes", "difficulty"], ["prompt"]),
    "ielts_speaking":  (["part", "topic", "questions", "cue_card", "prep_seconds", "speak_seconds", "difficulty"], ["topic"]),
}
# skill in ielts_questions -> parent table it links to via parent_id
Q_SKILL_PARENT = {"Reading": "ielts_reading", "Listening": "ielts_listening"}
Q_COLS = ["skill", "parent_id", "question_type", "question_text", "options", "correct_answer", "hint", "order_index"]


def coerce(table, colname, value):
    """If the prod column is a JSON type, parse stringified JSON; else pass through."""
    col = table.c[colname]
    if isinstance(col.type, SA_JSON) and isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return value
    return value


def main():
    url = os.environ.get("TARGET_DATABASE_URL")
    if not url:
        raise SystemExit("Set TARGET_DATABASE_URL to the prod Postgres URL")
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    con = sqlite3.connect(LOCAL_DB)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    engine = create_engine(url, future=True)
    md = MetaData()
    ptables = {name: Table(name, md, autoload_with=engine) for name in PARENTS}
    qtable = Table("ielts_questions", md, autoload_with=engine)

    # local_parent_id -> new prod id, per parent table
    id_map = {name: {} for name in PARENTS}

    with engine.begin() as c:
        # ---- parents ----
        for tname, (cols, keycols) in PARENTS.items():
            ptable = ptables[tname]
            rows = cur.execute(f"SELECT * FROM {tname} ORDER BY id").fetchall()
            seen_local = {}  # natural-key -> local id we keep (canonical)
            inserted = skipped_dup = skipped_exists = 0
            for r in rows:
                key = tuple(r[k] for k in keycols)
                if key in seen_local:
                    # duplicate within local -> point its id at the canonical prod id later
                    id_map[tname][r["id"]] = id_map[tname].get(seen_local[key])
                    skipped_dup += 1
                    continue
                seen_local[key] = r["id"]
                # already in prod? (by natural key)
                where = [ptable.c[k] == r[k] for k in keycols]
                existing = c.execute(select(ptable.c.id).where(*where)).first()
                if existing:
                    id_map[tname][r["id"]] = existing[0]
                    skipped_exists += 1
                    continue
                vals = {col: coerce(ptable, col, r[col]) for col in cols}
                new_id = c.execute(insert(ptable).values(**vals).returning(ptable.c.id)).scalar()
                id_map[tname][r["id"]] = new_id
                inserted += 1
            print(f"{tname}: +{inserted} inserted, {skipped_dup} local-dup, {skipped_exists} already-in-prod")

        # ---- questions (Reading + Listening only) ----
        q_inserted = q_skipped = 0
        qrows = cur.execute("SELECT * FROM ielts_questions ORDER BY parent_id, order_index").fetchall()
        for r in qrows:
            parent_tbl = Q_SKILL_PARENT.get(r["skill"])
            if not parent_tbl:
                q_skipped += 1
                continue
            new_parent = id_map[parent_tbl].get(r["parent_id"])
            if new_parent is None:
                q_skipped += 1
                continue
            # dedup: same parent + question_text already in prod?
            exists = c.execute(select(qtable.c.id).where(
                qtable.c.skill == r["skill"],
                qtable.c.parent_id == new_parent,
                qtable.c.question_text == r["question_text"],
            )).first()
            if exists:
                q_skipped += 1
                continue
            vals = {col: coerce(qtable, col, r[col]) for col in Q_COLS}
            vals["parent_id"] = new_parent
            c.execute(insert(qtable).values(**vals))
            q_inserted += 1
        print(f"ielts_questions: +{q_inserted} inserted, {q_skipped} skipped (dup/no-parent)")

    # ---- verify ----
    with engine.connect() as c:
        print("\n=== PROD row counts now ===")
        for tname in list(PARENTS) + ["ielts_questions"]:
            n = c.execute(select(ptables[tname].c.id if tname in ptables else qtable.c.id)).rowcount
        for tname in list(PARENTS):
            from sqlalchemy import func
            n = c.execute(select(func.count()).select_from(ptables[tname])).scalar()
            print(f"  {tname}: {n}")
        from sqlalchemy import func
        print(f"  ielts_questions: {c.execute(select(func.count()).select_from(qtable)).scalar()}")


if __name__ == "__main__":
    main()
