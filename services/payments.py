import json
import os
import secrets
import base64
import hmac
import hashlib
import requests
from datetime import datetime
from typing import Any
from fastapi import HTTPException

from services.subscriptions import upgrade_to_premium
from services.monitoring import track_error

DATA_DIR = "data/payments"
os.makedirs(DATA_DIR, exist_ok=True)

# Test mode — set to False for real Payme/Click integration
TEST_MODE = os.environ.get("PAYMENT_TEST_MODE", "true").lower() == "true"

# Payme configuration
PAYME_MERCHANT_ID = os.environ.get("PAYME_MERCHANT_ID", "")
PAYME_KEY = os.environ.get("PAYME_KEY", "")
PAYME_API_URL = "https://checkout.paycom.uz/api"

# Click configuration
CLICK_SERVICE_ID = os.environ.get("CLICK_SERVICE_ID", "")
CLICK_MERCHANT_ID = os.environ.get("CLICK_MERCHANT_ID", "")
CLICK_SECRET_KEY = os.environ.get("CLICK_SECRET_KEY", "")
CLICK_API_URL = "https://api.click.uz/v2"

# Payment amounts
PREMIUM_PRICE_UZS = 99000  # Premium subscription price in UZS


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


def create_checkout(user_id: int, plan: str = "premium", gateway: str = "payme") -> dict[str, Any]:
    session_id = f"test_{secrets.token_hex(12)}" if TEST_MODE else secrets.token_hex(12)
    sessions = _load_sessions()
    
    amount_uzs = PREMIUM_PRICE_UZS
    
    checkout_data = {
        "user_id": user_id,
        "plan": plan,
        "gateway": gateway,
        "amount_uzs": amount_uzs,
        "currency": "UZS",
        "status": "pending",
        "test_mode": TEST_MODE,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    
    sessions[session_id] = checkout_data
    _save_sessions(sessions)

    if TEST_MODE:
        return {
            "session_id": session_id,
            "gateway": gateway,
            "amount_uzs": amount_uzs,
            "message": f"Test {gateway} checkout created.",
            "confirm_url": f"/payments/confirm?session_id={session_id}&user_id={user_id}",
            "checkout_url": None,  # In test mode, no redirect; frontend shows payment modal
        }
    
    # Real payment integration
    if gateway == "payme":
        checkout_url = _create_payme_checkout(session_id, amount_uzs, user_id)
    elif gateway == "click":
        checkout_url = _create_click_checkout(session_id, amount_uzs, user_id)
    else:
        return {"ok": False, "error": f"Unsupported payment gateway: {gateway}"}
    
    return {
        "session_id": session_id,
        "gateway": gateway,
        "amount_uzs": amount_uzs,
        "message": f"{gateway.capitalize()} checkout created.",
        "confirm_url": None,  # Real payment gateways handle their own callbacks
        "checkout_url": checkout_url,  # Redirect user to this URL to complete payment
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


def _create_payme_checkout(session_id: str, amount: int, user_id: int) -> str:
    """Create Payme checkout URL using Payme API."""
    if not PAYME_MERCHANT_ID or not PAYME_KEY:
        raise ValueError("Payme credentials not configured")
    
    try:
        # Payme API request to create payment
        payload = {
            "method": "CreateTransaction",
            "params": {
                "amount": amount * 100,  # Payme uses tiyin (1 UZS = 100 tiyin)
                "account": {
                    "order_id": session_id,
                    "user_id": user_id
                },
                "description": f"Ilm AI Premium subscription for user {user_id}"
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "X-Auth": PAYME_MERCHANT_ID
        }
        
        # Sign the request
        headers["X-Auth"] = _generate_payme_signature(payload)
        
        response = requests.post(PAYME_API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("error"):
            error_code = result["error"].get("code")
            error_message = result["error"].get("message", "Unknown error")
            raise HTTPException(status_code=400, detail=f"Payme API error: {error_message} (code: {error_code})")
        
        # Return Payme checkout URL
        transaction_id = result.get("result", {}).get("transaction_id", session_id)
        return f"https://checkout.paycom.uz?m={PAYME_MERCHANT_ID}&ac.transaction_id={transaction_id}"
        
    except requests.exceptions.RequestException as e:
        track_error(e, context={"operation": "create_payme_checkout", "user_id": user_id})
        raise HTTPException(status_code=503, detail=f"Failed to connect to Payme API: {str(e)}")
    except Exception as e:
        track_error(e, context={"operation": "create_payme_checkout", "user_id": user_id})
        raise HTTPException(status_code=500, detail=f"Failed to create Payme checkout: {str(e)}")


def _create_click_checkout(session_id: str, amount: int, user_id: int) -> str:
    """Create Click checkout URL using Click API."""
    if not CLICK_SERVICE_ID or not CLICK_MERCHANT_ID:
        raise ValueError("Click credentials not configured")
    
    try:
        # Click API request to create payment
        payload = {
            "service_id": CLICK_SERVICE_ID,
            "merchant_id": CLICK_MERCHANT_ID,
            "amount": amount,
            "transaction_param": session_id,
            "user_id": user_id,
            "return_url": f"https://your-domain.com/payments/success?session_id={session_id}",
            "description": f"Ilm AI Premium subscription for user {user_id}"
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        response = requests.post(f"{CLICK_API_URL}/payment/create", json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("error_code"):
            error_message = result.get("error_note", "Unknown error")
            raise HTTPException(status_code=400, detail=f"Click API error: {error_message}")
        
        # Return Click checkout URL
        payment_id = result.get("payment_id")
        return f"https://my.click.uz/pay?service_id={CLICK_SERVICE_ID}&merchant_id={CLICK_MERCHANT_ID}&payment_id={payment_id}"
        
    except requests.exceptions.RequestException as e:
        track_error(e, context={"operation": "create_click_checkout", "user_id": user_id})
        raise HTTPException(status_code=503, detail=f"Failed to connect to Click API: {str(e)}")
    except Exception as e:
        track_error(e, context={"operation": "create_click_checkout", "user_id": user_id})
        raise HTTPException(status_code=500, detail=f"Failed to create Click checkout: {str(e)}")


def _generate_payme_signature(payload: dict) -> str:
    """Generate signature for Payme API requests."""
    # Payme signature generation
    # This is a simplified version - in production use Payme's official SDK
    payload_str = json.dumps(payload, separators=(',', ':'), sort_keys=True)
    signature = hashlib.sha256((payload_str + PAYME_KEY).encode()).hexdigest()
    return signature


def verify_payme_webhook(data: dict) -> bool:
    """Verify Payme webhook signature."""
    if TEST_MODE:
        return True
    
    try:
        # Verify the signature from Payme
        # In production, use proper signature verification
        received_signature = data.get("signature") or data.get("headers", {}).get("X-Auth")
        if not received_signature:
            return False
        
        # Generate expected signature
        expected_signature = _generate_payme_signature(data.get("params", {}))
        
        # Use constant-time comparison to prevent timing attacks
        return hmac.compare_digest(received_signature, expected_signature)
        
    except Exception as e:
        track_error(e, context={"operation": "verify_payme_webhook"})
        return False


def verify_click_webhook(data: dict) -> bool:
    """Verify Click webhook signature."""
    if TEST_MODE:
        return True
    
    try:
        # Click signature verification
        # Click sends a signature in the headers
        received_signature = data.get("signature") or data.get("headers", {}).get("Authorization")
        if not received_signature:
            return False
        
        # Generate expected signature using Click's method
        # Click uses HMAC-SHA256 with the secret key
        params_str = "|".join([
            data.get("service_id", ""),
            data.get("merchant_id", ""),
            data.get("transaction_param", ""),
            str(data.get("amount", "")),
            CLICK_SECRET_KEY
        ])
        
        expected_signature = hmac.HMAC(
            CLICK_SECRET_KEY.encode(),
            params_str.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Use constant-time comparison
        return hmac.compare_digest(received_signature, expected_signature)
        
    except Exception as e:
        track_error(e, context={"operation": "verify_click_webhook"})
        return False
