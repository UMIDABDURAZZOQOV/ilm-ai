from fastapi import APIRouter
from pydantic import BaseModel

from services.quiz_engine import check_answer as evaluate_answer, generate_quiz as build_quiz

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


@router.post("/generate")
def generate_quiz(data: QuizRequest):
    result = build_quiz(data.user_id, data.num_questions, data.difficulty)
    if "_context" in result:
        del result["_context"]
    return result


@router.post("/check")
def check_answer(data: AnswerRequest):
    return evaluate_answer(
        data.question,
        data.user_answer,
        data.correct_answer,
        data.context,
    )