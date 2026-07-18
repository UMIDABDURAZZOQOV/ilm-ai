"""
routers/parent.py -- Parent dashboard (Ota-ona paneli). A student generates a
stable family code and shares it; a parent redeems it to link, then gets
read-only visibility into the child's streak, weakest subject, and activity.

Identity comes from the JWT (auth_user_id).
"""
from __future__ import annotations

import secrets

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from services.auth_deps import get_authenticated_user_id
from services.db import get_db
from services.models import FamilyCode, ParentChildLink, User
from services.skill_stats import student_detail

router = APIRouter(prefix="/parent", tags=["parent"])

_CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def _ensure_family_code(db: Session, child_id: int) -> str:
    existing = db.query(FamilyCode).filter(FamilyCode.child_id == child_id).first()
    if existing:
        return existing.code
    for _ in range(8):
        code = "".join(secrets.choice(_CODE_ALPHABET) for _ in range(6))
        if not db.query(FamilyCode).filter(FamilyCode.code == code).first():
            fc = FamilyCode(child_id=child_id, code=code)
            db.add(fc)
            db.commit()
            return code
    raise HTTPException(status_code=500, detail="Could not allocate a family code")


@router.get("/my-code")
def my_family_code(
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    """A student fetches (creating on first call) the code they share with a parent."""
    code = _ensure_family_code(db, auth_user_id)
    parents = (
        db.query(ParentChildLink).filter(ParentChildLink.child_id == auth_user_id).all()
    )
    parent_ids = [p.parent_id for p in parents]
    names = {u.id: u.name for u in db.query(User).filter(User.id.in_(parent_ids)).all()} if parent_ids else {}
    return {
        "code": code,
        "linked_parents": [{"parent_id": pid, "name": names.get(pid, "...")} for pid in parent_ids],
    }


class LinkChildRequest(BaseModel):
    code: str


@router.post("/link")
def link_child(
    data: LinkChildRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    """A parent redeems a child's family code to link to their account."""
    fc = db.query(FamilyCode).filter(FamilyCode.code == data.code.strip().upper()).first()
    if not fc:
        raise HTTPException(status_code=404, detail="invalid_code")
    if fc.child_id == auth_user_id:
        raise HTTPException(status_code=400, detail="self_link")
    existing = (
        db.query(ParentChildLink)
        .filter(ParentChildLink.parent_id == auth_user_id, ParentChildLink.child_id == fc.child_id)
        .first()
    )
    if existing:
        child = db.query(User).filter(User.id == fc.child_id).first()
        return {"linked": True, "child_id": fc.child_id, "child_name": child.name if child else "...", "already": True}
    db.add(ParentChildLink(parent_id=auth_user_id, child_id=fc.child_id))
    db.commit()
    child = db.query(User).filter(User.id == fc.child_id).first()
    return {"linked": True, "child_id": fc.child_id, "child_name": child.name if child else "...", "already": False}


@router.get("/children")
def my_children(
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    links = db.query(ParentChildLink).filter(ParentChildLink.parent_id == auth_user_id).all()
    child_ids = [l.child_id for l in links]
    users = {u.id: u for u in db.query(User).filter(User.id.in_(child_ids)).all()} if child_ids else {}
    children = []
    for cid in child_ids:
        u = users.get(cid)
        if not u:
            continue
        children.append(student_detail(db, u))
    return {"children": children}


@router.get("/child/{child_id}")
def child_detail(
    child_id: int,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    link = (
        db.query(ParentChildLink)
        .filter(ParentChildLink.parent_id == auth_user_id, ParentChildLink.child_id == child_id)
        .first()
    )
    if not link:
        raise HTTPException(status_code=403, detail="Not linked to this child")
    child = db.query(User).filter(User.id == child_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    return student_detail(db, child)


class UnlinkRequest(BaseModel):
    child_id: int


@router.post("/unlink")
def unlink_child(
    data: UnlinkRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    db.query(ParentChildLink).filter(
        ParentChildLink.parent_id == auth_user_id,
        ParentChildLink.child_id == data.child_id,
    ).delete()
    db.commit()
    return {"unlinked": True}
