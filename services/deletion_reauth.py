"""Email-free, fresh, owner-bound deletion authorization. No account creation."""

from datetime import timedelta
import hashlib
import hmac
import json
import logging
import os
import re
import secrets
from urllib.parse import urlencode

import jwt
import requests
from fastapi import HTTPException
from sqlalchemy import inspect, select, update
from starlette.concurrency import run_in_threadpool

from services.account_deletion import (
    digest,
    require_ready,
    _rate_limit,
    confirm_deletion,
)
from services.account_models import DeletionChallenge
from services.account_ownership import DELETED_PROVIDER
from services.deletion_reauth_models import DeletionReauth, ManualDeletionRequest
from services.models import User
from services.study import utcnow, aware
from services.mobile_oauth import pkce_challenge

logger = logging.getLogger(__name__)


def log_google_failure(error):
    """Only allowlisted categories; never exception text, codes or token claims."""
    if isinstance(error, HTTPException):
        known = {
            "google_reauthentication_failed",
            "invalid_google_identity",
            "google_verification_unavailable",
            "recent_google_authentication_required",
        }
        reason = (
            error.detail
            if isinstance(error.detail, str) and error.detail in known
            else "provider_rejected"
        )
    elif isinstance(error, jwt.PyJWTError):
        reason = "invalid_signed_identity"
    elif isinstance(error, requests.RequestException):
        reason = "provider_connection_failed"
    else:
        reason = "verification_failed"
    logger.warning("Google deletion reauthentication denied: %s", reason)


def sha(value):
    return hashlib.sha256(value.encode()).hexdigest()


def ready(db):
    if os.getenv("EMAIL_FREE_ACCOUNT_DELETION") != "true":
        raise HTTPException(503, "email_free_deletion_not_configured")
    require_ready(db, delivery=False)
    if "account_deletion_reauth" not in inspect(db.get_bind()).get_table_names():
        raise HTTPException(503, "deletion_reauth_migration_required")


def active(db, uid):
    user = db.execute(
        select(User).where(User.id == uid).with_for_update()
    ).scalar_one_or_none()
    if not user or user.oauth_provider == DELETED_PROVIDER:
        raise HTTPException(401, "invalid_account")
    return user


def fingerprint(user):
    # A later password change or identity relink invalidates an unconsumed proof.
    identity = (
        user.oauth_provider_id if user.oauth_provider == "google" else user.password
    ) or ""
    return digest(f"identity:{user.id}:{user.oauth_provider or 'password'}:{identity}")


def limit(db, peer, identity=""):
    _rate_limit(db, peer)
    if identity:
        _rate_limit(db, "reauth-identity:" + identity)
    # Persist attempted authentication counts even when verification fails.
    db.commit()


def issue_proof(db, row, user):
    proof = secrets.token_urlsafe(32)
    request_id = (
        "dap_" if row.surface == "mobile" else "daw_"
    ) + secrets.token_urlsafe(29)
    assert len(request_id) == 43
    now = utcnow()
    row.user_id, row.identity_hash, row.phase = user.id, fingerprint(user), "exchanged"
    row.expires_at = now + timedelta(minutes=5)
    challenge = DeletionChallenge(
        id=request_id,
        user_id=user.id,
        email_hash=digest("email:" + user.email.strip().lower()),
        code_hash=digest(request_id + ":" + proof),
        attempts=0,
        consumed=False,
        created_at=now,
        expires_at=row.expires_at,
    )
    db.add(challenge)
    db.flush()
    row.challenge_id = request_id
    db.commit()
    return {"request_id": request_id, "proof": proof, "expires_in_seconds": 300}


def password_proof(db, email, password, peer, *, uid=None, surface="web"):
    ready(db)
    limit(db, peer, str(uid) if uid else email.strip().lower())
    user = (
        active(db, uid)
        if uid
        else db.execute(
            select(User).where(User.email == email.strip().lower()).with_for_update()
        ).scalar_one_or_none()
    )
    from services.users import password_matches

    if (
        not user
        or user.oauth_provider not in {None, ""}
        or not password_matches(password, user.password)
    ):
        raise HTTPException(401, "reauthentication_failed")
    row = DeletionReauth(
        state_hash=sha(secrets.token_urlsafe(32)),
        user_id=user.id,
        method="password",
        surface=surface,
        phase="started",
        created_at=utcnow(),
        expires_at=utcnow() + timedelta(minutes=5),
    )
    db.add(row)
    return issue_proof(db, row, user)


def begin_google(db, challenge, peer, *, uid=None, surface="web"):
    ready(db)
    from services import google_oauth

    if not google_oauth.is_google_oauth_enabled():
        raise HTTPException(503, "google_not_configured")
    if not re.fullmatch(r"[A-Za-z0-9_-]{43}", challenge):
        raise HTTPException(400, "pkce_s256_required")
    limit(db, peer, str(uid) if uid else "")
    if uid:
        user = active(db, uid)
        if user.oauth_provider != "google" or not user.oauth_provider_id:
            raise HTTPException(400, "google_identity_not_linked")
    origin = (
        os.getenv("STAGING_PUBLIC_ORIGIN")
        if os.getenv("DEPLOYMENT_STAGE") == "staging"
        else os.getenv("PUBLIC_API_ORIGIN")
    )
    redirect = os.getenv("MOBILE_OAUTH_REDIRECT_URI", "")
    # Reuse the owner's exact already registered HTTPS callback, never a caller URL.
    from urllib.parse import urlsplit

    uri = urlsplit(redirect)
    if (
        uri.scheme != "https"
        or uri.path != "/auth/google-callback-mobile"
        or uri.query
        or uri.fragment
        or uri.username
    ):
        raise HTTPException(503, "deletion_callback_not_configured")
    if origin and redirect != origin.rstrip("/") + "/auth/google-callback-mobile":
        raise HTTPException(503, "deletion_callback_not_configured")
    state, nonce = "del_" + secrets.token_urlsafe(32), secrets.token_urlsafe(32)
    db.add(
        DeletionReauth(
            state_hash=sha(state),
            user_id=uid,
            method="google",
            surface=surface,
            phase="started",
            nonce_hash=sha(nonce),
            challenge=challenge,
            created_at=utcnow(),
            expires_at=utcnow() + timedelta(minutes=10),
        )
    )
    db.commit()
    params = dict(
        client_id=google_oauth.GOOGLE_CLIENT_ID,
        redirect_uri=redirect,
        response_type="code",
        scope="openid email profile",
        state=state,
        nonce=nonce,
        prompt="select_account",
    )
    return {
        "auth_url": "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params),
        "state": state,
    }


def verify_google_identity(code, nonce_hash, created_at):
    from services import google_oauth

    response = requests.post(
        google_oauth.GOOGLE_TOKEN_URL,
        data={
            "code": code,
            "client_id": google_oauth.GOOGLE_CLIENT_ID,
            "client_secret": google_oauth.GOOGLE_CLIENT_SECRET,
            "redirect_uri": os.getenv("MOBILE_OAUTH_REDIRECT_URI"),
            "grant_type": "authorization_code",
        },
        timeout=(5, 15),
        allow_redirects=False,
    )
    if response.status_code != 200:
        raise HTTPException(400, "google_reauthentication_failed")
    encoded = response.json().get("id_token", "")
    header = jwt.get_unverified_header(encoded)
    if header.get("alg") != "RS256" or not header.get("kid"):
        raise HTTPException(400, "invalid_google_identity")
    keys = requests.get(
        "https://www.googleapis.com/oauth2/v3/certs",
        timeout=(5, 15),
        allow_redirects=False,
    )
    if keys.status_code != 200:
        raise HTTPException(503, "google_verification_unavailable")
    key = next((k for k in keys.json()["keys"] if k.get("kid") == header["kid"]), None)
    if not key:
        raise HTTPException(400, "invalid_google_identity")
    claims = jwt.decode(
        encoded,
        jwt.PyJWK.from_dict(key).key,
        algorithms=["RS256"],
        audience=google_oauth.GOOGLE_CLIENT_ID,
        issuer=["https://accounts.google.com", "accounts.google.com"],
        options={"require": ["sub", "aud", "iss", "exp", "iat", "nonce"]},
        leeway=30,
    )
    issued_at = claims["iat"]
    auth_time = claims.get("auth_time")
    now = utcnow().timestamp()
    # Google Account auth_time describes the browser/device's Google session,
    # not this application's reauthentication. Google does not support forcing
    # Google Account reauth, and these optional claims require verified-app setup.
    # Require a newly signed, nonce-bound response issued during this exact flow.
    # Do not substitute an old/cached ID token or claim fresh password/MFA entry.
    if (
        not isinstance(issued_at, int)
        or isinstance(issued_at, bool)
        or not now - 300 <= issued_at <= now + 30
        or issued_at < aware(created_at).timestamp() - 30
        or (
            auth_time is not None
            and (
                not isinstance(auth_time, int)
                or isinstance(auth_time, bool)
                or auth_time < 0
                or auth_time > issued_at + 30
            )
        )
        or not hmac.compare_digest(sha(claims["nonce"]), nonce_hash)
        or (claims.get("azp") and claims["azp"] != google_oauth.GOOGLE_CLIENT_ID)
        or not isinstance(claims["sub"], str)
        or not claims["sub"]
    ):
        raise HTTPException(400, "recent_google_authentication_required")
    return claims["sub"]


async def google_callback(db, state, code, error=None):
    ready(db)
    row = db.get(DeletionReauth, sha(state or ""))
    if (
        not row
        or row.method != "google"
        or aware(row.expires_at) <= utcnow()
        or row.phase != "started"
    ):
        raise HTTPException(400, "invalid_deletion_state")
    claimed = db.execute(
        update(DeletionReauth)
        .where(
            DeletionReauth.state_hash == row.state_hash,
            DeletionReauth.phase == "started",
        )
        .values(phase="consumed")
    ).rowcount
    db.commit()
    if not claimed or error or not code:
        raise HTTPException(400, "google_reauthentication_cancelled")
    try:
        subject = await run_in_threadpool(
            verify_google_identity, code, row.nonce_hash, row.created_at
        )
    except HTTPException as error:
        log_google_failure(error)
        raise
    except Exception as error:
        log_google_failure(error)
        raise HTTPException(400, "google_reauthentication_failed") from None
    # Strict provider-subject ownership, never email/name linking or account creation.
    user = db.execute(
        select(User)
        .where(User.oauth_provider == "google", User.oauth_provider_id == subject)
        .with_for_update()
    ).scalar_one_or_none()
    if not user or (row.user_id is not None and user.id != row.user_id):
        raise HTTPException(403, "deletion_account_mismatch")
    grant = secrets.token_urlsafe(32)
    row.user_id, row.identity_hash, row.phase = user.id, fingerprint(user), "verified"
    row.grant_hash, row.exchange_expires_at = (
        sha(grant),
        utcnow() + timedelta(seconds=90),
    )
    row.expires_at = utcnow() + timedelta(minutes=5)
    db.commit()
    return grant, row.surface


def exchange(db, code, verifier):
    ready(db)
    challenge = pkce_challenge(verifier)
    row = db.execute(
        select(DeletionReauth)
        .where(DeletionReauth.grant_hash == sha(code))
        .with_for_update()
    ).scalar_one_or_none()
    if (
        not row
        or row.phase != "verified"
        or aware(row.exchange_expires_at) <= utcnow()
        or not hmac.compare_digest(row.challenge, challenge)
    ):
        raise HTTPException(400, "invalid_deletion_grant")
    user = active(db, row.user_id)
    if not hmac.compare_digest(row.identity_hash, fingerprint(user)):
        raise HTTPException(401, "identity_changed_reauthenticate")
    claimed = db.execute(
        update(DeletionReauth)
        .where(
            DeletionReauth.state_hash == row.state_hash,
            DeletionReauth.phase == "verified",
        )
        .values(phase="exchanging")
    ).rowcount
    if not claimed:
        raise HTTPException(400, "invalid_deletion_grant")
    return issue_proof(db, row, user)


def confirm(db, request_id, proof, confirmation, bearer_uid=None):
    ready(db)
    row = db.execute(
        select(DeletionReauth)
        .where(DeletionReauth.challenge_id == request_id)
        .with_for_update()
    ).scalar_one_or_none()
    challenge = db.get(DeletionChallenge, request_id)
    if (
        not row
        or not challenge
        or row.phase != "exchanged"
        or aware(row.expires_at) <= utcnow()
    ):
        raise HTTPException(400, "invalid_or_expired_deletion_proof")
    if bearer_uid is not None and bearer_uid != row.user_id:
        raise HTTPException(403, "deletion_account_mismatch")
    # A lost response may be retried with the same narrow proof after revocation;
    # an unconsumed mobile proof still requires a currently valid owner session.
    if not challenge.consumed:
        if row.surface == "mobile" and bearer_uid != row.user_id:
            raise HTTPException(401, "active_owner_session_required")
        user = active(db, row.user_id)
        if not hmac.compare_digest(row.identity_hash, fingerprint(user)):
            raise HTTPException(401, "identity_changed_reauthenticate")
    return confirm_deletion(db, request_id, proof, confirmation)


def manual_request(db, account_email, contact_email, reason, peer):
    ready(db)
    if (
        "account_deletion_manual_requests"
        not in inspect(db.get_bind()).get_table_names()
    ):
        raise HTTPException(503, "deletion_reauth_migration_required")
    limit(db, peer, contact_email.strip().lower())
    from cryptography.fernet import Fernet
    import base64

    key = base64.urlsafe_b64encode(
        hashlib.sha256(
            (os.environ["ACCOUNT_DELETION_SECRET"] + ":manual-review-v1").encode()
        ).digest()
    )
    ticket = secrets.token_urlsafe(32)
    encrypted = (
        Fernet(key)
        .encrypt(
            json.dumps(
                {
                    "account_email": account_email.strip().lower(),
                    "contact_email": contact_email.strip().lower(),
                    "reason": reason,
                }
            ).encode()
        )
        .decode()
    )
    db.add(
        ManualDeletionRequest(
            id=ticket,
            account_hash=digest("email:" + account_email.strip().lower()),
            contact_hash=digest("email:" + contact_email.strip().lower()),
            encrypted_details=encrypted,
            state="pending_identity_review",
            created_at=utcnow(),
        )
    )
    db.commit()
    return {
        "request_id": ticket,
        "state": "pending_identity_review",
        "account_deleted": False,
    }
