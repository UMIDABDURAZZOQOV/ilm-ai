"""
routers/classes.py -- Teacher / class mode (Sinf rejimi) for the Milliy
Sertifikat skill tree. Any user can open a class (becoming its teacher) and
share a join code; students join and the teacher sees each student's progress
and can assign lessons/subjects as homework.

Identity comes from the JWT (auth_user_id) -- no user_id is trusted from the body.
"""
from __future__ import annotations

import secrets

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from services.auth_deps import get_authenticated_user_id
from services.db import get_db
from services.models import (
    SkillClass,
    SkillClassAssignment,
    SkillClassMember,
    SkillLesson,
    SkillSubject,
    User,
)
from services.skill_stats import student_row

router = APIRouter(prefix="/classes", tags=["classes"])

_CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def _gen_join_code(db: Session) -> str:
    for _ in range(8):
        code = "".join(secrets.choice(_CODE_ALPHABET) for _ in range(6))
        if not db.query(SkillClass).filter(SkillClass.join_code == code).first():
            return code
    raise HTTPException(status_code=500, detail="Could not allocate a join code")


def _class_or_404(db: Session, class_id: int) -> SkillClass:
    cls = db.query(SkillClass).filter(SkillClass.id == class_id).first()
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")
    return cls


def _require_teacher(db: Session, class_id: int, auth_user_id: int) -> SkillClass:
    cls = _class_or_404(db, class_id)
    if cls.teacher_id != auth_user_id:
        raise HTTPException(status_code=403, detail="Not the teacher of this class")
    return cls


def _class_brief(db: Session, cls: SkillClass) -> dict:
    member_count = db.query(SkillClassMember).filter(SkillClassMember.class_id == cls.id).count()
    return {
        "id": cls.id,
        "name": cls.name,
        "subject_slug": cls.subject_slug,
        "join_code": cls.join_code,
        "member_count": member_count,
        "created_at": cls.created_at.isoformat() if cls.created_at else None,
    }


class CreateClassRequest(BaseModel):
    name: str
    subject_slug: str | None = None


@router.post("")
def create_class(
    data: CreateClassRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    name = data.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Name required")
    cls = SkillClass(
        teacher_id=auth_user_id,
        name=name[:160],
        subject_slug=data.subject_slug,
        join_code=_gen_join_code(db),
    )
    db.add(cls)
    db.commit()
    db.refresh(cls)
    return _class_brief(db, cls)


@router.get("/mine")
def my_classes(
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    teaching = (
        db.query(SkillClass)
        .filter(SkillClass.teacher_id == auth_user_id, SkillClass.archived.is_(False))
        .order_by(SkillClass.created_at.desc())
        .all()
    )
    member_rows = db.query(SkillClassMember).filter(SkillClassMember.student_id == auth_user_id).all()
    enrolled_ids = [m.class_id for m in member_rows]
    enrolled = (
        db.query(SkillClass)
        .filter(SkillClass.id.in_(enrolled_ids), SkillClass.archived.is_(False))
        .all()
        if enrolled_ids else []
    )
    teacher_ids = {c.teacher_id for c in enrolled}
    teachers = {u.id: u.name for u in db.query(User).filter(User.id.in_(teacher_ids)).all()} if teacher_ids else {}
    return {
        "teaching": [_class_brief(db, c) for c in teaching],
        "enrolled": [
            {
                "id": c.id,
                "name": c.name,
                "subject_slug": c.subject_slug,
                "teacher_name": teachers.get(c.teacher_id, "..."),
            }
            for c in enrolled
        ],
    }


class JoinClassRequest(BaseModel):
    code: str


@router.post("/join")
def join_class(
    data: JoinClassRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    cls = db.query(SkillClass).filter(SkillClass.join_code == data.code.strip().upper()).first()
    if not cls or cls.archived:
        raise HTTPException(status_code=404, detail="invalid_code")
    if cls.teacher_id == auth_user_id:
        raise HTTPException(status_code=400, detail="own_class")
    existing = (
        db.query(SkillClassMember)
        .filter(SkillClassMember.class_id == cls.id, SkillClassMember.student_id == auth_user_id)
        .first()
    )
    if existing:
        return {"joined": True, "class_id": cls.id, "name": cls.name, "already": True}
    db.add(SkillClassMember(class_id=cls.id, student_id=auth_user_id))
    db.commit()
    return {"joined": True, "class_id": cls.id, "name": cls.name, "already": False}


class LeaveClassRequest(BaseModel):
    class_id: int


@router.post("/leave")
def leave_class(
    data: LeaveClassRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    db.query(SkillClassMember).filter(
        SkillClassMember.class_id == data.class_id,
        SkillClassMember.student_id == auth_user_id,
    ).delete()
    db.commit()
    return {"left": True}


@router.get("/{class_id}")
def class_detail(
    class_id: int,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    """Teacher-only roster with each student's live progress + assignments."""
    cls = _require_teacher(db, class_id, auth_user_id)
    members = db.query(SkillClassMember).filter(SkillClassMember.class_id == class_id).all()
    student_ids = [m.student_id for m in members]
    users = {u.id: u for u in db.query(User).filter(User.id.in_(student_ids)).all()} if student_ids else {}
    roster = [student_row(db, users[sid]) for sid in student_ids if sid in users]
    roster.sort(key=lambda r: r["weekly_xp"], reverse=True)

    assignments = (
        db.query(SkillClassAssignment)
        .filter(SkillClassAssignment.class_id == class_id)
        .order_by(SkillClassAssignment.created_at.desc())
        .all()
    )
    return {
        "id": cls.id,
        "name": cls.name,
        "subject_slug": cls.subject_slug,
        "join_code": cls.join_code,
        "roster": roster,
        "assignments": [
            {
                "id": a.id,
                "title": a.title,
                "subject_slug": a.subject_slug,
                "lesson_id": a.lesson_id,
                "due_date": a.due_date,
            }
            for a in assignments
        ],
    }


class AssignRequest(BaseModel):
    title: str
    subject_slug: str | None = None
    lesson_id: int | None = None
    due_date: str | None = None


@router.post("/{class_id}/assign")
def create_assignment(
    class_id: int,
    data: AssignRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    _require_teacher(db, class_id, auth_user_id)
    title = data.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title required")
    if data.subject_slug and not db.query(SkillSubject).filter(SkillSubject.slug == data.subject_slug).first():
        raise HTTPException(status_code=404, detail="Subject not found")
    if data.lesson_id and not db.query(SkillLesson).filter(SkillLesson.id == data.lesson_id).first():
        raise HTTPException(status_code=404, detail="Lesson not found")
    a = SkillClassAssignment(
        class_id=class_id,
        title=title[:200],
        subject_slug=data.subject_slug,
        lesson_id=data.lesson_id,
        due_date=data.due_date,
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return {"id": a.id, "title": a.title}


@router.delete("/{class_id}/assignments/{assignment_id}")
def delete_assignment(
    class_id: int,
    assignment_id: int,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    _require_teacher(db, class_id, auth_user_id)
    db.query(SkillClassAssignment).filter(
        SkillClassAssignment.id == assignment_id,
        SkillClassAssignment.class_id == class_id,
    ).delete()
    db.commit()
    return {"deleted": True}


@router.delete("/{class_id}/members/{student_id}")
def remove_member(
    class_id: int,
    student_id: int,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    _require_teacher(db, class_id, auth_user_id)
    db.query(SkillClassMember).filter(
        SkillClassMember.class_id == class_id,
        SkillClassMember.student_id == student_id,
    ).delete()
    db.commit()
    return {"removed": True}


@router.delete("/{class_id}")
def archive_class(
    class_id: int,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    cls = _require_teacher(db, class_id, auth_user_id)
    cls.archived = True
    db.add(cls)
    db.commit()
    return {"archived": True}
