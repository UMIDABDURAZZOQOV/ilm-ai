"""Validate by default; --apply writes only to an explicit local SQLite staging DB.

No PDFs are included and application startup never calls this importer.
"""

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--database-url")
    parser.add_argument(
        "--lesson",
        type=Path,
        help="Another reviewed original lesson manifest; defaults to the first grade-5 lesson.",
    )
    args = parser.parse_args()
    if args.apply and (
        os.getenv("ENVIRONMENT") == "production"
        or not (args.database_url or "").startswith("sqlite:///")
    ):
        parser.error(
            "Apply is restricted to an explicit local SQLite test/staging database; production is forbidden."
        )
    from services.curriculum_validation import load_documents, validate_lesson

    catalog, lesson = load_documents()
    if args.lesson:
        lesson = json.loads(args.lesson.read_text())
    validate_lesson(catalog, lesson)
    print("Sources and original lesson validated; unavailable grades remain blocked.")
    if not args.apply:
        return
    os.environ["DATABASE_URL"] = args.database_url
    from services.curriculum import import_curriculum
    from services.db import Base, engine, SessionLocal

    Base.metadata.create_all(engine)
    with SessionLocal.begin() as db:
        print(import_curriculum(db, catalog, lesson))


if __name__ == "__main__":
    main()
