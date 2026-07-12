"""
question_bank.py — CRUD, validation and selection helpers for SAT/IELTS questions.
"""
from __future__ import annotations

import random
import time
from typing import Optional

from sqlalchemy.orm import Session

from services.models import SatIeltsQuestion

REQUIRED_FIELDS = ["exam_type", "domain", "difficulty", "question_type", "question_text"]
VALID_EXAM_TYPES = {"SAT", "IELTS"}
VALID_DIFFICULTIES = {"easy", "medium", "hard"}
VALID_QUESTION_TYPES = {"mcq", "short_answer", "essay"}


def validate_question(q: dict) -> tuple[bool, str]:
    """Return (ok, error_message). Checks all required fields, MCQ option count, rubric rule."""
    # Required fields presence
    for field in REQUIRED_FIELDS:
        if not q.get(field):
            return False, f"Missing required field: {field}"

    # Enum validation
    if q["exam_type"] not in VALID_EXAM_TYPES:
        return False, f"exam_type must be one of {VALID_EXAM_TYPES}"
    if q["difficulty"] not in VALID_DIFFICULTIES:
        return False, f"difficulty must be one of {VALID_DIFFICULTIES}"
    if q["question_type"] not in VALID_QUESTION_TYPES:
        return False, f"question_type must be one of {VALID_QUESTION_TYPES}"

    q_type = q["question_type"]

    if q_type == "mcq":
        options = q.get("options")
        if not options or len(options) != 4:
            return False, "MCQ questions must have exactly 4 options"
        correct = q.get("correct_answer")
        if not correct:
            return False, "MCQ questions must have a correct_answer"
        if correct not in options:
            return False, "correct_answer must be one of the options"
    else:
        # short_answer or essay
        if not q.get("rubric") and not q.get("correct_answer"):
            return False, f"{q_type} questions must have a rubric or correct_answer"

    return True, ""


def add_question(db: Session, q_in: dict) -> SatIeltsQuestion:
    """Validate then insert a question into the database. Raises ValueError on invalid input."""
    ok, err = validate_question(q_in)
    if not ok:
        raise ValueError(err)

    question = SatIeltsQuestion(
        exam_type=q_in["exam_type"],
        domain=q_in["domain"],
        skill=q_in.get("skill"),
        difficulty=q_in["difficulty"],
        question_type=q_in["question_type"],
        question_text=q_in["question_text"],
        options=q_in.get("options"),
        correct_answer=q_in.get("correct_answer"),
        rubric=q_in.get("rubric"),
        source_filename=q_in.get("source_filename"),
        tags=q_in.get("tags", []),
        created_by=q_in.get("created_by"),
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def get_questions(
    db: Session,
    exam_type: Optional[str] = None,
    domain: Optional[str] = None,
    skill: Optional[str] = None,
    difficulty: Optional[str] = None,
    question_type: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    exclude_ids: Optional[list[int]] = None,
) -> list[SatIeltsQuestion]:
    """Filter questions from the bank."""
    q = db.query(SatIeltsQuestion)
    if exam_type:
        q = q.filter(SatIeltsQuestion.exam_type == exam_type)
    if domain:
        q = q.filter(SatIeltsQuestion.domain == domain)
    if skill:
        q = q.filter(SatIeltsQuestion.skill == skill)
    if difficulty:
        q = q.filter(SatIeltsQuestion.difficulty == difficulty)
    if question_type:
        q = q.filter(SatIeltsQuestion.question_type == question_type)
    if exclude_ids:
        q = q.filter(SatIeltsQuestion.id.notin_(exclude_ids))
    return q.offset(offset).limit(limit).all()


def select_questions_for_session(
    db: Session,
    exam_type: str,
    domain: Optional[str],
    difficulty: str,
    count: int,
    exclude_ids: Optional[list[int]] = None,
    skill: Optional[str] = None,
    section: Optional[str] = None,
) -> list[SatIeltsQuestion]:
    """Random sample of min(count, available) questions matching the given params.

    When ``section`` is given (e.g. "Reading & Writing"), the pool is restricted
    to that section's domains only — so a section/mock test never interleaves
    Math and Reading questions the way a plain mixed pull would.

    Falls back to difficulty-agnostic (then skill-agnostic) pools rather than
    returning nothing — a thin bank shouldn't hard-fail a practice request."""
    # Section filter: gather questions across all domains in the section, then
    # difficulty is treated as a soft preference (mock tests want a full spread).
    if section and not domain:
        from services.sat_taxonomy import get_section_domains

        section_domains = set(get_section_domains(exam_type, section))
        if section_domains:
            all_q = get_questions(
                db, exam_type=exam_type, limit=2000, exclude_ids=exclude_ids,
            )
            pool = [q for q in all_q if q.domain in section_domains]
            k = min(count, len(pool))
            return random.sample(pool, k) if k > 0 else []

    pool = get_questions(
        db,
        exam_type=exam_type,
        domain=domain,
        skill=skill,
        difficulty=difficulty,
        limit=1000,  # pull a large pool then random-sample
        exclude_ids=exclude_ids,
    )
    if not pool:
        pool = get_questions(
            db, exam_type=exam_type, domain=domain, skill=skill,
            limit=1000, exclude_ids=exclude_ids,
        )
    if not pool and skill:
        pool = get_questions(
            db, exam_type=exam_type, domain=domain,
            limit=1000, exclude_ids=exclude_ids,
        )
    k = min(count, len(pool))
    return random.sample(pool, k) if k > 0 else []


def generate_questions_from_materials(
    user_id: int,
    exam_type: str,
    domain: str,
    difficulty: str,
    num_questions: int,
    db: Session,
) -> list[SatIeltsQuestion]:
    """Use existing RAG vectors + Gemini to produce questions, tag them, persist."""
    from services.quiz_engine import load_vectors, client, _parse_json_response
    import random as _random

    vectors = load_vectors(user_id)
    if not vectors:
        return []

    chunks = [v["text"] for v in vectors]
    selected = _random.sample(chunks, min(5, len(chunks)))
    context = "\n\n---\n\n".join(selected)

    # Clamp num_questions to [5, 20] per spec
    num_questions = max(5, min(20, num_questions))

    prompt = f"""You are an expert {exam_type} question writer.
Generate exactly {num_questions} {difficulty} {exam_type} questions for the domain "{domain}" based on the following context.

CONTEXT:
{context}

Return a JSON array of question objects with this schema:
[
  {{
    "question_type": "mcq" | "short_answer",
    "question_text": "...",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],  // only for mcq, exactly 4
    "correct_answer": "...",
    "rubric": null | "...",  // required for short_answer
    "tags": ["tag1", "tag2"]
  }}
]
Return ONLY valid JSON, no extra text."""

    from services.monitoring import log_llm_call

    start = time.time()
    try:
        response = client.models.generate_content(model="gemini-flash-latest", contents=prompt)
    except Exception:
        return []

    latency_ms = int((time.time() - start) * 1000)
    log_llm_call(
        user_id=user_id,
        prompt=prompt,
        response_text=response.text,
        latency_ms=latency_ms,
        model="gemini-flash-latest",
    )

    try:
        raw = _parse_json_response(response.text)
        if isinstance(raw, dict):
            # Sometimes Gemini wraps in {"questions": [...]}
            raw = raw.get("questions", [])
    except Exception:
        return []

    created: list[SatIeltsQuestion] = []
    source_fname = f"user_{user_id}_materials"
    for item in raw:
        q_in = {
            "exam_type": exam_type,
            "domain": domain,
            "difficulty": difficulty,
            "question_type": item.get("question_type", "mcq"),
            "question_text": item.get("question_text", ""),
            "options": item.get("options"),
            "correct_answer": item.get("correct_answer"),
            "rubric": item.get("rubric"),
            "source_filename": source_fname,
            "tags": item.get("tags", [exam_type, domain, difficulty]),
            "created_by": user_id,
        }
        ok, _ = validate_question(q_in)
        if ok:
            try:
                q = add_question(db, q_in)
                created.append(q)
            except Exception:
                continue

    return created
