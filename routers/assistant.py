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
from services.assistant_context import (
    build_student_context,
    retrieve_material_context,
    memories_block,
    save_memory,
    parse_tags,
)
from services.monitoring import log_llm_call, track_error
from services.tts import synthesize_speech, TTSError

load_dotenv()
from services.gemini import generate_content as gemini_generate, embed_content as gemini_embed

router = APIRouter(prefix="/assistant", tags=["assistant"])

MAX_HISTORY_PAIRS = 10

SYSTEM_PROMPT = """You are Ilm AI — the learner's personal AI tutor and companion, the heart of the
Ilm AI study app. You are fully general-purpose (answer anything: general knowledge, math,
science, coding, writing, translations, advice), but you are NOT a blank ChatGPT: you know this
specific learner and you help them reach their goals.

How to behave:
- Use the "O'QUVCHI HAQIDA" profile and remembered facts to make answers personal — greet by name
  when natural, connect help to their goal, exam date, weak areas and level. Don't recite the
  profile back; just let it shape your help.
- If material from the learner's own uploaded documents is provided, ANSWER FROM IT and name the
  source. If their question clearly isn't covered by it, answer from general knowledge instead.
- Be accurate and honest — if you don't know, say so. Format code in code blocks. Keep answers
  reasonably concise unless they ask for depth. Reply in the requested language.

Two optional tags you MAY add at the very END of your reply (never mention them, never explain them):
1. When you learn a DURABLE fact about the learner worth remembering long-term (a goal, a persistent
   struggle, a preference — NOT trivia or one-off details), add: <remember>the fact, one short sentence</remember>
2. When the best next step is somewhere in the app, suggest ONE action button:
   <action label="short call to action" href="/route"/>
   Allowed routes only:
     /skills            — lessons, daily practice, review mistakes (Milliy Sertifikat subjects)
     /skills/progress   — their progress and mastery
     /ielts             — IELTS practice (listening/reading/writing/speaking)
     /sat               — SAT practice
     /sat/planner       — study plan
     /course            — a structured course Ilm AI builds from their OWN uploaded materials
     /studio            — Ilm AI Studio: photo study kit, audio recap, knowledge map, cheat sheet, mock test
     /dashboard?panel=quiz       — generate a quiz from their uploaded materials
     /dashboard?panel=files      — upload/manage study materials
     /dashboard?panel=flashcards — flashcards from their materials
     /dashboard?panel=review     — spaced-repetition review
     /dashboard?panel=gaps       — their knowledge-gaps report
   Use an action only when it genuinely helps — not on every reply. Prefer /dashboard?panel=upload-style
   material actions when they ask something that would be better answered from their own notes.
3. Suggest up to THREE natural follow-up questions the learner might ask next, each as:
   <follow>the follow-up question</follow>
   Keep them short, specific to the topic, and phrased in the learner's language."""


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
    filename: str | None = None   # scope RAG to one uploaded document (chat-with-a-document)


@router.post("/ask")
def ask_assistant(data: AssistantRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    ensure_own_user(data.user_id, auth_user_id)
    ok, msg = can_use_assistant(data.user_id)
    if not ok:
        raise HTTPException(status_code=403, detail=msg)

    lang_instruction = f"\nRespond in the following language: {data.language}." if data.language else ""
    # The four companion capabilities, all folded into a single Gemini call:
    student = build_student_context(data.user_id)                    # personalization
    memory = memories_block(data.user_id)                            # long-term memory
    material, sources = retrieve_material_context(                   # RAG (optionally one doc)
        data.user_id, data.question, filename=data.filename
    )
    prompt = (
        f"{SYSTEM_PROMPT}{lang_instruction}{student}{memory}{material}"
        f"{_build_history_text(data.user_id)}\n\nQUESTION:\n{data.question}"
    )

    raw = _call_gemini(prompt, data.user_id)
    answer, new_memories, action, followups = parse_tags(raw)

    for fact in new_memories:
        save_memory(data.user_id, fact)

    record_assistant_use(data.user_id)
    append_message(data.user_id, "user", data.question)
    append_message(data.user_id, "assistant", answer)

    return {"answer": answer, "action": action, "sources": sources, "followups": followups}


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
    # Voice stays personal and remembers too (no RAG here — the question is audio,
    # so there's no text to embed for retrieval). Tags are stripped before speaking.
    student = build_student_context(user_id)
    memory = memories_block(user_id)
    instruction = (
        f"{SYSTEM_PROMPT}{lang_instruction}{voice_instruction}{student}{memory}{_build_history_text(user_id)}\n\n"
        "The user's question is in the attached audio clip. Transcribe it mentally, "
        "then answer it directly — don't repeat the transcription back, just answer."
    )

    audio_part = types.Part.from_bytes(data=audio_bytes, mime_type=mime_type)
    raw = _call_gemini([instruction, audio_part], user_id)
    answer, new_memories, action, _followups = parse_tags(raw)

    for fact in new_memories:
        save_memory(user_id, fact)

    record_assistant_use(user_id)
    # We don't have the transcribed question text to store on our side — just log the answer.
    append_message(user_id, "user", "🎤 (voice message)")
    append_message(user_id, "assistant", answer)

    return {"answer": answer, "action": action}


@router.post("/ask-image")
async def ask_assistant_image(
    user_id: int = Form(...),
    question: str = Form(""),
    language: str = Form("en"),
    image: UploadFile = File(...),
    auth_user_id: int = Depends(get_authenticated_user_id),
):
    """Multimodal chat: the learner attaches a photo (a problem, notes, a diagram)
    and optionally a question. The companion sees the image and answers in context,
    staying personal and remembering facts like the text path."""
    ensure_own_user(user_id, auth_user_id)
    ok, msg = can_use_assistant(user_id)
    if not ok:
        raise HTTPException(status_code=403, detail=msg)

    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty image file")

    mime_type = image.content_type
    if not mime_type or mime_type == "application/octet-stream":
        name = (image.filename or "").lower()
        if name.endswith(".png"):
            mime_type = "image/png"
        elif name.endswith(".webp"):
            mime_type = "image/webp"
        elif name.endswith(".heic"):
            mime_type = "image/heic"
        else:
            mime_type = "image/jpeg"

    lang_instruction = f"\nRespond in the following language: {language}." if language else ""
    student = build_student_context(user_id)
    memory = memories_block(user_id)
    q = question.strip() or "(look at the attached image and help me with it)"
    instruction = (
        f"{SYSTEM_PROMPT}{lang_instruction}{student}{memory}{_build_history_text(user_id)}\n\n"
        f"The learner attached an image. Look at it carefully and respond to their message.\n"
        f"QUESTION: {q}"
    )
    image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
    raw = _call_gemini([instruction, image_part], user_id)
    answer, new_memories, action, followups = parse_tags(raw)

    for fact in new_memories:
        save_memory(user_id, fact)

    record_assistant_use(user_id)
    append_message(user_id, "user", f"🖼️ {q}")
    append_message(user_id, "assistant", answer)

    return {"answer": answer, "action": action, "followups": followups}


@router.get("/briefing/{user_id}")
def daily_briefing(user_id: int = Depends(verify_user_access)):
    """A short, proactive 'here's what to do today' from the companion, built from
    the learner's own state (exam countdown, weak areas, streak). One cheap call;
    the client shows it at the top of the chat."""
    student = build_student_context(user_id)
    if not student:
        # Nothing personal to brief on yet — let the client show a generic hello.
        return {"briefing": "", "action": None}
    prompt = (
        f"{SYSTEM_PROMPT}\nRespond in Uzbek.{student}{memories_block(user_id)}\n\n"
        "Write a SHORT proactive daily briefing (2-3 warm sentences) as their tutor: greet them, "
        "point at the single most useful thing to do today based on their profile (due reviews, weak "
        "areas, exam countdown), and motivate them. You MAY add ONE <action .../> button. No <remember> "
        "or <follow> tags here."
    )
    try:
        raw = _call_gemini(prompt, user_id)
    except HTTPException:
        return {"briefing": "", "action": None}
    text, _mem, action, _f = parse_tags(raw)
    return {"briefing": text, "action": action}


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


@router.get("/memory/{user_id}")
def get_assistant_memory(user_id: int = Depends(verify_user_access)):
    """What the companion has remembered about the learner — surfaced so they can
    see (and clear) it, keeping the personalization transparent."""
    from services.assistant_context import load_memories
    return {"memories": load_memories(user_id)}


@router.delete("/memory/{user_id}")
def clear_assistant_memory(user_id: int = Depends(verify_user_access)):
    from services.assistant_context import clear_memories
    clear_memories(user_id)
    return {"message": "Assistant memory cleared"}
