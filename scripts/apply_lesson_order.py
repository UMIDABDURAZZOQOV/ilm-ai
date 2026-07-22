"""
apply_lesson_order.py — push the outline's lesson order into the database.

Only the structure: no Gemini call, so it finishes in seconds. seed_skilltree.py does
this too, but as a preamble to generation, and a run that stalls on the API never
reaches the later subjects.

Rewrites `order_index` and the prerequisite chain to match the current outline. Slugs
are untouched, so UserLessonProgress keeps pointing at the same lessons.

    PYTHONIOENCODING=utf-8 python scripts/apply_lesson_order.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.db import SessionLocal                              # noqa: E402
from services.skilltree_taxonomy import SKILLTREE_OUTLINE         # noqa: E402
from seed_skilltree import upsert_structure                       # noqa: E402


def main() -> int:
    db = SessionLocal()
    try:
        for slug, subject in SKILLTREE_OUTLINE.items():
            upsert_structure(db, slug, subject)
            print(f"{slug:18} ok", flush=True)
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
