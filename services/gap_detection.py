import json
import os

from google import genai
from google.genai.errors import ClientError
from dotenv import load_dotenv

from services.quiz_engine import load_vectors
from services.quiz_history import load_sessions

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def _parse_json(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    return json.loads(cleaned)


def generate_gaps_report(user_id: int, is_premium: bool) -> dict:
    sessions = load_sessions(user_id)

    if len(sessions) < 2:
        return {
            "ready": False,
            "message": "Complete at least 2 quiz sessions to generate a Gaps Report.",
            "sessions_completed": len(sessions),
        }

    vectors = load_vectors(user_id)
    filenames = list({v["filename"] for v in vectors}) if vectors else []

    wrong_items = []
    for s in sessions[-10:]:
        for r in s.get("results", []):
            if not r.get("is_correct", True):
                wrong_items.append(
                    {
                        "question": r.get("question", ""),
                        "topic": r.get("topic", "general"),
                        "explanation": r.get("explanation", ""),
                    }
                )

    history_summary = json.dumps(
        {
            "sessions": len(sessions),
            "recent_scores": [
                {"score": s["score"], "total": s["total"]} for s in sessions[-5:]
            ],
            "wrong_answers": wrong_items[:20],
            "materials": filenames,
        },
        ensure_ascii=False,
    )

    detail_level = "full" if is_premium else "summary"
    import time
    from services.monitoring import log_llm_call
    start_time = time.time()
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""You are a learning analytics agent for Ilm AI.
Analyze quiz history and identify knowledge gaps.

Report level: {detail_level}
- summary: short overview only
- full: detailed strengths, weaknesses, sections to revisit, study tips

HISTORY:
{history_summary}

Return JSON:
{{
  "ready": true,
  "summary": "Plain-language overview",
  "strengths": ["strength 1"],
  "gaps": ["gap 1", "gap 2"],
  "weak_topics": ["topic"],
  "recommended_sections": [
    {{"material": "filename.pdf", "reason": "why revisit", "priority": "high"}}
  ],
  "study_tips": ["tip 1"],
  "confidence_score": 0.75
}}

Return ONLY JSON.""",
        )
    except ClientError as e:
        return {
            "ready": False,
            "message": "Gemini API rate limit exceeded or error occurred. Try again later.",
        }

    latency_ms = int((time.time() - start_time) * 1000)
    
    log_llm_call(
        user_id=user_id,
        prompt=history_summary, # Simplified prompt for logging
        response_text=response.text,
        latency_ms=latency_ms,
        model="gemini-2.5-flash"
    )

    try:
        report = _parse_json(response.text)
        report["ready"] = True
        report["sessions_analyzed"] = len(sessions)
        if not is_premium:
            report["premium_note"] = (
                "Upgrade to Premium for full Gaps Reports and unlimited quizzes."
            )
            report["gaps"] = (report.get("gaps") or [])[:3]
            report["recommended_sections"] = (
                report.get("recommended_sections") or []
            )[:2]
        return report
    except (json.JSONDecodeError, IndexError, AttributeError):
        return {
            "ready": False,
            "message": "Could not generate gaps report. Try again later.",
        }



def inject_sat_weak_areas(user_id: int, weak_areas: list[str]) -> None:
    """Inject SAT/IELTS weak domains as synthetic wrong-answer entries into the gap pipeline.

    This appends structured entries to the user's quiz history so that the existing
    ``generate_gaps_report`` can surface them alongside upload-based gaps without
    any structural changes to the quiz history schema.
    """
    from services.quiz_history import load_sessions, add_session

    if not weak_areas:
        return

    # Build a synthetic "session" entry that looks like a quiz session result
    synthetic_results = [
        {
            "question": f"SAT/IELTS weak area: {area}",
            "topic": area,
            "is_correct": False,
            "explanation": f"Identified as a weak area in SAT/IELTS practice session.",
            "user_answer": "",
            "correct_answer": "N/A",
        }
        for area in weak_areas
    ]

    try:
        add_session(
            user_id=user_id,
            score=0,
            total=len(weak_areas),
            difficulty="medium",
            results=synthetic_results,
        )
    except Exception:
        # Non-critical helper — swallow errors silently
        pass
