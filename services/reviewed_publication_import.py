"""Explicit transactional import; never startup, migration, preview authorization or progress writes."""

from copy import deepcopy
from sqlalchemy import inspect
from services.reviewed_mobile_release import expected_rows


def import_reviewed_publication(db):
    """Caller owns transaction. All validators finish before any content is added.

    Existing v2 lessons/private graders must match exactly. Missing rows can be
    inserted; content is never overwritten and unknown keys require review.
    Biology uses its existing immutable, source-validated additive importer.
    """
    from services.curriculum_validation import (
        load_documents,
        load_lesson_set,
        validate_lesson,
    )
    from services.curriculum import import_curriculum

    catalog, _ = load_documents()
    biology = load_lesson_set()
    for row in biology:
        validate_lesson(catalog, row)
    specs, lessons, assessments = expected_rows()
    names = set(inspect(db.get_bind()).get_table_names())
    if any(not set(spec[0].metadata.tables) <= names for spec in specs.values()):
        raise ValueError("publication_schema_migration_required")
    pending = []
    for model, expected in [*lessons.items(), *assessments.items()]:
        existing = {row.key: row for row in db.query(model).all()}
        if set(existing) - set(expected):
            raise ValueError("publication_unknown_content_requires_review")
        for key, fields in expected.items():
            row = existing.get(key)
            if row is not None:
                if any(getattr(row, name) != value for name, value in fields.items()):
                    raise ValueError("publication_existing_content_requires_review")
            else:
                pending.append((model, fields))
    catalog_cache = {}
    created_biology = sum(
        import_curriculum(
            db, catalog, row, allow_source_upgrade=True, catalog_cache=catalog_cache
        )["created"]
        for row in biology
    )
    # Lesson parents precede assessments regardless of ORM relationship mappings.
    for model, fields in pending:
        db.add(model(**deepcopy(fields)))
        if model in lessons:
            db.flush()
    db.flush()
    return {
        "biology_lessons_inserted": created_biology,
        "reviewed_rows_inserted": len(pending),
        "progress_rows_modified": 0,
    }
