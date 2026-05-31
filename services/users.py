import hashlib
import json
import os
from datetime import date
from typing import Any

USERS_FILE = "users.json"


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def load_users() -> list[dict[str, Any]]:
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users: list[dict[str, Any]]) -> None:
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def find_user_by_email(email: str) -> dict[str, Any] | None:
    return next((u for u in load_users() if u["email"] == email), None)


def find_user_by_id(user_id: int) -> dict[str, Any] | None:
    return next((u for u in load_users() if u["id"] == user_id), None)


def verify_login(email: str, password: str) -> dict[str, Any] | None:
    user = find_user_by_email(email.strip().lower())
    if not user:
        return None
    if user["password"] != hash_password(password):
        return None
    return user


def create_user(name: str, email: str, password: str) -> dict[str, Any]:
    users = load_users()
    user_id = max((u["id"] for u in users), default=0) + 1
    user = {
        "id": user_id,
        "name": name.strip(),
        "email": email.strip().lower(),
        "password": hash_password(password),
        "telegram_chat_id": None,
        "reminder_time": "09:00",
        "streak_days": 0,
        "last_study_date": None,
    }
    users.append(user)
    save_users(users)
    return user


def find_user_by_chat_id(chat_id: int) -> dict[str, Any] | None:
    return next(
        (u for u in load_users() if u.get("telegram_chat_id") == chat_id),
        None,
    )


def link_telegram(email: str, password: str, chat_id: int) -> dict[str, Any]:
    users = load_users()
    user = next(
        (
            u
            for u in users
            if u["email"] == email and u["password"] == hash_password(password)
        ),
        None,
    )
    if not user:
        return {"ok": False, "error": "Invalid email or password"}

    if any(
        u.get("telegram_chat_id") == chat_id and u["id"] != user["id"]
        for u in users
    ):
        return {
            "ok": False,
            "error": "This Telegram account is already linked to another user",
        }

    for u in users:
        if u["id"] != user["id"] and u.get("telegram_chat_id") == chat_id:
            u.pop("telegram_chat_id", None)

    user.setdefault("telegram_chat_id", None)
    user.setdefault("reminder_time", "09:00")
    user.setdefault("streak_days", 0)
    user.setdefault("last_study_date", None)

    user["telegram_chat_id"] = chat_id
    save_users(users)
    return {"ok": True, "user": user}


def set_reminder_time(user_id: int, reminder_time: str) -> bool:
    users = load_users()
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return False
    user["reminder_time"] = reminder_time
    save_users(users)
    return True


def record_study_activity(user_id: int) -> dict[str, Any]:
    users = load_users()
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return {"streak_days": 0}

    today = date.today().isoformat()
    last = user.get("last_study_date")
    streak = int(user.get("streak_days") or 0)

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

    user["streak_days"] = streak
    user["last_study_date"] = today
    save_users(users)
    return {"streak_days": streak, "last_study_date": today}


def users_with_reminder_at(hour: int, minute: int) -> list[dict[str, Any]]:
    target = f"{hour:02d}:{minute:02d}"
    return [
        u
        for u in load_users()
        if u.get("telegram_chat_id") and u.get("reminder_time") == target
    ]
