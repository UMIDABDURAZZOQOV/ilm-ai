"""Auto-seed the Milliy Sertifikat skill tree on startup, from the reviewed
fixture JSON dumped by scripts/seed_skilltree.py -- mirrors services/seed_bank.py.
Production never calls Gemini live; this just loads the committed static content.
"""
import json
import logging
import os

from services.db import SessionLocal
from services.models import (
    SkillLesson,
    SkillLessonPrerequisite,
    SkillQuestion,
    SkillSubject,
    SkillUnit,
)
from services.skilltree_taxonomy import SKILLTREE_OUTLINE

logger = logging.getLogger(__name__)

_SEEDS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "seeds")


def _upsert_structure_only(db, subject_slug: str, subject_def: dict) -> SkillSubject:
    """Same structure-upsert as scripts/seed_skilltree.py's upsert_structure,
    but without any Gemini call -- just subjects/units/lessons/prerequisites."""
    subject = db.query(SkillSubject).filter(SkillSubject.slug == subject_slug).first()
    if not subject:
        subject = SkillSubject(
            slug=subject_slug,
            name_uz=subject_def["name"]["uz"],
            name_ru=subject_def["name"]["ru"],
            name_en=subject_def["name"]["en"],
            icon=subject_def.get("icon"),
            color=subject_def.get("color"),
            order_index=list(SKILLTREE_OUTLINE.keys()).index(subject_slug),
        )
        db.add(subject)
        db.commit()
        db.refresh(subject)

    previous_lesson = None
    for u_idx, unit_def in enumerate(subject_def["units"]):
        unit = (
            db.query(SkillUnit)
            .filter(SkillUnit.subject_id == subject.id, SkillUnit.slug == unit_def["slug"])
            .first()
        )
        if not unit:
            unit = SkillUnit(
                subject_id=subject.id,
                slug=unit_def["slug"],
                title_uz=unit_def["title"]["uz"],
                title_ru=unit_def["title"]["ru"],
                title_en=unit_def["title"]["en"],
                order_index=u_idx,
            )
            db.add(unit)
            db.commit()
            db.refresh(unit)

        for l_idx, lesson_def in enumerate(unit_def["lessons"]):
            lesson = (
                db.query(SkillLesson)
                .filter(SkillLesson.unit_id == unit.id, SkillLesson.slug == lesson_def["slug"])
                .first()
            )
            if not lesson:
                lesson = SkillLesson(
                    unit_id=unit.id,
                    slug=lesson_def["slug"],
                    title_uz=lesson_def["title"]["uz"],
                    title_ru=lesson_def["title"]["ru"],
                    title_en=lesson_def["title"]["en"],
                    order_index=l_idx,
                    xp_reward=10,
                )
                db.add(lesson)
                db.commit()
                db.refresh(lesson)

            if previous_lesson is not None:
                exists = (
                    db.query(SkillLessonPrerequisite)
                    .filter(
                        SkillLessonPrerequisite.lesson_id == lesson.id,
                        SkillLessonPrerequisite.requires_lesson_id == previous_lesson.id,
                    )
                    .first()
                )
                if not exists:
                    db.add(SkillLessonPrerequisite(lesson_id=lesson.id, requires_lesson_id=previous_lesson.id))
                    db.commit()
            previous_lesson = lesson

    return subject


def seed_skilltree_if_empty() -> None:
    """Bulk-load subjects/units/lessons + fixture questions when the skill
    tree is empty. Best-effort -- never blocks startup on failure."""
    db = SessionLocal()
    try:
        existing = db.query(SkillSubject).count()
        if existing > 0:
            return

        lesson_by_key: dict[tuple, int] = {}

        for subject_slug, subject_def in SKILLTREE_OUTLINE.items():
            subject = _upsert_structure_only(db, subject_slug, subject_def)
            for unit in db.query(SkillUnit).filter(SkillUnit.subject_id == subject.id).all():
                for lesson in db.query(SkillLesson).filter(SkillLesson.unit_id == unit.id).all():
                    lesson_by_key[(subject_slug, unit.slug, lesson.slug)] = lesson.id

            fixture_path = os.path.join(_SEEDS_DIR, f"skilltree_{subject_slug}.json")
            if not os.path.exists(fixture_path):
                logger.warning("Skill tree structure seeded but fixture missing at %s", fixture_path)
                continue

            with open(fixture_path, "r", encoding="utf-8") as f:
                rows = json.load(f)

            mappings = []
            for r in rows:
                key = (r.get("subject_slug"), r.get("unit_slug"), r.get("lesson_slug"))
                lesson_id = lesson_by_key.get(key)
                if not lesson_id:
                    continue
                mappings.append({
                    "lesson_id": lesson_id,
                    "order_index": r.get("order_index", 0),
                    "language": r.get("language", "uz"),
                    "question_type": "mcq",
                    "question_text": r.get("question_text"),
                    "options": r.get("options"),
                    "correct_answer": r.get("correct_answer"),
                    "explanation": r.get("explanation"),
                    "difficulty": r.get("difficulty", "medium"),
                })
            if mappings:
                db.bulk_insert_mappings(SkillQuestion, mappings)
                db.commit()
                logger.info("Seeded %s skill-tree questions for subject %s.", len(mappings), subject_slug)

            # Teaching cards (learn-first phase), from the theory fixture.
            theory_path = os.path.join(_SEEDS_DIR, f"skilltree_theory_{subject_slug}.json")
            if os.path.exists(theory_path):
                with open(theory_path, "r", encoding="utf-8") as f:
                    theory_rows = json.load(f)
                applied = 0
                for r in theory_rows:
                    key = (r.get("subject_slug"), r.get("unit_slug"), r.get("lesson_slug"))
                    lesson_id = lesson_by_key.get(key)
                    if not lesson_id or not r.get("theory"):
                        continue
                    lesson = db.query(SkillLesson).filter(SkillLesson.id == lesson_id).first()
                    if lesson and not lesson.theory:
                        lesson.theory = r["theory"]
                        db.add(lesson)
                        applied += 1
                if applied:
                    db.commit()
                    logger.info("Seeded theory cards for %s lessons in subject %s.", applied, subject_slug)
    except Exception as e:  # noqa: BLE001 -- never block startup on seeding
        db.rollback()
        logger.warning("Skill tree auto-seed failed: %s", e)
    finally:
        db.close()
