"""
skilltree_bank.py -- validation + insert helper for skill-tree questions.
Mirrors services/question_bank.py's validate_question/add_question shape.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from services.models import SkillQuestion

VALID_LANGUAGES = {"uz", "ru", "en"}
VALID_DIFFICULTIES = {"easy", "medium", "hard"}


def validate_question(q: dict) -> tuple[bool, str]:
    for field in ("lesson_id", "language", "question_text", "correct_answer"):
        if not q.get(field):
            return False, f"Missing required field: {field}"

    if q["language"] not in VALID_LANGUAGES:
        return False, f"language must be one of {VALID_LANGUAGES}"

    difficulty = q.get("difficulty", "medium")
    if difficulty not in VALID_DIFFICULTIES:
        return False, f"difficulty must be one of {VALID_DIFFICULTIES}"

    options = q.get("options")
    if not options or len(options) != 4:
        return False, "Questions must have exactly 4 options"
    if q["correct_answer"] not in options:
        return False, "correct_answer must be one of the options"

    return True, ""


def add_question(db: Session, q_in: dict) -> SkillQuestion:
    ok, err = validate_question(q_in)
    if not ok:
        raise ValueError(err)

    question = SkillQuestion(
        lesson_id=q_in["lesson_id"],
        order_index=q_in.get("order_index", 0),
        language=q_in["language"],
        question_type="mcq",
        question_text=q_in["question_text"],
        options=q_in.get("options"),
        correct_answer=q_in["correct_answer"],
        explanation=q_in.get("explanation"),
        difficulty=q_in.get("difficulty", "medium"),
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question
