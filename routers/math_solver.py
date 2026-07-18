import json
import time

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from google.genai import types
from google.genai.errors import ClientError

from services.auth_deps import ensure_own_user, get_authenticated_user_id
from services.subscriptions import can_use_assistant, record_assistant_use
from services.monitoring import log_llm_call
from services.gemini import generate_content as gemini_generate

router = APIRouter(prefix="/math", tags=["math-solver"])

SOLVER_INSTRUCTION = """You are a Photomath-style math tutor. You are given either a photo of a
handwritten/printed math problem or typed problem text. Recognize the problem, solve it fully, and
explain it the way a patient teacher would — clear enough that a student who is stuck can follow
every step and actually understand it, not just copy an answer.

Cover: arithmetic, fractions/decimals, algebra (linear/quadratic equations, systems, inequalities,
polynomials), geometry, trigonometry, calculus (limits/derivatives/integrals), statistics/probability,
and word problems. If the image is unreadable or not a math problem, say so in "recognized_problem"
and leave "steps" empty.

Respond in the following language: {language}.

Return ONLY this exact JSON shape, no markdown fences, no extra text:
{{
  "recognized_problem": "the problem exactly as written/typed, in standard math notation",
  "topic": "short topic label, e.g. \\"Algebra - Linear Equations\\"",
  "steps": [
    {{"expression": "the math at this step (e.g. 2x = 12)", "explanation": "one clear sentence on what was done and why"}}
  ],
  "final_answer": "the final answer, concisely",
  "graph": {{"type": "linear", "a": 2, "b": 5}}
}}

The "graph" field is OPTIONAL and only for a single-variable function of x that can be sensibly
plotted on a simple x/y plane:
- Linear (y = a*x + b): {{"type": "linear", "a": <number>, "b": <number>}}
- Quadratic (y = a*x^2 + b*x + c): {{"type": "quadratic", "a": <number>, "b": <number>, "c": <number>}}
Omit the "graph" key entirely if the problem isn't a simple plottable function of x."""


def _call_gemini_json(contents, user_id: int) -> dict:
    start_time = time.time()
    try:
        response = gemini_generate(
            model="gemini-flash-latest",
            contents=contents,
            config={"response_mime_type": "application/json"},
        )
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

    try:
        data = json.loads(response.text)
    except (json.JSONDecodeError, TypeError):
        raise HTTPException(status_code=502, detail="Could not parse the solution — please try again.")

    data.setdefault("steps", [])
    data.setdefault("recognized_problem", "")
    data.setdefault("final_answer", "")
    data.setdefault("topic", "")
    return data


@router.post("/solve-image")
async def solve_image(
    user_id: int = Form(...),
    language: str = Form("en"),
    image: UploadFile = File(...),
    auth_user_id: int = Depends(get_authenticated_user_id),
):
    ensure_own_user(user_id, auth_user_id)
    ok, msg = can_use_assistant(user_id)
    if not ok:
        raise HTTPException(status_code=403, detail=msg)

    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty image file")

    mime_type = image.content_type
    if not mime_type or mime_type == "application/octet-stream":
        filename = (image.filename or "").lower()
        if filename.endswith(".png"):
            mime_type = "image/png"
        elif filename.endswith(".webp"):
            mime_type = "image/webp"
        else:
            mime_type = "image/jpeg"

    instruction = SOLVER_INSTRUCTION.format(language=language or "en")
    image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)

    data = _call_gemini_json([instruction, image_part], user_id)
    record_assistant_use(user_id)
    return data


class SolveTextRequest(BaseModel):
    user_id: int
    problem: str
    language: str = "en"


@router.post("/solve-text")
def solve_text(data: SolveTextRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    ensure_own_user(data.user_id, auth_user_id)
    ok, msg = can_use_assistant(data.user_id)
    if not ok:
        raise HTTPException(status_code=403, detail=msg)

    instruction = SOLVER_INSTRUCTION.format(language=data.language or "en")
    prompt = f"{instruction}\n\nPROBLEM (typed by the student):\n{data.problem}"

    result = _call_gemini_json(prompt, data.user_id)
    record_assistant_use(data.user_id)
    return result
