"""
routers/share.py -- create read-only public share links for study artifacts
(diagram, flashcards, cheat sheet, course). Creating a link needs auth; viewing
one is public (no auth) so it can be opened by anyone with the URL.
"""
from __future__ import annotations

import secrets

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.auth_deps import ensure_own_user, get_authenticated_user_id
from services.db import get_db
from services.models import ShareLink
from sqlalchemy.orm import Session

router = APIRouter(prefix="/share", tags=["share"])

ALLOWED_KINDS = {"diagram", "flashcards", "cheatsheet", "course"}
MAX_PER_USER = 100


class CreateShare(BaseModel):
    user_id: int
    kind: str
    title: str = ""
    payload: dict


@router.post("")
def create_share(data: CreateShare, auth_user_id: int = Depends(get_authenticated_user_id), db: Session = Depends(get_db)):
    ensure_own_user(data.user_id, auth_user_id)
    if data.kind not in ALLOWED_KINDS:
        raise HTTPException(status_code=400, detail="bad_kind")
    if not data.payload:
        raise HTTPException(status_code=400, detail="empty_payload")

    # Keep the store bounded per user (drop oldest beyond the cap).
    existing = db.query(ShareLink).filter(ShareLink.user_id == data.user_id).order_by(ShareLink.created_at.asc()).all()
    for old in existing[: max(0, len(existing) + 1 - MAX_PER_USER)]:
        db.delete(old)

    token = secrets.token_urlsafe(9)[:16]
    db.add(ShareLink(token=token, user_id=data.user_id, kind=data.kind, title=data.title[:200], payload=data.payload))
    db.commit()
    return {"token": token}


@router.get("/{token}")
def get_share(token: str, db: Session = Depends(get_db)):
    row = db.query(ShareLink).filter(ShareLink.token == token).first()
    if not row:
        raise HTTPException(status_code=404, detail="not_found")
    return {"kind": row.kind, "title": row.title or "", "payload": row.payload}
