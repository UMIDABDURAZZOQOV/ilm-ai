"""
Ilm AI Studio — power tools built on the learner's OWN uploaded materials:

  photo_kit()      -- one photo of a page  -> summary + flashcards + quiz
  audio_recap()    -- materials            -> a spoken-style recap script (for TTS)
  knowledge_map()  -- materials            -> a concept graph (nodes + edges)
  cheat_sheet()    -- materials            -> a one-page markdown study sheet
  mock_from_materials() -- materials       -> a longer exam-style MCQ set

Everything is grounded in what the learner uploaded, so the study aids are about
their actual course, not generic content.
"""
from __future__ import annotations

import json
import re

from google.genai import types

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


def material_text(user_id: int, filename: str | None = None) -> tuple[str, list[str]]:
    vectors = load_vectors(user_id)
    if not vectors:
        return "", []
    if filename:
        scoped = [v for v in vectors if v.get("filename") == filename]
        if scoped:
            vectors = scoped
    files = list({v.get("filename", "") for v in vectors if v.get("filename")})
    text = "\n\n".join(v.get("text", "") for v in vectors if v.get("text"))
    return text[:MAX_MATERIAL_CHARS], files


def _guess_image_mime(content_type: str | None, filename: str | None) -> str:
    if content_type and content_type != "application/octet-stream":
        return content_type
    name = (filename or "").lower()
    if name.endswith(".png"):
        return "image/png"
    if name.endswith(".webp"):
        return "image/webp"
    if name.endswith(".heic"):
        return "image/heic"
    return "image/jpeg"


# ─── Photo -> full study kit ──────────────────────────────────────────────────

def photo_kit(image_bytes: bytes, content_type: str | None, filename: str | None, language: str = "uz") -> dict:
    prompt = (
        f"You are Ilm AI. The image is a page of study material (textbook, notes, slides). "
        f"Read it and turn it into a complete study kit in this language: {language}.\n"
        f"Return ONLY this JSON, no fences:\n"
        f'{{\"title\": \"short topic title\", \"summary\": \"4-6 sentence clear summary of the page\", '
        f'\"flashcards\": [{{\"front\": \"term/question\", \"back\": \"answer\"}}], '
        f'\"quiz\": [{{\"question\": \"...\", \"options\": [\"a\",\"b\",\"c\",\"d\"], '
        f'\"correct_answer\": \"exact correct option text\", \"explanation\": \"one sentence\"}}]}}\n'
        f"Make 5-8 flashcards and 4-6 quiz questions. If the image is unreadable, set summary to say so "
        f"and leave the lists empty."
    )
    part = types.Part.from_bytes(data=image_bytes, mime_type=_guess_image_mime(content_type, filename))
    try:
        resp = gemini_generate(
            model="gemini-flash-latest",
            contents=[prompt, part],
            config={"response_mime_type": "application/json"},
        )
        data = _parse_json(resp.text)
    except Exception:
        return {"error": "generation_failed"}
    return {
        "title": data.get("title", ""),
        "summary": data.get("summary", ""),
        "flashcards": [c for c in data.get("flashcards", []) if c.get("front") and c.get("back")],
        "quiz": [
            q for q in data.get("quiz", [])
            if q.get("question") and len(q.get("options", [])) >= 2 and q.get("correct_answer")
        ],
    }


# ─── Audio recap (script for TTS) ─────────────────────────────────────────────

def audio_recap(user_id: int, filename: str | None = None, language: str = "uz") -> dict:
    text, files = material_text(user_id, filename)
    if not text:
        return {"error": "no_materials"}
    prompt = (
        f"You are Ilm AI narrating a short audio recap of the learner's material — like a friendly "
        f"mini-podcast they can listen to on the go. Language: {language}. Write a natural, spoken-style "
        f"script (no headings, no bullet points, no markdown) that recaps the key ideas clearly in about "
        f"150-220 words. Just the words to be read aloud.\n\nMATERIAL:\n{text}"
    )
    try:
        resp = gemini_generate(model="gemini-flash-latest", contents=prompt)
        script = (resp.text or "").strip()
    except Exception:
        return {"error": "generation_failed"}
    if not script:
        return {"error": "generation_failed"}
    return {"script": script, "sources": files}


# ─── Knowledge map (concept graph) ────────────────────────────────────────────

def knowledge_map(user_id: int, language: str = "uz") -> dict:
    text, files = material_text(user_id)
    if not text:
        return {"error": "no_materials"}
    prompt = (
        f"You are Ilm AI. From the learner's material, build a concept map: the main concepts and how "
        f"they connect. Language: {language}. 8-16 nodes. Group related concepts with a short 'group' "
        f"label. Return ONLY this JSON, no fences:\n"
        f'{{\"nodes\": [{{\"id\": \"c1\", \"label\": \"concept\", \"group\": \"theme\"}}], '
        f'\"edges\": [{{\"from\": \"c1\", \"to\": \"c2\", \"label\": \"relation (optional)\"}}]}}\n\n'
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
    nodes = [n for n in data.get("nodes", []) if n.get("id") and n.get("label")]
    node_ids = {n["id"] for n in nodes}
    edges = [
        e for e in data.get("edges", [])
        if e.get("from") in node_ids and e.get("to") in node_ids and e.get("from") != e.get("to")
    ]
    if not nodes:
        return {"error": "generation_failed"}
    return {"nodes": nodes, "edges": edges, "sources": files}


# ─── One-page cheat sheet (markdown) ──────────────────────────────────────────

def cheat_sheet(user_id: int, filename: str | None = None, language: str = "uz") -> dict:
    text, files = material_text(user_id, filename)
    if not text:
        return {"error": "no_materials"}
    prompt = (
        f"You are Ilm AI. Condense the learner's material into a ONE-PAGE cheat sheet in Markdown. "
        f"Language: {language}. Use short sections with headings, bullet points, key formulas/definitions "
        f"in bold, and only the highest-yield facts — the sheet a student would keep for last-minute review. "
        f"Return only the Markdown.\n\nMATERIAL:\n{text}"
    )
    try:
        resp = gemini_generate(model="gemini-flash-latest", contents=prompt)
        md = (resp.text or "").strip()
    except Exception:
        return {"error": "generation_failed"}
    if not md:
        return {"error": "generation_failed"}
    return {"markdown": md, "sources": files}


# ─── Mock test from materials ─────────────────────────────────────────────────

def mock_from_materials(user_id: int, language: str = "uz", n: int = 15) -> dict:
    text, files = material_text(user_id)
    if not text:
        return {"error": "no_materials"}
    prompt = (
        f"You are Ilm AI. Write a {n}-question mock exam (multiple choice) covering the learner's material "
        f"broadly, mixing easy and hard. Language: {language}. Return ONLY this JSON, no fences:\n"
        f'{{\"questions\": [{{\"question\": \"...\", \"options\": [\"a\",\"b\",\"c\",\"d\"], '
        f'\"correct_answer\": \"exact correct option text\", \"explanation\": \"one sentence\"}}]}}\n\n'
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
    questions = [
        q for q in data.get("questions", [])
        if q.get("question") and len(q.get("options", [])) >= 2 and q.get("correct_answer")
    ]
    if not questions:
        return {"error": "generation_failed"}
    return {"questions": questions, "sources": files}
