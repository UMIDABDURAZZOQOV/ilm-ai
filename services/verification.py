import secrets
from datetime import datetime, timedelta, timezone

from services.db import SessionLocal
from services.models import EmailVerificationCode
from services.email import send_verification_code

CODE_TTL_MINUTES = 10
MAX_ATTEMPTS = 5
RESEND_COOLDOWN_SECONDS = 60


def _generate_code() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def issue_code(email: str, purpose: str) -> dict:
    """
    Create and send a new verification code for `email`/`purpose`.
    Invalidates any previous unused codes for the same email+purpose so only
    the most recent one is valid.

    Returns {"ok": True} or {"ok": False, "error": "cooldown", "retry_after": N}
    if a code was already issued too recently (basic anti-spam).
    """
    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)

        latest = (
            db.query(EmailVerificationCode)
            .filter(EmailVerificationCode.email == email, EmailVerificationCode.purpose == purpose)
            .order_by(EmailVerificationCode.created_at.desc())
            .first()
        )
        if latest and latest.created_at:
            created_at = latest.created_at
            if created_at.tzinfo is None:
                created_at = created_at.replace(tzinfo=timezone.utc)
            elapsed = (now - created_at).total_seconds()
            if elapsed < RESEND_COOLDOWN_SECONDS:
                return {"ok": False, "error": "cooldown", "retry_after": int(RESEND_COOLDOWN_SECONDS - elapsed)}

        # Invalidate older unused codes for this email+purpose
        db.query(EmailVerificationCode).filter(
            EmailVerificationCode.email == email,
            EmailVerificationCode.purpose == purpose,
            EmailVerificationCode.used == False,  # noqa: E712
        ).update({"used": True})

        code = _generate_code()
        entry = EmailVerificationCode(
            email=email,
            code=code,
            purpose=purpose,
            expires_at=now + timedelta(minutes=CODE_TTL_MINUTES),
        )
        db.add(entry)
        db.commit()

        send_verification_code(email, code, purpose)
        return {"ok": True}
    finally:
        db.close()


def check_code(email: str, code: str, purpose: str) -> dict:
    """
    Verify a submitted code. Returns {"ok": True} on success, or
    {"ok": False, "error": "..."} on failure (invalid, expired, or too many
    attempts). Marks the code used on success so it can't be replayed.
    """
    db = SessionLocal()
    try:
        entry = (
            db.query(EmailVerificationCode)
            .filter(
                EmailVerificationCode.email == email,
                EmailVerificationCode.purpose == purpose,
                EmailVerificationCode.used == False,  # noqa: E712
            )
            .order_by(EmailVerificationCode.created_at.desc())
            .first()
        )
        if not entry:
            return {"ok": False, "error": "No active code — request a new one"}

        if entry.attempts >= MAX_ATTEMPTS:
            return {"ok": False, "error": "Too many attempts — request a new code"}

        expires_at = entry.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > expires_at:
            return {"ok": False, "error": "Code expired — request a new one"}

        if entry.code != code.strip():
            entry.attempts += 1
            db.add(entry)
            db.commit()
            return {"ok": False, "error": "Incorrect code"}

        entry.used = True
        db.add(entry)
        db.commit()
        return {"ok": True}
    finally:
        db.close()
