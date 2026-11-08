"""Owner reauthentication for app/web deletion; no session token in a URL."""

from pathlib import Path
import os
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, Response, JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.exc import IntegrityError

from services.db import get_db
from services.auth_deps import get_authenticated_user_id
from services.account_deletion import request_deletion, confirm_deletion, require_ready
from services.models import User
from services import deletion_reauth

router = APIRouter(tags=["account-deletion"])
DB = Annotated[object, Depends(get_db)]
UID = Annotated[int, Depends(get_authenticated_user_id)]
STATIC = Path(__file__).resolve().parents[1] / "static/account-deletion"
HEADERS = {
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "no-referrer",
    "X-Frame-Options": "DENY",
    "Content-Security-Policy": "default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'",
}


class EmailRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    # Address syntax is only input hygiene; mailbox possession is proved by OTP.
    email: str = Field(max_length=200, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class Confirmation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: str = Field(min_length=43, max_length=43, pattern=r"^[A-Za-z0-9_-]+$")
    code: str = Field(pattern=r"^\d{6}$")
    confirmation: str = Field(max_length=6)


@router.get("/account-deletion", response_class=HTMLResponse)
def public_page():
    return HTMLResponse(
        (STATIC / "index.html").read_text(encoding="utf8"), headers=HEADERS
    )


@router.get("/account-deletion.js")
def public_script():
    return Response(
        (STATIC / "deletion.js").read_text(encoding="utf8"),
        media_type="application/javascript",
        headers=HEADERS,
    )


@router.get("/account-deletion.css")
def public_styles():
    return Response(
        (STATIC / "deletion.css").read_text(encoding="utf8"),
        media_type="text/css",
        headers=HEADERS,
    )


@router.get("/account/deletion/config")
def capabilities(db: DB):
    if os.getenv("EMAIL_FREE_ACCOUNT_DELETION") == "true":
        try:
            deletion_reauth.ready(db)
        except HTTPException:
            return {
                "available": False,
                "web_path": "/account-deletion",
                "email_required": False,
            }
        return {
            "available": True,
            "web_path": "/account-deletion",
            "email_required": False,
            "reauthentication_methods": ["google", "password"],
            "proof_ttl_seconds": 300,
        }
    try:
        require_ready(db)
    except HTTPException:
        return {"available": False, "web_path": "/account-deletion"}
    return {"available": True, "web_path": "/account-deletion"}


@router.post("/account/deletion/request")
def web_request(data: EmailRequest, request: Request, db: DB):
    return request_deletion(
        db, str(data.email), request.client.host if request.client else "unknown"
    )


@router.post("/account/deletion/me/request")
def app_request(request: Request, db: DB, user_id: UID):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(401, "account_not_found")
    return request_deletion(
        db,
        user.email,
        request.client.host if request.client else "unknown",
        expected_user=user_id,
    )


@router.post("/account/deletion/confirm")
def confirm(data: Confirmation, db: DB):
    return confirm_deletion(db, data.request_id, data.code, data.confirmation)


class PasswordReauth(BaseModel):
    model_config = ConfigDict(extra="forbid")
    password: str = Field(min_length=1, max_length=1024)


class WebPasswordReauth(PasswordReauth):
    email: str = Field(max_length=200, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class GoogleReauth(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code_challenge: str = Field(pattern=r"^[A-Za-z0-9_-]{43}$")


class DeletionExchange(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: str = Field(pattern=r"^[A-Za-z0-9_-]{43}$")
    code_verifier: str = Field(pattern=r"^[A-Za-z0-9._~-]{43,128}$")


class ReauthConfirmation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: str = Field(pattern=r"^da[pw]_[A-Za-z0-9_-]{39}$")
    proof: str = Field(pattern=r"^[A-Za-z0-9_-]{43}$")
    confirmation: str = Field(max_length=6)


class ManualRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    account_email: str = Field(max_length=200, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    contact_email: str = Field(max_length=200, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    reason: str = Field(min_length=10, max_length=1000)


@router.get("/account/deletion/reauth/options")
def reauth_options(db: DB, user_id: UID):
    deletion_reauth.ready(db)
    user = deletion_reauth.active(db, user_id)
    method = (
        "google"
        if user.oauth_provider == "google" and user.oauth_provider_id
        else "password"
    )
    return {"method": method}


@router.post("/account/deletion/manual-request")
def manual_deletion_request(data: ManualRequest, request: Request, db: DB):
    return deletion_reauth.manual_request(
        db,
        data.account_email,
        data.contact_email,
        data.reason,
        request.client.host if request.client else "unknown",
    )


@router.post("/account/deletion/reauth/password")
def password_reauth(data: PasswordReauth, request: Request, db: DB, user_id: UID):
    return deletion_reauth.password_proof(
        db,
        "",
        data.password,
        request.client.host if request.client else "unknown",
        uid=user_id,
        surface="mobile",
    )


@router.post("/account/deletion/web/password")
def web_password_reauth(data: WebPasswordReauth, request: Request, db: DB):
    return deletion_reauth.password_proof(
        db,
        data.email,
        data.password,
        request.client.host if request.client else "unknown",
    )


@router.post("/account/deletion/reauth/google")
def google_reauth(data: GoogleReauth, request: Request, db: DB, user_id: UID):
    return deletion_reauth.begin_google(
        db,
        data.code_challenge,
        request.client.host if request.client else "unknown",
        uid=user_id,
        surface="mobile",
    )


@router.post("/account/deletion/web/google")
def web_google_reauth(data: GoogleReauth, request: Request, db: DB):
    return deletion_reauth.begin_google(
        db, data.code_challenge, request.client.host if request.client else "unknown"
    )


@router.post("/account/deletion/reauth/exchange")
def deletion_exchange(data: DeletionExchange, db: DB):
    return deletion_reauth.exchange(db, data.code, data.code_verifier)


@router.post("/account/deletion/reauth/confirm")
def reauth_confirm(data: ReauthConfirmation, request: Request, db: DB):
    from services.tokens import verify_access_token

    authorization = request.headers.get("authorization", "")
    uid = (
        verify_access_token(authorization[7:])
        if authorization.startswith("Bearer ")
        else None
    )
    return deletion_reauth.confirm(
        db, data.request_id, data.proof, data.confirmation, uid
    )


async def google_deletion_callback_response(state, code, error):
    """Only deletion-prefixed state reaches this purpose-specific callback."""
    from urllib.parse import urlencode
    from fastapi.responses import RedirectResponse
    from services.db import SessionLocal
    from services.deletion_reauth_models import DeletionReauth
    from services.deployment_config import mobile_app_scheme

    with SessionLocal() as db:
        row = db.get(DeletionReauth, deletion_reauth.sha(state or ""))
        if row is None:
            raise HTTPException(400, "invalid_deletion_state")
        surface = row.surface
        try:
            grant, surface = await deletion_reauth.google_callback(
                db, state, code, error
            )
        except HTTPException:
            query = urlencode({"error": "reauthentication_failed", "state": state})
        else:
            query = urlencode({"code": grant, "state": state})
        target = (
            f"{mobile_app_scheme()}://deletion/callback?{query}"
            if surface == "mobile"
            else "/account-deletion#" + query
        )
        return RedirectResponse(
            target,
            headers={"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"},
        )


def install(app):
    app.include_router(router)

    @app.exception_handler(IntegrityError)
    async def lifecycle_conflict(request, error):
        if "account_deleted" in str(error.orig):
            return JSONResponse({"detail": "account_deleted"}, status_code=401)
        return JSONResponse({"detail": "database_write_failed"}, status_code=500)
