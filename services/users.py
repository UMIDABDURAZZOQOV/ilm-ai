import hashlib
import json
import os
from datetime import date
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()

USERS_FILE = "users.json"


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# Use DB when DATABASE_URL is set; otherwise fall back to JSON file storage.
USE_DB = bool(os.environ.get("DATABASE_URL"))
if USE_DB:
    from services.db import SessionLocal
    from services.models import User as UserModel


def _load_users_from_file() -> List[Dict[str, Any]]:
    if not os.path.exists(USERS_FILE):
        return []
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, ValueError):
        return []


def _save_users_to_file(users: List[Dict[str, Any]]) -> None:
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def load_users() -> List[Dict[str, Any]]:
    if USE_DB:
        db = SessionLocal()
        try:
            res = db.query(UserModel).all()
            return [{c: getattr(u, c) for c in u.__table__.columns.keys()} for u in res]
        finally:
            db.close()
    return _load_users_from_file()


def save_users(users: List[Dict[str, Any]]) -> None:
    if USE_DB:
        db = SessionLocal()
        try:
            for u in users:
                uid = u.get("id")
                obj = None
                if uid is not None:
                    obj = db.query(UserModel).filter(UserModel.id == uid).first()
                if obj:
                    for k, v in u.items():
                        if k in obj.__table__.columns.keys():
                            setattr(obj, k, v)
                    db.add(obj)
                else:
                    # create new user with allowed fields
                    allowed = {k: v for k, v in u.items() if k in UserModel.__table__.columns.keys()}
                    obj = UserModel(**allowed)
                    db.add(obj)
            db.commit()
        finally:
            db.close()
        return

    _save_users_to_file(users)


def find_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    email = email.strip().lower()
    if USE_DB:
        db = SessionLocal()
        try:
            u = db.query(UserModel).filter(UserModel.email == email).first()
            if not u:
                return None
            return {c: getattr(u, c) for c in u.__table__.columns.keys()}
        finally:
            db.close()

    return next((u for u in _load_users_from_file() if u.get("email") == email), None)


def find_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    if USE_DB:
        db = SessionLocal()
        try:
            u = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not u:
                return None
            return {c: getattr(u, c) for c in u.__table__.columns.keys()}
        finally:
            db.close()

    return next((u for u in _load_users_from_file() if u.get("id") == user_id), None)


def verify_login(email: str, password: str) -> Optional[Dict[str, Any]]:
    user = find_user_by_email(email)
    if not user:
        return None
    if user.get("password") != hash_password(password):
        return None
    return user


def create_user(name: str, email: str, password: str) -> Dict[str, Any]:
    email = email.strip().lower()
    if USE_DB:
        db = SessionLocal()
        try:
            u = UserModel(name=name.strip(), email=email, password=hash_password(password), email_verified=False)
            db.add(u)
            db.commit()
            db.refresh(u)
            return {c: getattr(u, c) for c in u.__table__.columns.keys()}
        finally:
            db.close()

    users = _load_users_from_file()
    user_id = max((u.get("id", 0) for u in users), default=0) + 1
    user = {
        "id": user_id,
        "name": name.strip(),
        "email": email,
        "password": hash_password(password),
        "telegram_chat_id": None,
        "reminder_time": "09:00",
        "streak_days": 0,
        "last_study_date": None,
        "subscription_tier": "free",
        "uploads_count": 0,
        "quiz_count_today": 0,
        "quiz_count_date": None,
        "chat_count_today": 0,
        "chat_count_date": None,
        "learning_goal": None,
        "target_date": None,
        "email_verified": False,
    }
    users.append(user)
    _save_users_to_file(users)
    return user


def set_email_verified(user_id: int, verified: bool = True) -> bool:
    if USE_DB:
        db = SessionLocal()
        try:
            u = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not u:
                return False
            u.email_verified = verified
            db.add(u)
            db.commit()
            return True
        finally:
            db.close()

    users = _load_users_from_file()
    u = next((x for x in users if x.get("id") == user_id), None)
    if not u:
        return False
    u["email_verified"] = verified
    _save_users_to_file(users)
    return True


def update_password(user_id: int, new_password: str) -> bool:
    if USE_DB:
        db = SessionLocal()
        try:
            u = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not u:
                return False
            u.password = hash_password(new_password)
            db.add(u)
            db.commit()
            return True
        finally:
            db.close()

    users = _load_users_from_file()
    u = next((x for x in users if x.get("id") == user_id), None)
    if not u:
        return False
    u["password"] = hash_password(new_password)
    _save_users_to_file(users)
    return True


def create_user_with_oauth(name: str, email: str, provider: str = "google", provider_id: str = None, picture: str = None) -> Dict[str, Any]:
    """Create a user account using OAuth authentication (no password)."""
    email = email.strip().lower()
    if USE_DB:
        db = SessionLocal()
        try:
            u = UserModel(
                name=name.strip(),
                email=email,
                password=None,  # No password for OAuth users
                oauth_provider=provider,
                oauth_provider_id=provider_id,
                profile_picture=picture,
                email_verified=True,  # OAuth provider already verified this address
            )
            db.add(u)
            db.commit()
            db.refresh(u)
            return {c: getattr(u, c) for c in u.__table__.columns.keys()}
        finally:
            db.close()

    users = _load_users_from_file()
    user_id = max((u.get("id", 0) for u in users), default=0) + 1
    user = {
        "id": user_id,
        "name": name.strip(),
        "email": email,
        "password": None,  # No password for OAuth users
        "oauth_provider": provider,
        "oauth_provider_id": provider_id,
        "profile_picture": picture,
        "telegram_chat_id": None,
        "reminder_time": "09:00",
        "streak_days": 0,
        "last_study_date": None,
        "subscription_tier": "free",
        "uploads_count": 0,
        "quiz_count_today": 0,
        "quiz_count_date": None,
        "chat_count_today": 0,
        "chat_count_date": None,
        "learning_goal": None,
        "target_date": None,
        "email_verified": True,  # OAuth provider already verified this address
    }
    users.append(user)
    _save_users_to_file(users)
    return user


def update_user_oauth_info(user_id: int, provider: str = None, provider_id: str = None, picture: str = None) -> bool:
    """Update user OAuth information."""
    if USE_DB:
        db = SessionLocal()
        try:
            u = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not u:
                return False
            if provider is not None:
                u.oauth_provider = provider
            if provider_id is not None:
                u.oauth_provider_id = provider_id
            if picture is not None:
                u.profile_picture = picture
            db.add(u)
            db.commit()
            return True
        finally:
            db.close()

    users = _load_users_from_file()
    u = next((x for x in users if x.get("id") == user_id), None)
    if not u:
        return False
    if provider is not None:
        u["oauth_provider"] = provider
    if provider_id is not None:
        u["oauth_provider_id"] = provider_id
    if picture is not None:
        u["profile_picture"] = picture
    _save_users_to_file(users)
    return True


def update_user_profile(user_id: int, learning_goal: str = None, target_date: str = None, name: str = None, avatar: str = None) -> bool:
    if USE_DB:
        db = SessionLocal()
        try:
            u = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not u:
                return False
            if learning_goal is not None:
                u.learning_goal = learning_goal
            if target_date is not None:
                u.target_date = target_date
            if name is not None:
                u.name = name
            if avatar is not None:
                # Empty string clears the avatar (fall back to initials on the client).
                u.profile_picture = avatar or None
            db.add(u)
            db.commit()
            return True
        finally:
            db.close()

    users = _load_users_from_file()
    u = next((x for x in users if x.get("id") == user_id), None)
    if not u:
        return False
    if learning_goal is not None:
        u["learning_goal"] = learning_goal
    if target_date is not None:
        u["target_date"] = target_date
    if name is not None:
        u["name"] = name
    if avatar is not None:
        u["profile_picture"] = avatar or None
    _save_users_to_file(users)
    return True


def find_user_by_chat_id(chat_id: int) -> Optional[Dict[str, Any]]:
    if USE_DB:
        db = SessionLocal()
        try:
            u = db.query(UserModel).filter(UserModel.telegram_chat_id == str(chat_id)).first()
            if not u:
                return None
            return {c: getattr(u, c) for c in u.__table__.columns.keys()}
        finally:
            db.close()

    return next((u for u in _load_users_from_file() if u.get("telegram_chat_id") == chat_id), None)


def link_telegram(email: str, password: str, chat_id: int) -> Dict[str, Any]:
    email = email.strip().lower()
    if USE_DB:
        db = SessionLocal()
        try:
            user = db.query(UserModel).filter(UserModel.email == email, UserModel.password == hash_password(password)).first()
            if not user:
                return {"ok": False, "error": "Invalid email or password"}

            other = db.query(UserModel).filter(UserModel.telegram_chat_id == str(chat_id), UserModel.id != user.id).first()
            if other:
                return {"ok": False, "error": "This Telegram account is already linked to another user"}

            # Unlink any previous owner
            prev = db.query(UserModel).filter(UserModel.telegram_chat_id == str(chat_id)).first()
            if prev and prev.id != user.id:
                prev.telegram_chat_id = None
                db.add(prev)

            user.telegram_chat_id = str(chat_id)
            db.add(user)
            db.commit()
            db.refresh(user)
            return {"ok": True, "user": {c: getattr(user, c) for c in user.__table__.columns.keys()}}
        finally:
            db.close()

    users = _load_users_from_file()
    user = next((u for u in users if u.get("email") == email and u.get("password") == hash_password(password)), None)
    if not user:
        return {"ok": False, "error": "Invalid email or password"}

    if any(u.get("telegram_chat_id") == chat_id and u.get("id") != user.get("id") for u in users):
        return {"ok": False, "error": "This Telegram account is already linked to another user"}

    for u in users:
        if u.get("id") != user.get("id") and u.get("telegram_chat_id") == chat_id:
            u.pop("telegram_chat_id", None)

    user.setdefault("telegram_chat_id", None)
    user["telegram_chat_id"] = chat_id
    _save_users_to_file(users)
    return {"ok": True, "user": user}


def set_reminder_time(user_id: int, reminder_time: str) -> bool:
    if USE_DB:
        db = SessionLocal()
        try:
            u = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not u:
                return False
            u.reminder_time = reminder_time
            db.add(u)
            db.commit()
            return True
        finally:
            db.close()

    users = _load_users_from_file()
    u = next((x for x in users if x.get("id") == user_id), None)
    if not u:
        return False
    u["reminder_time"] = reminder_time
    _save_users_to_file(users)
    return True


def record_study_activity(user_id: int) -> Dict[str, Any]:
    if USE_DB:
        db = SessionLocal()
        try:
            u = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not u:
                return {"streak_days": 0}

            today = date.today().isoformat()
            last = u.last_study_date
            streak = int(u.streak_days or 0)
            if last == today:
                pass
            elif last is None:
                streak = 1
            else:
                try:
                    last_date = date.fromisoformat(last)
                    delta = (date.today() - last_date).days
                    if delta == 1:
                        streak += 1
                    elif delta > 1:
                        streak = 1
                except Exception:
                    streak = 1

            u.streak_days = streak
            u.last_study_date = today
            db.add(u)
            db.commit()
            return {"streak_days": streak, "last_study_date": today}
        finally:
            db.close()

    users = _load_users_from_file()
    u = next((x for x in users if x.get("id") == user_id), None)
    if not u:
        return {"streak_days": 0}

    today = date.today().isoformat()
    last = u.get("last_study_date")
    streak = int(u.get("streak_days") or 0)
    if last == today:
        pass
    elif last is None:
        streak = 1
    else:
        try:
            last_date = date.fromisoformat(last)
            delta = (date.today() - last_date).days
            if delta == 1:
                streak += 1
            elif delta > 1:
                streak = 1
        except ValueError:
            streak = 1

    u["streak_days"] = streak
    u["last_study_date"] = today
    _save_users_to_file(users)
    return {"streak_days": streak, "last_study_date": today}


def users_with_reminder_at(hour: int, minute: int) -> List[Dict[str, Any]]:
    target = f"{hour:02d}:{minute:02d}"
    if USE_DB:
        db = SessionLocal()
        try:
            res = db.query(UserModel).filter(UserModel.telegram_chat_id.isnot(None), UserModel.reminder_time == target).all()
            return [{c: getattr(u, c) for c in u.__table__.columns.keys()} for u in res]
        finally:
            db.close()

    return [u for u in _load_users_from_file() if u.get("telegram_chat_id") and u.get("reminder_time") == target]


def set_push_token(user_id: int, token: str) -> bool:
    if USE_DB:
        db = SessionLocal()
        try:
            u = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not u:
                return False
            u.push_token = token
            db.add(u)
            db.commit()
            return True
        finally:
            db.close()

    users = _load_users_from_file()
    u = next((x for x in users if x.get("id") == user_id), None)
    if not u:
        return False
    u["push_token"] = token
    _save_users_to_file(users)
    return True


def users_with_push_reminder_at(hour: int, minute: int) -> List[Dict[str, Any]]:
    target = f"{hour:02d}:{minute:02d}"
    if USE_DB:
        db = SessionLocal()
        try:
            res = db.query(UserModel).filter(UserModel.push_token.isnot(None), UserModel.reminder_time == target).all()
            return [{c: getattr(u, c) for c in u.__table__.columns.keys()} for u in res]
        finally:
            db.close()

    return [u for u in _load_users_from_file() if u.get("push_token") and u.get("reminder_time") == target]


def users_with_push_token() -> List[Dict[str, Any]]:
    if USE_DB:
        db = SessionLocal()
        try:
            res = db.query(UserModel).filter(UserModel.push_token.isnot(None)).all()
            return [{c: getattr(u, c) for c in u.__table__.columns.keys()} for u in res]
        finally:
            db.close()

    return [u for u in _load_users_from_file() if u.get("push_token")]