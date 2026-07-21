from fastapi import APIRouter, Depends, HTTPException
from services.auth_deps import verify_user_access, ensure_own_user, get_authenticated_user_id
from pydantic import BaseModel

from services.quiz_engine import check_answer as evaluate_answer, generate_quiz as build_quiz
from services.quiz_history import add_session, load_sessions
from services.subscriptions import can_take_quiz, record_quiz_session

router = APIRouter(prefix="/quiz", tags=["quiz"])


class QuizRequest(BaseModel):
    user_id: int
    difficulty: str = "medium"
    num_questions: int = 5
    language: str = "en"
    topic: str | None = None


class AnswerRequest(BaseModel):
    user_id: int
    question: str
    user_answer: str
    correct_answer: str
    context: str


class QuizResultItem(BaseModel):
    question: str
    user_answer: str
    correct_answer: str
    is_correct: bool
    topic: str = "general"
    explanation: str = ""


class CompleteQuizRequest(BaseModel):
    user_id: int
    difficulty: str = "medium"
    score: int
    total: int
    results: list[QuizResultItem]


class FlashcardsRequest(BaseModel):
    user_id: int
    language: str = "en"


# Difficulty mapping: frontend sends easy/medium/hard, backend maps to prompt labels
DIFFICULTY_MAP = {
    "easy": "gentle review",
    "medium": "solid understanding",
    "hard": "expert challenge",
    "gentle review": "gentle review",
    "solid understanding": "solid understanding",
    "expert challenge": "expert challenge",
}


@router.post("/generate")
def generate_quiz(data: QuizRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    ensure_own_user(data.user_id, auth_user_id)
    ok, msg = can_take_quiz(data.user_id)
    if not ok:
        raise HTTPException(status_code=403, detail=msg)

    # Map frontend difficulty to backend difficulty label
    difficulty = DIFFICULTY_MAP.get(data.difficulty, "solid understanding")

    result = build_quiz(data.user_id, data.num_questions, difficulty, language=data.language, topic=data.topic)
    if "error" in result:
        return result
    if "_context" in result:
        del result["_context"]

    # Safety: Ensure all questions have options (MCQ format)
    if "questions" in result:
        for q in result["questions"]:
            if not q.get("options") or len(q.get("options", [])) == 0:
                # Convert non-MCQ to MCQ with placeholder options
                q["type"] = "mcq"
                q["options"] = [
                    f"A) {q.get('correct_answer', 'Option A')}",
                    "B) Not available",
                    "C) Not available",
                    "D) Not available",
                ]
                q["correct_answer"] = q["options"][0]

    record_quiz_session(data.user_id)
    return result


@router.post("/complete")
def complete_quiz(data: CompleteQuizRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    ensure_own_user(data.user_id, auth_user_id)
    session = add_session(
        data.user_id,
        data.score,
        data.total,
        data.difficulty,
        [r.model_dump() for r in data.results],
    )
    return {"message": "Quiz session saved", "session_id": session["id"]}


@router.get("/stats/{user_id}")
def get_quiz_stats(user_id: int = Depends(verify_user_access)):
    """Return quiz session history and aggregated stats for the dashboard."""
    sessions = load_sessions(user_id)
    if not sessions:
        return {
            "sessions_completed": 0,
            "total_questions": 0,
            "correct_answers": 0,
            "average_score": 0,
            "topics_covered": [],
            "score_trend": [],
            "sessions": [],
        }

    total_questions = 0
    correct_answers = 0
    topics_set = set()
    score_trend = []

    for s in sessions:
        total_questions += s.get("total", 0)
        correct_answers += s.get("score", 0)
        score_pct = round(s.get("score", 0) / max(s.get("total", 1), 1) * 100)
        score_trend.append({
            "session_id": s.get("id"),
            "date": s.get("completed_at", ""),
            "score_pct": score_pct,
        })
        for r in s.get("results", []):
            topic = r.get("topic", "general")
            if topic:
                topics_set.add(topic)

    avg_score = round(correct_answers / max(total_questions, 1) * 100)

    return {
        "sessions_completed": len(sessions),
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "average_score": avg_score,
        "topics_covered": sorted(list(topics_set)),
        "score_trend": score_trend[-10:],  # last 10 sessions
        "sessions": sessions[-10:],  # last 10 sessions
    }


@router.post("/check")
def check_answer(data: AnswerRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    ensure_own_user(data.user_id, auth_user_id)
    return evaluate_answer(
        data.question,
        data.user_answer,
        data.correct_answer,
        data.context,
        user_id=data.user_id,
    )


@router.post("/flashcards")
def generate_flashcards_post(
    data: FlashcardsRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
):
    ensure_own_user(data.user_id, auth_user_id)
    """Stretch feature: Generate study flashcards from materials (POST)."""
    return _generate_flashcards(data.user_id, data.language)


@router.get("/flashcards/{user_id}")
def generate_flashcards(user_id: int = Depends(verify_user_access)):
    """Stretch feature: Generate study flashcards from materials (GET)."""
    return _generate_flashcards(user_id, "en")


from google.genai.errors import ClientError

def _generate_flashcards(user_id: int, language: str = "en"):
    from services.quiz_engine import load_vectors
    import random

    vectors = load_vectors(user_id)
    if not vectors:
        return {"error": "No materials found"}

    # quiz_engine no longer exposes a raw `client` — go through services.gemini,
    # which rotates GEMINI_API_KEYS and applies a request timeout.
    from services.quiz_engine import _parse_json_response
    from services.gemini import generate_content as gemini_generate

    chunks = [v["text"] for v in vectors]
    selected = random.sample(chunks, min(3, len(chunks)))
    context = "\n\n---\n\n".join(selected)

    prompt = f"""Generate 5 study flashcards (front/back) from this context:
{context}

Return JSON:
{{
  "flashcards": [
    {{"front": "Question/Term", "back": "Answer/Definition"}}
  ]
}}
Return ONLY JSON."""

    import time
    from services.monitoring import log_llm_call
    start_time = time.time()
    try:
        response = gemini_generate(
            model="gemini-flash-latest",
            contents=prompt
        )
    except ClientError as e:
        if getattr(e, "code", None) == 429:
            raise HTTPException(status_code=429, detail="Gemini API rate limit exceeded. Please wait a moment.")
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")

    latency_ms = int((time.time() - start_time) * 1000)

    log_llm_call(
        user_id=user_id,
        prompt=prompt,
        response_text=response.text,
        latency_ms=latency_ms,
        model="gemini-flash-latest"
    )

    try:
        return _parse_json_response(response.text)
    except Exception:
        return {"error": "Failed to generate flashcards"}

