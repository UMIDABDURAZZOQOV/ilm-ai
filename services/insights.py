"""
Learning insights — a lightweight, deterministic (no-LLM) roll-up of what the
learner has actually done: materials covered, quiz performance and its trend, and
their strongest / weakest topics. Cheap enough to compute on every page load.
"""
from __future__ import annotations

from services.quiz_history import load_sessions
from services.quiz_engine import load_vectors


def _avg(scores: list[float]) -> float:
    return round(sum(scores) / len(scores), 1) if scores else 0.0


def build_insights(user_id: int) -> dict:
    sessions = load_sessions(user_id)
    vectors = load_vectors(user_id)

    files = sorted({v.get("filename", "") for v in vectors if v.get("filename")})
    topics_covered = sorted({v.get("topic", "") for v in vectors if v.get("topic")})

    total_sessions = len(sessions)
    total_questions = sum(int(s.get("total") or 0) for s in sessions)
    total_correct = sum(int(s.get("score") or 0) for s in sessions)
    overall_pct = round(100 * total_correct / total_questions) if total_questions else 0

    # Score percentage per session, in order.
    pcts = [
        round(100 * int(s.get("score") or 0) / int(s.get("total") or 1))
        for s in sessions if int(s.get("total") or 0) > 0
    ]
    # Trend: recent third vs the third before it.
    trend = 0
    if len(pcts) >= 4:
        half = max(1, len(pcts) // 3)
        recent = _avg(pcts[-half:])
        prev = _avg(pcts[-2 * half:-half])
        trend = round(recent - prev)

    # Per-topic accuracy from individual results.
    per_topic: dict[str, list[int]] = {}
    for s in sessions:
        for r in (s.get("results") or []):
            topic = (r.get("topic") or "general").strip() or "general"
            bucket = per_topic.setdefault(topic, [0, 0])  # [correct, total]
            bucket[1] += 1
            if r.get("is_correct"):
                bucket[0] += 1

    topic_stats = [
        {"topic": t, "accuracy": round(100 * c / n), "attempts": n}
        for t, (c, n) in per_topic.items() if n >= 3
    ]
    strong = sorted([t for t in topic_stats if t["accuracy"] >= 75], key=lambda x: -x["accuracy"])[:5]
    weak = sorted([t for t in topic_stats if t["accuracy"] < 55], key=lambda x: x["accuracy"])[:5]

    return {
        "has_data": total_sessions > 0 or bool(files),
        "materials": {"files": files, "count": len(files), "topics": topics_covered},
        "quiz": {
            "sessions": total_sessions,
            "questions": total_questions,
            "overall_pct": overall_pct,
            "trend": trend,               # +/- percentage points, recent vs earlier
            "recent_scores": pcts[-10:],  # sparkline
        },
        "strong_topics": strong,
        "weak_topics": weak,
    }
