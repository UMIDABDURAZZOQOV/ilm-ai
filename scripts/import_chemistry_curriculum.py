"""Pure reviewed validation by default; explicit local staging apply only."""
import argparse
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--database-url")
    parser.add_argument("--install-schema", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if args.apply and (os.getenv("ENVIRONMENT") == "production" or
                       not (args.database_url or "").startswith("sqlite:///") or
                       "chemistry_staging" not in (args.database_url or "")):
        parser.error("Apply requires an explicit disposable local chemistry_staging SQLite DB; production is forbidden")
    if args.install_schema and not args.apply:
        parser.error("Schema installation requires explicit --apply")
    from services.chemistry_validation import load_catalog, load_lessons, readiness
    catalog = load_catalog()
    lessons = load_lessons(catalog)
    report = readiness(catalog, lessons)
    print(f"Validated {len(lessons)} unchanged reviewed Chemistry lesson(s).")
    if args.report:
        args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if not args.apply:
        return
    os.environ.update(DATABASE_URL=args.database_url,ENVIRONMENT="test",
                      CHEMISTRY_PREVIEW_ENABLED="true", AUTH_STORAGE="database")
    from services.chemistry_curriculum import import_lesson, install_schema
    from services.db import Base, engine, SessionLocal
    Base.metadata.create_all(engine)
    if args.install_schema:
        install_schema(engine)
    with SessionLocal.begin() as db:
        for document in lessons:
            print(import_lesson(db, document))


if __name__ == "__main__":
    main()
