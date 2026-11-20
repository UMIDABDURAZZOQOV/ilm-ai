"""First-party recovery-key accounts for an explicitly enabled loopback QA build."""

import base64
import binascii
import hashlib
import hmac
import json
import os
from pathlib import Path
from urllib.parse import urlsplit

from fastapi import HTTPException, Request
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from services import tokens, users
from services.models import User


PROVIDER = "ilm_access_key"
LOOPBACK = {"127.0.0.1", "::1", "localhost"}


def qa_allowed(request: Request, db) -> bool:
    origin = request.headers.get("origin")
    try:
        origin_allowed = not origin or urlsplit(origin).hostname in LOOPBACK
        host_allowed = request.url.hostname in LOOPBACK
    except ValueError:
        return False
    url = db.get_bind().url
    database_name = Path(url.database or "").name
    if url.get_backend_name() == "postgresql":
        isolated = url.host in LOOPBACK and "staging" in database_name
    else:
        isolated = url.get_backend_name() == "sqlite" and (
            "staging" in database_name
            or (os.getenv("ENVIRONMENT") == "test" and database_name == "owned.db")
        )
    return (
        os.getenv("ENVIRONMENT") in {"test", "development"}
        and os.getenv("ILM_INDEPENDENT_AUTH_QA") == "true"
        and users.USE_DB and tokens.USE_DB
        and request.client is not None
        and request.client.host in LOOPBACK
        and host_allowed and origin_allowed and isolated
        and not any(header in request.headers for header in (
            "forwarded", "x-forwarded-for", "x-forwarded-host", "x-real-ip"
        ))
    )


async def read_request(request: Request, fields: set[str]):
    if request.headers.get("content-type", "").split(";", 1)[0].strip().lower() != "application/json":
        raise HTTPException(415, "application_json_required")
    raw = bytearray()
    async for chunk in request.stream():
        if len(raw) + len(chunk) > 256:
            raise HTTPException(413, "invalid_ilm_access_request")
        raw.extend(chunk)
    try:
        data = json.loads(raw)
    except (ValueError, RecursionError):
        raise HTTPException(400, "invalid_ilm_access_request") from None
    if not isinstance(data, dict) or set(data) != fields or not isinstance(data["key"], str):
        raise HTTPException(400, "invalid_ilm_access_request")
    return data


def alias_for_key(key: str) -> str | None:
    if not key.startswith("ilm1_") or len(key) != 48:
        return None
    encoded = key[5:]
    try:
        raw = base64.b64decode(encoded + "=", altchars=b"-_", validate=True)
    except (ValueError, binascii.Error):
        return None
    if len(raw) != 32 or base64.urlsafe_b64encode(raw).decode().rstrip("=") != encoded:
        return None
    digest = hashlib.sha256(raw).hexdigest()
    return f"{digest}@{users.ILM_ACCESS_ALIAS_DOMAIN}"


def matches(user: User, key: str) -> bool:
    identity = alias_for_key(key)
    return bool(
        identity and user.oauth_provider == PROVIDER
        and hmac.compare_digest(user.email, identity)
    )


def authenticate(db, key: str, *, create: bool):
    identity = alias_for_key(key)
    if identity is None:
        raise HTTPException(400, "invalid_ilm_access_key")
    account = select(User).where(User.email == identity).with_for_update()
    user = db.scalar(account)
    if user is None and create:
        user = User(name="O‘quvchi", email=identity, oauth_provider=PROVIDER)
        db.add(user)
        try:
            db.flush()
        except IntegrityError:
            # The unique alias makes a concurrent retry resolve the same user.
            db.rollback()
            user = db.scalar(account)
            if user is None:
                raise
    if user is None or user.oauth_provider != PROVIDER:
        raise HTTPException(401, "invalid_ilm_access_key")

    payload = {
        "user_id": user.id,
        "name": user.name,
        "email": "",
        "needs_onboarding": user.age is None,
        "access_token": tokens.create_access_token(user.id),
        "refresh_token": tokens.stage_refresh_token(db, user.id),
    }
    db.commit()
    return payload
