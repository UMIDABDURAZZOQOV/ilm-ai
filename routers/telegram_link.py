from fastapi import APIRouter, Depends
from services.auth_deps import verify_user_access, ensure_own_user, get_authenticated_user_id
from pydantic import BaseModel

from services.users import link_telegram, set_reminder_time, find_user_by_id

router = APIRouter(prefix="/telegram", tags=["telegram"])


class LinkRequest(BaseModel):
    email: str
    password: str
    chat_id: int


class ReminderRequest(BaseModel):
    user_id: int
    reminder_time: str  # HH:MM


@router.post("/link")
def link_account(data: LinkRequest):
    result = link_telegram(data.email, data.password, data.chat_id)
    if not result["ok"]:
        return {"error": result["error"]}
    user = result["user"]
    return {
        "message": "Telegram linked successfully",
        "user_id": user["id"],
        "reminder_time": user.get("reminder_time", "09:00"),
    }


@router.get("/status/{user_id}")
def telegram_status(user_id: int = Depends(verify_user_access)):
    user = find_user_by_id(user_id)
    if not user:
        return {"error": "User not found"}
    return {
        "linked": bool(user.get("telegram_chat_id")),
        "reminder_time": user.get("reminder_time", "09:00"),
        "streak_days": user.get("streak_days", 0),
        "last_study_date": user.get("last_study_date"),
    }


@router.post("/reminder")
def set_reminder(
    data: ReminderRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
):
    ensure_own_user(data.user_id, auth_user_id)
    ok = set_reminder_time(data.user_id, data.reminder_time)
    if not ok:
        return {"error": "User not found"}
    return {"message": "Reminder updated", "reminder_time": data.reminder_time}
