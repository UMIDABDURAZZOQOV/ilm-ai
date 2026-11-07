"""Email reauthentication for app and public-web deletion; no token in any URL."""

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, Response, JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.exc import IntegrityError

from services.db import get_db
from services.auth_deps import get_authenticated_user_id
from services.account_deletion import request_deletion, confirm_deletion, require_ready
from services.models import User

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


def install(app):
    app.include_router(router)

    @app.exception_handler(IntegrityError)
    async def lifecycle_conflict(request, error):
        if "account_deleted" in str(error.orig):
            return JSONResponse({"detail": "account_deleted"}, status_code=401)
        return JSONResponse({"detail": "database_write_failed"}, status_code=500)
