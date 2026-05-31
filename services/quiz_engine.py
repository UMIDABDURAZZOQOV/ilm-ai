import json
import os
import random

from google import genai
from dotenv import load_dotenv

load_dotenv()

VECTOR_DIR = "vectors"
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def load_vectors(user_id: int) -> list[dict]:
    path = f"{VECTOR_DIR}/user_{user_id}.json"
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _parse_json_response(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    return json.loads(cleaned)


def generate_quiz(
    user_id: int,
    num_questions: int = 5,
    difficulty: str = "medium",
) -> dict:
    vectors = load_vectors(user_id)
    if not vectors:
        return {
            "error": "No materials uploaded yet. Upload a PDF on the website first.",
        }

    chunks = [v["text"] for v in vectors]
    selected = random.sample(chunks, min(5, len(chunks)))
    context = "\n\n---\n\n".join(selected)

    difficulty_prompt = {
        "easy": "Generate simple recall questions",
        "medium": "Generate questions requiring understanding",
        "hard": "Generate questions requiring deep analysis",
    }.get(difficulty, "Generate questions requiring understanding")

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""You are a quiz generator. Based on the context below, generate {num_questions} quiz questions.

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
  ],
  "context": "short summary of source material used"
}}

Return ONLY the JSON, no other text.""",
    )

    try:
        quiz_data = _parse_json_response(response.text)
        quiz_data["_context"] = context
        return quiz_data
    except (json.JSONDecodeError, IndexError, AttributeError):
        return {"error": "Could not generate quiz", "raw": getattr(response, "text", "")}


def check_answer(
    question: str,
    user_answer: str,
    correct_answer: str,
    context: str,
) -> dict:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""You are a quiz evaluator.

Question: {question}
Correct answer: {correct_answer}
User's answer: {user_answer}
Context: {context}

Evaluate if the user's answer is correct. Respond in JSON:
{{
  "is_correct": true or false,
  "score": 1 or 0,
  "feedback": "Brief feedback in Uzbek if user writes in Uzbek",
  "explanation": "Full explanation"
}}

Return ONLY the JSON.""",
    )

    try:
        return _parse_json_response(response.text)
    except (json.JSONDecodeError, IndexError, AttributeError):
        return {
            "is_correct": False,
            "feedback": "Could not evaluate answer",
            "explanation": "",
        }
