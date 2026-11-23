"""First-party recovery-key accounts for an explicitly enabled loopback QA build."""

import base64
import binascii
import hashlib
import hmac
import json
import os
import secrets
from pathlib import Path
from urllib.parse import urlsplit

from fastapi import HTTPException, Request
from sqlalchemy import delete, or_, select, update
from sqlalchemy.exc import IntegrityError

from services import tokens, users
from services.models import RefreshToken, User


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


async def read_request(request: Request, fields: set[str], optional_fields: set[str] | frozenset[str] = frozenset()):
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
    if (not isinstance(data, dict) or not fields <= data.keys() <= fields | optional_fields
            or not all(isinstance(value, str) for value in data.values())):
        raise HTTPException(400, "invalid_ilm_access_request")
    return data


def key_digest(key: str, prefix: str) -> str | None:
    if not key.startswith(prefix) or len(key) != len(prefix) + 43:
        return None
    encoded = key[len(prefix):]
    try:
        raw = base64.b64decode(encoded + "=", altchars=b"-_", validate=True)
    except (ValueError, binascii.Error):
        return None
    if len(raw) != 32 or base64.urlsafe_b64encode(raw).decode().rstrip("=") != encoded:
        return None
    return hashlib.sha256(raw).hexdigest()


def alias_for_key(key: str) -> str | None:
    digest = key_digest(key, "ilm1_")
    return f"{digest}@{users.ILM_ACCESS_ALIAS_DOMAIN}" if digest else None


def credential_rotated(owner_marker: str | None) -> bool:
    return bool(owner_marker and owner_marker.startswith("ilm-rotated:"))


def _backup_marker(key: str, alias: str, *, revision: str | None = None) -> str:
    digest = key_digest(key, "ilmr1_")
    if digest is None or alias.startswith(digest + "@"):
        raise HTTPException(400, "invalid_ilm_recovery_key")
    return "ilm-backup:" + digest if revision is None else f"ilm-rotated:{digest}:{revision}"


def matches(user: User, key: str) -> bool:
    identity = alias_for_key(key)
    return bool(
        identity and user.oauth_provider == PROVIDER
        and hmac.compare_digest(user.email, identity)
    )


def _session(db, user_id: int, name: str, age: int | None, alias: str, marker: str | None):
    binding = tokens.ilm_credential_binding(alias, marker)
    payload = {
        "user_id": user_id,
        "name": name,
        "email": "",
        "needs_onboarding": age is None,
        "access_token": tokens.create_access_token(user_id, ilm_binding=binding),
        "refresh_token": tokens.stage_refresh_token(db, user_id, ilm_binding=binding),
    }
    db.commit()
    return payload


def authenticate(db, key: str, *, create: bool, recovery_key: str | None = None):
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

    marker = user.oauth_provider_id
    if recovery_key is not None:
        revision = marker.rsplit(":", 1)[1] if credential_rotated(marker) else None
        marker = _backup_marker(recovery_key, identity, revision=revision)
        if create and user.oauth_provider_id not in (None, marker):
            raise HTTPException(409, "ilm_backup_already_configured")
        # SQLite does not enforce SELECT FOR UPDATE. Compare the old marker and
        # alias in the update so late enrollment cannot overwrite a recovery.
        configured = db.execute(
            update(User).where(User.id == user.id, User.oauth_provider == PROVIDER,
                               User.email == identity, User.oauth_provider_id == user.oauth_provider_id)
            .values(oauth_provider_id=marker)
        )
        if configured.rowcount != 1:
            raise HTTPException(409, "ilm_credentials_changed")
    return _session(db, user.id, user.name, user.age, identity, marker)


def recover(db, key: str, recovery_key: str, next_recovery_key: str):
    new_alias = alias_for_key(key)
    old_digest = key_digest(recovery_key, "ilmr1_")
    if new_alias is None or old_digest is None or new_alias.startswith(old_digest + "@") or recovery_key == next_recovery_key:
        raise HTTPException(400, "invalid_ilm_recovery_key")
    next_marker = _backup_marker(next_recovery_key, new_alias, revision=secrets.token_hex(16))
    owners = db.execute(
        select(User.id, User.name, User.age, User.email, User.oauth_provider_id)
        .where(User.oauth_provider == PROVIDER,
               or_(User.oauth_provider_id == "ilm-backup:" + old_digest,
                   User.oauth_provider_id.startswith(f"ilm-rotated:{old_digest}:")))
        .limit(2)
    ).all()
    if len(owners) != 1:
        raise HTTPException(401, "invalid_ilm_recovery_key")
    uid, name, age, old_alias, old_marker = owners[0]
    if (new_alias == old_alias
            or old_alias.startswith(next_marker.split(":")[1] + "@")):
        raise HTTPException(400, "invalid_ilm_recovery_key")
    try:
        changed = db.execute(
            update(User).where(User.id == uid, User.oauth_provider == PROVIDER,
                               User.email == old_alias, User.oauth_provider_id == old_marker)
            .values(email=new_alias, oauth_provider_id=next_marker)
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "ilm_replacement_key_in_use") from None
    if changed.rowcount != 1:
        raise HTTPException(401, "invalid_ilm_recovery_key")
    db.execute(delete(RefreshToken).where(RefreshToken.user_id == uid))
    return _session(db, uid, name, age, new_alias, next_marker)
