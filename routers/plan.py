from fastapi import APIRouter, Depends, HTTPException
from services.auth_deps import verify_user_access, ensure_own_user, get_authenticated_user_id
from pydantic import BaseModel
import os
import json
from google import genai
from google.genai.errors import ClientError
from dotenv import load_dotenv
from datetime import datetime
from typing import Optional

load_dotenv()

from services.gemini import generate_content as gemini_generate, embed_content as gemini_embed

router = APIRouter(prefix="/plan", tags=["plan"])

VECTOR_DIR = "vectors"
PLANS_DIR = "data/plans"
os.makedirs(PLANS_DIR, exist_ok=True)

from services.users import USE_DB
from services.db import SessionLocal
from services.models import VectorEntry, LearningPlan

def load_vectors(user_id: int):
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

def save_plan_to_file(user_id: int, plan: dict):
    if USE_DB:
        db = SessionLocal()
        try:
            row = db.query(LearningPlan).filter(LearningPlan.user_id == user_id).first()
            if row:
                row.plan = plan
            else:
                db.add(LearningPlan(user_id=user_id, plan=plan))
            db.commit()
        finally:
            db.close()
        return

    path = f"{PLANS_DIR}/user_{user_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

def load_plan_from_file(user_id: int):
    if USE_DB:
        db = SessionLocal()
        try:
            row = db.query(LearningPlan).filter(LearningPlan.user_id == user_id).first()
            return row.plan if row else None
        finally:
            db.close()

    path = f"{PLANS_DIR}/user_{user_id}.json"
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

class PlanGenerateRequest(BaseModel):
    user_id: int
    daily_hours: float = 1.0
    goal: Optional[str] = None
    target_date: Optional[str] = None

from services.subscriptions import get_subscription_status
from services.users import find_user_by_id, update_user_profile
from services.gap_detection import generate_gaps_report

@router.get("/{user_id}")
def get_plan(user_id: int = Depends(verify_user_access)):
    plan = load_plan_from_file(user_id)
    if not plan:
        raise HTTPException(status_code=404, detail="No plan generated yet")
    return plan


@router.get("/{user_id}/today")
def get_today_plan(user_id: int = Depends(verify_user_access)):
    plan = load_plan_from_file(user_id)
    if not plan or not plan.get("generated_at"):
        return {"status": "no_plan", "day": None, "days_elapsed": 0, "days_total": 0}

    # Flatten by position, not by the LLM's "day" field — that field can repeat
    # or reset per week, but list position is always a reliable sequential index.
    flattened = [
        day
        for week in plan.get("weekly_breakdown", [])
        for day in week.get("days", [])
    ]
    days_total = len(flattened)
    if days_total == 0:
        return {"status": "no_plan", "day": None, "days_elapsed": 0, "days_total": 0}

    try:
        generated_date = datetime.fromisoformat(plan["generated_at"]).date()
    except (ValueError, TypeError):
        return {"status": "no_plan", "day": None, "days_elapsed": 0, "days_total": 0}

    days_elapsed = (datetime.now().date() - generated_date).days

    if days_elapsed >= days_total:
        return {"status": "finished", "day": None, "days_elapsed": days_elapsed, "days_total": days_total}
    if days_elapsed < 0:
        days_elapsed = 0

    return {
        "status": "today",
        "day": flattened[days_elapsed],
        "days_elapsed": days_elapsed,
        "days_total": days_total,
    }

@router.post("/generate")
def generate_plan(data: PlanGenerateRequest, auth_user_id: int = Depends(get_authenticated_user_id)):
    ensure_own_user(data.user_id, auth_user_id)
    user = find_user_by_id(data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    goal = data.goal or user.get("learning_goal")
    target_date = data.target_date or user.get("target_date")

    if not goal or not target_date:
        raise HTTPException(status_code=400, detail="Please set your learning goal and target date in your profile first.")

    # Persist goal and target_date to user profile
    update_user_profile(data.user_id, learning_goal=goal, target_date=target_date)

    status = get_subscription_status(data.user_id)
    is_premium = status.get("is_premium", False)

    vectors = load_vectors(data.user_id)
    if not vectors:
        raise HTTPException(status_code=400, detail="No materials uploaded yet. Upload a PDF first.")

    # Get Gaps Report to inform the plan
    gaps_report = generate_gaps_report(data.user_id, is_premium)
    gaps_text = json.dumps(gaps_report.get("gaps", []), ensure_ascii=False) if gaps_report.get("ready") else "No gaps detected yet."

    filenames = list(set(v["filename"] for v in vectors))
    topics = list(set(v.get("topic", "General") for v in vectors))
    
    today = datetime.now().date()
    try:
        target = datetime.strptime(target_date, "%Y-%m-%d").date()
        days_available = (target - today).days
    except (ValueError, TypeError):
        days_available = 30

    if days_available <= 0:
        days_available = 7 # fallback

    plan_type = "full detailed" if is_premium else "basic summary"
    
    prompt = f"""You are a learning plan generator for Ilm AI.

Create a {plan_type} day-by-day learning plan based on:
- Goal: {goal}
- Target date: {target_date}
- Days available: {days_available} days
- Daily study time: {data.daily_hours} hours
- Uploaded materials: {', '.join(filenames)}
- Topics identified: {', '.join(topics)}
- Identified Gaps: {gaps_text}

{"Premium users get a full day-by-day breakdown." if is_premium else "Free users get only a weekly overview."}

Generate a practical learning plan in this JSON format:
{{
  "goal": "{goal}",
  "target_date": "{target_date}",
  "days_available": {days_available},
  "daily_hours": {data.daily_hours},
  "summary": "Brief overview of the plan focusing on bridging the gaps",
  "weekly_breakdown": [
    {{
      "week": 1,
      "focus": "Main topic for this week",
      "days": [
        {{
          "day": 1,
          "topic": "Topic to study",
          "material": "Which uploaded file or topic to use",
          "tasks": ["Task 1", "Task 2"],
          "duration_minutes": 60
        }}
      ]
    }}
  ],
  "tips": ["Study tip 1", "Study tip 2"]
}}

Return ONLY the JSON, no other text. Keep the plan realistic and specific."""

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
            raise HTTPException(status_code=429, detail="Gemini API rate limit exceeded (429). Please wait a moment and try again.")
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")
    
    latency_ms = int((time.time() - start_time) * 1000)

    log_llm_call(
        user_id=data.user_id,
        prompt=prompt,
        response_text=response.text,
        latency_ms=latency_ms,
        model="gemini-flash-latest"
    )

    try:
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        
        plan_data = json.loads(text)
        plan_data["generated_at"] = datetime.now().isoformat()
        save_plan_to_file(data.user_id, plan_data)
        return plan_data
    except Exception:
        return {"error": "Could not generate plan", "raw": response.text}
