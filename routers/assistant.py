import base64
import os
import time

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError

from services.auth_deps import ensure_own_user, get_authenticated_user_id, verify_user_access
from services.subscriptions import can_use_assistant, record_assistant_use
from services.assistant_history import load_history, append_message, clear_history
from services.monitoring import log_llm_call, track_error
from services.tts import synthesize_speech, TTSError

load_dotenv()
from services.gemini import generate_content as gemini_generate, embed_content as gemini_embed

router = APIRouter(prefix="/assistant", tags=["assistant"])

MAX_HISTORY_PAIRS = 10

SYSTEM_PROMPT = """You are a helpful, knowledgeable general-purpose AI assistant — like ChatGPT or Gemini.
You are NOT restricted to any particular topic, document, or material. Answer anything the
user asks: general knowledge, math, science, coding, writing, advice, explanations,
translations, brainstorming — anything.

Be accurate, clear, and genuinely helpful. If you don't know something, say so honestly
rather than making things up. Format code in code blocks. Keep answers reasonably concise
unless the user asks for depth."""


def _build_history_text(user_id: int) -> str:
    history = load_history(user_id)
    if not history:
        return ""
    lines = []
    for msg in history[-MAX_HISTORY_PAIRS * 2:]:
        role_label = "User" if msg["role"] == "user" else "Assistant"
        lines.append(f"{role_label}: {msg['content']}")
    return "\n\nRECENT CONVERSATION:\n" + "\n".join(lines)


def _call_gemini(contents, user_id: int) -> str:
    start_time = time.time()
    try:
        response = gemini_generate(model="gemini-flash-latest", contents=contents)
    except ClientError as e:
        if getattr(e, "code", None) == 429:
            raise HTTPException(status_code=429, detail="Gemini API rate limit exceeded. Please wait a moment and try again.")
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")

    latency_ms = int((time.time() - start_time) * 1000)
    token_count = None
    try:
        token_count = response.usage_metadata.total_token_count
    except AttributeError:
        pass

    log_llm_call(
        user_id=user_id,
        prompt=str(contents)[:2000],
        response_text=response.text,
        latency_ms=latency_ms,
        token_count=token_count,
        model="gemini-flash-latest",
    )
    return response.text


class AssistantRequest(BaseModel):
    user_id: int
    question: str
    language: str = "en"


@router.post("/ask")
def ask_assistant(data: AssistantRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    ensure_own_user(data.user_id, auth_user_id)
    ok, msg = can_use_assistant(data.user_id)
    if not ok:
        raise HTTPException(status_code=403, detail=msg)

    lang_instruction = f"\nRespond in the following language: {data.language}." if data.language else ""
    prompt = f"{SYSTEM_PROMPT}{lang_instruction}{_build_history_text(data.user_id)}\n\nQUESTION:\n{data.question}"

    answer = _call_gemini(prompt, data.user_id)

    record_assistant_use(data.user_id)
    append_message(data.user_id, "user", data.question)
    append_message(data.user_id, "assistant", answer)

    return {"answer": answer}


@router.post("/ask-voice")
async def ask_assistant_voice(
    user_id: int = Form(...),
    language: str = Form("en"),
    audio: UploadFile = File(...),
    auth_user_id: int = Depends(get_authenticated_user_id),
):
    """
    Voice input: the client records a short audio clip and uploads it here.
    Gemini transcribes AND answers in a single multimodal call — no separate
    speech-to-text service or cost involved.
    """
    ensure_own_user(user_id, auth_user_id)
    ok, msg = can_use_assistant(user_id)
    if not ok:
        raise HTTPException(status_code=403, detail=msg)

    audio_bytes = await audio.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty audio file")

    # Clients (curl, some upload libraries) fall back to the generic
    # "application/octet-stream" when they can't detect a type — Gemini
    # rejects that outright, so treat it the same as a missing content type
    # and guess from the filename extension instead.
    mime_type = audio.content_type
    if not mime_type or mime_type == "application/octet-stream":
        filename = (audio.filename or "").lower()
        if filename.endswith(".wav"):
            mime_type = "audio/wav"
        elif filename.endswith(".mp3"):
            mime_type = "audio/mp3"
        elif filename.endswith(".m4a") or filename.endswith(".mp4"):
            mime_type = "audio/mp4"
        else:
            mime_type = "audio/m4a"
    lang_instruction = f"\nRespond in the following language: {language}." if language else ""
    voice_instruction = (
        "\nThis is a spoken voice conversation, not a written document — your answer will be "
        "read aloud by text-to-speech. Answer like you're talking to someone: natural, "
        "conversational, and reasonably brief (a few sentences for simple questions, a short "
        "paragraph at most for something that genuinely needs more). Avoid bullet lists, "
        "headers, or long structured breakdowns — say it the way you'd say it out loud."
    )
    instruction = (
        f"{SYSTEM_PROMPT}{lang_instruction}{voice_instruction}{_build_history_text(user_id)}\n\n"
        "The user's question is in the attached audio clip. Transcribe it mentally, "
        "then answer it directly — don't repeat the transcription back, just answer."
    )

    audio_part = types.Part.from_bytes(data=audio_bytes, mime_type=mime_type)
    answer = _call_gemini([instruction, audio_part], user_id)

    record_assistant_use(user_id)
    # We don't have the transcribed question text to store on our side — just log the answer.
    append_message(user_id, "user", "🎤 (voice message)")
    append_message(user_id, "assistant", answer)

    return {"answer": answer}


class SpeakRequest(BaseModel):
    text: str
    language: str = "en"


@router.post("/speak")
def speak(data: SpeakRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    """Synthesize natural speech for assistant text via ElevenLabs. Raises 502
    on any TTS failure (missing key, quota exhausted, network) — the mobile
    client falls back to on-device TTS in that case rather than breaking."""
    try:
        audio_bytes = synthesize_speech(data.text, data.language)
    except TTSError as e:
        track_error(e, {"endpoint": "assistant/speak"})
        raise HTTPException(status_code=502, detail="TTS unavailable")

    return {"audio_base64": base64.b64encode(audio_bytes).decode("ascii")}


@router.get("/history/{user_id}")
def get_assistant_history(user_id: int = Depends(verify_user_access)):
    return {"history": load_history(user_id)}


@router.delete("/history/{user_id}")
def clear_assistant_history(user_id: int = Depends(verify_user_access)):
    clear_history(user_id)
    return {"message": "Assistant history cleared"}
