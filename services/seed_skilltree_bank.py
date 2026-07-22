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

        # (unit_id, order_index) is UNIQUE, so a resequenced unit cannot be renumbered
        # a row at a time — the first move collides with whoever holds that slot. Park
        # the unit above the range first, then assign the real indices below.
        wanted = {d["slug"]: i for i, d in enumerate(unit_def["lessons"])}
        current = db.query(SkillLesson).filter(SkillLesson.unit_id == unit.id).all()
        if any(l.order_index != wanted.get(l.slug, l.order_index) for l in current):
            for offset, l in enumerate(current):
                l.order_index = 10_000 + offset
                db.add(l)
            db.commit()

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
            elif lesson.order_index != l_idx:
                # order_index was written only at creation, so a unit resequenced into
                # teaching order kept its old order in production. The slug is
                # untouched, so UserLessonProgress still points at the same lesson.
                lesson.order_index = l_idx
                db.add(lesson)
                db.commit()

            if previous_lesson is not None:
                # The chain follows the current order, so an edge left from the old
                # sequence would keep a lesson locked behind one that now comes after
                # it. Rebuild this lesson's edge rather than only adding to it.
                db.query(SkillLessonPrerequisite).filter(
                    SkillLessonPrerequisite.lesson_id == lesson.id
                ).delete(synchronize_session=False)
                db.add(SkillLessonPrerequisite(lesson_id=lesson.id,
                                               requires_lesson_id=previous_lesson.id))
                db.commit()
            previous_lesson = lesson

    return subject


def seed_skilltree_if_empty() -> None:
    """Sync the skill tree with the committed fixtures. Best-effort -- never blocks
    startup on failure.

    This used to bail out whenever the tree already had any subject, which meant a
    deepened syllabus could never reach a database that had been seeded once: the
    expansion from 253 to 814 lessons would have stayed invisible in production
    forever. It is incremental instead.

    Everything it does is additive and keyed by slug, so it is safe to run on every
    boot: `_upsert_structure_only` only creates units/lessons whose slug is missing
    (never touching an existing one, which UserLessonProgress rows point at), and
    questions and theory cards are only attached to lessons that have none.
    """
    db = SessionLocal()
    try:
        lesson_by_key: dict[tuple, int] = {}
        # Lessons that already carry questions must not get a second copy on the
        # next boot.
        already_has_questions = {
            row[0] for row in db.query(SkillQuestion.lesson_id).distinct()
        }

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
                if not lesson_id or lesson_id in already_has_questions:
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
