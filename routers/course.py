"""
routers/course.py -- "Materialdan avtomatik kurs": Ilm AI builds a structured
mini-course from the learner's OWN uploaded materials. Outline is generated once
and stored; per-lesson questions are generated on demand.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.auth_deps import ensure_own_user, get_authenticated_user_id, verify_user_access
from services.subscriptions import can_use_assistant, record_assistant_use
from services.user_course import (
    generate_course,
    load_course,
    generate_lesson_questions,
    set_lesson_progress,
)

router = APIRouter(prefix="/course", tags=["course"])


class GenerateRequest(BaseModel):
    user_id: int
    language: str = "uz"


@router.post("/generate")
def generate(data: GenerateRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    ensure_own_user(data.user_id, auth_user_id)
    ok, msg = can_use_assistant(data.user_id)
    if not ok:
        raise HTTPException(status_code=403, detail=msg)
    result = generate_course(data.user_id, data.language)
    if result.get("error"):
        code = 400 if result["error"] == "no_materials" else 502
        raise HTTPException(status_code=code, detail=result["error"])
    record_assistant_use(data.user_id)
    return result


@router.get("/{user_id}")
def get_course(user_id: int = Depends(verify_user_access)):
    data = load_course(user_id)
    if not data:
        return {"course": None, "progress": {}}
    return data


class LessonQuestionsRequest(BaseModel):
    user_id: int
    chapter_title: str
    lesson_title: str
    lesson_summary: str = ""
    language: str = "uz"


@router.post("/lesson-questions")
def lesson_questions(data: LessonQuestionsRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    ensure_own_user(data.user_id, auth_user_id)
    ok, msg = can_use_assistant(data.user_id)
    if not ok:
        raise HTTPException(status_code=403, detail=msg)
    questions = generate_lesson_questions(
        data.user_id, data.chapter_title, data.lesson_title, data.lesson_summary, data.language
    )
    if not questions:
        raise HTTPException(status_code=502, detail="generation_failed")
    record_assistant_use(data.user_id)
    return {"questions": questions}


class LessonCompleteRequest(BaseModel):
    user_id: int
    lesson_key: str
    score: int = 0


@router.post("/lesson-complete")
def lesson_complete(data: LessonCompleteRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    ensure_own_user(data.user_id, auth_user_id)
    progress = set_lesson_progress(data.user_id, data.lesson_key, data.score)
    return {"progress": progress}
