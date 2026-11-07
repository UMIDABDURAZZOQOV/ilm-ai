"""Explicit mobile publication over reviewed engines; preview guards stay closed.

This dependency never imports/seeds/migrates data. It compares every used content
object with the pinned source documents, including private grading specifications.
The activation reference records operator provenance, not an expert signoff.
"""

from copy import deepcopy
from functools import lru_cache
import os

from fastapi import Depends, HTTPException
from sqlalchemy import event, inspect
from sqlalchemy.exc import OperationalError, ProgrammingError

from services.db import get_db

_AUTHORIZATION = object()
_SCOPE = "reviewed_mobile_release_authorization"


@lru_cache(maxsize=1)
def expected_rows():
    from services import physics_curriculum as physics
    from services.chemistry_validation import (
        load_lessons as chemistry,
        fingerprint as chemistry_hash,
    )
    from services.world_history_lessons import load_lessons as world
    from services.world_history_validation import fingerprint as world_hash
    from services.uzbekistan_history_validation import load_course as history
    from services.uzbekistan_history_sources import digest as history_hash
    from services.assessment_models import (
        AssessmentBase,
        CurriculumLessonV2,
        CurriculumAssessment,
    )
    from services.chemistry_models import (
        ChemistryBase,
        ChemistryLesson,
        ChemistryAssessment,
    )
    from services.world_history_models import (
        WorldHistoryBase,
        WorldHistoryLesson,
        WorldHistoryAssessment,
    )
    from services.uzbekistan_history_models import (
        HistoryBase,
        HistoryLesson,
        HistoryAssessment,
    )

    specs = {
        "fizika": (AssessmentBase, CurriculumLessonV2, CurriculumAssessment),
        "kimyo": (ChemistryBase, ChemistryLesson, ChemistryAssessment),
        "jahon_tarixi": (WorldHistoryBase, WorldHistoryLesson, WorldHistoryAssessment),
        "ozbekiston_tarixi": (HistoryBase, HistoryLesson, HistoryAssessment),
    }
    lessons, questions = {}, {}

    def add(slug, document, grade, content, digest, phase=False):
        _, lesson_type, assessment_type = specs[slug]
        lessons.setdefault(lesson_type, {})[document["key"]] = dict(
            key=document["key"],
            subject=slug,
            grade=grade,
            sequence=document["sequence"],
            revision=document["revision"],
            topic_id=document["topic_id"],
            content_sha256=digest,
            title=document["title"],
            content=content,
        )
        for number, q in enumerate(document["assessments"], 0 if phase else 1):
            questions.setdefault(assessment_type, {})[q["key"]] = dict(
                key=q["key"],
                lesson_key=document["key"],
                order_index=number,
                response_kind=q["response_kind"],
                public_prompt=(
                    {"phase": q["phase"], **q["public"]} if phase else q["public"]
                ),
                grading_spec=q["grading_spec"],
                source_refs=q["source_refs"],
            )

    for batch in physics.load_course():
        for row in batch["lessons"]:
            content = {
                k: row[k]
                for k in ("cards", "formulas", "examples", "source_refs", "xp_reward")
            }
            add(
                "fizika",
                row,
                batch["grade"],
                content,
                physics.fingerprint(row),
                phase=True,
            )
    for slug, loader, fingerprint in [
        ("kimyo", chemistry, chemistry_hash),
        ("jahon_tarixi", world, world_hash),
    ]:
        for row in loader():
            add(slug, row, row["grade"], row["content"], fingerprint(row))
    for batch in history():
        for row in batch["lessons"]:
            content = {
                k: deepcopy(row[k])
                for k in (
                    "cards",
                    "formulas",
                    "examples",
                    "reflections",
                    "source_refs",
                    "xp_reward",
                )
            }
            for example in content["examples"]:
                example["steps"] = []
            add(
                "ozbekiston_tarixi",
                row,
                batch["grade"],
                content,
                history_hash(row),
                phase=True,
            )
    return specs, lessons, questions


def authorized(db, slug):
    return db.info.get(_SCOPE) is _AUTHORIZATION and slug in expected_rows()[0]


def validate_object(instance):
    _, lessons, questions = expected_rows()
    expected = lessons.get(type(instance), questions.get(type(instance)))
    if expected is None:
        return
    row = expected.get(instance.key)
    if row is None or any(
        getattr(instance, field) != value for field, value in row.items()
    ):
        raise HTTPException(503, "mobile_release_content_not_reviewed")


def publication_db(db=Depends(get_db)):
    if os.getenv("MOBILE_REVIEWED_RELEASE") != "true":
        raise HTTPException(404, "reviewed_mobile_release_disabled")
    if not os.getenv("MOBILE_PUBLICATION_REVIEW_REFERENCE", "").strip():
        raise HTTPException(503, "mobile_publication_review_required")
    if (
        os.getenv("ENVIRONMENT") == "production"
        and db.get_bind().url.get_backend_name() != "postgresql"
    ):
        raise HTTPException(503, "persistent_release_database_required")
    try:
        specs, lessons, questions = expected_rows()
        tables = set(inspect(db.get_bind()).get_table_names())
        if any(not set(spec[0].metadata.tables) <= tables for spec in specs.values()):
            raise HTTPException(503, "mobile_release_schema_not_installed")
        # Exact coverage and pinned identities; no missing or extra lesson is
        # silently promoted. Full objects are checked again when used below.
        for model, rows in lessons.items():
            actual = dict(db.query(model.key, model.content_sha256).all())
            if actual != {key: row["content_sha256"] for key, row in rows.items()}:
                raise HTTPException(503, "mobile_release_curriculum_not_imported")
        for model, rows in questions.items():
            if {key for (key,) in db.query(model.key).all()} != set(rows):
                raise HTTPException(503, "mobile_release_assessments_not_imported")
    except (OperationalError, ProgrammingError):
        db.rollback()
        raise HTTPException(503, "mobile_release_schema_not_installed") from None
    except ValueError:
        raise HTTPException(503, "mobile_release_source_validation_failed") from None

    def check(session, instance):
        validate_object(instance)

    previous = db.info.get(_SCOPE)
    db.info[_SCOPE] = _AUTHORIZATION
    event.listen(db, "loaded_as_persistent", check)
    try:
        yield db
    finally:
        event.remove(db, "loaded_as_persistent", check)
        if previous is None:
            db.info.pop(_SCOPE, None)
        else:
            db.info[_SCOPE] = previous
