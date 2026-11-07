"""Serialize the remaining per-user file writes with deletion's account lock."""

from contextlib import contextmanager
import os
from fastapi import HTTPException
from sqlalchemy import select
from services.account_ownership import DELETED_PROVIDER


@contextmanager
def active_account_file_write(user_id):
    if os.getenv("ACCOUNT_DELETION_ENABLED") != "true":
        yield
        return
    from services.db import SessionLocal
    from services.models import User

    with SessionLocal() as db:
        if db.get_bind().dialect.name == "sqlite":
            db.connection().exec_driver_sql("BEGIN IMMEDIATE")
        user = db.execute(
            select(User)
            .where(User.id == user_id)
            .with_for_update(read=True, key_share=True)
        ).scalar_one_or_none()
        if user is None or user.oauth_provider == DELETED_PROVIDER:
            raise HTTPException(401, "account_deleted")
        yield
        db.commit()
