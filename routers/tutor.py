"""
routers/tutor.py -- in-lesson AI tutor (AI repetitor). On demand only: when a
learner gets a question wrong and taps "Tushuntirib ber", the client calls this
to get a short, plain-language explanation from Gemini. Not called per question,
so API usage stays low.
"""
from __future__ import annotations

import json
import re

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from google.genai import types

from services.auth_deps import get_authenticated_user_id
from services.gemini import generate_content as gemini_generate

router = APIRouter(prefix="/skills", tags=["tutor"])

_LANG_NAME = {"uz": "o'zbek", "ru": "русском", "en": "English"}


class ExplainRequest(BaseModel):
    question_text: str
    options: list[str] | None = None
    correct_answer: str
    user_answer: str | None = None
    lang: str = "uz"


@router.post("/tutor/explain")
def explain(
    data: ExplainRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
):
    lang = data.lang if data.lang in _LANG_NAME else "uz"
    lang_word = _LANG_NAME[lang]

    opts = ""
    if data.options:
        opts = "\nVariantlar:\n" + "\n".join(f"- {o}" for o in data.options)
    wrong = ""
    if data.user_answer and data.user_answer.strip() and data.user_answer.strip() != data.correct_answer.strip():
        wrong = f"\nO'quvchi tanlagan (noto'g'ri) javob: {data.user_answer}"

    prompt = (
        f"Sen sabrli, do'stona repetitorsan. Quyidagi test savolini {lang_word} tilida, "
        f"oddiy va tushunarli qilib tushuntir. Nega to'g'ri javob to'g'ri ekanini ayt; "
        f"agar o'quvchi noto'g'ri javob bergan bo'lsa, uning xatosini yumshoq tuzat. "
        f"3-5 qisqa jumla, formulalar/atamalarni sodda misol bilan. Faqat tushuntirishni yoz, "
        f"kirish so'zlarsiz.\n\n"
        f"Savol: {data.question_text}{opts}\n"
        f"To'g'ri javob: {data.correct_answer}{wrong}"
    )

    try:
        resp = gemini_generate(model="gemini-flash-latest", contents=prompt)
        text = (resp.text or "").strip()
    except Exception:
        raise HTTPException(status_code=502, detail="tutor_unavailable")

    if not text:
        raise HTTPException(status_code=502, detail="tutor_unavailable")
    return {"explanation": text}


class TutorMessage(BaseModel):
    role: str          # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    question_text: str
    options: list[str] | None = None
    correct_answer: str
    messages: list[TutorMessage]     # the conversation so far, oldest first
    lang: str = "uz"


@router.post("/tutor/chat")
def chat(data: ChatRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    """A follow-up turn with the tutor: the learner can keep asking about the same
    question and the tutor answers in context. Still on-demand (only when they type),
    so cost stays tied to real use."""
    lang = data.lang if data.lang in _LANG_NAME else "uz"
    lang_word = _LANG_NAME[lang]

    if not data.messages:
        raise HTTPException(status_code=400, detail="no message")
    # Keep the window short so the prompt stays cheap; the last several turns are enough.
    history = data.messages[-8:]
    opts = ("\nVariantlar: " + "; ".join(data.options)) if data.options else ""

    convo = "\n".join(
        f"{'Savol' if m.role == 'user' else 'Repetitor'}: {m.content}" for m in history
    )
    prompt = (
        f"Sen sabrli, do'stona repetitorsan va {lang_word} tilida javob berasan. Quyidagi "
        f"test savoli bo'yicha o'quvchi bilan suhbatlashyapsan. Uning oxirgi savoliga qisqa, "
        f"aniq va sodda javob ber (ko'pi bilan 4-5 jumla). Faqat shu mavzuda qol; boshqa "
        f"mavzuga o'tsa, muloyimlik bilan savolga qaytar.\n\n"
        f"Savol: {data.question_text}{opts}\n"
        f"To'g'ri javob: {data.correct_answer}\n\n"
        f"Suhbat:\n{convo}\n\nRepetitor:"
    )
    try:
        resp = gemini_generate(model="gemini-flash-latest", contents=prompt)
        text = (resp.text or "").strip()
    except Exception:
        raise HTTPException(status_code=502, detail="tutor_unavailable")
    if not text:
        raise HTTPException(status_code=502, detail="tutor_unavailable")
    return {"reply": text}


def _guess_audio_mime(upload: UploadFile) -> str:
    """Some upload clients send a generic/blank content type; fall back to the
    file extension the way /assistant/ask-voice does so Gemini accepts it."""
    mime = upload.content_type
    if mime and mime != "application/octet-stream":
        return mime
    name = (upload.filename or "").lower()
    if name.endswith(".wav"):
        return "audio/wav"
    if name.endswith(".mp3"):
        return "audio/mp3"
    if name.endswith((".m4a", ".mp4")):
        return "audio/mp4"
    if name.endswith(".ogg"):
        return "audio/ogg"
    return "audio/webm"


@router.post("/tutor/voice-check")
async def voice_check(
    question_text: str = Form(...),
    correct_answer: str = Form(...),
    lang: str = Form("uz"),
    audio: UploadFile = File(...),
    auth_user_id: int = Depends(get_authenticated_user_id),
):
    """Spoken-answer check for non-speaking subjects (history, biology, ...). The
    learner explains the answer out loud in Uzbek; Gemini transcribes it and judges
    whether they actually understand the concept — not just whether they hit the
    exact keyword. One multimodal call: transcription + evaluation together."""
    lang = lang if lang in _LANG_NAME else "uz"
    lang_word = _LANG_NAME[lang]

    audio_bytes = await audio.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="empty_audio")

    prompt = (
        f"Sen sabrli repetitorsan. O'quvchi quyidagi savolga OG'ZAKI javob berdi (biriktirilgan "
        f"audio). Avval uning gapini o'zbekcha transkripsiya qil, keyin javobi mazmunan to'g'ri "
        f"va tushunganini bahola — aynan bir xil so'z bo'lishi shart emas, ma'no muhim. "
        f"Qisqa, do'stona izoh yoz ({lang_word} tilida): to'g'ri joyini maqta, kam joyini yumshoq "
        f"to'ldir. FAQAT JSON qaytar, boshqa matnsiz:\n"
        f'{{\"understood\": true/false, \"transcript\": \"...\", \"feedback\": \"...\"}}\n\n'
        f"Savol: {question_text}\n"
        f"To'g'ri javob: {correct_answer}"
    )
    audio_part = types.Part.from_bytes(data=audio_bytes, mime_type=_guess_audio_mime(audio))

    try:
        resp = gemini_generate(model="gemini-flash-latest", contents=[prompt, audio_part])
        raw = (resp.text or "").strip()
    except Exception:
        raise HTTPException(status_code=502, detail="tutor_unavailable")
    if not raw:
        raise HTTPException(status_code=502, detail="tutor_unavailable")

    # Gemini usually returns clean JSON but may wrap it in ```json fences or prose.
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    try:
        data = json.loads(match.group(0) if match else raw)
        return {
            "understood": bool(data.get("understood")),
            "transcript": str(data.get("transcript", "")).strip(),
            "feedback": str(data.get("feedback", "")).strip(),
        }
    except (ValueError, AttributeError):
        # Parsing failed — still give the learner the model's words as feedback.
        return {"understood": False, "transcript": "", "feedback": raw}


def _guess_image_mime(upload: UploadFile) -> str:
    mime = upload.content_type
    if mime and mime != "application/octet-stream":
        return mime
    name = (upload.filename or "").lower()
    if name.endswith(".png"):
        return "image/png"
    if name.endswith(".webp"):
        return "image/webp"
    if name.endswith(".heic"):
        return "image/heic"
    return "image/jpeg"


@router.post("/tutor/photo-check")
async def photo_check(
    question_text: str = Form(""),
    lang: str = Form("uz"),
    image: UploadFile = File(...),
    auth_user_id: int = Depends(get_authenticated_user_id),
):
    """Read a photo of the learner's handwritten answer for ANY subject and give
    feedback. Unlike the math solver (which solves the problem), this reads what
    the learner actually wrote and evaluates it — right/wrong, what's missing,
    how to improve — so it works for history, biology, essays, and so on. One
    multimodal call does OCR + evaluation. The question is optional: with it, the
    answer is judged against it; without it, the writing is assessed on its own."""
    lang = lang if lang in _LANG_NAME else "uz"
    lang_word = _LANG_NAME[lang]

    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="empty_image")

    q = question_text.strip()
    context = f"\nSavol/topshiriq: {q}" if q else ""
    against = (
        "javob savolga to'g'ri va to'liq ekanini bahola"
        if q
        else "yozilgan javob mazmunan to'g'ri va aniq ekanini bahola"
    )
    prompt = (
        f"Sen sabrli repetitorsan. Rasmda o'quvchining QO'LDA yozgan javobi bor. Avval matnni "
        f"diqqat bilan o'qib transkripsiya qil (o'zbekcha), keyin {against}. Qisqa, do'stona izoh "
        f"yoz ({lang_word} tilida): to'g'ri joyini maqta, xato yoki kam joyini yumshoq to'g'irlab "
        f"ayt. FAQAT JSON qaytar, boshqa matnsiz:\n"
        f'{{\"correct\": true/false, \"score\": 0-100, \"transcript\": \"...\", \"feedback\": \"...\"}}'
        f"{context}"
    )
    image_part = types.Part.from_bytes(data=image_bytes, mime_type=_guess_image_mime(image))

    try:
        resp = gemini_generate(
            model="gemini-flash-latest",
            contents=[prompt, image_part],
            config={"response_mime_type": "application/json"},
        )
        raw = (resp.text or "").strip()
    except Exception:
        raise HTTPException(status_code=502, detail="tutor_unavailable")
    if not raw:
        raise HTTPException(status_code=502, detail="tutor_unavailable")

    match = re.search(r"\{.*\}", raw, re.DOTALL)
    try:
        data = json.loads(match.group(0) if match else raw)
        score = data.get("score")
        return {
            "correct": bool(data.get("correct")),
            "score": int(score) if isinstance(score, (int, float)) else None,
            "transcript": str(data.get("transcript", "")).strip(),
            "feedback": str(data.get("feedback", "")).strip(),
        }
    except (ValueError, AttributeError):
        return {"correct": False, "score": None, "transcript": "", "feedback": raw}
