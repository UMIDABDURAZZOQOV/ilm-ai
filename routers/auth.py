import re

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from services.auth_deps import verify_user_access, ensure_own_user, get_authenticated_user_id
from pydantic import BaseModel, field_validator

from services.users import (
    create_user,
    find_user_by_email,
    verify_login,
)
from services.tokens import create_access_token, create_refresh_token, verify_refresh_token, revoke_refresh_token
from services.google_oauth import get_google_auth_url, handle_google_callback, is_google_oauth_enabled
from services.monitoring import track_user_signup, track_user_login, track_error

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
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
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
    access = create_access_token(user["id"])
    refresh = create_refresh_token(user["id"])
    
    # Track signup event
    track_user_signup(user["id"], user["email"], method="email")
    
    return {
        "message": "Account created successfully",
        "user_id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "access_token": access,
        "refresh_token": refresh,
    }


@router.post("/login")
def login(data: LoginRequest):
    user = verify_login(data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
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
    success = update_user_profile(data.user_id, data.learning_goal, data.target_date)
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
async def google_callback(code: str, state: str, request: Request):
    """Handle Google OAuth callback. Exchanges code for user info and tokens."""
    if not is_google_oauth_enabled():
        raise HTTPException(
            status_code=503,
            detail="Google OAuth is not configured. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables."
        )
    
    redirect_uri = f"{request.base_url}auth/google-callback"
    result = await handle_google_callback(request, redirect_uri)
    
    # Track login/signup event for OAuth
    if result.get("user_id"):
        track_user_login(result["user_id"], result["email"], method="google")
    
    return result
