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
    parser.add_argument(
        "--all",
        action="store_true",
        help="Import the explicit reviewed lesson set in one transaction",
    )
    parser.add_argument(
        "--allow-source-upgrade",
        action="store_true",
        help="Allow only empty blocked grade shells to acquire newly verified sources",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Write honest source/lesson readiness counts as JSON",
    )
    args = parser.parse_args()
    if args.all and args.lesson:
        parser.error("Choose --all or --lesson, not both")
    if args.apply and (
        os.getenv("ENVIRONMENT") == "production"
        or not (args.database_url or "").startswith("sqlite:///")
    ):
        parser.error(
            "Apply is restricted to an explicit local SQLite test/staging database; production is forbidden."
        )
    from services.curriculum_validation import (
        load_documents,
        load_lesson_set,
        validate_lesson,
        readiness_report,
    )

    catalog, lesson = load_documents()
    if args.lesson:
        lesson = json.loads(args.lesson.read_text())
    lessons = load_lesson_set() if args.all else [lesson]
    for document in lessons:
        validate_lesson(catalog, document)
    print(f"Sources and original lesson validated: {len(lessons)} reviewed lesson(s).")
    report = readiness_report(catalog, lessons)
    for item in report:
        print(
            f"Grade {item['grade']}: {item['chapters']} chapters, {item['topics']} topics, {item['ready_lessons']} ready lessons, {item['questions']} questions; course_ready={item['course_ready']}"
        )
    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    if not args.apply:
        return
    os.environ["DATABASE_URL"] = args.database_url
    from services.curriculum import import_curriculum
    from services.db import Base, engine, SessionLocal

    Base.metadata.create_all(engine)
    with SessionLocal.begin() as db:
        for document in lessons:
            print(
                import_curriculum(
                    db,
                    catalog,
                    document,
                    allow_source_upgrade=args.allow_source_upgrade,
                )
            )


if __name__ == "__main__":
    main()
