"""Explicit immutable History imports, never production startup or legacy seeds."""

import os
from copy import deepcopy

from services.uzbekistan_history_sources import SUBJECT, digest, require
from services.uzbekistan_history_validation import load_course


def safe_staging_url(url):
    require(
        os.getenv("ENVIRONMENT", "development") in {"test", "development"},
        "history_import_local_test_only",
    )
    local_sqlite = (
        url.get_backend_name() == "sqlite"
        and "uzbekistan_history_staging" in (url.database or "")
    )
    local_pg = (
        url.get_backend_name() == "postgresql"
        and url.host in {"127.0.0.1", "localhost", "::1"}
        and "staging" in (url.database or "")
    )
    require(local_sqlite or local_pg, "history_import_owned_local_staging_only")
    return url


def import_course(db):
    # Validate all reviewed documents before any write, without importing ORM.
    documents = load_course()
    safe_staging_url(db.get_bind().url)
    from sqlalchemy import MetaData, Table, select

    md = MetaData()
    lessons = Table(
        "uzbekistan_history_preview_lessons", md, autoload_with=db.connection()
    )
    questions = Table(
        "uzbekistan_history_preview_assessments", md, autoload_with=db.connection()
    )
    result = {"created": 0, "skipped": 0}
    for document in documents:
        for l in document["lessons"]:
            saved = db.execute(
                select(lessons.c.content_sha256).where(lessons.c.key == l["key"])
            ).scalar_one_or_none()
            sha = digest(l)
            if saved is not None:
                require(
                    saved == sha,
                    "changed_history_content_requires_new_reviewed_revision",
                )
                result["skipped"] += 1
                continue
            content = {
                k: deepcopy(l[k])
                for k in [
                    "cards",
                    "formulas",
                    "examples",
                    "reflections",
                    "source_refs",
                    "xp_reward",
                ]
            }
            # Preserve common v2 example display shape without private facts.
            for example in content["examples"]:
                example["steps"] = []
            db.execute(
                lessons.insert().values(
                    key=l["key"],
                    subject=SUBJECT,
                    grade=document["grade"],
                    sequence=l["sequence"],
                    revision=l["revision"],
                    topic_id=l["topic_id"],
                    content_sha256=sha,
                    title=l["title"],
                    content=content,
                )
            )
            for index, q in enumerate(l["assessments"]):
                db.execute(
                    questions.insert().values(
                        key=q["key"],
                        lesson_key=l["key"],
                        order_index=index,
                        response_kind=q["response_kind"],
                        public_prompt={"phase": q["phase"], **q["public"]},
                        grading_spec=q["grading_spec"],
                        source_refs=q["source_refs"],
                    )
                )
            result["created"] += 1
    return result
