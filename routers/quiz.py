from fastapi import APIRouter
from pydantic import BaseModel
import os
import json
import numpy as np
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

router = APIRouter(prefix="/quiz", tags=["quiz"])

VECTOR_DIR = "vectors"

def load_vectors(user_id: int):
    path = f"{VECTOR_DIR}/user_{user_id}.json"
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

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
    vectors = load_vectors(data.user_id)

    if not vectors:
        return {"error": "No materials uploaded yet"}

    import random
    chunks = [v["text"] for v in vectors]
    selected = random.sample(chunks, min(5, len(chunks)))
    context = "\n\n---\n\n".join(selected)

    difficulty_prompt = {
        "easy": "Generate simple recall questions",
        "medium": "Generate questions requiring understanding",
        "hard": "Generate questions requiring deep analysis"
    }.get(data.difficulty, "Generate questions requiring understanding")

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""You are a quiz generator. Based on the context below, generate {data.num_questions} quiz questions.

Difficulty: {difficulty_prompt}

CONTEXT:
{context}

Generate questions in this exact JSON format:
{{
  "questions": [
    {{
      "question": "Question text here?",
      "type": "mcq",
      "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
      "correct_answer": "A) option1",
      "explanation": "Brief explanation"
    }}
  ]
}}

Return ONLY the JSON, no other text."""
    )

    try:
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        quiz_data = json.loads(text)
        return quiz_data
    except:
        return {"error": "Could not generate quiz", "raw": response.text}

@router.post("/check")
def check_answer(data: AnswerRequest):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""You are a quiz evaluator.

Question: {data.question}
Correct answer: {data.correct_answer}
User's answer: {data.user_answer}
Context: {data.context}

Evaluate if the user's answer is correct. Respond in JSON:
{{
  "is_correct": true or false,
  "score": 1 or 0,
  "feedback": "Brief feedback explaining what was right or wrong",
  "explanation": "Full explanation of the correct answer"
}}

Return ONLY the JSON."""
    )

    try:
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text)
    except:
        return {"is_correct": False, "feedback": "Could not evaluate answer"}