"""
sat_plan.py — SAT/IELTS-specific study plan generator.

Builds a richer prompt than the generic plan service by incorporating
per-domain weakness data from completed SAT/IELTS sessions.
"""
from __future__ import annotations

import json
import os
import time
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from services.sat_session_engine import compute_domain_accuracy
from services.models import SatIeltsSession


def generate_sat_plan(
    db: Session,
    user_id: int,
    exam_type: str,
    target_date_str: str,
    target_score: Optional[float],
    daily_hours: float,
    is_premium: bool,
) -> dict:
    """Generate a SAT/IELTS study plan using Gemini.

    1. Loads completed sessions to extract weak-domain data.
    2. Builds a SAT/IELTS-specific prompt.
    3. Calls Gemini 2.5 Flash.
    4. Returns the parsed plan JSON (same schema as the existing /plan endpoint).
    """
    from google import genai
    from google.genai.errors import ClientError
    from dotenv import load_dotenv
    from services.monitoring import log_llm_call

    load_dotenv()
    from services.gemini import generate_content as gemini_generate

    # --- Gather session data ---
    sessions = (
        db.query(SatIeltsSession)
        .filter(
            SatIeltsSession.user_id == user_id,
            SatIeltsSession.exam_type == exam_type,
            SatIeltsSession.status == "completed",
        )
        .order_by(SatIeltsSession.completed_at.desc())
        .limit(10)
        .all()
    )

    domain_acc = compute_domain_accuracy(sessions) if sessions else {}
    weak_domains = [d for d, acc in domain_acc.items() if acc < 0.70]
    strong_domains = [d for d, acc in domain_acc.items() if acc >= 0.70]

    # --- Gather analysis results ---
    analysis_texts: list[str] = []
    for s in sessions[:5]:
        if s.analysis_result and s.analysis_result.get("weak_areas"):
            analysis_texts.extend(s.analysis_result["weak_areas"])
    ai_weak_areas = list(set(analysis_texts))

    # --- Compute days available ---
    today = datetime.now().date()
    try:
        target_dt = datetime.strptime(target_date_str, "%Y-%m-%d").date()
        days_available = (target_dt - today).days
    except (ValueError, TypeError):
        days_available = 60
    if days_available <= 0:
        days_available = 14

    # --- Target score string ---
    if target_score is not None:
        score_str = str(int(target_score)) if exam_type == "SAT" else str(target_score)
    else:
        score_str = "improve overall"

    # --- Full-test cadence for premium ---
    full_test_note = ""
    if is_premium:
        full_test_note = (
            "\nFor premium users: schedule one full-length practice test every 7 days "
            "to simulate real exam conditions."
        )

    plan_type = "detailed day-by-day" if is_premium else "weekly overview"

    domain_accuracy_json = json.dumps(domain_acc, ensure_ascii=False)
    weak_json = json.dumps(weak_domains, ensure_ascii=False)
    ai_weak_json = json.dumps(ai_weak_areas, ensure_ascii=False)
    strong_json = json.dumps(strong_domains, ensure_ascii=False)

    prompt = f"""You are an expert {exam_type} tutor creating a personalised study plan.

Student profile:
- Target exam: {exam_type}
- Target score/band: {score_str}
- Target date: {target_date_str}
- Days available: {days_available}
- Daily study hours: {daily_hours}
- Domain accuracy: {domain_accuracy_json}
- Weak domains (< 70%): {weak_json}
- AI-identified weak areas: {ai_weak_json}
- Strong domains (≥ 70%): {strong_json}

Plan type: {plan_type}{full_test_note}

Create a {plan_type} {exam_type} study plan that:
1. Prioritises weak domains heavily
2. Maintains strong domains with light review
3. Incorporates mixed practice and timed sessions
4. Is realistic for {daily_hours} hours/day

Return a JSON object in this exact schema:
{{
  "goal": "{exam_type} target {score_str} by {target_date_str}",
  "target_date": "{target_date_str}",
  "days_available": {days_available},
  "daily_hours": {daily_hours},
  "exam_type": "{exam_type}",
  "summary": "Plain-language summary of the plan",
  "weak_domains": {weak_json},
  "weekly_breakdown": [
    {{
      "week": 1,
      "focus": "Primary focus topic",
      "days": [
        {{
          "day": 1,
          "topic": "Topic name",
          "material": "Recommended resource or practice type",
          "tasks": ["Task 1", "Task 2"],
          "duration_minutes": 60
        }}
      ]
    }}
  ],
  "tips": ["Tip 1", "Tip 2"]
}}

Return ONLY the JSON, no other text."""

    start = time.time()
    try:
        response = gemini_generate(model="gemini-flash-latest", contents=prompt)
    except ClientError as exc:
        if getattr(exc, "code", None) == 429:
            return {"error": "Gemini API rate limit exceeded. Please try again shortly."}
        return {"error": f"Gemini API error: {str(exc)}"}
    except Exception as exc:
        return {"error": f"Unexpected error generating plan: {str(exc)}"}

    latency_ms = int((time.time() - start) * 1000)
    log_llm_call(
        user_id=user_id,
        prompt=prompt,
        response_text=response.text,
        latency_ms=latency_ms,
        model="gemini-flash-latest",
    )

    # --- Parse response ---
    try:
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        plan_data = json.loads(text)
        plan_data["generated_at"] = datetime.now().isoformat()
        return plan_data
    except Exception:
        return {"error": "Could not parse plan response", "raw": response.text}
