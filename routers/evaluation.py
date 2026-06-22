from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from pydantic import BaseModel, ConfigDict
from services.db import get_db
from services.models import LLMLog, User, QuizSession, VectorEntry
from typing import List

router = APIRouter(prefix="/evaluation", tags=["evaluation"])

class RatingRequest(BaseModel):
    log_id: int
    rating: int = None
    accuracy: int = None
    groundedness: int = None
    helpfulness: int = None
    tone: int = None
    eval_comment: str = None

class LLMLogResponse(BaseModel):
    id: int
    user_id: int = None
    prompt: str
    response: str
    latency_ms: int
    model: str
    rating: int = None
    accuracy: int = None
    groundedness: int = None
    helpfulness: int = None
    tone: int = None
    eval_comment: str = None

    model_config = ConfigDict(from_attributes=True)

@router.get("/metrics")
def get_usage_metrics(db: Session = Depends(get_db)):
    from datetime import datetime, timedelta
    total_users = db.query(User).count()
    total_quizzes = db.query(QuizSession).count()
    total_uploads = db.query(VectorEntry).count()
    total_llm_calls = db.query(LLMLog).count()
    
    # Active users today (proxy via LLM logs)
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    active_today = db.query(func.count(func.distinct(LLMLog.user_id))).filter(
        LLMLog.created_at >= one_day_ago
    ).scalar()

    return {
        "total_users": total_users,
        "total_quizzes": total_quizzes,
        "total_uploads": total_uploads,
        "total_llm_calls": total_llm_calls,
        "active_users_last_24h": active_today or 0
    }


@router.get("/logs", response_model=List[LLMLogResponse])
def get_logs(limit: int = 50, db: Session = Depends(get_db)):
    logs = db.query(LLMLog).order_by(LLMLog.created_at.desc()).limit(limit).all()
    return logs

@router.post("/rate")
def rate_log(data: RatingRequest, db: Session = Depends(get_db)):
    log_entry = db.query(LLMLog).filter(LLMLog.id == data.log_id).first()
    if not log_entry:
        raise HTTPException(status_code=404, detail="Log not found")
    
    if data.rating is not None: log_entry.rating = data.rating
    if data.accuracy is not None: log_entry.accuracy = data.accuracy
    if data.groundedness is not None: log_entry.groundedness = data.groundedness
    if data.helpfulness is not None: log_entry.helpfulness = data.helpfulness
    if data.tone is not None: log_entry.tone = data.tone
    if data.eval_comment is not None: log_entry.eval_comment = data.eval_comment
    
    db.commit()
    return {"message": "Rating saved"}

@router.get("/report")
def evaluation_report(db: Session = Depends(get_db)):
    logs = db.query(LLMLog).filter(LLMLog.rating.isnot(None)).all()
    if not logs:
        return {"message": "No rated logs yet"}
    
    avg_rating = sum(l.rating for l in logs) / len(logs)
    avg_latency = sum(l.latency_ms for l in logs) / len(logs)
    
    return {
        "total_rated": len(logs),
        "average_rating": round(avg_rating, 2),
        "average_latency_ms": round(avg_latency, 2),
        "samples": [
            {
                "id": l.id,
                "rating": l.rating,
                "comment": l.eval_comment,
                "model": l.model
            } for l in logs
        ]
    }
