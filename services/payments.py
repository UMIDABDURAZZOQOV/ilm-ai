import json
import os
import secrets
from datetime import datetime
from typing import Any

from services.subscriptions import upgrade_to_premium

DATA_DIR = "data/payments"
os.makedirs(DATA_DIR, exist_ok=True)

# Test mode — no real Payme/Click/Stripe charges
TEST_MODE = True


def _sessions_file() -> str:
    return f"{DATA_DIR}/checkout_sessions.json"


def _load_sessions() -> dict[str, Any]:
    path = _sessions_file()
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_sessions(data: dict[str, Any]) -> None:
    with open(_sessions_file(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def create_checkout(user_id: int, plan: str = "premium") -> dict[str, Any]:
    session_id = f"test_{secrets.token_hex(12)}"
    sessions = _load_sessions()
    sessions[session_id] = {
        "user_id": user_id,
        "plan": plan,
        "amount_uzs": 99000,
        "currency": "UZS",
        "status": "pending",
        "test_mode": TEST_MODE,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    _save_sessions(sessions)

    return {
        "session_id": session_id,
        "test_mode": TEST_MODE,
        "plan": plan,
        "amount_uzs": 99000,
        "message": "Test checkout created. No real payment will be charged.",
        "confirm_url": f"/payments/confirm?session_id={session_id}&user_id={user_id}",
    }


def confirm_checkout(session_id: str, user_id: int) -> dict[str, Any]:
    sessions = _load_sessions()
    session = sessions.get(session_id)
    if not session:
        return {"ok": False, "error": "Checkout session not found"}
    if session["user_id"] != user_id:
        return {"ok": False, "error": "Session does not match user"}
    if session["status"] == "paid":
        return {"ok": True, "message": "Already activated", "tier": "premium"}

    session["status"] = "paid"
    session["paid_at"] = datetime.utcnow().isoformat() + "Z"
    sessions[session_id] = session
    _save_sessions(sessions)

    upgrade_to_premium(user_id)
    return {
        "ok": True,
        "message": "Premium activated (test mode)",
        "tier": "premium",
        "session_id": session_id,
    }


def handle_webhook(payload: dict[str, Any]) -> dict[str, Any]:
    """Simulates Payme/Click/Stripe webhook in test mode."""
    session_id = payload.get("session_id")
    user_id = payload.get("user_id")
    event = payload.get("event", "payment.success")

    if event != "payment.success" or not session_id or not user_id:
        return {"ok": False, "error": "Invalid webhook payload"}

    return confirm_checkout(session_id, int(user_id))
