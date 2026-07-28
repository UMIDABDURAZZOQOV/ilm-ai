"""
routers/college.py -- College Application helpers. The essay coach reviews an
admissions essay (personal statement / supplemental) and gives structured,
constructive feedback — self-contained, no dependency on the college browser.
"""
from __future__ import annotations

import json
import re

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.auth_deps import ensure_own_user, get_authenticated_user_id
from services.subscriptions import can_use_assistant, record_assistant_use
from services.gemini import generate_content as gemini_generate

router = APIRouter(prefix="/college", tags=["college"])


def _parse_json(text: str) -> dict:
    cleaned = (text or "").strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned[:4].lower() == "json":
            cleaned = cleaned[4:]
    m = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if m:
        cleaned = m.group(0)
    return json.loads(cleaned)


class EssayRequest(BaseModel):
    user_id: int
    essay: str
    prompt: str = ""                 # the essay prompt, if any
    essay_type: str = "personal_statement"   # or "supplemental"
    language: str = "en"


@router.post("/essay-review")
def essay_review(data: EssayRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    """Structured admissions-essay feedback: an overall read, concrete strengths and
    improvements, and a couple of line-level suggestions — like a thoughtful counselor."""
    ensure_own_user(data.user_id, auth_user_id)
    ok, msg = can_use_assistant(data.user_id)
    if not ok:
        raise HTTPException(status_code=403, detail=msg)

    essay = (data.essay or "").strip()
    if len(essay) < 40:
        raise HTTPException(status_code=400, detail="essay_too_short")

    kind = "supplemental essay" if data.essay_type == "supplemental" else "personal statement"
    prompt_ctx = f"\nEssay prompt: {data.prompt}" if data.prompt.strip() else ""
    prompt = (
        f"You are an experienced US college admissions counselor reviewing a student's {kind}. "
        f"Give warm but honest, specific feedback (write the text fields in {data.language}). "
        f"Judge authenticity of voice, specificity/'show don't tell', structure, and how memorable it is. "
        f"Return ONLY this JSON, no fences:\n"
        f'{{\"overall\": \"2-4 sentence overall read\", \"rating\": 1-10, '
        f'\"strengths\": [\"...\"], \"improvements\": [\"concrete, actionable suggestion\"], '
        f'\"line_edits\": [{{\"before\": \"a phrase from the essay\", \"after\": \"a stronger rewrite\"}}]}}\n\n'
        f"{prompt_ctx}\nESSAY:\n{essay}"
    )
    try:
        resp = gemini_generate(
            model="gemini-flash-latest",
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )
        parsed = _parse_json(resp.text)
    except Exception:
        raise HTTPException(status_code=502, detail="review_failed")

    record_assistant_use(data.user_id)
    rating = parsed.get("rating")
    return {
        "overall": str(parsed.get("overall", "")).strip(),
        "rating": int(rating) if isinstance(rating, (int, float)) else None,
        "strengths": [s for s in parsed.get("strengths", []) if isinstance(s, str)],
        "improvements": [s for s in parsed.get("improvements", []) if isinstance(s, str)],
        "line_edits": [
            {"before": str(e.get("before", "")), "after": str(e.get("after", ""))}
            for e in parsed.get("line_edits", []) if isinstance(e, dict) and e.get("before") and e.get("after")
        ],
    }
