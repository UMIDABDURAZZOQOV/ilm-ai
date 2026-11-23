import os
import json
import time
import secrets
import hmac
from typing import Optional

import jwt
from dotenv import load_dotenv
from services.security_config import require_production_secret

load_dotenv()
JWT_SECRET = os.environ.get("JWT_SECRET", "dev_secret")
require_production_secret("JWT_SECRET", JWT_SECRET, "dev_secret")
ACCESS_EXPIRE = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_EXPIRE_DAYS = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", "30"))
DATA_DIR = "data"
REFRESH_FILE = f"{DATA_DIR}/refresh_tokens.json"

# ensure data dir
os.makedirs(DATA_DIR, exist_ok=True)


# Use the same storage mode as auth/users and skills.
USE_DB = os.environ.get("AUTH_STORAGE", "database") != "legacy_json"
if USE_DB:
    from services.db import SessionLocal
    from services.models import RefreshToken as RefreshTokenModel
    from services.models import User as UserModel


def _load_refresh():
    if not os.path.exists(REFRESH_FILE):
        return {}
    with open(REFRESH_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return {}


def _save_refresh(d):
    with open(REFRESH_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def ilm_credential_binding(alias: str, marker: str | None) -> str:
    from services.ilm_access import credential_rotated

    revision = marker.rsplit(":", 1)[1] if credential_rotated(marker) else ""
    return hmac.digest(JWT_SECRET.encode(), (alias + ":" + revision).encode(), "sha256").hex()[:32]


def create_access_token(user_id: int, *, ilm_binding: str | None = None) -> str:
    now = int(time.time())
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + ACCESS_EXPIRE * 60,
    }
    if ilm_binding is not None:
        payload["ilm_credential"] = ilm_binding
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def stage_refresh_token(db, user_id: int, *, ilm_binding: str | None = None) -> str:
    prefix = f"ilmref_{ilm_binding}_" if ilm_binding is not None else "ref_"
    token = prefix + secrets.token_hex(32)
    exp = int(time.time()) + REFRESH_EXPIRE_DAYS * 24 * 3600
    db.add(RefreshTokenModel(token=token, user_id=user_id, exp=exp))
    return token


def create_refresh_token(user_id: int) -> str:
    if USE_DB:
        db = SessionLocal()
        try:
            token = stage_refresh_token(db, user_id)
            db.commit()
            return token
        finally:
            db.close()

    token = "ref_" + secrets.token_hex(32)
    exp = int(time.time()) + REFRESH_EXPIRE_DAYS * 24 * 3600
    data = _load_refresh()
    data[token] = {"user_id": user_id, "exp": exp}
    _save_refresh(data)
    return token


def _ilm_token_state(db, user_id: int, provider: str | None):
    from services.ilm_access import PROVIDER, credential_rotated

    if provider != PROVIDER:
        return None, False
    alias, marker = db.query(UserModel.email, UserModel.oauth_provider_id).filter(
        UserModel.id == user_id
    ).one()
    return ilm_credential_binding(alias, marker), not credential_rotated(marker)


def _refresh_binding_valid(token: str, binding: str | None, allow_legacy: bool) -> bool:
    if binding is None:
        return not token.startswith("ilmref_")
    if not token.startswith("ilmref_"):
        return allow_legacy
    return hmac.compare_digest(token.split("_", 2)[1], binding)


def verify_access_token(token: str) -> Optional[int]:
    try:
        p = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id = int(p.get("sub"))
        if USE_DB:
            from services.account_ownership import DELETED_PROVIDER
            with SessionLocal() as db:
                provider = db.query(UserModel.oauth_provider).filter(UserModel.id == user_id).scalar()
                if provider == DELETED_PROVIDER:
                    return None
                binding, allow_legacy = _ilm_token_state(db, user_id, provider)
                claim = p.get("ilm_credential")
                if binding is not None:
                    if claim is None and not allow_legacy:
                        return None
                    if claim is not None and (not isinstance(claim, str) or not hmac.compare_digest(claim, binding)):
                        return None
                elif claim is not None:
                    return None
        return user_id
    except Exception:
        return None


def rotate_refresh_token(token: str):
    """Consume and replace a refresh token in one database transaction."""
    if not USE_DB:
        user_id = verify_refresh_token(token)
        if not user_id:
            return None
        revoke_refresh_token(token)
        return {"access_token": create_access_token(user_id), "refresh_token": create_refresh_token(user_id)}
    from sqlalchemy import delete
    with SessionLocal() as db:
        user_id = db.execute(delete(RefreshTokenModel).where(
            RefreshTokenModel.token == token, RefreshTokenModel.exp >= int(time.time())
        ).returning(RefreshTokenModel.user_id)).scalar_one_or_none()
        if user_id is None:
            return None
        from services.account_ownership import DELETED_PROVIDER
        provider = db.query(UserModel.oauth_provider).filter(UserModel.id == user_id).scalar()
        if provider == DELETED_PROVIDER:
            return None
        binding, allow_legacy = _ilm_token_state(db, user_id, provider)
        if not _refresh_binding_valid(token, binding, allow_legacy):
            return None
        if binding is None:
            replacement = secrets.token_urlsafe(32)
            db.add(RefreshTokenModel(token=replacement, user_id=user_id,
                                    exp=int(time.time()) + REFRESH_EXPIRE_DAYS * 86400))
        else:
            replacement = stage_refresh_token(db, user_id, ilm_binding=binding)
        result = {"access_token": create_access_token(user_id, ilm_binding=binding), "refresh_token": replacement}
        db.commit()
        return result


def verify_refresh_token(token: str) -> Optional[int]:
    if USE_DB:
        db = SessionLocal()
        try:
            rt = db.query(RefreshTokenModel).filter(RefreshTokenModel.token == token).first()
            if not rt:
                return None
            from services.account_ownership import DELETED_PROVIDER
            provider = db.query(UserModel.oauth_provider).filter(UserModel.id == rt.user_id).scalar()
            if provider == DELETED_PROVIDER:
                return None
            binding, allow_legacy = _ilm_token_state(db, rt.user_id, provider)
            if not _refresh_binding_valid(token, binding, allow_legacy):
                return None
            if int(time.time()) > int(rt.exp):
                db.delete(rt)
                db.commit()
                return None
            return int(rt.user_id)
        finally:
            db.close()

    data = _load_refresh()
    rec = data.get(token)
    if not rec:
        return None
    if int(time.time()) > rec.get("exp", 0):
        # expired - remove
        data.pop(token, None)
        _save_refresh(data)
        return None
    return int(rec.get("user_id"))


def revoke_refresh_token(token: str) -> None:
    if USE_DB:
        db = SessionLocal()
        try:
            rt = db.query(RefreshTokenModel).filter(RefreshTokenModel.token == token).first()
            if rt:
                db.delete(rt)
                db.commit()
        finally:
            db.close()
        return

    data = _load_refresh()
    if token in data:
        data.pop(token, None)
        _save_refresh(data)


def revoke_user_refreshs(user_id: int) -> None:
    if USE_DB:
        db = SessionLocal()
        try:
            db.query(RefreshTokenModel).filter(RefreshTokenModel.user_id == user_id).delete()
            db.commit()
        finally:
            db.close()
        return

    data = _load_refresh()
    to_del = [k for k, v in data.items() if v.get("user_id") == user_id]
    for k in to_del:
        data.pop(k, None)
    _save_refresh(data)
