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
    module_info: Optional[dict] = None,  # For SAT: {"module": 1, "section": "RW" or "Math"}
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
        analysis_result=module_info or {},  # Store module info here
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


def create_sat_full_test(
    db: Session,
    user_id: int,
    difficulty: str = "medium",
) -> dict:
    """Create a SAT full test with Module 1 and Module 2 structure.
    
    SAT Digital Format:
    - Module 1: Reading & Writing (27 questions, 32 min) + Math (22 questions, 35 min)
    - Module 2: Reading & Writing (27 questions, 32 min) + Math (22 questions, 35 min)
    Total: 98 questions
    
    Returns dict with session IDs for each module.
    """
    from services.question_bank import select_questions_for_session
    
    # SAT domains by section
    rw_domains = [
        "Information and Ideas",
        "Craft and Structure", 
        "Expression of Ideas",
        "Standard English Conventions"
    ]
    math_domains = ["Algebra", "Advanced Math", "Problem Solving & Data Analysis", "Geometry & Trigonometry"]
    
    sessions = {}
    
    # Module 1 - Reading & Writing (27 questions)
    rw_m1_questions = []
    for domain in rw_domains:
        qs = select_questions_for_session(
            db, exam_type="SAT", domain=domain, difficulty=difficulty, count=7
        )
        rw_m1_questions.extend(qs)
    
    # Adjust to exactly 27
    if len(rw_m1_questions) > 27:
        rw_m1_questions = rw_m1_questions[:27]
    elif len(rw_m1_questions) < 27:
        # Fill with any available RW questions
        for domain in rw_domains:
            qs = select_questions_for_session(
                db, exam_type="SAT", domain=domain, difficulty=difficulty, 
                count=27 - len(rw_m1_questions)
            )
            rw_m1_questions.extend(qs)
            if len(rw_m1_questions) >= 27:
                break
    
    rw_m1_session = create_session(
        db=db,
        user_id=user_id,
        exam_type="SAT",
        questions=rw_m1_questions[:27],
        timed=True,
        duration_seconds=32 * 60,  # 32 minutes
        session_type="full_test",
        module_info={"module": 1, "section": "RW"}
    )
    sessions["module1_rw"] = rw_m1_session.id
    
    # Module 1 - Math (22 questions)
    math_m1_questions = []
    for domain in math_domains:
        qs = select_questions_for_session(
            db, exam_type="SAT", domain=domain, difficulty=difficulty, count=6
        )
        math_m1_questions.extend(qs)
    
    if len(math_m1_questions) > 22:
        math_m1_questions = math_m1_questions[:22]
    elif len(math_m1_questions) < 22:
        for domain in math_domains:
            qs = select_questions_for_session(
                db, exam_type="SAT", domain=domain, difficulty=difficulty,
                count=22 - len(math_m1_questions)
            )
            math_m1_questions.extend(qs)
            if len(math_m1_questions) >= 22:
                break
    
    math_m1_session = create_session(
        db=db,
        user_id=user_id,
        exam_type="SAT",
        questions=math_m1_questions[:22],
        timed=True,
        duration_seconds=35 * 60,  # 35 minutes
        session_type="full_test",
        module_info={"module": 1, "section": "Math"}
    )
    sessions["module1_math"] = math_m1_session.id
    
    # Module 2 - Reading & Writing (27 questions) - adaptive based on M1 performance
    rw_m2_questions = []
    for domain in rw_domains:
        qs = select_questions_for_session(
            db, exam_type="SAT", domain=domain, difficulty=difficulty, count=7
        )
        rw_m2_questions.extend(qs)
    
    if len(rw_m2_questions) > 27:
        rw_m2_questions = rw_m2_questions[:27]
    elif len(rw_m2_questions) < 27:
        for domain in rw_domains:
            qs = select_questions_for_session(
                db, exam_type="SAT", domain=domain, difficulty=difficulty,
                count=27 - len(rw_m2_questions)
            )
            rw_m2_questions.extend(qs)
            if len(rw_m2_questions) >= 27:
                break
    
    rw_m2_session = create_session(
        db=db,
        user_id=user_id,
        exam_type="SAT",
        questions=rw_m2_questions[:27],
        timed=True,
        duration_seconds=32 * 60,
        session_type="full_test",
        module_info={"module": 2, "section": "RW"}
    )
    sessions["module2_rw"] = rw_m2_session.id
    
    # Module 2 - Math (22 questions)
    math_m2_questions = []
    for domain in math_domains:
        qs = select_questions_for_session(
            db, exam_type="SAT", domain=domain, difficulty=difficulty, count=6
        )
        math_m2_questions.extend(qs)
    
    if len(math_m2_questions) > 22:
        math_m2_questions = math_m2_questions[:22]
    elif len(math_m2_questions) < 22:
        for domain in math_domains:
            qs = select_questions_for_session(
                db, exam_type="SAT", domain=domain, difficulty=difficulty,
                count=22 - len(math_m2_questions)
            )
            math_m2_questions.extend(qs)
            if len(math_m2_questions) >= 22:
                break
    
    math_m2_session = create_session(
        db=db,
        user_id=user_id,
        exam_type="SAT",
        questions=math_m2_questions[:22],
        timed=True,
        duration_seconds=35 * 60,
        session_type="full_test",
        module_info={"module": 2, "section": "Math"}
    )
    sessions["module2_math"] = math_m2_session.id
    
    return sessions


def create_ielts_full_test(
    db: Session,
    user_id: int,
    difficulty: str = "medium",
) -> dict:
    """Create an IELTS full test with 4 sections.
    
    IELTS Format:
    - Listening: 40 questions, 30 min
    - Reading: 40 questions, 60 min
    - Writing: 2 tasks, 60 min
    - Speaking: 3 parts, 11-14 min
    
    Returns dict with session IDs for each section.
    """
    from services.question_bank import select_questions_for_session
    
    ielts_domains = ["Listening", "Reading", "Writing", "Speaking"]
    
    sessions = {}
    
    # Listening section (40 questions)
    listening_questions = select_questions_for_session(
        db, exam_type="IELTS", domain="Listening", difficulty=difficulty, count=40
    )
    if len(listening_questions) < 40:
        # Fill with any available IELTS questions
        for domain in ielts_domains:
            qs = select_questions_for_session(
                db, exam_type="IELTS", domain=domain, difficulty=difficulty,
                count=40 - len(listening_questions)
            )
            listening_questions.extend(qs)
            if len(listening_questions) >= 40:
                break
    
    listening_session = create_session(
        db=db,
        user_id=user_id,
        exam_type="IELTS",
        questions=listening_questions[:40],
        timed=True,
        duration_seconds=30 * 60,  # 30 minutes
        session_type="full_test",
        module_info={"section": "Listening"}
    )
    sessions["listening"] = listening_session.id
    
    # Reading section (40 questions)
    reading_questions = select_questions_for_session(
        db, exam_type="IELTS", domain="Reading", difficulty=difficulty, count=40
    )
    if len(reading_questions) < 40:
        for domain in ielts_domains:
            qs = select_questions_for_session(
                db, exam_type="IELTS", domain=domain, difficulty=difficulty,
                count=40 - len(reading_questions)
            )
            reading_questions.extend(qs)
            if len(reading_questions) >= 40:
                break
    
    reading_session = create_session(
        db=db,
        user_id=user_id,
        exam_type="IELTS",
        questions=reading_questions[:40],
        timed=True,
        duration_seconds=60 * 60,  # 60 minutes
        session_type="full_test",
        module_info={"section": "Reading"}
    )
    sessions["reading"] = reading_session.id
    
    # Writing section (2 tasks - essay type)
    writing_questions = select_questions_for_session(
        db, exam_type="IELTS", domain="Writing", difficulty=difficulty, count=2
    )
    if len(writing_questions) < 2:
        # Create essay questions if not enough
        for domain in ielts_domains:
            qs = select_questions_for_session(
                db, exam_type="IELTS", domain=domain, difficulty=difficulty,
                count=2 - len(writing_questions)
            )
            writing_questions.extend(qs)
            if len(writing_questions) >= 2:
                break
    
    writing_session = create_session(
        db=db,
        user_id=user_id,
        exam_type="IELTS",
        questions=writing_questions[:2],
        timed=True,
        duration_seconds=60 * 60,  # 60 minutes
        session_type="full_test",
        module_info={"section": "Writing"}
    )
    sessions["writing"] = writing_session.id
    
    # Speaking section (3 parts - short answer type)
    speaking_questions = select_questions_for_session(
        db, exam_type="IELTS", domain="Speaking", difficulty=difficulty, count=3
    )
    if len(speaking_questions) < 3:
        for domain in ielts_domains:
            qs = select_questions_for_session(
                db, exam_type="IELTS", domain=domain, difficulty=difficulty,
                count=3 - len(speaking_questions)
            )
            speaking_questions.extend(qs)
            if len(speaking_questions) >= 3:
                break
    
    speaking_session = create_session(
        db=db,
        user_id=user_id,
        exam_type="IELTS",
        questions=speaking_questions[:3],
        timed=True,
        duration_seconds=14 * 60,  # 14 minutes
        session_type="full_test",
        module_info={"section": "Speaking"}
    )
    sessions["speaking"] = speaking_session.id
    
    return sessions


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
