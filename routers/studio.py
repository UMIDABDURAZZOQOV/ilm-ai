"""
routers/studio.py -- Ilm AI Studio: power tools over the learner's OWN uploaded
materials (photo study kit, audio recap, knowledge map, cheat sheet, mock test).
"""
from __future__ import annotations

import base64

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from services.auth_deps import ensure_own_user, get_authenticated_user_id, verify_user_access
from services.subscriptions import can_use_assistant, record_assistant_use
from services.tts import synthesize_speech, TTSError
from services.quiz_engine import load_vectors
from services import studio

router = APIRouter(prefix="/studio", tags=["studio"])


def _guard(user_id: int, auth_user_id: int):
    ensure_own_user(user_id, auth_user_id)
    ok, msg = can_use_assistant(user_id)
    if not ok:
        raise HTTPException(status_code=403, detail=msg)


def _handle(user_id: int, result: dict) -> dict:
    if result.get("error"):
        code = 400 if result["error"] == "no_materials" else 502
        raise HTTPException(status_code=code, detail=result["error"])
    record_assistant_use(user_id)
    try:
        from services.gamify import award_study
        award_study(user_id)
    except Exception:
        pass
    return result


class SearchRequest(BaseModel):
    user_id: int
    query: str


@router.post("/search")
def search(data: SearchRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    """Semantic 'search your notes' over the learner's uploaded materials."""
    ensure_own_user(data.user_id, auth_user_id)
    return studio.search_materials(data.user_id, data.query)


@router.get("/files/{user_id}")
def list_files(user_id: int = Depends(verify_user_access)):
    """Filenames the learner has uploaded — lets the UI scope a tool to one file."""
    vectors = load_vectors(user_id)
    files = sorted({v.get("filename", "") for v in vectors if v.get("filename")})
    return {"files": files}


@router.post("/photo-kit")
async def photo_kit(
    user_id: int = Form(...),
    language: str = Form("uz"),
    image: UploadFile = File(...),
    auth_user_id: int = Depends(get_authenticated_user_id),
):
    _guard(user_id, auth_user_id)
    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="empty_image")
    result = studio.photo_kit(image_bytes, image.content_type, image.filename, language)
    return _handle(user_id, result)


class MaterialRequest(BaseModel):
    user_id: int
    language: str = "uz"
    filename: str | None = None


@router.post("/audio-recap")
def audio_recap(data: MaterialRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    _guard(data.user_id, auth_user_id)
    result = studio.audio_recap(data.user_id, data.filename, data.language)
    result = _handle(data.user_id, result)
    # Best-effort TTS: if it fails (no key / quota), still return the script so the
    # client can fall back to on-device speech synthesis.
    audio_b64 = None
    try:
        audio_bytes = synthesize_speech(result["script"], data.language)
        audio_b64 = base64.b64encode(audio_bytes).decode("ascii")
    except TTSError:
        audio_b64 = None
    return {"script": result["script"], "audio_base64": audio_b64, "sources": result.get("sources", [])}


@router.post("/podcast")
def podcast(data: MaterialRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    """Two-host podcast SCRIPT from the learner's material (read aloud client-side)."""
    _guard(data.user_id, auth_user_id)
    return _handle(data.user_id, studio.podcast(data.user_id, data.filename, data.language))


@router.post("/knowledge-map")
def knowledge_map(data: MaterialRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    _guard(data.user_id, auth_user_id)
    return _handle(data.user_id, studio.knowledge_map(data.user_id, data.language))


@router.post("/cheat-sheet")
def cheat_sheet(data: MaterialRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    _guard(data.user_id, auth_user_id)
    return _handle(data.user_id, studio.cheat_sheet(data.user_id, data.filename, data.language))


@router.post("/translate")
def translate(data: MaterialRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    _guard(data.user_id, auth_user_id)
    return _handle(data.user_id, studio.translate_explain(data.user_id, data.filename, data.language))


class TextFlashcardsRequest(BaseModel):
    user_id: int
    text: str
    language: str = "uz"


@router.post("/text-flashcards")
def text_flashcards(data: TextFlashcardsRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    """Flashcards from any passage (e.g. a companion answer) — no upload needed."""
    _guard(data.user_id, auth_user_id)
    result = studio.text_flashcards(data.text, data.language)
    if result.get("error"):
        code = 400 if result["error"] == "empty" else 502
        raise HTTPException(status_code=code, detail=result["error"])
    record_assistant_use(data.user_id)
    return result


class DiagramRequest(BaseModel):
    user_id: int
    topic: str = ""
    from_materials: bool = False
    language: str = "uz"


@router.post("/diagram")
def diagram(data: DiagramRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    """Generate a Mermaid diagram / mind-map for a topic or the learner's materials."""
    _guard(data.user_id, auth_user_id)
    result = studio.diagram(data.user_id, data.topic, data.from_materials, data.language)
    if result.get("error"):
        code = 400 if result["error"] in ("no_materials", "empty") else 502
        raise HTTPException(status_code=code, detail=result["error"])
    record_assistant_use(data.user_id)
    return result


class MockRequest(BaseModel):
    user_id: int
    language: str = "uz"
    n: int = 15


@router.post("/mock")
def mock(data: MockRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    _guard(data.user_id, auth_user_id)
    n = max(5, min(30, data.n))
    return _handle(data.user_id, studio.mock_from_materials(data.user_id, data.language, n))
