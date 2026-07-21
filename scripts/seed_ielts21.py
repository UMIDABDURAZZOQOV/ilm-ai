"""
seed_ielts21.py — load scripts/seeds/ielts21.json into the IELTS tables.

Replaces the whole Cambridge 21 set on every run (matched by the "Cambridge 21 Test n"
title prefix), so re-running after a parser fix never duplicates rows.

    python scripts/seed_ielts21.py [--dry-run]
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.db import SessionLocal, engine, Base          # noqa: E402
from services.models import (                               # noqa: E402
    IeltsListening, IeltsReading, IeltsWriting, IeltsSpeaking, IeltsQuestion,
)

SEED_PATH = os.path.join(os.path.dirname(__file__), "seeds", "ielts21.json")
PREFIX = "Cambridge 21 Test"


def wipe(db, legacy: bool = False) -> None:
    """Delete our own rows; with `legacy`, also the first (broken) extraction's rows.

    That first pass left 16 reading rows holding nothing but "You should spend about 20
    minutes on", transcripts truncated to exactly 800 characters, and zero questions.
    """
    for model in (IeltsListening, IeltsReading, IeltsWriting, IeltsSpeaking):
        title = model_title(model)
        rows = db.query(model).filter(
            title.like(f"{PREFIX}%") if not legacy else True  # noqa: E712
        ).all()
        skill = "Listening" if model is IeltsListening else "Reading"
        if model in (IeltsListening, IeltsReading):
            ids = [r.id for r in rows]
            if ids:
                db.query(IeltsQuestion).filter(
                    IeltsQuestion.skill == skill, IeltsQuestion.parent_id.in_(ids)
                ).delete(synchronize_session=False)
            if legacy:
                db.query(IeltsQuestion).filter(IeltsQuestion.skill == skill).delete(
                    synchronize_session=False)
        for r in rows:
            db.delete(r)
    db.flush()


def model_title(model):
    """The column that carries our "Cambridge 21 Test n" tag on each table."""
    return {
        IeltsListening: IeltsListening.title,
        IeltsReading: IeltsReading.title,
        IeltsWriting: IeltsWriting.category,
        IeltsSpeaking: IeltsSpeaking.topic,
    }[model]


def add_questions(db, skill: str, parent_id: int, questions: list[dict]) -> int:
    for q in questions:
        db.add(IeltsQuestion(
            skill=skill,
            parent_id=parent_id,
            question_type=q["question_type"],
            question_text=q["question_text"],
            options=q.get("options"),
            correct_answer=q.get("correct_answer") or "",
            hint=q.get("group_instruction") or None,
            order_index=q["number"],
        ))
    return len(questions)


def main() -> int:
    dry = "--dry-run" in sys.argv
    legacy = "--purge-legacy" in sys.argv
    with open(SEED_PATH, encoding="utf-8") as fh:
        data = json.load(fh)

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    counts = {"listening": 0, "reading": 0, "writing": 0, "speaking": 0, "questions": 0}
    try:
        wipe(db, legacy=legacy)

        for test in data["tests"]:
            n = test["test"]

            for sec in test["listening"]:
                # Resolved at parse time — the mp3s are not on the server.
                urls = sec.get("audio_parts") or []
                row = IeltsListening(
                    section=sec["section"],
                    title=f"{PREFIX} {n} — Listening Part {sec['section']}: {sec['title']}"[:300],
                    audio_url=urls[0] if urls else None,
                    audio_parts=urls if len(urls) > 1 else None,
                    transcript=sec["transcript"] or None,
                    difficulty="medium",
                    duration_seconds=None,
                )
                db.add(row)
                db.flush()
                counts["questions"] += add_questions(db, "Listening", row.id, sec["questions"])
                counts["listening"] += 1

            for sec in test["reading"]:
                row = IeltsReading(
                    section=sec["section"],
                    title=f"{PREFIX} {n} — Reading Passage {sec['section']}: {sec['title']}"[:300],
                    passage_text=sec["passage_text"],
                    difficulty="medium",
                    word_count=sec["word_count"],
                )
                db.add(row)
                db.flush()
                counts["questions"] += add_questions(db, "Reading", row.id, sec["questions"])
                counts["reading"] += 1

            for task in test["writing"]:
                db.add(IeltsWriting(
                    task_type=task["task_type"],
                    category=f"{PREFIX} {n}",
                    prompt=task["prompt"],
                    image_url=None,
                    min_words=task["min_words"],
                    duration_minutes=task["duration_minutes"],
                    difficulty="medium",
                ))
                counts["writing"] += 1

            for part in test["speaking"]:
                db.add(IeltsSpeaking(
                    part=part["part"],
                    topic=f"{PREFIX} {n} — Part {part['part']}: {part['topic']}"[:300],
                    questions=part["questions"],
                    cue_card=part["cue_card"],
                    prep_seconds=part["prep_seconds"],
                    speak_seconds=part["speak_seconds"],
                    difficulty="medium",
                ))
                counts["speaking"] += 1

        if dry:
            db.rollback()
            print("dry run — rolled back")
        else:
            db.commit()
        print(counts)
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
