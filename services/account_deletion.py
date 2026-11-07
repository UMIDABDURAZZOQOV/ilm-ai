"""Verified, idempotent account deletion. Never called from startup or migration."""

from datetime import timedelta
import hashlib
import hmac
import os
import secrets

from fastapi import HTTPException
from sqlalchemy import delete, inspect, or_, select, update, text
from sqlalchemy.exc import IntegrityError

from services.account_models import (
    AccountBase,
    DeletionChallenge,
    DeletionJob,
    DeletionRateBucket,
)
from services.account_ownership import DIRECT_OWNERS, ANSWER_TABLES, DELETED_PROVIDER
from services.models import User, CheckoutSession
from services.study import utcnow


def digest(value):
    key = os.getenv("ACCOUNT_DELETION_SECRET", "")
    if len(key) < 32:
        raise HTTPException(503, "account_deletion_not_configured")
    return hmac.new(key.encode(), value.encode(), hashlib.sha256).hexdigest()


def require_ready(db, *, delivery=True):
    if os.getenv("ACCOUNT_DELETION_ENABLED") != "true":
        raise HTTPException(503, "account_deletion_not_configured")
    if (
        os.getenv("AUTH_STORAGE", "database") != "database"
        or not os.getenv("ACCOUNT_DELETION_POLICY_REFERENCE", "").strip()
    ):
        raise HTTPException(503, "account_deletion_not_configured")
    from services import users, tokens

    if (
        not users.USE_DB
        or not tokens.USE_DB
        or db.get_bind().dialect.name not in {"sqlite", "postgresql"}
    ):
        raise HTTPException(503, "account_deletion_database_runtime_required")
    digest("configuration-check")
    from services.account_file_cleanup import storage_root

    storage_root()
    from services.email import is_email_configured

    if delivery and not is_email_configured():
        raise HTTPException(503, "account_deletion_email_unavailable")
    inspector = inspect(db.get_bind())
    names = set(inspector.get_table_names())
    if not set(AccountBase.metadata.tables) <= names:
        raise HTTPException(503, "account_deletion_migration_required")
    if db.get_bind().dialect.name == "sqlite":
        triggers = {
            r[0]
            for r in db.execute(
                text("SELECT name FROM sqlite_master WHERE type='trigger'")
            )
        }
        required = {"account_guard_users_update", "account_guard_users_delete"}
        suffix = "_insert"
    else:
        triggers = {
            r[0]
            for r in db.execute(
                text(
                    "SELECT t.tgname FROM pg_trigger t JOIN pg_class c ON t.tgrelid=c.oid JOIN pg_namespace n ON c.relnamespace=n.oid WHERE n.nspname=current_schema() AND NOT t.tgisinternal"
                )
            )
        }
        required, suffix = {"account_guard_users"}, ""
    required |= {
        "account_guard_" + table + "_" + col + suffix
        for table, cols in DIRECT_OWNERS.items()
        if table in names
        for col in cols
    }
    required |= {
        "account_guard_" + table + "_session_id" + suffix
        for table in ANSWER_TABLES
        if table in names
    }
    required |= {
        "account_guard_" + table + "_class_id" + suffix
        for table in ("skilltree_class_assignments", "skilltree_class_members")
        if table in names
    }
    if suffix:
        required |= {
            name.removesuffix("_insert") + "_update"
            for name in required
            if name.endswith("_insert")
        }
    if not required <= triggers:
        raise HTTPException(503, "account_deletion_write_barriers_required")


def _rate_limit(db, peer):
    now = utcnow()
    key = digest("peer:" + peer + ":" + str(int(now.timestamp()) // 3600))
    count = db.execute(
        update(DeletionRateBucket)
        .where(DeletionRateBucket.key_hash == key, DeletionRateBucket.count < 30)
        .values(count=DeletionRateBucket.count + 1)
        .returning(DeletionRateBucket.count)
    ).scalar_one_or_none()
    if count is None:
        if db.get(DeletionRateBucket, key) is not None:
            raise HTTPException(429, "deletion_try_later")
        bucket = DeletionRateBucket(
            key_hash=key, count=1, expires_at=now + timedelta(hours=2)
        )
        db.add(bucket)
        try:
            db.flush()
        except IntegrityError:
            db.rollback()
            raise HTTPException(429, "deletion_try_later") from None


def request_deletion(db, email, peer, *, expected_user=None):
    require_ready(db)
    normalized = email.strip().lower()
    tag = digest("email:" + normalized)
    now = utcnow()
    _rate_limit(db, peer)
    user = db.execute(
        select(User).where(User.email == normalized).with_for_update()
    ).scalar_one_or_none()
    if expected_user is not None and (user is None or user.id != expected_user):
        raise HTTPException(403, "account_identity_changed")
    recent = (
        db.query(DeletionChallenge)
        .filter(
            DeletionChallenge.email_hash == tag,
            DeletionChallenge.created_at > now - timedelta(seconds=60),
        )
        .first()
    )
    if recent:
        db.commit()
        raise HTTPException(429, "deletion_try_later")
    code, request_id = f"{secrets.randbelow(1000000):06d}", secrets.token_urlsafe(32)
    row = DeletionChallenge(
        id=request_id,
        user_id=user.id if user and user.oauth_provider != DELETED_PROVIDER else None,
        email_hash=tag,
        code_hash=digest(request_id + ":" + code),
        attempts=0,
        consumed=False,
        created_at=now,
        expires_at=now + timedelta(minutes=10),
    )
    db.add(row)
    db.commit()
    # The same response is returned for unknown accounts. No recipient/user ID
    # or delivery exception is returned. Failed delivery consumes the challenge.
    if row.user_id is not None:
        from services.email import send_verification_code

        if not send_verification_code(normalized, code, purpose="account_deletion"):
            row.consumed = True
            db.commit()
            if expected_user is not None:
                raise HTTPException(503, "account_deletion_email_delivery_failed")
    return {
        "request_id": request_id,
        "message": "If an account exists, a verification code has been sent.",
        "expires_in_seconds": 600,
    }


def _purge_owned_rows(db, user):
    from sqlalchemy import MetaData, Table

    metadata = MetaData()
    names = set(inspect(db.get_bind()).get_table_names())

    def table(name):
        return Table(name, metadata, autoload_with=db.connection())

    sessions = select(table("study_sessions").c.id).where(
        table("study_sessions").c.user_id == user.id
    )
    for name in ANSWER_TABLES:
        if name in names:
            target = table(name)
            db.execute(delete(target).where(target.c.session_id.in_(sessions)))
    if "skilltree_classes" in names:
        owned = select(table("skilltree_classes").c.id).where(
            table("skilltree_classes").c.teacher_id == user.id
        )
        for name in ("skilltree_class_members", "skilltree_class_assignments"):
            if name in names:
                target = table(name)
                db.execute(delete(target).where(target.c.class_id.in_(owned)))
    # Delete dependent rows first; shared curriculum and other users' own progress stay.
    order = [
        n for n in DIRECT_OWNERS if n not in {"study_sessions", "skilltree_classes"}
    ]
    for name in [*order, "study_sessions", "skilltree_classes"]:
        if name in names:
            target = table(name)
            db.execute(
                delete(target).where(
                    or_(*(target.c[c] == user.id for c in DIRECT_OWNERS[name]))
                )
            )
    if "email_verification_codes" in names:
        target = table("email_verification_codes")
        db.execute(delete(target).where(target.c.email == user.email))
    db.execute(update(User).where(User.referred_by == user.id).values(referred_by=None))


def _scrub_user(user):
    # Reserve the non-reusable ID, without original email/provider subject/name.
    # An immutable DB tombstone prevents stale requests from restoring the row.
    from sqlalchemy import Boolean, Integer

    for column in User.__table__.columns:
        if column.name == "id":
            continue
        if column.nullable:
            setattr(user, column.name, None)
        elif isinstance(column.type, Boolean):
            setattr(user, column.name, False)
        elif isinstance(column.type, Integer):
            setattr(user, column.name, 0)
    user.name = "Deleted account"
    user.email = "deleted-" + secrets.token_hex(24) + "@account.invalid"
    user.oauth_provider = DELETED_PROVIDER
    user.subscription_tier = "free"


def confirm_deletion(db, request_id, code, confirmation):
    require_ready(db, delivery=False)
    if confirmation != "DELETE":
        raise HTTPException(400, "explicit_deletion_confirmation_required")
    now = utcnow()
    claimed = db.execute(
        update(DeletionChallenge)
        .where(
            DeletionChallenge.id == request_id,
            DeletionChallenge.expires_at > now,
            DeletionChallenge.attempts < 5,
        )
        .values(attempts=DeletionChallenge.attempts + 1)
        .returning(DeletionChallenge.id)
    ).scalar_one_or_none()
    if claimed is None:
        raise HTTPException(400, "invalid_or_expired_deletion_code")
    row = db.get(DeletionChallenge, request_id, populate_existing=True)
    valid = hmac.compare_digest(row.code_hash, digest(request_id + ":" + code))
    if not valid:
        db.commit()
        raise HTTPException(400, "invalid_or_expired_deletion_code")
    job = (
        db.query(DeletionJob).filter_by(user_id=row.user_id).first()
        if row.user_id
        else None
    )
    if row.consumed:
        if job is None:
            raise HTTPException(400, "invalid_or_expired_deletion_code")
        return finish_cleanup(db, job)
    if row.user_id is None:
        raise HTTPException(400, "invalid_or_expired_deletion_code")
    user = db.execute(
        select(User).where(User.id == row.user_id).with_for_update()
    ).scalar_one_or_none()
    if user is None or user.oauth_provider == DELETED_PROVIDER:
        raise HTTPException(400, "invalid_or_expired_deletion_code")
    if job is not None:
        row.consumed = True
        db.commit()
        return finish_cleanup(db, job)
    # Real financial records need the operator's actual retention decision.
    paid = db.query(CheckoutSession).filter_by(user_id=user.id).all()
    if user.subscription_tier not in {None, "", "free"} or any(
        not r.session_id.startswith("test_") for r in paid
    ):
        row.consumed = True
        job = DeletionJob(
            id=secrets.token_urlsafe(32),
            user_id=user.id,
            state="retention_review",
            email_hash=None,
            created_at=now,
        )
        db.add(job)
        db.commit()
        return {"state": "retention_review", "account_revoked": False}
    row.consumed = True
    job = DeletionJob(
        id=secrets.token_urlsafe(32),
        user_id=user.id,
        state="pending_cleanup",
        email_hash=row.email_hash,
        created_at=now,
    )
    db.add(job)
    _purge_owned_rows(db, user)
    _scrub_user(user)
    db.flush()
    db.commit()  # revocation + DB purge are atomic; file cleanup is a durable job
    return finish_cleanup(db, job)


def finish_cleanup(db, job):
    if job.state == "retention_review":
        return {"state": "retention_review", "account_revoked": False}
    if job.state != "complete":
        from services.account_file_cleanup import purge_account_files

        try:
            purge_account_files(job.user_id, job.email_hash, job.created_at)
        except (OSError, ValueError, HTTPException):
            return {"state": "pending_cleanup", "account_revoked": True}
        job.state, job.email_hash, job.completed_at = "complete", None, utcnow()
        db.commit()
    return {"state": "deleted", "account_revoked": True}
