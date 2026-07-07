import os
from datetime import date
from typing import Any

from services.users import find_user_by_id, load_users, save_users

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

FREE_LIMITS = {
    "quiz_per_day": 3,
    "max_uploads": 5,
    "max_chat_per_day": 50,
}

PREMIUM_LIMITS = {
    "quiz_per_day": 999,
    "max_uploads": 999,
    "max_chat_per_day": 999,
}


def _ensure_usage_fields(user: dict[str, Any]) -> None:
    user.setdefault("subscription_tier", "free")
    user.setdefault("uploads_count", 0)
    user.setdefault("quiz_count_today", 0)
    user.setdefault("quiz_count_date", None)
    user.setdefault("chat_count_today", 0)
    user.setdefault("chat_count_date", None)


def _reset_daily_if_needed(user: dict[str, Any]) -> None:
    today = date.today().isoformat()
    if user.get("quiz_count_date") != today:
        user["quiz_count_today"] = 0
        user["quiz_count_date"] = today
    if user.get("chat_count_date") != today:
        user["chat_count_today"] = 0
        user["chat_count_date"] = today


def get_limits(user: dict[str, Any]) -> dict[str, int]:
    tier = user.get("subscription_tier", "free")
    return PREMIUM_LIMITS if tier == "premium" else FREE_LIMITS


def get_subscription_status(user_id: int) -> dict[str, Any]:
    users = load_users()
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return {"error": "User not found"}

    _ensure_usage_fields(user)
    _reset_daily_if_needed(user)
    save_users(users)

    limits = get_limits(user)
    return {
        "tier": user.get("subscription_tier", "free"),
        "uploads_count": user.get("uploads_count", 0),
        "uploads_limit": limits["max_uploads"],
        "quiz_today": user.get("quiz_count_today", 0),
        "quiz_limit": limits["quiz_per_day"],
        "chat_today": user.get("chat_count_today", 0),
        "chat_limit": limits["max_chat_per_day"],
        "is_premium": user.get("subscription_tier") == "premium",
    }


def can_upload(user_id: int) -> tuple[bool, str]:
    user = find_user_by_id(user_id)
    if not user:
        return False, "User not found"
    _ensure_usage_fields(user)
    limits = get_limits(user)
    count = user.get("uploads_count", 0)
    if count >= limits["max_uploads"]:
        return False, f"Upload limit reached ({limits['max_uploads']}). Upgrade to Premium."
    return True, ""


def record_upload(user_id: int) -> None:
    users = load_users()
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return
    _ensure_usage_fields(user)
    user["uploads_count"] = user.get("uploads_count", 0) + 1
    save_users(users)


def record_delete_upload(user_id: int) -> None:
    users = load_users()
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return
    _ensure_usage_fields(user)
    user["uploads_count"] = max(0, user.get("uploads_count", 0) - 1)
    save_users(users)


def can_take_quiz(user_id: int) -> tuple[bool, str]:
    users = load_users()
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return False, "User not found"
    _ensure_usage_fields(user)
    _reset_daily_if_needed(user)
    limits = get_limits(user)
    if user.get("quiz_count_today", 0) >= limits["quiz_per_day"]:
        return False, f"Daily quiz limit reached ({limits['quiz_per_day']}). Upgrade to Premium."
    save_users(users)
    return True, ""


def record_quiz_session(user_id: int) -> None:
    users = load_users()
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return
    _ensure_usage_fields(user)
    _reset_daily_if_needed(user)
    user["quiz_count_today"] = user.get("quiz_count_today", 0) + 1
    save_users(users)


def can_chat(user_id: int) -> tuple[bool, str]:
    users = load_users()
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return False, "User not found"
    _ensure_usage_fields(user)
    _reset_daily_if_needed(user)
    limits = get_limits(user)
    if user.get("chat_count_today", 0) >= limits["max_chat_per_day"]:
        return False, "Daily chat limit reached. Upgrade to Premium."
    save_users(users)
    return True, ""


def record_chat(user_id: int) -> None:
    users = load_users()
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return
    _ensure_usage_fields(user)
    _reset_daily_if_needed(user)
    user["chat_count_today"] = user.get("chat_count_today", 0) + 1
    save_users(users)


def upgrade_to_premium(user_id: int) -> bool:
    users = load_users()
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return False
    user["subscription_tier"] = "premium"
    save_users(users)
    return True


def downgrade_to_free(user_id: int) -> bool:
    users = load_users()
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return False
    user["subscription_tier"] = "free"
    save_users(users)
    return True
