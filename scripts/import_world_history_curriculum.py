"""Pure reviewed history validation by default; explicit disposable SQLite apply."""
import argparse
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--database-url')
    parser.add_argument('--install-schema', action='store_true')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if args.apply and (os.getenv('ENVIRONMENT') == 'production'
                       or not (args.database_url or '').startswith('sqlite:///')
                       or 'world_history_staging' not in (args.database_url or '')):
        parser.error('Apply requires an explicit disposable world_history_staging SQLite database')
    if args.install_schema and not args.apply:
        parser.error('Schema installation requires --apply')
    from services.world_history_lessons import load_lessons
    from services.world_history_validation import load_catalog, require_complete_catalog
    catalog = require_complete_catalog(load_catalog())
    lessons = load_lessons(catalog)
    report = {'subject': 'jahon_tarixi', 'source_pages': 961,
              'total_teaching_topics': catalog['total_teaching_topics'],
              'reviewed_manifests': len(lessons),
              'unimplemented_topics': catalog['total_teaching_topics'] - len(lessons),
              'publication': 'local_test_preview_only', 'course_complete': False}
    print(f'Validated {len(lessons)} unchanged reviewed history manifest(s); not course completion.')
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf8')
    if not args.apply:
        return
    os.environ.update(DATABASE_URL=args.database_url, ENVIRONMENT='test',
                      WORLD_HISTORY_PREVIEW_ENABLED='true', AUTH_STORAGE='database')
    from services.db import Base, engine, SessionLocal
    from services.world_history_curriculum import install_schema, import_reviewed_lessons
    Base.metadata.create_all(engine)
    if args.install_schema:
        install_schema(engine)
    with SessionLocal.begin() as db:
        for result in import_reviewed_lessons(db):
            print(result)


if __name__ == '__main__':
    main()
