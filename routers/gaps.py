from fastapi import APIRouter, HTTPException

from services.gap_detection import generate_gaps_report
from services.subscriptions import get_subscription_status

router = APIRouter(prefix="/gaps", tags=["gaps"])


@router.get("/report/{user_id}")
def gaps_report(user_id: int):
    sub = get_subscription_status(user_id)
    if "error" in sub:
        raise HTTPException(status_code=404, detail=sub["error"])

    return generate_gaps_report(user_id, is_premium=sub.get("is_premium", False))
