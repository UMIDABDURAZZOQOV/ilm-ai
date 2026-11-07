"""Validate reviewed publication by default; apply only to an explicit local staging DB.

No hosted/production write is authorized by this tool. URL is read from a private
file outside any Git checkout and never printed, even on connection failure.
"""

import argparse
import json
import os
from pathlib import Path
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def local_staging_url(filename):
    path = filename.resolve(strict=True)
    if any((parent / ".git").exists() for parent in path.parents):
        raise ValueError("private_file_must_be_outside_checkout")
    value = path.read_text(encoding="utf-8-sig").strip()
    parsed = urlsplit(value)
    if (
        parsed.scheme != "postgresql"
        or parsed.hostname not in {"localhost", "127.0.0.1"}
        or "staging" not in parsed.path
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("explicit_local_postgres_staging_required")
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database-url-file", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if not args.apply:
        from services.curriculum_validation import (
            load_documents,
            load_lesson_set,
            validate_lesson,
        )
        from services.physics_curriculum import load_course as physics
        from services.chemistry_validation import load_lessons as chemistry
        from services.world_history_lessons import load_lessons as world
        from services.uzbekistan_history_validation import load_course as history

        catalog, _ = load_documents()
        biology = load_lesson_set()
        for lesson in biology:
            validate_lesson(catalog, lesson)
        lessons = [row for batch in physics() for row in batch["lessons"]]
        lessons += chemistry() + world()
        lessons += [row for batch in history() for row in batch["lessons"]]
        print(
            json.dumps(
                {
                    "source_validation": True,
                    "database_written": False,
                    "biology_lessons": len(biology),
                    "reviewed_lessons": len(lessons),
                    "reviewed_assessments": sum(
                        len(row["assessments"]) for row in lessons
                    ),
                }
            )
        )
        return 0
    if os.getenv("ENVIRONMENT") == "production" or not args.database_url_file:
        parser.error("Apply requires explicit local staging, never production")
    try:
        value = local_staging_url(args.database_url_file)
        # Prevent services.db from selecting another inherited database.
        os.environ["DATABASE_URL"] = value
        os.environ["PYTHON_DOTENV_DISABLED"] = "1"
        from sqlalchemy import create_engine
        from sqlalchemy.orm import Session
        from services.database_url import normalize_database_url
        from services.reviewed_publication_import import import_reviewed_publication

        engine = create_engine(normalize_database_url(value))
        try:
            with Session(engine) as db, db.begin():
                result = import_reviewed_publication(db)
            print(
                json.dumps(
                    {"database_written": True, **result, "production_signoff": False}
                )
            )
        finally:
            engine.dispose()
        return 0
    except Exception:
        print(
            json.dumps(
                {
                    "database_written": False,
                    "error": "publication_import_rejected_or_failed",
                }
            )
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
