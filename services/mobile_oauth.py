"""One-use, expiring OAuth state and PKCE-bound mobile login grants."""

import base64
import hashlib
import hmac
import re
import secrets
from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy import update

from services.db import SessionLocal
from services.models import MobileLoginGrant, OAuthState, User
from services.study import aware, utcnow


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def pkce_challenge(verifier):
    if not re.fullmatch(r"[A-Za-z0-9._~-]{43,128}", verifier or ""):
        raise HTTPException(400, "invalid_pkce_verifier")
    return (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest())
        .decode()
        .rstrip("=")
    )


def save_state(state, redirect_uri, challenge=None):
    if challenge and not re.fullmatch(r"[A-Za-z0-9_-]{43}", challenge):
        raise HTTPException(400, "invalid_pkce_challenge")
    with SessionLocal() as db:
        db.add(
            OAuthState(
                state_hash=digest(state),
                challenge=challenge,
                redirect_uri=redirect_uri,
                expires_at=utcnow() + timedelta(minutes=10),
            )
        )
        db.commit()


def consume_state(state, redirect_uri):
    if not state:
        raise HTTPException(400, "invalid_oauth_state")
    with SessionLocal() as db:
        row = db.get(OAuthState, digest(state))
        if (
            not row
            or row.redirect_uri != redirect_uri
            or aware(row.expires_at) <= utcnow()
        ):
            raise HTTPException(400, "invalid_oauth_state")
        claimed = db.execute(
            update(OAuthState)
            .where(
                OAuthState.state_hash == row.state_hash, OAuthState.consumed.is_(False)
            )
            .values(consumed=True)
        ).rowcount
        if not claimed:
            raise HTTPException(400, "invalid_oauth_state")
        challenge = row.challenge
        db.commit()
        return challenge


def issue_grant(user_id, challenge):
    if not challenge:
        raise HTTPException(400, "mobile_client_upgrade_required")
    code = secrets.token_urlsafe(32)
    with SessionLocal() as db:
        db.add(
            MobileLoginGrant(
                code_hash=digest(code),
                user_id=user_id,
                challenge=challenge,
                expires_at=utcnow() + timedelta(seconds=90),
            )
        )
        db.commit()
    return code


def exchange_grant(code, verifier):
    challenge = pkce_challenge(verifier)
    with SessionLocal() as db:
        row = db.get(MobileLoginGrant, digest(code))
        if (
            not row
            or aware(row.expires_at) <= utcnow()
            or not hmac.compare_digest(row.challenge, challenge)
        ):
            raise HTTPException(400, "invalid_or_expired_login_code")
        claimed = db.execute(
            update(MobileLoginGrant)
            .where(
                MobileLoginGrant.code_hash == row.code_hash,
                MobileLoginGrant.consumed.is_(False),
            )
            .values(consumed=True)
        ).rowcount
        if not claimed:
            raise HTTPException(400, "invalid_or_expired_login_code")
        user = db.get(User, row.user_id)
        if not user:
            raise HTTPException(400, "invalid_or_expired_login_code")
        # Tokens are issued only on the HTTPS exchange, never into a custom URI.
        from services.tokens import create_access_token, REFRESH_EXPIRE_DAYS
        from services.models import RefreshToken
        import time

        refresh = secrets.token_urlsafe(32)
        db.add(
            RefreshToken(
                token=refresh,
                user_id=user.id,
                exp=int(time.time()) + REFRESH_EXPIRE_DAYS * 86400,
            )
        )
        result = {
            "access_token": create_access_token(user.id),
            "refresh_token": refresh,
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "message": "Google login successful",
            "needs_onboarding": user.age is None,
        }
        db.commit()
        return result
