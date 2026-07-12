import json
import os
import random
import time

from google import genai
from google.genai.errors import ClientError
from dotenv import load_dotenv
from services.monitoring import log_llm_call

load_dotenv()

VECTOR_DIR = "vectors"
from services.gemini import generate_content as gemini_generate


from services.users import USE_DB
from services.db import SessionLocal
from services.models import VectorEntry

def load_vectors(user_id: int) -> list[dict]:
    if USE_DB:
        db = SessionLocal()
        try:
            entries = db.query(VectorEntry).filter(VectorEntry.user_id == user_id).all()
            return [
                {
                    "id": e.chunk_id,
                    "filename": e.filename,
                    "topic": e.topic,
                    "text": e.text,
                    "embedding": e.embedding
                }
                for e in entries
            ]
        finally:
            db.close()

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
    difficulty: str = "solid understanding",
    language: str = "en",
    topic: str | None = None,
) -> dict:
    vectors = load_vectors(user_id)
    if not vectors:
        return {
            "error": "No materials uploaded yet. Upload a PDF on the website first.",
        }

    if topic:
        matched = [v for v in vectors if v.get("topic", "").strip().lower() == topic.strip().lower()]
        if matched:
            vectors = matched
        # else: topic no longer matches any uploaded material (e.g. it was removed) —
        # fall back to the full set rather than failing the quiz outright.

    chunks = [v["text"] for v in vectors]
    selected = random.sample(chunks, min(5, len(chunks)))
    context = "\n\n---\n\n".join(selected)

    difficulty_prompt = {
        "gentle review": "Generate simple recall questions (easy)",
        "solid understanding": "Generate questions requiring understanding and application (medium)",
        "expert challenge": "Generate questions requiring deep analysis and critical thinking (hard)",
    }.get(difficulty, "Generate questions requiring understanding")

    lang_instruction = ""
    if language and language != "en":
        lang_names = {"uz": "Uzbek", "ru": "Russian"}
        lang_name = lang_names.get(language, language)
        lang_instruction = f"\nIMPORTANT: Generate all questions and content in {lang_name} language."

    prompt = f"""You are a quiz generator for Ilm AI. Based on the context below, generate exactly {num_questions} quiz questions.

Difficulty: {difficulty_prompt}{lang_instruction}

IMPORTANT: Generate ALL questions as Multiple Choice (MCQ) with exactly 4 options each.

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
      "explanation": "Brief explanation",
      "topic": "topic name"
    }}
  ],
  "context": "short summary of source material used"
}}

Rules:
- Generate EXACTLY {num_questions} questions
- Every question MUST have exactly 4 options labeled A), B), C), D)
- The correct_answer MUST exactly match one of the options
- Include a topic field for each question

Return ONLY the JSON, no other text."""

    start_time = time.time()
    try:
        response = gemini_generate(
            model="gemini-flash-latest",
            contents=prompt,
        )
    except ClientError as e:
        if getattr(e, "code", None) == 429:
            return {"error": "Gemini API rate limit exceeded. Please try again in a moment."}
        return {"error": f"Gemini API Error: {str(e)}"}
    
    latency_ms = int((time.time() - start_time) * 1000)

    log_llm_call(
        user_id=user_id,
        prompt=prompt,
        response_text=response.text,
        latency_ms=latency_ms,
        model="gemini-flash-latest"
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
    user_id: int = None,
) -> dict:
    prompt = f"""You are a quiz evaluator for Ilm AI.

Question: {question}
Correct answer: {correct_answer}
User's answer: {user_answer}
Context: {context}

Evaluate if the user's answer is correct. Be encouraging and Socratic.
Respond in JSON:
{{
  "is_correct": true or false,
  "score": 1 or 0,
  "feedback": "Brief feedback in Uzbek if user writes in Uzbek",
  "explanation": "Full explanation"
}}

Return ONLY the JSON."""

    start_time = time.time()
    try:
        response = gemini_generate(
            model="gemini-flash-latest",
            contents=prompt,
        )
    except ClientError as e:
        if getattr(e, "code", None) == 429:
            return {"error": "Gemini API rate limit exceeded. Please try again in a moment."}
        return {"error": f"Gemini API Error: {str(e)}"}
    
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
    except (json.JSONDecodeError, IndexError, AttributeError):
        return {
            "is_correct": False,
            "feedback": "Could not evaluate answer",
            "explanation": "",
        }

