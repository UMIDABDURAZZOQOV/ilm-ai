"""
sat_analyzer.py — Gemini-powered session analysis for SAT/IELTS.
"""
from __future__ import annotations

import json
import os
import time
from typing import TYPE_CHECKING

from sqlalchemy.orm import Session

from services.models import SatIeltsSession

if TYPE_CHECKING:
    from services.models import User

WEAK_AREA_THRESHOLD = 0.70  # domains below this are flagged as weak

# ---------------------------------------------------------------------------
# Prompt builder
# ---------------------------------------------------------------------------

def _build_analysis_prompt(session: SatIeltsSession, is_premium: bool) -> str:
    """Build the Gemini prompt for session analysis."""
    answers = session.answers or {}
    question_ids = session.questions or []

    detail_level = "full" if is_premium else "summary"

    return f"""You are an expert {session.exam_type} tutor analyzing a student's practice session.

Session details:
- Exam: {session.exam_type}
- Domain/Section: {session.domain or "Mixed"}
- Difficulty: {session.difficulty}
- Score: {session.score}/{session.total} ({session.score_pct:.1f}%)
- Questions attempted: {len(question_ids)}
- Questions answered: {len(answers)}

Analysis level: {detail_level}
- summary: concise overview, top 3 weak areas, 2–3 study tips
- full: detailed per-domain breakdown, step-by-step explanations for wrong answers, prioritised study topics, exam strategy tips

Based on this session's performance, provide:
1. Weak areas (domains/skills where accuracy < {int(WEAK_AREA_THRESHOLD * 100)}%)
2. Recommended study topics (prioritised)
3. Study tips{"" if not is_premium else " with detailed explanations"}

Return JSON:
{{
  "weak_areas": ["domain1", "domain2"],
  "recommended_topics": ["topic1", "topic2"],
  "study_tips": ["tip1", "tip2"],
  "summary": "Plain-language performance summary",
  "domain_feedback": {{
    "domain_name": "specific feedback"
  }}
}}

Return ONLY valid JSON."""


# ---------------------------------------------------------------------------
# Main async function
# ---------------------------------------------------------------------------

async def analyse_session(
    db: Session,
    session: SatIeltsSession,
    user: "User",
    is_premium: bool,
) -> dict:
    """Call Gemini to analyse the session and persist results.

    On LLM failure: sets analysis_status='pending', does NOT raise.
    """
    from google import genai
    from google.genai.errors import ClientError
    from dotenv import load_dotenv
    from services.monitoring import log_llm_call

    load_dotenv()
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    prompt = _build_analysis_prompt(session, is_premium)

    start = time.time()
    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        latency_ms = int((time.time() - start) * 1000)

        log_llm_call(
            user_id=session.user_id,
            prompt=prompt,
            response_text=response.text,
            latency_ms=latency_ms,
            model="gemini-2.5-flash",
        )

        # Parse response
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        result = json.loads(text)

        # Persist
        session.analysis_result = result
        session.analysis_status = "complete"
        db.commit()

        # Pass weak areas to gap detection pipeline
        weak_areas = result.get("weak_areas", [])
        if weak_areas:
            _pass_weak_areas_to_gap_detector(session.user_id, weak_areas)

        return result

    except (ClientError, Exception) as exc:
        # Graceful degradation: mark pending, don't raise
        session.analysis_status = "pending"
        db.commit()
        return {
            "weak_areas": [],
            "recommended_topics": [],
            "study_tips": [],
            "summary": "Analysis pending — will retry shortly.",
            "domain_feedback": {},
        }


# ---------------------------------------------------------------------------
# Gap detector bridge
# ---------------------------------------------------------------------------

def _pass_weak_areas_to_gap_detector(user_id: int, weak_areas: list[str]) -> None:
    """Inject SAT/IELTS weak domains into the existing gap_detection service."""
    try:
        from services.gap_detection import inject_sat_weak_areas
        inject_sat_weak_areas(user_id, weak_areas)
    except Exception:
        # Non-critical: don't propagate errors to the caller
        pass
