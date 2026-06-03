from fastapi import APIRouter
from pydantic import BaseModel
import os
import json
from google import genai
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

router = APIRouter(prefix="/plan", tags=["plan"])

VECTOR_DIR = "vectors"

def load_vectors(user_id: int):
    path = f"{VECTOR_DIR}/user_{user_id}.json"
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

class PlanRequest(BaseModel):
    user_id: int
    goal: str
    target_date: str  
    daily_hours: float = 1.0

@router.post("/generate")
def generate_plan(data: PlanRequest):
    vectors = load_vectors(data.user_id)

    if not vectors:
        return {"error": "No materials uploaded yet. Upload a PDF first."}


    filenames = list(set(v["filename"] for v in vectors))
    total_chunks = len(vectors)

 
    today = datetime.now().date()

    try:
        target = datetime.strptime(data.target_date, "%Y-%m-%d").date()
        days_available = (target - today).days
    except (ValueError, TypeError):
        days_available = 30

    if days_available <= 0:
        return {"error": "Target date must be in the future"}

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""You are a learning plan generator for Ilm AI.

Create a realistic day-by-day learning plan based on:
- Goal: {data.goal}
- Target date: {data.target_date}
- Days available: {days_available} days
- Daily study time: {data.daily_hours} hours
- Uploaded materials: {', '.join(filenames)}
- Total content chunks: {total_chunks}

Generate a practical learning plan in this JSON format:
{{
  "goal": "{data.goal}",
  "target_date": "{data.target_date}",
  "days_available": {days_available},
  "daily_hours": {data.daily_hours},
  "summary": "Brief overview of the plan",
  "weekly_breakdown": [
    {{
      "week": 1,
      "focus": "Main topic for this week",
      "days": [
        {{
          "day": 1,
          "date": "2026-05-29",
          "topic": "Topic to study",
          "material": "Which uploaded file to use",
          "tasks": ["Task 1", "Task 2"],
          "duration_minutes": 60
        }}
      ]
    }}
  ],
  "tips": ["Study tip 1", "Study tip 2"]
}}

Return ONLY the JSON, no other text. Keep the plan realistic and specific."""
    )

    try:
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text)
    except Exception:
        return {"error": "Could not generate plan", "raw": response.text}