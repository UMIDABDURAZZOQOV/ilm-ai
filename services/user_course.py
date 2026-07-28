"""
Turn a learner's own uploaded materials into a structured mini-course: chapters →
lessons → checkpoint questions, a Duolingo-style path generated from their PDFs
rather than a fixed syllabus. The course outline is built once (cheap-ish, one
Gemini call) and stored; each lesson's questions are generated on demand so we
don't spend tokens on lessons the learner never opens.
"""
from __future__ import annotations

import json
import re

from services.db import SessionLocal
from services.models import UserCourse
from services.quiz_engine import load_vectors
from services.gemini import generate_content as gemini_generate

MAX_MATERIAL_CHARS = 14000


def _parse_json(text: str) -> dict:
    cleaned = (text or "").strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned[:4].lower() == "json":
            cleaned = cleaned[4:]
    m = re.search(r"[\{\[].*[\}\]]", cleaned, re.DOTALL)
    if m:
        cleaned = m.group(0)
    return json.loads(cleaned)


def _material_text(user_id: int) -> tuple[str, list[str]]:
    vectors = load_vectors(user_id)
    if not vectors:
        return "", []
    files = list({v.get("filename", "") for v in vectors if v.get("filename")})
    chunks = [v.get("text", "") for v in vectors if v.get("text")]
    text = "\n\n".join(chunks)
    return text[:MAX_MATERIAL_CHARS], files


def generate_course(user_id: int, language: str = "uz") -> dict:
    """Build (and store) the course outline from the learner's materials. Returns
    {"error": ...} when they have uploaded nothing."""
    text, files = _material_text(user_id)
    if not text:
        return {"error": "no_materials"}

    prompt = (
        f"You are Ilm AI, building a structured self-study course from a learner's OWN uploaded "
        f"materials. Read the material below and organise it into a logical learning path.\n\n"
        f"Rules:\n"
        f"- 3 to 6 chapters, each with 2 to 4 lessons, ordered from foundational to advanced.\n"
        f"- Every lesson must be grounded in the material (don't invent topics not present).\n"
        f"- Each lesson needs a short 1-2 sentence summary of what it teaches.\n"
        f"- Write all titles and summaries in this language: {language}.\n"
        f"- Return ONLY this JSON, no markdown fences:\n"
        f'{{\"title\": \"course title\", \"chapters\": [{{\"title\": \"chapter\", \"lessons\": '
        f'[{{\"title\": \"lesson\", \"summary\": \"what it teaches\"}}]}}]}}\n\n'
        f"MATERIAL:\n{text}"
    )
    try:
        resp = gemini_generate(
            model="gemini-flash-latest",
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )
        data = _parse_json(resp.text)
    except Exception:
        return {"error": "generation_failed"}

    chapters = data.get("chapters") or []
    if not chapters:
        return {"error": "generation_failed"}
    course = {
        "title": data.get("title") or "Mening kursim",
        "chapters": chapters,
        "sources": files,
    }
    _save_course(user_id, course)
    return course


def _save_course(user_id: int, course: dict) -> None:
    db = SessionLocal()
    try:
        row = db.query(UserCourse).filter(UserCourse.user_id == user_id).first()
        if row:
            row.course = course
            row.progress = {}
        else:
            db.add(UserCourse(user_id=user_id, course=course, progress={}))
        db.commit()
    finally:
        db.close()


def load_course(user_id: int) -> dict | None:
    db = SessionLocal()
    try:
        row = db.query(UserCourse).filter(UserCourse.user_id == user_id).first()
        if not row:
            return None
        return {"course": row.course, "progress": row.progress or {}}
    finally:
        db.close()


def set_lesson_progress(user_id: int, lesson_key: str, score: int) -> dict:
    db = SessionLocal()
    try:
        row = db.query(UserCourse).filter(UserCourse.user_id == user_id).first()
        if not row:
            return {}
        progress = dict(row.progress or {})
        progress[lesson_key] = {"completed": True, "score": score}
        row.progress = progress
        db.commit()
        return progress
    finally:
        db.close()


def generate_lesson_questions(
    user_id: int, chapter_title: str, lesson_title: str, lesson_summary: str, language: str = "uz"
) -> list[dict]:
    """On-demand MCQs for one lesson, grounded in the learner's material."""
    text, _ = _material_text(user_id)
    context = text[:8000]
    prompt = (
        f"You are Ilm AI. Write 5 multiple-choice questions to check understanding of this lesson, "
        f"based ONLY on the learner's material below. Language: {language}.\n"
        f"Chapter: {chapter_title}\nLesson: {lesson_title}\nWhat it teaches: {lesson_summary}\n\n"
        f"Return ONLY this JSON, no fences:\n"
        f'{{\"questions\": [{{\"question\": \"...\", \"options\": [\"a\",\"b\",\"c\",\"d\"], '
        f'\"correct_answer\": \"exact text of the correct option\", \"explanation\": \"one sentence\"}}]}}\n\n'
        f"MATERIAL:\n{context}"
    )
    try:
        resp = gemini_generate(
            model="gemini-flash-latest",
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )
        data = _parse_json(resp.text)
    except Exception:
        return []
    out = []
    for q in data.get("questions", []):
        opts = q.get("options") or []
        ans = q.get("correct_answer", "")
        if q.get("question") and len(opts) >= 2 and ans:
            out.append({
                "question": q["question"],
                "options": opts,
                "correct_answer": ans,
                "explanation": q.get("explanation", ""),
            })
    return out
