"""
sat_session_engine.py — Create/update SAT/IELTS sessions, answer recording, scoring.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from services.models import SatIeltsQuestion, SatIeltsSession


def create_session(
    db: Session,
    user_id: int,
    exam_type: str,
    questions: list[SatIeltsQuestion],
    timed: bool = False,
    duration_seconds: Optional[int] = None,
    session_type: str = "practice",
) -> SatIeltsSession:
    """Create a new SAT/IELTS session and persist it."""
    # Derive domain: single domain if all questions share one, else None
    domains = list({q.domain for q in questions})
    domain = domains[0] if len(domains) == 1 else None

    # Derive difficulty: use most common difficulty across questions (fallback: "medium")
    from collections import Counter
    difficulties = [q.difficulty for q in questions]
    difficulty = Counter(difficulties).most_common(1)[0][0] if difficulties else "medium"

    session = SatIeltsSession(
        user_id=user_id,
        exam_type=exam_type,
        domain=domain,
        difficulty=difficulty,
        session_type=session_type,
        status="in_progress",
        timed=timed,
        duration_seconds=duration_seconds if timed else None,
        questions=[q.id for q in questions],
        answers={},
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def record_answer(
    db: Session,
    session_id: int,
    question_id: int,
    answer: str,
    elapsed_ms: int,
) -> None:
    """Record an answer for a question in a session. Immutable: no-op if already recorded."""
    session = db.query(SatIeltsSession).filter(SatIeltsSession.id == session_id).first()
    if not session:
        return

    answers: dict = dict(session.answers or {})
    key = str(question_id)

    # Immutability: if already answered, do nothing
    if key in answers:
        return

    answers[key] = {"answer": answer, "elapsed_ms": elapsed_ms}
    session.answers = answers
    db.commit()


def _score_session(session: SatIeltsSession, db: Session) -> tuple[int, int]:
    """Compute (correct_count, total) for a session by checking answers against questions."""
    question_ids = session.questions or []
    answers = session.answers or {}

    if not question_ids:
        return 0, 0

    questions = (
        db.query(SatIeltsQuestion)
        .filter(SatIeltsQuestion.id.in_(question_ids))
        .all()
    )
    q_map = {str(q.id): q for q in questions}

    correct = 0
    total = len(question_ids)

    for qid in question_ids:
        key = str(qid)
        q = q_map.get(key)
        if q is None:
            continue
        recorded = answers.get(key)
        if not recorded:
            continue
        user_answer = recorded.get("answer", "").strip()
        if q.question_type == "mcq" and q.correct_answer:
            if user_answer == q.correct_answer.strip():
                correct += 1
        # short_answer / essay: credit only if exact match (rubric-based grading is async)
        elif q.question_type == "short_answer" and q.correct_answer:
            if user_answer.lower() == q.correct_answer.strip().lower():
                correct += 1
        # essay: skip automatic scoring

    return correct, total


def finalise_session(db: Session, session_id: int) -> SatIeltsSession:
    """Compute score/total/score_pct, mark completed_at, set status=completed."""
    session = db.query(SatIeltsSession).filter(SatIeltsSession.id == session_id).first()
    if not session:
        raise ValueError(f"Session {session_id} not found")

    if session.status == "completed":
        return session

    correct, total = _score_session(session, db)
    score_pct = round(correct / total * 100, 2) if total > 0 else 0.0

    session.score = correct
    session.total = total
    session.score_pct = score_pct
    session.status = "completed"
    session.completed_at = datetime.now(tz=timezone.utc)
    db.commit()
    db.refresh(session)
    return session


def auto_submit_expired_session(db: Session, session_id: int) -> SatIeltsSession:
    """Mark unanswered questions as empty (incorrect), then finalise."""
    session = db.query(SatIeltsSession).filter(SatIeltsSession.id == session_id).first()
    if not session:
        raise ValueError(f"Session {session_id} not found")

    if session.status == "completed":
        return session

    answers: dict = dict(session.answers or {})
    for qid in session.questions or []:
        key = str(qid)
        if key not in answers:
            # Record empty answer — will be scored as incorrect
            answers[key] = {"answer": "", "elapsed_ms": 0}

    session.answers = answers
    session.status = "expired"
    db.commit()

    return finalise_session(db, session_id)


def compute_domain_accuracy(sessions: list[SatIeltsSession]) -> dict[str, float]:
    """Aggregate per-domain accuracy across a list of completed sessions.

    Returns a dict mapping domain name -> accuracy (0.0–1.0).
    Only considers completed sessions that have non-null score/total data.
    Since per-question domain data lives in the questions table (not the session),
    this function uses the session-level domain field as a proxy. For multi-domain
    sessions (domain=None), the session is skipped in the per-domain breakdown.
    """
    domain_correct: dict[str, int] = {}
    domain_total: dict[str, int] = {}

    for s in sessions:
        if s.status != "completed":
            continue
        if s.domain is None:
            continue  # multi-domain session — skip for per-domain breakdown
        if s.total is None or s.total == 0:
            continue

        d = s.domain
        domain_correct[d] = domain_correct.get(d, 0) + (s.score or 0)
        domain_total[d] = domain_total.get(d, 0) + s.total

    return {
        d: round(domain_correct[d] / domain_total[d], 4)
        for d in domain_total
        if domain_total[d] > 0
    }
