from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.payments import confirm_checkout, create_checkout, handle_webhook
from services.subscriptions import downgrade_to_free, get_subscription_status

router = APIRouter(prefix="/payments", tags=["payments"])


class CheckoutRequest(BaseModel):
    user_id: int
    plan: str = "premium"


class WebhookPayload(BaseModel):
    session_id: str
    user_id: int
    event: str = "payment.success"


@router.get("/status/{user_id}")
def payment_status(user_id: int):
    return get_subscription_status(user_id)


@router.post("/checkout")
def checkout(data: CheckoutRequest):
    return create_checkout(data.user_id, data.plan)


@router.post("/confirm")
def confirm(session_id: str, user_id: int):
    result = confirm_checkout(session_id, user_id)
    if not result.get("ok"):
        raise HTTPException(status_code=400, detail=result.get("error", "Failed"))
    return result


@router.post("/webhook")
def webhook(payload: WebhookPayload):
    """Test-mode webhook — simulates payment provider callback."""
    result = handle_webhook(payload.model_dump())
    if not result.get("ok"):
        raise HTTPException(status_code=400, detail=result.get("error", "Failed"))
    return result


@router.post("/cancel/{user_id}")
def cancel_subscription(user_id: int):
    downgrade_to_free(user_id)
    return {"message": "Downgraded to free tier (test mode)"}
