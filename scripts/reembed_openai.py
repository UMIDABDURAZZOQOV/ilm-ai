"""One-off migration: re-embed every stored chunk with the current OpenAI
embedding model.

Existing `vectors` rows were embedded with Gemini (gemini-embedding-001, 3072
dims). After switching the app to OpenAI (text-embedding-3-small, 1536 dims) the
old vectors no longer match query vectors, so RAG silently returns nothing for
already-uploaded materials. This script rewrites each row's `embedding` using
OpenAI so retrieval works again.

It is idempotent and re-runnable: it probes the live embedding dimension first
and only re-embeds rows whose stored vector isn't already that dimension, so
running it twice does no extra work and interrupting it is safe.

Run it where the app's DATABASE_URL points at the real database (e.g. the Render
shell), with OPENAI_API_KEY set:

    python -m scripts.reembed_openai
    python -m scripts.reembed_openai --all      # force re-embed every row
"""
from __future__ import annotations

import sys
import time

from dotenv import load_dotenv

load_dotenv()

from services.db import SessionLocal
from services.models import VectorEntry
from services.gemini import embed_content  # OpenAI-backed despite the name

BATCH = 64


def _embed(texts: list[str]) -> list[list[float]]:
    result = embed_content(model="openai", contents=texts)
    return [list(e.values) for e in result.embeddings]


def _target_dim() -> int:
    probe = _embed(["dimension probe"])
    return len(probe[0])


def main(force_all: bool = False) -> None:
    dim = _target_dim()
    print(f"Target embedding dimension: {dim}")

    db = SessionLocal()
    try:
        total = db.query(VectorEntry).count()
        print(f"{total} chunk rows in the store.")

        # Pull ids first so we don't hold a huge result set in memory.
        ids = [row[0] for row in db.query(VectorEntry.id).all()]

        done = 0
        skipped = 0
        pending: list[VectorEntry] = []

        def flush(rows: list[VectorEntry]) -> int:
            if not rows:
                return 0
            texts = [(r.text or "") for r in rows]
            vectors = _embed(texts)
            for r, v in zip(rows, vectors):
                r.embedding = v
            db.commit()
            return len(rows)

        for i, vid in enumerate(ids):
            entry = db.get(VectorEntry, vid)
            if entry is None:
                continue
            emb = entry.embedding
            already_ok = (not force_all) and isinstance(emb, list) and len(emb) == dim
            if already_ok:
                skipped += 1
                continue
            pending.append(entry)
            if len(pending) >= BATCH:
                try:
                    done += flush(pending)
                except Exception as exc:  # noqa: BLE001
                    print(f"  batch failed ({str(exc)[:120]}) — retrying after 15s")
                    time.sleep(15)
                    done += flush(pending)
                pending = []
                print(f"  re-embedded {done} / updated so far (skipped {skipped})")

        done += flush(pending)
        print(f"Done. Re-embedded {done} rows, skipped {skipped} already-current rows.")
    finally:
        db.close()


if __name__ == "__main__":
    main(force_all="--all" in sys.argv)
