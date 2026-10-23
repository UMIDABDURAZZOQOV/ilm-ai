"""Immutable opt-in Chemistry import using the pinned common v2 contract.

Never called by main/startup. Only explicit reviewed files may enter isolated
local QA. Existing Biology/Physics models, tables and content are not altered.
"""
from copy import deepcopy
import os

from services.chemistry_models import ChemistryAssessment, ChemistryBase, ChemistryLesson
from services.chemistry_validation import fingerprint, load_lessons


def require_local(bind):
    url = bind.url if hasattr(bind, "url") else bind.engine.url
    local = (url.get_backend_name() == "sqlite" and
             "chemistry_staging" in (url.database or "")) or (
        url.get_backend_name() == "postgresql" and
        url.host in {"localhost", "127.0.0.1", "::1"} and
        "staging" in (url.database or ""))
    if (os.getenv("ENVIRONMENT") not in {"test", "development"}
            or os.getenv("CHEMISTRY_PREVIEW_ENABLED", "").lower() != "true" or not local):
        raise ValueError("explicit_local_chemistry_staging_required")


def install_schema(bind):
    require_local(bind)
    ChemistryBase.metadata.create_all(bind)


def import_lesson(db, document):
    require_local(db.get_bind())
    reviewed = next((d for d in load_lessons() if d["key"] == document["key"]), None)
    digest = fingerprint(document)
    if reviewed is None or fingerprint(reviewed) != digest:
        raise ValueError("only_explicit_unchanged_reviewed_lessons_may_be_imported")
    existing = db.get(ChemistryLesson, document["key"])
    if existing is not None:
        if (existing.content_sha256 != digest or existing.revision != document["revision"]
                or existing.content != document["content"] or existing.title != document['title']
                or existing.subject != 'kimyo' or existing.grade != document['grade']
                or existing.sequence != document['sequence'] or existing.topic_id != document['topic_id']):
            raise ValueError("published_chemistry_lesson_is_immutable")
        rows = (db.query(ChemistryAssessment).filter_by(lesson_key=existing.key)
                .order_by(ChemistryAssessment.order_index).all())
        expected = document["assessments"]
        if len(rows) != len(expected) or any(
            a.order_index != index or a.key != b["key"] or a.response_kind != b["response_kind"] or
            a.public_prompt != b["public"] or a.grading_spec != b["grading_spec"] or
            a.source_refs != b["source_refs"] for index,(a,b) in enumerate(zip(rows,expected),1)
        ):
            raise ValueError("published_chemistry_assessment_is_immutable")
        return {"key": existing.key, "created": False}
    row = ChemistryLesson(key=document["key"], subject="kimyo", grade=document["grade"],
        sequence=document["sequence"], revision=document["revision"],
        topic_id=document["topic_id"], content_sha256=digest,
        title=document["title"], content=deepcopy(document["content"]))
    db.add(row)
    db.flush()
    for i, q in enumerate(document["assessments"], 1):
        db.add(ChemistryAssessment(key=q["key"], lesson_key=row.key, order_index=i,
            response_kind=q["response_kind"], public_prompt=deepcopy(q["public"]),
            grading_spec=deepcopy(q["grading_spec"]), source_refs=deepcopy(q["source_refs"])))
    db.flush()
    return {"key": row.key, "created": True}
