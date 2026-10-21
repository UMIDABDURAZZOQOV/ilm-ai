"""Explicit LOCAL/TEST import, never publication. No startup seed or PDF copying.

python -m scripts.import_physics_preview --dry-run
DATABASE_URL=sqlite:////absolute/preview.db ENVIRONMENT=test \
  python -m scripts.import_physics_preview --import-content
Run reviewed additive migration 0013 on an existing local schema first.
"""

import argparse
import os

from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from services.database_url import normalize_database_url
from services.physics_curriculum import load_batch, load_course, validate_batch


def safe_url(raw, environment):
    if not raw or environment not in {"development", "test"}:
        raise ValueError("explicit_local_test_database_required")
    url = make_url(normalize_database_url(raw))
    if url.get_backend_name() == "sqlite" and url.database:
        return url
    if (
        url.get_backend_name() == "postgresql"
        and url.host in {"localhost", "127.0.0.1", "::1"}
        and "staging" in (url.database or "")
    ):
        return url
    raise ValueError("only_explicit_sqlite_or_loopback_postgresql_staging_permitted")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--dry-run", action="store_true")
    action.add_argument("--import-content", action="store_true")
    parser.add_argument(
        "--all-reviewed",
        action="store_true",
        help="Import every explicitly reviewed batch, preserving existing lessons/progress.",
    )
    args = parser.parse_args()
    documents = load_course() if args.all_reviewed else [load_batch()]
    if args.dry_run:
        print([dict(grade=d["grade"], **validate_batch(d)) for d in documents])
        return
    url = safe_url(os.getenv("DATABASE_URL"), os.getenv("ENVIRONMENT", "development"))
    # Validate and check tables before importing services.db (legacy import hooks).
    engine = create_engine(url)
    with engine.connect() as conn:
        names = set(inspect(conn).get_table_names())
    required = {
        "users",
        "study_sessions",
        "study_events",
        "curriculum_v2_lessons",
        "curriculum_assessments_v2",
        "curriculum_progress_v2",
        "curriculum_answers_v2",
    }
    if not required <= names:
        engine.dispose()
        raise SystemExit(
            "Apply reviewed local migration 0013 before importing; no schema/seeds were created."
        )
    from services.physics_curriculum import import_batch

    with Session(engine) as db, db.begin():
        print([import_batch(db, document) for document in documents])
    engine.dispose()


if __name__ == "__main__":
    main()
