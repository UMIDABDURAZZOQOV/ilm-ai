"""Versioned opt-in local/test API. Legacy /skills and /mobile are unchanged."""

from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from sqlalchemy.orm import Session

from services import assessment_runtime as runtime
from services.auth_deps import get_authenticated_user_id
from services.db import get_db


def preview_db(db: Annotated[Session, Depends(get_db)]):
    runtime.preview_gate(db)
    return db


router = APIRouter(
    prefix="/preview/physics/v2",
    tags=["local-physics-preview"],
    dependencies=[Depends(preview_db)],
)
PreviewDB = Annotated[Session, Depends(preview_db)]
AuthID = Annotated[int, Depends(get_authenticated_user_id)]
Text128 = Annotated[StrictStr, Field(min_length=1, max_length=128)]


class Start(BaseModel):
    model_config = ConfigDict(extra="forbid")
    assessment_version: Literal[2]
    request_id: UUID


class Answer(BaseModel):
    model_config = ConfigDict(extra="forbid")
    choice_id: Text128 | None = None
    order: list[Text128] | None = Field(default=None, max_length=20)
    value: Text128 | None = None
    unit: Text128 | None = None
    formula: Text128 | None = None


class Submission(BaseModel):
    model_config = ConfigDict(extra="forbid")
    assessment_version: Literal[2]
    assessment_key: Annotated[StrictStr, Field(min_length=1, max_length=140)]
    answer: Answer


class Completion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    assessment_version: Literal[2]


@router.get("/catalog")
def catalog(db: PreviewDB, uid: AuthID):
    return runtime.catalog(db, uid)


@router.post("/lessons/{key}/start")
def start(key: str, data: Start, db: PreviewDB, uid: AuthID):
    return runtime.start(db, uid, key, str(data.request_id))


@router.post("/attempts/{sid}/answers")
def answer(sid: str, data: Submission, db: PreviewDB, uid: AuthID):
    return runtime.submit(
        db, uid, sid, data.assessment_key, data.answer.model_dump(exclude_none=True)
    )


@router.post("/attempts/{sid}/complete")
def complete(sid: str, data: Completion, db: PreviewDB, uid: AuthID):
    return runtime.complete(db, uid, sid)
