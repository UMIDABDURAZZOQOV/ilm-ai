"""Retry only already-verified cleanup jobs; never discovers/deletes new users."""

from datetime import timedelta
import os
from sqlalchemy import delete, select
from services.account_models import DeletionJob, DeletionChallenge, DeletionRateBucket
from services.account_deletion import finish_cleanup, require_ready
from services.study import utcnow


def process_pending(db, limit=50):
    require_ready(db, delivery=False)
    jobs = (
        db.execute(
            select(DeletionJob)
            .where(DeletionJob.state == "pending_cleanup")
            .order_by(DeletionJob.created_at)
            .limit(limit)
            .with_for_update(skip_locked=True)
        )
        .scalars()
        .all()
    )
    completed = sum(finish_cleanup(db, job)["state"] == "deleted" for job in jobs)
    db.execute(
        delete(DeletionChallenge).where(
            DeletionChallenge.expires_at < utcnow() - timedelta(days=1)
        )
    )
    db.execute(
        delete(DeletionRateBucket).where(DeletionRateBucket.expires_at < utcnow())
    )
    db.commit()
    return {"processed": len(jobs), "completed": completed}


def scheduled_cleanup():
    if os.getenv("ACCOUNT_DELETION_ENABLED") != "true":
        return
    from services.db import SessionLocal
    import logging

    try:
        with SessionLocal() as db:
            process_pending(db)
    except Exception:
        logging.getLogger(__name__).warning("account_cleanup_retry_failed")
