"""
routers/tutor.py -- in-lesson AI tutor (AI repetitor). On demand only: when a
learner gets a question wrong and taps "Tushuntirib ber", the client calls this
to get a short, plain-language explanation from Gemini. Not called per question,
so API usage stays low.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

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
