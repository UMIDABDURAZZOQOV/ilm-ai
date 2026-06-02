from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.quiz_engine import check_answer as evaluate_answer, generate_quiz as build_quiz
from services.quiz_history import add_session
from services.subscriptions import can_take_quiz, record_quiz_session

router = APIRouter(prefix="/quiz", tags=["quiz"])


class QuizRequest(BaseModel):
    user_id: int
    difficulty: str = "medium"
    num_questions: int = 5


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


@router.post("/generate")
def generate_quiz(data: QuizRequest):
    ok, msg = can_take_quiz(data.user_id)
    if not ok:
        raise HTTPException(status_code=403, detail=msg)

    result = build_quiz(data.user_id, data.num_questions, data.difficulty)
    if "error" in result:
        return result
    if "_context" in result:
        del result["_context"]
    record_quiz_session(data.user_id)
    return result


@router.post("/complete")
def complete_quiz(data: CompleteQuizRequest):
    session = add_session(
        data.user_id,
        data.score,
        data.total,
        data.difficulty,
        [r.model_dump() for r in data.results],
    )
    return {"message": "Quiz session saved", "session_id": session["id"]}


@router.post("/check")
def check_answer(data: AnswerRequest):
    return evaluate_answer(
        data.question,
        data.user_answer,
        data.correct_answer,
        data.context,
    )