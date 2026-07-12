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

def _build_analysis_prompt(db: Session, session: SatIeltsSession, is_premium: bool) -> str:
    """Build the Gemini prompt for session analysis — grounded in the student's
    ACTUAL wrong answers (not just the aggregate score), so the model can explain
    specific mistake patterns and give concrete strategy tips instead of generic
    advice."""
    from services.models import SatIeltsQuestion

    answers = session.answers or {}
    question_ids = session.questions or []
    questions = db.query(SatIeltsQuestion).filter(SatIeltsQuestion.id.in_(question_ids)).all()
    q_map = {q.id: q for q in questions}

    mistakes = []
    for qid in question_ids:
        q = q_map.get(qid)
        if not q:
            continue
        recorded = answers.get(str(qid)) or {}
        user_answer = (recorded.get("answer") or "").strip()
        is_correct = False
        if q.question_type == "mcq" and q.correct_answer:
            is_correct = user_answer == q.correct_answer.strip()
        elif q.question_type == "short_answer" and q.correct_answer:
            is_correct = user_answer.lower() == q.correct_answer.strip().lower()
        if not is_correct:
            mistakes.append({
                "domain": q.domain,
                "question": q.question_text[:300],
                "your_answer": user_answer or "(no answer)",
                "correct_answer": q.correct_answer,
            })

    detail_level = "full" if is_premium else "summary"
    # Cap how many mistakes go into the prompt — keeps it fast/cheap even for
    # a full-length test with many wrong answers.
    mistakes_json = json.dumps(mistakes[:20], ensure_ascii=False)

    return f"""You are an expert {session.exam_type} tutor analyzing a student's practice session.

Session details:
- Exam: {session.exam_type}
- Domain/Section: {session.domain or "Mixed"}
- Difficulty: {session.difficulty}
- Score: {session.score}/{session.total} ({session.score_pct:.1f}%)

The student's actual wrong answers this session (question excerpt, what they answered, the correct answer):
{mistakes_json}

Analysis level: {detail_level}
- summary: concise overview, top 3 weak areas, 2–3 study tips
- full: detailed per-domain breakdown, a specific explanation for EACH mistake pattern, prioritised study topics, exam strategy tips

Based on the ACTUAL mistakes listed above (not just the score), provide:
1. Weak areas (domains where mistakes cluster, or accuracy < {int(WEAK_AREA_THRESHOLD * 100)}%)
2. For each notable mistake (or mistake pattern), a specific reason WHY the student likely got it wrong — misread the question, calculation error, vocabulary gap, timing pressure, wrong strategy, etc. Reference the actual question content, don't be generic.
3. Recommended study topics (prioritised)
4. Concrete, actionable strategy tips{"" if not is_premium else " with detailed explanations"}

Return JSON:
{{
  "weak_areas": ["domain1", "domain2"],
  "mistake_analysis": [
    {{"question": "short excerpt", "your_answer": "...", "correct_answer": "...", "why_wrong": "specific explanation grounded in the actual question"}}
  ],
  "recommended_topics": ["topic1", "topic2"],
  "study_tips": ["tip1", "tip2"],
  "summary": "Plain-language performance summary referencing the real mistake patterns above",
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
    from services.gemini import generate_content as gemini_generate

    prompt = _build_analysis_prompt(db, session, is_premium)

    start = time.time()
    try:
        response = gemini_generate(model="gemini-flash-latest", contents=prompt)
        latency_ms = int((time.time() - start) * 1000)

        log_llm_call(
            user_id=session.user_id,
            prompt=prompt,
            response_text=response.text,
            latency_ms=latency_ms,
            model="gemini-flash-latest",
        )

        # Parse response
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        result = json.loads(text)

        # Free tier: truncate the richer fields (mirrors the same premium-gating
        # pattern used by the general Gaps Report — services/gap_detection.py).
        if not is_premium:
            result["mistake_analysis"] = (result.get("mistake_analysis") or [])[:2]
            result["study_tips"] = (result.get("study_tips") or [])[:2]
            result["recommended_topics"] = (result.get("recommended_topics") or [])[:2]

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
        import traceback
        print(f"[sat_analyzer] analyse_session failed for session {session.id}: {exc}")
        traceback.print_exc()
        session.analysis_status = "pending"
        db.commit()
        return {
            "weak_areas": [],
            "mistake_analysis": [],
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
