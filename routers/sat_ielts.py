"""
routers/sat_ielts.py — SAT & IELTS Practice Module router.

All endpoints live under /sat-ielts/ prefix.
JWT auth via get_authenticated_user_id / verify_user_access / ensure_own_user.
"""
from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Literal, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from services.auth_deps import (
    ensure_own_user,
    get_authenticated_user_id,
    verify_user_access,
)
from services.db import SessionLocal, get_db
from services.models import SatIeltsQuestion, SatIeltsSession, SatIeltsUserPrefs, User
from services.question_bank import (
    add_question,
    generate_questions_from_materials,
    get_questions,
    select_questions_for_session,
)
from services.sat_session_engine import (
    compute_domain_accuracy,
    create_session,
    create_sat_full_test,
    create_ielts_full_test,
    finalise_session,
    record_answer,
)
from services.score_predictor import (
    get_prediction_response,
    update_prediction,
)
from services.sat_subscription import (
    can_attempt_sat_ielts,
    record_sat_ielts_attempt,
)
from services.sat_plan import generate_sat_plan

router = APIRouter(prefix="/sat-ielts", tags=["sat-ielts"])


# ===========================================================================
# Pydantic Schemas
# ===========================================================================


class QuestionIn(BaseModel):
    exam_type: Literal["SAT", "IELTS"]
    domain: str
    difficulty: Literal["easy", "medium", "hard"]
    question_type: Literal["mcq", "short_answer", "essay"]
    question_text: str
    options: Optional[list[str]] = None
    correct_answer: Optional[str] = None
    rubric: Optional[str] = None
    source_filename: Optional[str] = None
    tags: list[str] = []


class GenerateFromMaterialsRequest(BaseModel):
    user_id: int
    exam_type: Literal["SAT", "IELTS"]
    domain: str
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    num_questions: int = Field(default=10, ge=5, le=20)


class SessionStartRequest(BaseModel):
    user_id: int
    exam_type: Literal["SAT", "IELTS"]
    domain: Optional[str] = None
    section: Optional[str] = None
    skill: Optional[str] = None
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    num_questions: int = Field(default=10, ge=1, le=50)
    timed: bool = False
    duration_seconds: Optional[int] = None
    session_type: Optional[Literal["practice", "diagnostic"]] = "practice"


class AnswerSubmission(BaseModel):
    question_id: int
    answer: str
    elapsed_ms: int = Field(ge=0)


class TargetScoreRequest(BaseModel):
    sat_target_score: Optional[int] = None
    ielts_target_band: Optional[float] = None


class PlanGenerateRequest(BaseModel):
    user_id: int
    exam_type: Literal["SAT", "IELTS"]
    target_date: str          # YYYY-MM-DD
    target_score: Optional[float] = None
    daily_hours: float = 1.0


class TelegramAnswerRequest(BaseModel):
    user_id: int
    session_id: int
    question_id: int
    answer: str
    elapsed_ms: int = 0


# ===========================================================================
# Helpers
# ===========================================================================


def _question_out(q: SatIeltsQuestion) -> dict:
    return {
        "id": q.id,
        "exam_type": q.exam_type,
        "domain": q.domain,
        "skill": q.skill,
        "difficulty": q.difficulty,
        "question_type": q.question_type,
        "question_text": q.question_text,
        "options": q.options,
        "correct_answer": q.correct_answer,
        "rubric": q.rubric,
        "source_filename": q.source_filename,
        "tags": q.tags or [],
        "created_at": q.created_at.isoformat() if q.created_at else None,
    }


def _grade_answer(q: SatIeltsQuestion, user_answer: str) -> bool:
    """Same correctness rule used for scoring (services/sat_session_engine.py's
    _score_session) — kept in sync so per-question detail matches the score."""
    if not user_answer or not q.correct_answer:
        return False
    if q.question_type == "mcq":
        return user_answer.strip() == q.correct_answer.strip()
    if q.question_type == "short_answer":
        return user_answer.strip().lower() == q.correct_answer.strip().lower()
    return False  # essay: not auto-graded


def _build_per_question(s: SatIeltsSession, db: Session) -> list[dict]:
    question_ids = s.questions or []
    answers = s.answers or {}
    questions = db.query(SatIeltsQuestion).filter(SatIeltsQuestion.id.in_(question_ids)).all()
    q_map = {q.id: q for q in questions}
    results = []
    for qid in question_ids:
        q = q_map.get(qid)
        if not q:
            continue
        recorded = answers.get(str(qid)) or {}
        user_answer = recorded.get("answer")
        results.append({
            "question_id": q.id,
            "question_text": q.question_text,
            "question_type": q.question_type,
            "domain": q.domain,
            "options": q.options,
            "user_answer": user_answer,
            "correct_answer": q.correct_answer,
            "is_correct": _grade_answer(q, user_answer or ""),
            "explanation": q.rubric,
        })
    return results


def _session_out(s: SatIeltsSession, include_answers: bool = False, db: Session = None) -> dict:
    data = {
        "session_id": s.id,
        "user_id": s.user_id,
        "exam_type": s.exam_type,
        "domain": s.domain,
        "difficulty": s.difficulty,
        "session_type": s.session_type,
        "status": s.status,
        "timed": s.timed,
        "duration_seconds": s.duration_seconds,
        "questions": s.questions,
        "score": s.score,
        "total": s.total,
        "score_pct": s.score_pct,
        "questions_correct": s.score,
        "questions_total": s.total,
        "analysis_status": s.analysis_status,
        "analysis_result": s.analysis_result,
        "started_at": s.started_at.isoformat() if s.started_at else None,
        "completed_at": s.completed_at.isoformat() if s.completed_at else None,
    }
    if include_answers:
        data["answers"] = s.answers
    # Per-question detail + domain-grouped section scores — only computed when a
    # db handle is passed (session completion), since it requires a query.
    if db is not None and s.status == "completed":
        per_question = _build_per_question(s, db)
        data["per_question"] = per_question
        domain_totals: dict[str, list[int]] = {}
        for pq in per_question:
            d = pq["domain"] or "General"
            bucket = domain_totals.setdefault(d, [0, 0])
            bucket[1] += 1
            if pq["is_correct"]:
                bucket[0] += 1
        data["section_scores"] = {
            d: round(c / t * 100, 1) for d, (c, t) in domain_totals.items() if t > 0
        }
    return data


def _get_user_or_404(user_id: int, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def _is_premium(user: User) -> bool:
    return getattr(user, "subscription_tier", "free") == "premium"


def _background_analyse_and_predict(session_id: int, is_premium: bool) -> None:
    """Background task: run AI analysis then update score prediction."""
    db = SessionLocal()
    try:
        session = db.query(SatIeltsSession).filter(SatIeltsSession.id == session_id).first()
        if not session:
            return
        user = db.query(User).filter(User.id == session.user_id).first()
        if not user:
            return

        from services.sat_analyzer import analyse_session

        # Run async function in sync context
        try:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(analyse_session(db, session, user, is_premium))
            loop.close()
        except Exception:
            pass

        # Update score prediction
        try:
            update_prediction(db, session.user_id, session.exam_type)
        except Exception:
            pass
    finally:
        db.close()


def _select_diagnostic_questions(db: Session, exam_type: str, num_questions: int) -> list[SatIeltsQuestion]:
    """Select questions for a diagnostic test - balanced across domains and difficulties.
    
    For SAT diagnostic, we want:
    - Mix of Math and Reading & Writing domains
    - Mix of easy, medium, and hard questions
    - Representative sample of all skill areas
    """
    from services.sat_taxonomy import SAT_TAXONOMY, IELTS_TAXONOMY
    
    taxonomy = SAT_TAXONOMY if exam_type == "SAT" else IELTS_TAXONOMY
    questions = []
    
    if exam_type == "SAT":
        # SAT: Get domains from both sections
        all_domains = []
        for section in taxonomy.values():
            for domain_data in section:
                all_domains.append(domain_data["domain"])
        
        # Calculate questions per domain (roughly equal distribution)
        questions_per_domain = max(1, num_questions // len(all_domains))
        
        for domain in all_domains:
            # Get mix of difficulties for each domain
            for difficulty in ["easy", "medium", "hard"]:
                domain_questions = db.query(SatIeltsQuestion).filter(
                    SatIeltsQuestion.exam_type == exam_type,
                    SatIeltsQuestion.domain == domain,
                    SatIeltsQuestion.difficulty == difficulty
                ).order_by(db.func.random()).limit(questions_per_domain // 3 + 1).all()
                
                questions.extend(domain_questions)
                
                if len(questions) >= num_questions:
                    break
            
            if len(questions) >= num_questions:
                break
    else:
        # IELTS: Get questions from each section
        for section in taxonomy.values():
            for domain_data in section:
                domain = domain_data["domain"]
                domain_questions = db.query(SatIeltsQuestion).filter(
                    SatIeltsQuestion.exam_type == exam_type,
                    SatIeltsQuestion.domain == domain
                ).order_by(db.func.random()).limit(num_questions // 4 + 1).all()
                questions.extend(domain_questions)
    
    # Shuffle and limit to requested number
    import random
    random.shuffle(questions)
    return questions[:num_questions]


# ===========================================================================
# Question Bank Endpoints
# ===========================================================================


@router.get("/questions")
def list_questions(
    exam_type: Optional[str] = None,
    domain: Optional[str] = None,
    difficulty: Optional[str] = None,
    question_type: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    """List/filter questions from the question bank."""
    questions = get_questions(
        db,
        exam_type=exam_type,
        domain=domain,
        difficulty=difficulty,
        question_type=question_type,
        limit=limit,
        offset=offset,
    )
    return {"questions": [_question_out(q) for q in questions], "count": len(questions)}


@router.post("/questions", status_code=201)
def create_question(
    data: QuestionIn,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    """Add a new question to the bank (admin or content creator)."""
    q_in = data.model_dump()
    q_in["created_by"] = auth_user_id
    try:
        q = add_question(db, q_in)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return _question_out(q)


@router.post("/questions/generate-from-materials", status_code=201)
def generate_questions_from_materials_endpoint(
    data: GenerateFromMaterialsRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    """AI-generate questions from user's uploaded materials."""
    ensure_own_user(data.user_id, auth_user_id)

    user = _get_user_or_404(data.user_id, db)
    is_prem = _is_premium(user)

    questions = generate_questions_from_materials(
        user_id=data.user_id,
        exam_type=data.exam_type,
        domain=data.domain,
        difficulty=data.difficulty,
        num_questions=data.num_questions,
        db=db,
    )
    if not questions:
        raise HTTPException(
            status_code=400,
            detail="Could not generate questions. Upload study materials first.",
        )
    return {"questions": [_question_out(q) for q in questions], "count": len(questions)}


# ===========================================================================
# Practice Session Endpoints
# ===========================================================================


@router.post("/sessions/start", status_code=201)
def start_session(
    data: SessionStartRequest,
    background_tasks: BackgroundTasks,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    """Initiate a new practice session or diagnostic test."""
    ensure_own_user(data.user_id, auth_user_id)

    # Subscription gate
    ok, msg = can_attempt_sat_ielts(data.user_id, db)
    if not ok:
        raise HTTPException(status_code=403, detail=msg)

    if data.timed and not data.duration_seconds:
        raise HTTPException(
            status_code=400, detail="duration_seconds is required when timed=True"
        )

    # Diagnostic mode: adaptive question selection
    if data.session_type == "diagnostic":
        questions = _select_diagnostic_questions(
            db,
            exam_type=data.exam_type,
            num_questions=data.num_questions,
        )
    else:
        questions = select_questions_for_session(
            db,
            exam_type=data.exam_type,
            domain=data.domain,
            difficulty=data.difficulty,
            count=data.num_questions,
            skill=data.skill,
            section=data.section,
        )
    
    if not questions:
        raise HTTPException(
            status_code=404,
            detail="No questions found matching the requested criteria.",
        )

    session = create_session(
        db=db,
        user_id=data.user_id,
        exam_type=data.exam_type,
        questions=questions,
        timed=data.timed,
        duration_seconds=data.duration_seconds,
        session_type=data.session_type or "practice",
    )

    # Record usage
    record_sat_ielts_attempt(data.user_id, len(questions), db)

    return {
        "session_id": session.id,
        "exam_type": session.exam_type,
        "domain": session.domain,
        "difficulty": session.difficulty,
        "timed": session.timed,
        "duration_seconds": session.duration_seconds,
        "questions": [_question_out(q) for q in questions],
        "started_at": session.started_at.isoformat() if session.started_at else None,
    }


@router.post("/sessions/{session_id}/answer")
def submit_answer(
    session_id: int,
    data: AnswerSubmission,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    """Submit an answer for one question in a session."""
    session = db.query(SatIeltsSession).filter(SatIeltsSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    ensure_own_user(session.user_id, auth_user_id)

    if session.status != "in_progress":
        raise HTTPException(status_code=400, detail="Session is not in progress")

    if data.question_id not in (session.questions or []):
        raise HTTPException(status_code=400, detail="Question not part of this session")

    record_answer(db, session_id, data.question_id, data.answer, data.elapsed_ms)
    return {"recorded": True, "question_id": data.question_id}


@router.post("/sessions/{session_id}/complete")
def complete_session(
    session_id: int,
    background_tasks: BackgroundTasks,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    """Finalise a session and trigger background analysis + prediction."""
    session = db.query(SatIeltsSession).filter(SatIeltsSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    ensure_own_user(session.user_id, auth_user_id)

    user = _get_user_or_404(session.user_id, db)
    is_prem = _is_premium(user)

    session = finalise_session(db, session_id)

    background_tasks.add_task(_background_analyse_and_predict, session_id, is_prem)

    return _session_out(session, db=db)


@router.post("/sessions/{session_id}/analyze")
async def analyze_session_endpoint(
    session_id: int,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    """On-demand AI analysis of a completed session — explains the student's
    actual mistakes (grounded in their real wrong answers, not just the score)
    and gives concrete study strategy tips."""
    session = db.query(SatIeltsSession).filter(SatIeltsSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    ensure_own_user(session.user_id, auth_user_id)
    if session.status != "completed":
        raise HTTPException(status_code=400, detail="Session must be completed before analysis")

    user = _get_user_or_404(session.user_id, db)
    is_prem = _is_premium(user)

    from services.sat_analyzer import analyse_session
    result = await analyse_session(db, session, user, is_prem)
    return result


@router.get("/skills/{user_id}")
def get_skill_tree(
    user_id: int = Depends(verify_user_access),
    exam_type: str = "SAT",
    db: Session = Depends(get_db),
):
    """The domain/skill taxonomy with question counts and this user's progress
    (attempted/correct per skill) — powers the OnePrep-style Question Bank page."""
    from services.sat_taxonomy import get_taxonomy

    # All answered questions across this user's completed sessions
    sessions = (
        db.query(SatIeltsSession)
        .filter(
            SatIeltsSession.user_id == user_id,
            SatIeltsSession.exam_type == exam_type,
            SatIeltsSession.status == "completed",
        )
        .all()
    )
    answered: dict[str, str] = {}
    for s in sessions:
        for qid, rec in (s.answers or {}).items():
            answered[qid] = (rec or {}).get("answer", "")

    questions = db.query(SatIeltsQuestion).filter(SatIeltsQuestion.exam_type == exam_type).all()

    # Per-(domain, skill) aggregates. skill=None rows count toward the domain only.
    stats: dict[tuple, dict] = {}
    domain_totals: dict[str, dict] = {}
    for q in questions:
        d_bucket = domain_totals.setdefault(q.domain, {"question_count": 0, "attempted": 0, "correct": 0})
        d_bucket["question_count"] += 1
        s_bucket = stats.setdefault((q.domain, q.skill), {"question_count": 0, "attempted": 0, "correct": 0})
        s_bucket["question_count"] += 1
        user_answer = answered.get(str(q.id))
        if user_answer is not None:
            d_bucket["attempted"] += 1
            s_bucket["attempted"] += 1
            if _grade_answer(q, user_answer):
                d_bucket["correct"] += 1
                s_bucket["correct"] += 1

    taxonomy = get_taxonomy(exam_type)
    sections = []
    for section_name, domains in taxonomy.items():
        out_domains = []
        for d in domains:
            dn = d["domain"]
            totals = domain_totals.get(dn, {"question_count": 0, "attempted": 0, "correct": 0})
            out_skills = [
                {"skill": sk, **stats.get((dn, sk), {"question_count": 0, "attempted": 0, "correct": 0})}
                for sk in d["skills"]
            ]
            out_domains.append({"domain": dn, **totals, "skills": out_skills})
        sections.append({"section": section_name, "domains": out_domains})

    return {"exam_type": exam_type, "sections": sections}


@router.get("/sessions/{user_id}")
def list_user_sessions(
    user_id: int = Depends(verify_user_access),
    exam_type: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """List SAT/IELTS sessions for a user."""
    q = db.query(SatIeltsSession).filter(SatIeltsSession.user_id == user_id)
    if exam_type:
        q = q.filter(SatIeltsSession.exam_type == exam_type)
    sessions = q.order_by(SatIeltsSession.started_at.desc()).offset(offset).limit(limit).all()
    return {"sessions": [_session_out(s) for s in sessions], "count": len(sessions)}


# ===========================================================================
# Full-Length Test Endpoints  (premium only)
# ===========================================================================


@router.post("/full-tests/start", status_code=201)
def start_full_test(
    data: SessionStartRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    """Initiate a full-length exam simulation (premium only)."""
    ensure_own_user(data.user_id, auth_user_id)

    user = _get_user_or_404(data.user_id, db)
    if not _is_premium(user):
        raise HTTPException(
            status_code=403, detail="Full-length tests are a Premium feature."
        )

    ok, msg = can_attempt_sat_ielts(data.user_id, db)
    if not ok:
        raise HTTPException(status_code=403, detail=msg)

    # For SAT, use the new module structure
    if data.exam_type == "SAT":
        sessions = create_sat_full_test(
            db=db,
            user_id=data.user_id,
            difficulty=data.difficulty,
        )
        
        # Get all questions for all sessions
        all_questions = []
        for session_id in sessions.values():
            session = db.query(SatIeltsSession).filter(SatIeltsSession.id == session_id).first()
            if session:
                q_ids = session.questions or []
                questions = db.query(SatIeltsQuestion).filter(SatIeltsQuestion.id.in_(q_ids)).all()
                all_questions.extend([_question_out(q) for q in questions])
        
        record_sat_ielts_attempt(data.user_id, len(all_questions), db)
        
        return {
            "test_type": "sat_modular",
            "sessions": sessions,
            "modules": [
                {"module": 1, "section": "RW", "session_id": sessions["module1_rw"], "duration_seconds": 32 * 60, "question_count": 27},
                {"module": 1, "section": "Math", "session_id": sessions["module1_math"], "duration_seconds": 35 * 60, "question_count": 22},
                {"module": 2, "section": "RW", "session_id": sessions["module2_rw"], "duration_seconds": 32 * 60, "question_count": 27},
                {"module": 2, "section": "Math", "session_id": sessions["module2_math"], "duration_seconds": 35 * 60, "question_count": 22},
            ],
            "total_questions": 98,
            "total_duration_seconds": 134 * 60,  # 2 hours 14 minutes
            "started_at": datetime.now(timezone.utc).isoformat(),
        }
    
    # For IELTS, use the new section structure
    elif data.exam_type == "IELTS":
        sessions = create_ielts_full_test(
            db=db,
            user_id=data.user_id,
            difficulty=data.difficulty,
        )
        
        # Get all questions for all sessions
        all_questions = []
        for session_id in sessions.values():
            session = db.query(SatIeltsSession).filter(SatIeltsSession.id == session_id).first()
            if session:
                q_ids = session.questions or []
                questions = db.query(SatIeltsQuestion).filter(SatIeltsQuestion.id.in_(q_ids)).all()
                all_questions.extend([_question_out(q) for q in questions])
        
        record_sat_ielts_attempt(data.user_id, len(all_questions), db)
        
        return {
            "test_type": "ielts_sectional",
            "sessions": sessions,
            "sections": [
                {"section": "Listening", "session_id": sessions["listening"], "duration_seconds": 30 * 60, "question_count": 40},
                {"section": "Reading", "session_id": sessions["reading"], "duration_seconds": 60 * 60, "question_count": 40},
                {"section": "Writing", "session_id": sessions["writing"], "duration_seconds": 60 * 60, "question_count": 2},
                {"section": "Speaking", "session_id": sessions["speaking"], "duration_seconds": 14 * 60, "question_count": 3},
            ],
            "total_questions": 85,
            "total_duration_seconds": 164 * 60,  # 2 hours 44 minutes
            "started_at": datetime.now(timezone.utc).isoformat(),
        }
    
    # Fallback for other exam types
    questions = select_questions_for_session(
        db,
        exam_type=data.exam_type,
        domain=None,  # all domains
        difficulty=data.difficulty,
        count=50,
    )
    if not questions:
        raise HTTPException(status_code=404, detail="No questions available for full test.")

    session = create_session(
        db=db,
        user_id=data.user_id,
        exam_type=data.exam_type,
        questions=questions,
        timed=True,
        duration_seconds=data.duration_seconds or 3600,  # default 1 hour
        session_type="full_test",
    )

    record_sat_ielts_attempt(data.user_id, len(questions), db)

    return {
        "test_id": session.id,
        "exam_type": session.exam_type,
        "session_type": session.session_type,
        "timed": session.timed,
        "duration_seconds": session.duration_seconds,
        "questions": [_question_out(q) for q in questions],
        "started_at": session.started_at.isoformat() if session.started_at else None,
    }


@router.post("/full-tests/{test_id}/section/{section}/complete")
def complete_full_test_section(
    test_id: int,
    section: str,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    """Mark a section of a full-length test as complete and advance."""
    session = db.query(SatIeltsSession).filter(SatIeltsSession.id == test_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Test not found")
    ensure_own_user(session.user_id, auth_user_id)

    if session.status != "in_progress":
        raise HTTPException(status_code=400, detail="Test is not in progress")

    # Record section completion in analysis_result metadata
    meta = dict(session.analysis_result or {})
    completed_sections = meta.get("completed_sections", [])
    if section not in completed_sections:
        completed_sections.append(section)
    meta["completed_sections"] = completed_sections
    session.analysis_result = meta
    db.commit()

    return {
        "test_id": test_id,
        "section": section,
        "completed_sections": completed_sections,
        "status": session.status,
    }


@router.post("/full-tests/{test_id}/complete")
def complete_full_test(
    test_id: int,
    background_tasks: BackgroundTasks,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    """Finalise a full-length test."""
    session = db.query(SatIeltsSession).filter(SatIeltsSession.id == test_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Test not found")
    ensure_own_user(session.user_id, auth_user_id)

    user = _get_user_or_404(session.user_id, db)
    is_prem = _is_premium(user)

    session = finalise_session(db, test_id)
    background_tasks.add_task(_background_analyse_and_predict, test_id, is_prem)

    return _session_out(session, db=db)


# ===========================================================================
# Score Prediction Endpoints
# ===========================================================================


@router.get("/score/{user_id}")
def get_score_prediction(
    user_id: int = Depends(verify_user_access),
    exam_type: str = "SAT",
    db: Session = Depends(get_db),
):
    """Get current SAT/IELTS score prediction + history."""
    user = _get_user_or_404(user_id, db)
    is_prem = _is_premium(user)
    return get_prediction_response(db, user_id, exam_type, is_prem)


@router.post("/score/{user_id}/target")
def set_target_score(
    user_id: int,
    data: TargetScoreRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    """Set target SAT score or IELTS band for the user."""
    ensure_own_user(user_id, auth_user_id)

    prefs = db.query(SatIeltsUserPrefs).filter(SatIeltsUserPrefs.user_id == user_id).first()
    if not prefs:
        prefs = SatIeltsUserPrefs(user_id=user_id)
        db.add(prefs)

    if data.sat_target_score is not None:
        if not (400 <= data.sat_target_score <= 1600 and data.sat_target_score % 200 == 0):
            raise HTTPException(
                status_code=422,
                detail="SAT target score must be a multiple of 200 between 400 and 1600.",
            )
        prefs.sat_target_score = data.sat_target_score

    if data.ielts_target_band is not None:
        if not (1.0 <= data.ielts_target_band <= 9.0):
            raise HTTPException(
                status_code=422, detail="IELTS target band must be between 1.0 and 9.0."
            )
        prefs.ielts_target_band = data.ielts_target_band

    db.commit()
    return {
        "user_id": user_id,
        "sat_target_score": prefs.sat_target_score,
        "ielts_target_band": prefs.ielts_target_band,
    }


# ===========================================================================
# Dashboard Endpoint
# ===========================================================================


@router.get("/dashboard/{user_id}")
def get_dashboard(
    user_id: int = Depends(verify_user_access),
    exam_type: str = "SAT",
    db: Session = Depends(get_db),
):
    """Return aggregated stats for the SAT/IELTS dashboard panel."""
    user = _get_user_or_404(user_id, db)
    is_prem = _is_premium(user)

    sessions = (
        db.query(SatIeltsSession)
        .filter(
            SatIeltsSession.user_id == user_id,
            SatIeltsSession.exam_type == exam_type,
            SatIeltsSession.status == "completed",
        )
        .order_by(SatIeltsSession.completed_at.desc())
        .limit(20)
        .all()
    )

    empty_state = len(sessions) == 0

    domain_acc = compute_domain_accuracy(sessions) if sessions else {}
    weak_spots = [d for d, acc in domain_acc.items() if acc < 0.70]

    prediction = get_prediction_response(db, user_id, exam_type, is_prem)

    # Load target score
    prefs = db.query(SatIeltsUserPrefs).filter(SatIeltsUserPrefs.user_id == user_id).first()
    target_score = None
    if prefs:
        target_score = (
            prefs.sat_target_score if exam_type == "SAT" else prefs.ielts_target_band
        )

    predicted_score = prediction.get("predicted_score")
    target_gap = None
    if predicted_score is not None and target_score is not None:
        target_gap = round(float(target_score) - float(predicted_score), 1)

    # Score trend from prediction history
    score_trend = prediction.get("history", [])

    return {
        "exam_type": exam_type,
        "empty_state": empty_state,
        "sessions_completed": len(sessions),
        "domain_accuracy": domain_acc,
        "weak_spots": weak_spots,
        "score_trend": score_trend,
        "predicted_score": predicted_score,
        "target_score": target_score,
        "target_gap": target_gap,
        "prediction_available": prediction.get("prediction_available", False),
        "is_premium": is_prem,
    }


# ===========================================================================
# SAT/IELTS Study Plan Endpoint
# ===========================================================================


@router.post("/plan/generate")
def generate_sat_ielts_plan(
    data: PlanGenerateRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    """Generate a SAT/IELTS-specific study plan."""
    ensure_own_user(data.user_id, auth_user_id)

    user = _get_user_or_404(data.user_id, db)
    is_prem = _is_premium(user)

    plan = generate_sat_plan(
        db=db,
        user_id=data.user_id,
        exam_type=data.exam_type,
        target_date_str=data.target_date,
        target_score=data.target_score,
        daily_hours=data.daily_hours,
        is_premium=is_prem,
    )
    if "error" in plan:
        raise HTTPException(status_code=500, detail=plan["error"])
    return plan


# ===========================================================================
# Telegram Helper Endpoints  (internal / no JWT for Telegram bot)
# ===========================================================================


@router.get("/telegram/daily-question/{user_id}")
def telegram_daily_question(
    user_id: int,
    exam_type: str = "SAT",
    db: Session = Depends(get_db),
):
    """Return a daily question for the Telegram bot (internal, no JWT gate)."""
    ok, msg = can_attempt_sat_ielts(user_id, db)
    if not ok:
        return {"available": False, "message": msg}

    # Prefer weak domains for this user
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

    # Select from a weak domain if possible
    target_domain = weak_domains[0] if weak_domains else None
    questions = select_questions_for_session(
        db, exam_type=exam_type, domain=target_domain, difficulty="medium", count=1
    )
    if not questions:
        questions = select_questions_for_session(
            db, exam_type=exam_type, domain=None, difficulty="medium", count=1
        )
    if not questions:
        return {"available": False, "message": "No questions available."}

    # Create a single-question session for tracking
    session = create_session(
        db=db,
        user_id=user_id,
        exam_type=exam_type,
        questions=questions,
        timed=False,
        session_type="practice",
    )
    record_sat_ielts_attempt(user_id, 1, db)

    return {
        "available": True,
        "session_id": session.id,
        "question": _question_out(questions[0]),
    }


@router.post("/telegram/record-answer")
def telegram_record_answer(
    data: TelegramAnswerRequest,
    db: Session = Depends(get_db),
):
    """Record a Telegram user's answer and auto-complete the session."""
    session = db.query(SatIeltsSession).filter(SatIeltsSession.id == data.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.user_id != data.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    record_answer(db, data.session_id, data.question_id, data.answer, data.elapsed_ms)
    session = finalise_session(db, data.session_id)

    return {
        "session_id": session.id,
        "score": session.score,
        "total": session.total,
        "score_pct": session.score_pct,
    }
