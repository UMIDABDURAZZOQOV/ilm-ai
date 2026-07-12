import os
import json
import time
import secrets
from typing import Optional

import jwt
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET = os.environ.get("JWT_SECRET", "dev_secret")
if os.environ.get("ENVIRONMENT") == "production" and JWT_SECRET == "dev_secret":
    raise RuntimeError(
        "JWT_SECRET is not set. Refusing to start in production with the default "
        "dev_secret — anyone could forge valid auth tokens. Set JWT_SECRET in the "
        "environment."
    )
ACCESS_EXPIRE = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_EXPIRE_DAYS = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", "30"))
DATA_DIR = "data"
REFRESH_FILE = f"{DATA_DIR}/refresh_tokens.json"

# ensure data dir
os.makedirs(DATA_DIR, exist_ok=True)


# Prefer DB-backed refresh tokens when DATABASE_URL is set
USE_DB = bool(os.environ.get("DATABASE_URL"))
if USE_DB:
    from services.db import SessionLocal
    from services.models import RefreshToken as RefreshTokenModel


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


def create_access_token(user_id: int) -> str:
    now = int(time.time())
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + ACCESS_EXPIRE * 60,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def create_refresh_token(user_id: int) -> str:
    token = "ref_" + secrets.token_hex(32)
    exp = int(time.time()) + REFRESH_EXPIRE_DAYS * 24 * 3600
    if USE_DB:
        db = SessionLocal()
        try:
            rt = RefreshTokenModel(token=token, user_id=user_id, exp=exp)
            db.add(rt)
            db.commit()
            return token
        finally:
            db.close()

    data = _load_refresh()
    data[token] = {"user_id": user_id, "exp": exp}
    _save_refresh(data)
    return token


def verify_access_token(token: str) -> Optional[int]:
    try:
        p = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return int(p.get("sub"))
    except Exception:
        return None


def verify_refresh_token(token: str) -> Optional[int]:
    if USE_DB:
        db = SessionLocal()
        try:
            rt = db.query(RefreshTokenModel).filter(RefreshTokenModel.token == token).first()
            if not rt:
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
