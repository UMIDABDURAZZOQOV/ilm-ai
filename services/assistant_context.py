"""
Everything that turns the general-purpose companion into a tutor that knows the
learner. Four capabilities, all funnelled into one Gemini call by assistant.py:

  1. build_student_context()   -- who the learner is (goal, exam countdown, weak
                                   areas, placement levels, streak/XP).
  2. retrieve_material_context()-- RAG over the learner's uploaded materials
                                   (the VectorEntry embeddings), so the companion
                                   answers FROM their own PDFs, not just in general.
  3. load_memories/save_*       -- durable facts remembered across sessions.
  4. parse_tags()               -- pulls the optional <remember>…</remember> and
                                   <action …/> tags the model may emit, so a single
                                   response can both teach and act.
"""
from __future__ import annotations

import math
import re
from datetime import date, datetime, timezone

from services.db import SessionLocal
from services.models import (
    AssistantMemory,
    SkillMistake,
    SkillQuestion,
    SkillLesson,
    User,
    UserLanguageLevel,
)

MAX_MEMORIES = 30


# ─── 1. Personalization ───────────────────────────────────────────────────────

def build_student_context(user_id: int) -> str:
    """A compact, high-signal profile block. Kept short on purpose — enough for the
    companion to feel personal without bloating (or leaking a wall of) the prompt."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return ""
        bits: list[str] = []
        if user.name:
            bits.append(f"Ismi: {user.name}")
        if user.learning_goal:
            bits.append(f"Maqsadi: {user.learning_goal}")

        raw = (user.target_date or "").strip()
        if raw:
            try:
                target = datetime.strptime(raw, "%Y-%m-%d").date()
                days = (target - date.today()).days
                if days >= 0:
                    bits.append(f"Imtihongacha: {days} kun ({raw})")
            except ValueError:
                pass

        if user.streak_days:
            bits.append(f"Streak: {user.streak_days} kun")
        if user.xp_total:
            bits.append(f"XP: {user.xp_total}")

        # Placement levels (English/Korean/French).
        levels = db.query(UserLanguageLevel).filter(UserLanguageLevel.user_id == user_id).all()
        for lv in levels:
            bits.append(f"{lv.subject_slug} darajasi: {lv.level}")

        # Weakest areas: subjects/lessons with the most unresolved mistakes.
        weak = _weak_areas(db, user_id)
        if weak:
            bits.append("Zaif mavzular: " + ", ".join(weak))

        if not bits:
            return ""
        return "\n\nO'QUVCHI HAQIDA (shaxsiy repetitor sifatida shundan foydalan):\n- " + "\n- ".join(bits)
    finally:
        db.close()


def _weak_areas(db, user_id: int, limit: int = 3) -> list[str]:
    """Lesson titles the learner has the most open mistakes in — the companion uses
    these to steer help toward what actually trips them up."""
    rows = (
        db.query(SkillLesson.title_uz, SkillMistake.id)
        .join(SkillQuestion, SkillQuestion.id == SkillMistake.question_id)
        .join(SkillLesson, SkillLesson.id == SkillQuestion.lesson_id)
        .filter(SkillMistake.user_id == user_id, SkillMistake.resolved_at.is_(None))
        .all()
    )
    if not rows:
        return []
    counts: dict[str, int] = {}
    for title, _ in rows:
        if title:
            counts[title] = counts.get(title, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
    return [title for title, _ in ranked[:limit]]


# ─── 2. RAG over uploaded materials ───────────────────────────────────────────

def _cosine(a: list[float], b: list[float]) -> float:
    if not a or not b:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


def _embed(text: str) -> list[float] | None:
    try:
        from services.gemini import embed_content as gemini_embed
        result = gemini_embed(model="gemini-embedding-001", contents=[text])
        return list(result.embeddings[0].values)
    except Exception:
        return None


def retrieve_material_context(user_id: int, query: str, k: int = 4) -> tuple[str, list[str]]:
    """Top-k chunks from the learner's uploaded materials most relevant to the
    question. Returns (context_block, filenames_used). Empty when the learner has
    uploaded nothing or the query can't be embedded — the companion then just
    answers from general knowledge instead of failing."""
    from services.quiz_engine import load_vectors

    vectors = load_vectors(user_id)
    if not vectors:
        return "", []

    q_emb = _embed(query)
    if not q_emb:
        return "", []

    scored = []
    for v in vectors:
        emb = v.get("embedding")
        if emb:
            scored.append((_cosine(q_emb, emb), v))
    if not scored:
        return "", []
    scored.sort(key=lambda s: s[0], reverse=True)

    # Only keep chunks that are actually related — a low top score means the
    # question isn't about their materials, so we add nothing.
    top = [v for score, v in scored[:k] if score > 0.55]
    if not top:
        return "", []

    files = list({v.get("filename", "") for v in top if v.get("filename")})
    blocks = []
    for v in top:
        fn = v.get("filename", "material")
        blocks.append(f"[{fn}]\n{v.get('text', '')}")
    context = (
        "\n\nO'QUVCHI YUKLAGAN MATERIALDAN TEGISHLI PARCHALAR (javobni shularga asosla; "
        "agar javob shu yerda bo'lsa, aynan shundan foydalan va manbani ayt):\n"
        + "\n\n---\n\n".join(blocks)
    )
    return context, files


# ─── 3. Long-term memory ──────────────────────────────────────────────────────

def load_memories(user_id: int) -> list[str]:
    db = SessionLocal()
    try:
        rows = (
            db.query(AssistantMemory)
            .filter(AssistantMemory.user_id == user_id)
            .order_by(AssistantMemory.id.asc())
            .all()
        )
        return [r.content for r in rows]
    finally:
        db.close()


def memories_block(user_id: int) -> str:
    mems = load_memories(user_id)
    if not mems:
        return ""
    return "\n\nAVVALGI SUHBATLARDAN ESLAB QOLGANLARING:\n- " + "\n- ".join(mems)


def save_memory(user_id: int, content: str) -> None:
    content = content.strip()
    if not content:
        return
    db = SessionLocal()
    try:
        # Skip near-duplicates so the same fact isn't stored twice.
        existing = {
            m.content.strip().lower()
            for m in db.query(AssistantMemory).filter(AssistantMemory.user_id == user_id).all()
        }
        if content.lower() in existing:
            return
        db.add(AssistantMemory(user_id=user_id, content=content))
        # Cap the store: drop the oldest beyond MAX_MEMORIES.
        rows = (
            db.query(AssistantMemory)
            .filter(AssistantMemory.user_id == user_id)
            .order_by(AssistantMemory.id.asc())
            .all()
        )
        for old in rows[: max(0, len(rows) + 1 - MAX_MEMORIES)]:
            db.delete(old)
        db.commit()
    finally:
        db.close()


def clear_memories(user_id: int) -> None:
    db = SessionLocal()
    try:
        db.query(AssistantMemory).filter(AssistantMemory.user_id == user_id).delete()
        db.commit()
    finally:
        db.close()


# ─── 4. Tag parsing (memory + action, emitted inline in one response) ─────────

_REMEMBER_RE = re.compile(r"<remember>(.*?)</remember>", re.DOTALL | re.IGNORECASE)
_ACTION_RE = re.compile(
    r"""<action\s+label=["'](?P<label>[^"']+)["']\s+href=["'](?P<href>[^"']+)["']\s*/?>""",
    re.IGNORECASE,
)

# The companion may only route to these in-app destinations — a closed list so it
# can't invent broken links. "/dashboard" also covers its panels via ?panel=…
# (quiz, files, flashcards, chat, plans, gaps, review), handled by parse_tags below.
ALLOWED_ROUTES = (
    "/dashboard",
    "/skills",
    "/skills/progress",
    "/course",
    "/studio",
    "/ielts",
    "/sat",
    "/sat/planner",
)


def parse_tags(text: str) -> tuple[str, list[str], dict | None]:
    """Split the model's reply into (clean_text, new_memories, action|None)."""
    memories = [m.strip() for m in _REMEMBER_RE.findall(text) if m.strip()]

    action = None
    m = _ACTION_RE.search(text)
    if m:
        href = m.group("href").strip()
        if any(href == r or href.startswith(r + "?") or href.startswith(r + "/") for r in ALLOWED_ROUTES):
            action = {"label": m.group("label").strip(), "href": href}

    clean = _ACTION_RE.sub("", _REMEMBER_RE.sub("", text)).strip()
    return clean, memories, action
