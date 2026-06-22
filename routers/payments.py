from fastapi import APIRouter, Depends, HTTPException
from services.auth_deps import verify_user_access, ensure_own_user, get_authenticated_user_id
from pydantic import BaseModel
from typing import Optional

from services.payments import confirm_checkout, create_checkout, handle_webhook
from services.subscriptions import downgrade_to_free, get_subscription_status
from services.monitoring import track_payment_success, track_payment_failure

router = APIRouter(prefix="/payments", tags=["payments"])


class CheckoutRequest(BaseModel):
    user_id: int
    plan: str = "premium"
    gateway: str = "payme"
    method: Optional[str] = None  # frontend sends 'method' instead of 'gateway'


class WebhookPayload(BaseModel):
    session_id: str
    user_id: int
    event: str = "payment.success"


@router.get("/status/{user_id}")
def payment_status(user_id: int = Depends(verify_user_access)):
    return get_subscription_status(user_id)


@router.post("/checkout")
def checkout(data: CheckoutRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    ensure_own_user(data.user_id, auth_user_id)
    # Support both 'gateway' and 'method' field names
    gateway = data.method or data.gateway
    return create_checkout(data.user_id, data.plan, gateway)


@router.post("/confirm")
def confirm(
    session_id: str,
    user_id: int,
    auth_user_id: int = Depends(get_authenticated_user_id),
):
    ensure_own_user(user_id, auth_user_id)
    result = confirm_checkout(session_id, user_id)
    if not result.get("ok"):
        track_payment_failure(user_id, 0, "test", result.get("error", "Failed"))
        raise HTTPException(status_code=400, detail=result.get("error", "Failed"))
    
    # Track successful payment
    track_payment_success(user_id, 99000, "test", session_id)
    
    return result


@router.post("/webhook")
def webhook(payload: WebhookPayload):
    """Test-mode webhook — simulates payment provider callback."""
    result = handle_webhook(payload.model_dump())
    if not result.get("ok"):
        raise HTTPException(status_code=400, detail=result.get("error", "Failed"))
    return result


@router.post("/webhook/payme")
def payme_webhook(payload: dict):
    """Real Payme webhook handler."""
    from services.payments import verify_payme_webhook, confirm_checkout, _load_sessions, _save_sessions
    from services.monitoring import track_payment_success, track_payment_failure, track_error
    import json
    
    try:
        # Verify webhook signature
        if not verify_payme_webhook(payload):
            track_error(Exception("Invalid Payme signature"), context={"payload": payload})
            return {"error": {"code": -32504, "message": "Invalid signature"}}
        
        # Handle different Payme methods
        method = payload.get("method")
        
        if method == "CheckPerformTransaction":
            # Check if transaction can be performed
            order_id = payload.get("params", {}).get("account", {}).get("order_id")
            sessions = _load_sessions()
            session = sessions.get(order_id)
            if not session or session.get("status") == "paid":
                return {"error": {"code": -31050, "message": "Order not found or already paid"}}
            return {"result": {"allow": True}}
            
        elif method == "CreateTransaction":
            # Create transaction
            order_id = payload.get("params", {}).get("account", {}).get("order_id")
            sessions = _load_sessions()
            session = sessions.get(order_id)
            if not session:
                return {"error": {"code": -31050, "message": "Order not found"}}
            if session.get("status") == "paid":
                return {"error": {"code": -31008, "message": "Transaction already paid"}}
            
            # Update session with Payme transaction ID
            transaction_id = payload.get("params", {}).get("transaction_id")
            session["transaction_id"] = transaction_id
            sessions[order_id] = session
            _save_sessions(sessions)
            
            return {"result": {"transaction_id": transaction_id, "state": 1}}
            
        elif method == "PerformTransaction":
            # Complete the payment
            order_id = payload.get("params", {}).get("account", {}).get("order_id")
            sessions = _load_sessions()
            session = sessions.get(order_id)
            if not session:
                return {"error": {"code": -31050, "message": "Order not found"}}
            
            user_id = session["user_id"]
            result = confirm_checkout(order_id, user_id)
            
            if result.get("ok"):
                # Track successful payment
                track_payment_success(user_id, session.get("amount_uzs", 99000), "payme", order_id)
                return {"result": {"state": 2, "transaction_id": session.get("transaction_id", order_id)}}
            else:
                track_payment_failure(user_id, session.get("amount_uzs", 99000), "payme", result.get("error", "Failed"))
                return {"error": {"code": -31001, "message": result.get("error", "Failed")}}
                
        elif method == "CheckTransaction":
            # Check transaction status
            order_id = payload.get("params", {}).get("account", {}).get("order_id")
            sessions = _load_sessions()
            session = sessions.get(order_id)
            if not session:
                return {"error": {"code": -31050, "message": "Order not found"}}
            
            state = 2 if session.get("status") == "paid" else 1
            return {"result": {"state": state, "transaction_id": session.get("transaction_id", order_id)}}
            
        else:
            return {"result": {"status": "success"}}
            
    except Exception as e:
        track_error(e, context={"operation": "payme_webhook", "payload": payload})
        return {"error": {"code": -32494, "message": "Internal error"}}


@router.post("/webhook/click")
def click_webhook(payload: dict):
    """Real Click webhook handler."""
    from services.payments import verify_click_webhook, confirm_checkout, _load_sessions, _save_sessions
    from services.monitoring import track_payment_success, track_payment_failure, track_error
    
    try:
        # Verify webhook signature
        if not verify_click_webhook(payload):
            track_error(Exception("Invalid Click signature"), context={"payload": payload})
            return {"error": "-1", "error_note": "Invalid signature"}
        
        # Extract payment information
        transaction_param = payload.get("transaction_param") or payload.get("merchant_trans_id")
        if not transaction_param:
            return {"error": "-2", "error_note": "Invalid transaction_param"}
        
        # Find session and confirm
        sessions = _load_sessions()
        session = sessions.get(transaction_param)
        if not session:
            return {"error": "-3", "error_note": "Transaction not found"}
        
        user_id = session["user_id"]
        result = confirm_checkout(transaction_param, user_id)
        
        if result.get("ok"):
            # Track successful payment
            track_payment_success(user_id, session.get("amount_uzs", 99000), "click", transaction_param)
            return {"success": "true", "transaction_id": transaction_param}
        else:
            track_payment_failure(user_id, session.get("amount_uzs", 99000), "click", result.get("error", "Failed"))
            return {"success": "false", "error": result.get("error", "Failed")}
            
    except Exception as e:
        track_error(e, context={"operation": "click_webhook", "payload": payload})
        return {"error": "-1", "error_note": "Internal error"}


@router.post("/cancel/{user_id}")
def cancel_subscription(user_id: int = Depends(verify_user_access)):
    downgrade_to_free(user_id)
    return {"message": "Downgraded to free tier (test mode)"}
