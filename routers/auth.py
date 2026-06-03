import re

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator

from services.users import (
    create_user,
    find_user_by_email,
    verify_login,
)
from services.tokens import create_access_token, create_refresh_token, verify_refresh_token, revoke_refresh_token

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
