"""
dump_skilltree_fixtures.py — re-export the skill-tree fixtures straight from the DB.

seed_skilltree.py only writes a subject's fixture once it finishes that subject, so a
run stopped by the daily quota leaves the committed fixtures behind the database —
and production seeds from the fixtures, not the database. This dumps every subject's
current content without calling Gemini at all, so whatever has been generated so far
can be deployed.

    PYTHONIOENCODING=utf-8 python scripts/dump_skilltree_fixtures.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.db import SessionLocal                                    # noqa: E402
from services.models import (                                           # noqa: E402
    SkillLesson, SkillQuestion, SkillSubject, SkillUnit,
)

SEEDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seeds")


def main() -> int:
    os.makedirs(SEEDS_DIR, exist_ok=True)
    db = SessionLocal()
    try:
        for subject in db.query(SkillSubject).order_by(SkillSubject.order_index).all():
            questions: list[dict] = []
            theory: list[dict] = []

            units = (db.query(SkillUnit)
                     .filter(SkillUnit.subject_id == subject.id)
                     .order_by(SkillUnit.order_index).all())
            for unit in units:
                lessons = (db.query(SkillLesson)
                           .filter(SkillLesson.unit_id == unit.id)
                           .order_by(SkillLesson.order_index).all())
                for lesson in lessons:
                    if lesson.theory:
                        theory.append({
                            "subject_slug": subject.slug,
                            "unit_slug": unit.slug,
                            "lesson_slug": lesson.slug,
                            "theory": lesson.theory,
                        })
                    rows = (db.query(SkillQuestion)
                            .filter(SkillQuestion.lesson_id == lesson.id)
                            .order_by(SkillQuestion.order_index).all())
                    for q in rows:
                        questions.append({
                            "subject_slug": subject.slug,
                            "unit_slug": unit.slug,
                            "lesson_slug": lesson.slug,
                            "order_index": q.order_index,
                            "language": q.language,
                            "question_text": q.question_text,
                            "options": q.options,
                            "correct_answer": q.correct_answer,
                            "explanation": q.explanation,
                            "difficulty": q.difficulty,
                        })

            with open(os.path.join(SEEDS_DIR, f"skilltree_{subject.slug}.json"), "w", encoding="utf-8") as fh:
                json.dump(questions, fh, ensure_ascii=False, indent=1)
            with open(os.path.join(SEEDS_DIR, f"skilltree_theory_{subject.slug}.json"), "w", encoding="utf-8") as fh:
                json.dump(theory, fh, ensure_ascii=False, indent=1)
            print(f"{subject.slug:18} {len(questions):>5} questions  {len(theory):>4} lessons with theory")
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
