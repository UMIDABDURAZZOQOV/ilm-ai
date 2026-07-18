import re

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from services.auth_deps import verify_user_access, ensure_own_user, get_authenticated_user_id
from pydantic import BaseModel, field_validator

from services.users import (
    create_user,
    find_user_by_email,
    verify_login,
    set_email_verified,
    update_password,
)
from services.tokens import create_access_token, create_refresh_token, verify_refresh_token, revoke_refresh_token
from services.google_oauth import get_google_auth_url, handle_google_callback, is_google_oauth_enabled
from services.monitoring import track_user_signup, track_user_login
from services.verification import issue_code, check_code

router = APIRouter(prefix="/auth", tags=["auth"])

EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

    @field_validator("name")
    @classmethod
    def name_valid(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Name must be at least 2 characters")
        return v

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: str) -> str:
        v = v.strip().lower()
        if not EMAIL_PATTERN.match(v):
            raise ValueError("Invalid email address")
        return v

    @field_validator("password")
    @classmethod
    def password_valid(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: str) -> str:
        return v.strip().lower()


@router.post("/signup")
def signup(data: SignupRequest):
    if find_user_by_email(data.email):
        raise HTTPException(status_code=409, detail="An account with this email already exists")

    user = create_user(data.name, data.email, data.password)
    issue_code(user["email"], "signup")

    # Track signup event (account isn't usable yet — verification is required
    # before we issue tokens — but the funnel event is still meaningful)
    track_user_signup(user["id"], user["email"], method="email")

    return {
        "message": "Verification code sent to your email",
        "verification_required": True,
        "email": user["email"],
    }


@router.post("/login")
def login(data: LoginRequest):
    user = verify_login(data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.get("oauth_provider") and not user.get("email_verified"):
        raise HTTPException(
            status_code=403,
            detail={"code": "email_not_verified", "message": "Please verify your email before logging in", "email": user["email"]},
        )

    access = create_access_token(user["id"])
    refresh = create_refresh_token(user["id"])

    # Track login event
    track_user_login(user["id"], user["email"], method="email")

    return {
        "message": "Login successful",
        "user_id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "access_token": access,
        "refresh_token": refresh,
    }


class VerifyEmailRequest(BaseModel):
    email: str
    code: str

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: str) -> str:
        return v.strip().lower()


class ResendCodeRequest(BaseModel):
    email: str
    purpose: str = "signup"  # 'signup' | 'password_reset'

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator("purpose")
    @classmethod
    def purpose_valid(cls, v: str) -> str:
        if v not in ("signup", "password_reset"):
            raise ValueError("Invalid purpose")
        return v


@router.post("/verify-email")
def verify_email(data: VerifyEmailRequest):
    """Confirm the signup verification code and activate the account."""
    user = find_user_by_email(data.email)
    if not user:
        raise HTTPException(status_code=404, detail="Account not found")
    if user.get("email_verified"):
        raise HTTPException(status_code=400, detail="Email already verified")

    result = check_code(data.email, data.code, "signup")
    if not result.get("ok"):
        raise HTTPException(status_code=400, detail=result.get("error", "Invalid code"))

    set_email_verified(user["id"], True)
    access = create_access_token(user["id"])
    refresh = create_refresh_token(user["id"])

    return {
        "message": "Email verified",
        "user_id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "access_token": access,
        "refresh_token": refresh,
    }


@router.post("/resend-code")
def resend_code(data: ResendCodeRequest):
    """Resend a signup or password-reset verification code (rate-limited)."""
    user = find_user_by_email(data.email)
    if not user:
        # Don't reveal whether the email is registered
        return {"message": "If an account exists for this email, a code has been sent"}
    if data.purpose == "signup" and user.get("email_verified"):
        raise HTTPException(status_code=400, detail="Email already verified")

    result = issue_code(data.email, data.purpose)
    if not result.get("ok") and result.get("error") == "cooldown":
        raise HTTPException(
            status_code=429,
            detail=f"Please wait {result.get('retry_after', 30)}s before requesting another code",
        )
    return {"message": "Code sent"}


@router.get("/_diag/email")
def email_diag():
    """Temporary diagnostic: reports whether an email provider is configured and
    actually attempts a self-send, returning the real SMTP error if any. Exposes
    NO secret values — only booleans, lengths, and the error message (SMTP errors
    never contain the password)."""
    from services import email as em

    result = {
        "resend_key_set": bool(em.RESEND_API_KEY),
        "gmail_address_set": bool(em.GMAIL_ADDRESS),
        "gmail_address_len": len(em.GMAIL_ADDRESS or ""),
        "gmail_password_set": bool(em.GMAIL_APP_PASSWORD),
        "gmail_password_len": len(em.GMAIL_APP_PASSWORD or ""),
    }
    if em.GMAIL_ADDRESS and em.GMAIL_APP_PASSWORD:
        try:
            html, text = em._render("000000", "diagnostika", "diagnostika")
            em._send_via_gmail(em.GMAIL_ADDRESS, "Ilm AI — diagnostika", html, text)
            result["gmail_send"] = "ok"
        except Exception as e:  # noqa: BLE001
            result["gmail_send_error"] = str(e)[:400]
    return result


class PasswordResetRequest(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: str) -> str:
        return v.strip().lower()


class PasswordResetConfirm(BaseModel):
    email: str
    code: str
    new_password: str

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator("new_password")
    @classmethod
    def password_valid(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


@router.post("/password-reset/request")
def password_reset_request(data: PasswordResetRequest):
    user = find_user_by_email(data.email)
    if user and not user.get("oauth_provider"):
        issue_code(data.email, "password_reset")
    # Always return the same response regardless of whether the account
    # exists, so this endpoint can't be used to enumerate registered emails.
    return {"message": "If an account exists for this email, a code has been sent"}


@router.post("/password-reset/confirm")
def password_reset_confirm(data: PasswordResetConfirm):
    user = find_user_by_email(data.email)
    if not user:
        raise HTTPException(status_code=404, detail="Account not found")

    result = check_code(data.email, data.code, "password_reset")
    if not result.get("ok"):
        raise HTTPException(status_code=400, detail=result.get("error", "Invalid code"))

    update_password(user["id"], data.new_password)
    access = create_access_token(user["id"])
    refresh = create_refresh_token(user["id"])

    return {
        "message": "Password reset successfully",
        "user_id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "access_token": access,
        "refresh_token": refresh,
    }


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh")
def refresh_token(data: RefreshRequest):
    user_id = verify_refresh_token(data.refresh_token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    # issue new tokens
    access = create_access_token(user_id)
    refresh = create_refresh_token(user_id)
    # revoke old
    revoke_refresh_token(data.refresh_token)
    return {"access_token": access, "refresh_token": refresh}


@router.post("/logout")
def logout(data: RefreshRequest):
    # revoke refresh token
    revoke_refresh_token(data.refresh_token)
    return {"message": "Logged out"}


class ProfileUpdateRequest(BaseModel):
    user_id: int
    learning_goal: Optional[str] = None
    target_date: Optional[str] = None
    name: Optional[str] = None
    avatar: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Name cannot be blank")
        return v.strip() if v is not None else v


@router.get("/profile/{user_id}")
def get_profile(user_id: int = Depends(verify_user_access)):
    from services.users import find_user_by_id
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Remove password from response
    user.pop("password", None)
    return user


@router.post("/update-profile")
def update_profile(
    data: ProfileUpdateRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
):
    from services.users import update_user_profile
    ensure_own_user(data.user_id, auth_user_id)
    success = update_user_profile(data.user_id, data.learning_goal, data.target_date, data.name, data.avatar)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Profile updated successfully"}


@router.get("/google-login")
async def google_login(request: Request, redirect_uri: str = None):
    """Generate Google OAuth 2.0 authorization URL."""
    if not is_google_oauth_enabled():
        raise HTTPException(
            status_code=503,
            detail="Google OAuth is not configured. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables."
        )
    
    if not redirect_uri:
        redirect_uri = f"{request.base_url}auth/google-callback"
    
    auth_url, state = await get_google_auth_url(request, redirect_uri)
    return {"auth_url": auth_url, "state": state}


@router.get("/google-callback")
async def google_callback(code: str, state: str, request: Request, redirect_uri: str = None):
    """
    Handle Google OAuth callback. Exchanges code for user info and tokens.

    The redirect_uri used here MUST exactly match the one used when the
    authorization URL was generated (/auth/google-login), or Google's token
    exchange fails with redirect_uri_mismatch. The web frontend calls this
    endpoint with its own origin as `redirect_uri` (since that's what it
    passed to /auth/google-login) — use it when provided instead of always
    recomputing the backend's own origin, which only happened to work when
    frontend and backend shared a domain in local dev.
    """
    if not is_google_oauth_enabled():
        raise HTTPException(
            status_code=503,
            detail="Google OAuth is not configured. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables."
        )

    if not redirect_uri:
        redirect_uri = f"{request.base_url}auth/google-callback"
    result = await handle_google_callback(request, redirect_uri)

    # Track login/signup event for OAuth
    if result.get("user_id"):
        track_user_login(result["user_id"], result["email"], method="google")

    return result


@router.get("/google-callback-mobile")
async def google_callback_mobile(code: str, state: str, request: Request):
    """
    Handle Google OAuth callback for the mobile app.

    The mobile app opens the auth URL in an in-app browser
    (expo-web-browser's openAuthSessionAsync) and waits for a redirect to the
    `ilmai://auth/callback` deep link to detect success. Unlike /google-callback
    (used by the web frontend), this endpoint must issue an HTTP redirect —
    returning JSON here would leave the in-app browser stuck on a blank page.
    """
    if not is_google_oauth_enabled():
        raise HTTPException(
            status_code=503,
            detail="Google OAuth is not configured. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables."
        )

    redirect_uri = f"{request.base_url}auth/google-callback-mobile"

    try:
        result = await handle_google_callback(request, redirect_uri)
    except HTTPException as e:
        from urllib.parse import urlencode
        query = urlencode({"error": e.detail})
        return RedirectResponse(url=f"ilmai://auth/callback?{query}")

    if result.get("user_id"):
        track_user_login(result["user_id"], result["email"], method="google")

    from urllib.parse import urlencode
    query = urlencode({
        "access_token": result["access_token"],
        "refresh_token": result["refresh_token"],
        "user_id": result["user_id"],
        "name": result["name"],
        "email": result["email"],
    })
    return RedirectResponse(url=f"ilmai://auth/callback?{query}")
