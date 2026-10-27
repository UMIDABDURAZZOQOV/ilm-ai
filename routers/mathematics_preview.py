"""Additive authenticated Math v1 router, deliberately absent from main.py."""

from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from sqlalchemy.orm import Session

from services import mathematics_runtime as runtime
from services.auth_deps import get_authenticated_user_id
from services.db import get_db


def preview_db(db: Annotated[Session, Depends(get_db)]):
    runtime.preview_gate(db)
    return db


DB = Annotated[Session, Depends(preview_db)]
UID = Annotated[int, Depends(get_authenticated_user_id)]
router = APIRouter(
    prefix="/preview/mathematics/v1",
    tags=["local-mathematics-preview"],
    dependencies=[Depends(preview_db)],
)


class Start(BaseModel):
    model_config = ConfigDict(extra="forbid")
    assessment_version: Literal[1]
    request_id: UUID


class Answer(BaseModel):
    model_config = ConfigDict(extra="forbid")
    choice_id: Annotated[StrictStr, Field(min_length=1, max_length=80)] | None = None
    value: Annotated[StrictStr, Field(min_length=1, max_length=160)] | None = None


class Submission(Start):
    question_id: Annotated[StrictStr, Field(min_length=1, max_length=96)]
    answer: Answer


@router.get("/catalog")
def catalog(
    db: DB,
    uid: UID,
    grade: Annotated[int, Query(ge=1, le=11)] = 1,
    part: Annotated[int, Query(ge=1, le=4)] = 1,
):
    return runtime.catalog(db, uid, grade, part)


@router.post("/lessons/{key}/start")
def start(key: str, data: Start, db: DB, uid: UID):
    return runtime.start(db, uid, key, str(data.request_id))


@router.post("/attempts/{sid}/answers")
def submit(sid: str, data: Submission, db: DB, uid: UID):
    return runtime.submit(
        db,
        uid,
        sid,
        str(data.request_id),
        data.question_id,
        data.answer.model_dump(exclude_none=True),
    )


@router.post("/attempts/{sid}/complete")
def complete(sid: str, data: Start, db: DB, uid: UID):
    return runtime.complete(db, uid, sid)
