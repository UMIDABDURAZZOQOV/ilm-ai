"""
routers/vocab.py -- IELTS dictionary + "My Starred Words".

Definitions come from the free Dictionary API (dictionaryapi.dev), which is built
on Wiktionary data — no licensing problem, unlike commercial dictionaries.
"Examples in IELTS" are pulled from OUR OWN passage corpus (ielts_reading /
ielts_listening), so a word is always shown in a context we're allowed to serve.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone

import requests
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from services.auth_deps import ensure_own_user, get_authenticated_user_id, verify_user_access
from services.db import get_db
from services.models import IeltsListening, IeltsReading, UserStarredWord

router = APIRouter(prefix="/vocab", tags=["vocab"])

DICT_API = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
MAX_IELTS_EXAMPLES = 12


@router.get("/define")
def define(word: str):
    """Definition, part of speech, inflections and examples for a single word."""
    w = (word or "").strip().lower()
    if not w or not re.fullmatch(r"[a-z][a-z\-' ]{0,40}", w):
        raise HTTPException(status_code=400, detail="Invalid word")

    try:
        resp = requests.get(DICT_API.format(word=w), timeout=12)
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="Dictionary service unavailable")

    if resp.status_code == 404:
        return {"word": w, "found": False, "senses": [], "phonetic": None}
    if resp.status_code >= 400:
        raise HTTPException(status_code=502, detail="Dictionary lookup failed")

    entries = resp.json()
    if not isinstance(entries, list) or not entries:
        return {"word": w, "found": False, "senses": [], "phonetic": None}

    phonetic = None
    senses: list[dict] = []
    for entry in entries:
        phonetic = phonetic or entry.get("phonetic")
        for meaning in entry.get("meanings", []):
            pos = meaning.get("partOfSpeech")
            for d in meaning.get("definitions", []):
                senses.append(
                    {
                        "part_of_speech": pos,
                        "definition": d.get("definition"),
                        "example": d.get("example"),
                        "synonyms": (d.get("synonyms") or [])[:6],
                    }
                )

    return {
        "word": entries[0].get("word", w),
        "found": bool(senses),
        "phonetic": phonetic,
        "senses": senses[:12],
    }


@router.get("/examples")
def ielts_examples(word: str, db: Session = Depends(get_db)):
    """Sentences containing `word`, taken from our own IELTS passages/transcripts,
    each labelled with where it came from."""
    w = (word or "").strip().lower()
    if not w:
        raise HTTPException(status_code=400, detail="Invalid word")

    pattern = re.compile(rf"\b{re.escape(w)}\w*\b", re.IGNORECASE)
    out: list[dict] = []

    def harvest(text: str | None, source: str):
        if not text or len(out) >= MAX_IELTS_EXAMPLES:
            return
        for sentence in re.split(r"(?<=[.!?])\s+", text):
            if len(out) >= MAX_IELTS_EXAMPLES:
                return
            s = sentence.strip()
            if 20 <= len(s) <= 300 and pattern.search(s):
                out.append({"sentence": s, "source": source})

    for r in db.query(IeltsReading).all():
        harvest(r.passage_text, f"Reading Passage {r.section}" + (f" — {r.title}" if getattr(r, "title", None) else ""))
    for l in db.query(IeltsListening).all():
        harvest(getattr(l, "transcript", None), f"Listening Section {l.section}")

    return {"word": w, "examples": out}


# ─── Starred words ───────────────────────────────────────────────────────────

class StarWordRequest(BaseModel):
    user_id: int
    word: str
    note: str | None = None


@router.get("/{user_id}/starred")
def list_starred(user_id: int = Depends(verify_user_access), db: Session = Depends(get_db)):
    rows = (
        db.query(UserStarredWord)
        .filter(UserStarredWord.user_id == user_id)
        .order_by(UserStarredWord.created_at.desc().nullslast())
        .all()
    )
    return {
        "words": [
            {"word": r.word, "note": r.note, "created_at": r.created_at.isoformat() if r.created_at else None}
            for r in rows
        ]
    }


@router.post("/starred")
def add_starred(
    data: StarWordRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    ensure_own_user(data.user_id, auth_user_id)
    w = (data.word or "").strip().lower()
    if not w:
        raise HTTPException(status_code=400, detail="Invalid word")

    row = (
        db.query(UserStarredWord)
        .filter(UserStarredWord.user_id == data.user_id, UserStarredWord.word == w)
        .first()
    )
    if not row:
        row = UserStarredWord(user_id=data.user_id, word=w, created_at=datetime.now(timezone.utc))
        db.add(row)
    row.note = data.note
    db.commit()
    return {"word": w, "starred": True}


@router.delete("/starred")
def remove_starred(
    user_id: int,
    word: str,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db),
):
    ensure_own_user(user_id, auth_user_id)
    w = (word or "").strip().lower()
    (
        db.query(UserStarredWord)
        .filter(UserStarredWord.user_id == user_id, UserStarredWord.word == w)
        .delete()
    )
    db.commit()
    return {"word": w, "starred": False}
