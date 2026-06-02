from services.db import engine
from sqlalchemy import text
import json

"""
Prepare the database for pgvector migration:
- Ensure the `vector` extension exists (requires superuser privileges).
- Detect embedding dimension from an existing JSON embedding in `vectors.embedding`.
- Add `embedding_vector` column of type `vector(<dim>)` if not present.

This script does NOT migrate data; use it as a preparatory step before running a migration that fills `embedding_vector`.
"""

with engine.connect() as conn:
    # create extension if possible
    try:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        print("Ensured `vector` extension exists (if permitted)")
    except Exception as e:
        print("Could not create `vector` extension:", e)

    # detect dimension
    dim = None
    try:
        res = conn.execute(text("SELECT embedding FROM vectors WHERE embedding IS NOT NULL LIMIT 1;"))
        row = res.fetchone()
        if row and row[0]:
            emb = row[0]
            if isinstance(emb, str):
                try:
                    emb = json.loads(emb)
                except Exception:
                    emb = None
            if isinstance(emb, (list, tuple)):
                dim = len(emb)
    except Exception:
        pass

    if not dim:
        print("Could not detect embedding dimension automatically. Please provide dimension manually.")
    else:
        col_sql = f"ALTER TABLE vectors ADD COLUMN IF NOT EXISTS embedding_vector vector({dim});"
        try:
            conn.execute(text(col_sql))
            print(f"Added embedding_vector column with dimension {dim}")
        except Exception as e:
            print("Could not add embedding_vector column:", e)

    print("Done. Next: run a script to migrate JSON embeddings into the new column (not included).")
