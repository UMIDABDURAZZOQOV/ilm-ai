"""
score_predictor.py — Weighted accuracy → SAT/IELTS score prediction.
"""
from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from services.models import SatIeltsScorePrediction, SatIeltsSession
from services.sat_session_engine import compute_domain_accuracy

# ---------------------------------------------------------------------------
# Domain / section weights
# ---------------------------------------------------------------------------

SAT_DOMAIN_WEIGHTS: dict[str, float] = {
    "Algebra": 0.135,
    "Advanced Math": 0.135,
    "Problem Solving & Data Analysis": 0.155,
    "Geometry & Trigonometry": 0.075,
    "Information and Ideas": 0.12,
    "Craft and Structure": 0.12,
    "Expression of Ideas": 0.12,
    "Standard English Conventions": 0.14,
}

IELTS_SECTION_WEIGHTS: dict[str, float] = {
    "Listening": 0.25,
    "Reading": 0.25,
    "Writing": 0.25,
    "Speaking": 0.25,
}

_SAT_VALID_SCORES = [400, 600, 800, 1000, 1200, 1400, 1600]

# Minimum sessions required before a prediction is issued
MIN_SESSIONS_REQUIRED = 3


# ---------------------------------------------------------------------------
# Core computation
# ---------------------------------------------------------------------------

def compute_sat_score(domain_accuracy: dict[str, float]) -> float:
    """
    weighted_sum = Σ accuracy[d] × SAT_DOMAIN_WEIGHTS[d]  (only for known domains)
    predicted    = 400 + weighted_sum × 1200
    Snap to nearest value in {400, 600, 800, 1000, 1200, 1400, 1600}.
    """
    # Only include domains present in both the accuracy dict and the weight table
    total_weight = 0.0
    weighted_sum = 0.0
    for domain, weight in SAT_DOMAIN_WEIGHTS.items():
        if domain in domain_accuracy:
            weighted_sum += domain_accuracy[domain] * weight
            total_weight += weight

    if total_weight == 0:
        # No recognised domains — return floor score
        return 400.0

    # Scale to the covered weight so partial coverage still produces a useful estimate
    normalised = weighted_sum / total_weight
    raw = 400 + normalised * 1200

    # Snap to nearest 200-point increment in valid set
    best = min(_SAT_VALID_SCORES, key=lambda s: abs(s - raw))
    return float(best)


def compute_ielts_band(domain_accuracy: dict[str, float]) -> float:
    """
    weighted_sum = Σ accuracy[s] × IELTS_SECTION_WEIGHTS[s]
    raw = 1.0 + weighted_sum × 8.0
    Round to nearest 0.5, clamp to [1.0, 9.0].
    """
    total_weight = 0.0
    weighted_sum = 0.0
    for section, weight in IELTS_SECTION_WEIGHTS.items():
        if section in domain_accuracy:
            weighted_sum += domain_accuracy[section] * weight
            total_weight += weight

    if total_weight == 0:
        return 1.0

    normalised = weighted_sum / total_weight
    raw = 1.0 + normalised * 8.0

    # Round to nearest 0.5
    rounded = round(raw * 2) / 2

    # Clamp to [1.0, 9.0]
    return float(max(1.0, min(9.0, rounded)))


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def update_prediction(
    db: Session,
    user_id: int,
    exam_type: str,
) -> Optional[SatIeltsScorePrediction]:
    """Load last 10 completed sessions, compute accuracy, persist a prediction record.

    Returns None if the minimum session threshold is not met.
    """
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

    if len(sessions) < MIN_SESSIONS_REQUIRED:
        return None

    domain_acc = compute_domain_accuracy(sessions)

    if exam_type == "SAT":
        predicted = compute_sat_score(domain_acc)
    else:
        predicted = compute_ielts_band(domain_acc)

    record = SatIeltsScorePrediction(
        user_id=user_id,
        exam_type=exam_type,
        predicted_score=predicted,
        domain_weights=domain_acc,
        sessions_used=len(sessions),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_prediction_response(
    db: Session,
    user_id: int,
    exam_type: str,
    is_premium: bool,
) -> dict:
    """Return prediction dict.

    Free tier: only the latest prediction (history=[latest]).
    Premium tier: full history list.
    """
    all_predictions = (
        db.query(SatIeltsScorePrediction)
        .filter(
            SatIeltsScorePrediction.user_id == user_id,
            SatIeltsScorePrediction.exam_type == exam_type,
        )
        .order_by(SatIeltsScorePrediction.computed_at.desc())
        .all()
    )

    # Check session count to determine availability
    session_count = (
        db.query(SatIeltsSession)
        .filter(
            SatIeltsSession.user_id == user_id,
            SatIeltsSession.exam_type == exam_type,
            SatIeltsSession.status == "completed",
        )
        .count()
    )

    prediction_available = bool(all_predictions) and session_count >= MIN_SESSIONS_REQUIRED
    latest = all_predictions[0] if all_predictions else None

    def _pred_point(p: SatIeltsScorePrediction) -> dict:
        return {
            "predicted_score": p.predicted_score,
            "sessions_used": p.sessions_used,
            "computed_at": p.computed_at.isoformat() if p.computed_at else None,
        }

    if not prediction_available:
        message = (
            f"Complete at least {MIN_SESSIONS_REQUIRED} practice sessions to unlock your "
            f"{exam_type} score prediction."
        )
        return {
            "user_id": user_id,
            "exam_type": exam_type,
            "predicted_score": None,
            "prediction_available": False,
            "message": message,
            "computed_at": None,
            "history": [],
        }

    history = [_pred_point(p) for p in all_predictions] if is_premium else [_pred_point(latest)]

    return {
        "user_id": user_id,
        "exam_type": exam_type,
        "predicted_score": latest.predicted_score,
        "prediction_available": True,
        "message": None,
        "computed_at": latest.computed_at.isoformat() if latest.computed_at else None,
        "history": history,
    }
