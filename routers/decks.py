"""
routers/decks.py -- saved flashcard decks with spaced-repetition review. Cards are
stored inline on the deck; each carries an SRS `stage` and a `due` datetime. A
correct review advances the interval, a wrong one resets it.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from services.auth_deps import ensure_own_user, get_authenticated_user_id, verify_user_access
from services.db import get_db
from services.models import FlashcardDeck

router = APIRouter(prefix="/decks", tags=["decks"])

# Same ladder the skill-tree mistakes use, so review behaviour is consistent.
SRS_INTERVALS = [1, 3, 7, 16, 35]
MAX_DECKS = 60


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _is_due(card: dict, now: datetime) -> bool:
    due = card.get("due")
    if not due:
        return True
    try:
        return datetime.fromisoformat(due) <= now
    except ValueError:
        return True


class CardIn(BaseModel):
    front: str
    back: str


class CreateDeck(BaseModel):
    user_id: int
    title: str
    cards: list[CardIn]


@router.post("")
def create_deck(data: CreateDeck, auth_user_id: int = Depends(get_authenticated_user_id), db: Session = Depends(get_db)):
    ensure_own_user(data.user_id, auth_user_id)
    cards = [{"front": c.front.strip(), "back": c.back.strip(), "stage": 0, "due": None}
             for c in data.cards if c.front.strip() and c.back.strip()]
    if not cards:
        raise HTTPException(status_code=400, detail="no_cards")

    existing = db.query(FlashcardDeck).filter(FlashcardDeck.user_id == data.user_id).order_by(FlashcardDeck.id.asc()).all()
    for old in existing[: max(0, len(existing) + 1 - MAX_DECKS)]:
        db.delete(old)

    deck = FlashcardDeck(user_id=data.user_id, title=(data.title or "Deck")[:200], cards=cards)
    db.add(deck)
    db.commit()
    db.refresh(deck)
    return {"id": deck.id, "title": deck.title, "total": len(cards)}


@router.get("/{user_id}")
def list_decks(user_id: int = Depends(verify_user_access), db: Session = Depends(get_db)):
    now = _now()
    decks = db.query(FlashcardDeck).filter(FlashcardDeck.user_id == user_id).order_by(FlashcardDeck.id.desc()).all()
    out = []
    for d in decks:
        cards = d.cards or []
        out.append({
            "id": d.id,
            "title": d.title,
            "total": len(cards),
            "due": sum(1 for c in cards if _is_due(c, now)),
        })
    return {"decks": out}


@router.get("/{user_id}/{deck_id}")
def get_due(user_id: int = Depends(verify_user_access), deck_id: int = 0, db: Session = Depends(get_db)):
    deck = db.query(FlashcardDeck).filter(FlashcardDeck.id == deck_id, FlashcardDeck.user_id == user_id).first()
    if not deck:
        raise HTTPException(status_code=404, detail="not_found")
    now = _now()
    cards = deck.cards or []
    due = [{"index": i, "front": c["front"], "back": c["back"]} for i, c in enumerate(cards) if _is_due(c, now)]
    return {"title": deck.title, "cards": due, "total": len(cards)}


class ReviewResult(BaseModel):
    index: int
    correct: bool


class ReviewRequest(BaseModel):
    user_id: int
    deck_id: int
    results: list[ReviewResult]


@router.post("/review")
def review(data: ReviewRequest, auth_user_id: int = Depends(get_authenticated_user_id), db: Session = Depends(get_db)):
    ensure_own_user(data.user_id, auth_user_id)
    deck = db.query(FlashcardDeck).filter(FlashcardDeck.id == data.deck_id, FlashcardDeck.user_id == data.user_id).first()
    if not deck:
        raise HTTPException(status_code=404, detail="not_found")
    cards = list(deck.cards or [])
    now = _now()
    for r in data.results:
        if not (0 <= r.index < len(cards)):
            continue
        card = dict(cards[r.index])
        if r.correct:
            stage = min(len(SRS_INTERVALS) - 1, int(card.get("stage", 0)) + 1)
            days = SRS_INTERVALS[stage]
        else:
            stage = 0
            days = 1
        card["stage"] = stage
        card["due"] = (now + timedelta(days=days)).isoformat()
        cards[r.index] = card
    deck.cards = cards   # new list identity → tracked as a change
    db.commit()
    return {"ok": True, "due": sum(1 for c in cards if _is_due(c, now))}


@router.delete("/{user_id}/{deck_id}")
def delete_deck(user_id: int = Depends(verify_user_access), deck_id: int = 0, db: Session = Depends(get_db)):
    deck = db.query(FlashcardDeck).filter(FlashcardDeck.id == deck_id, FlashcardDeck.user_id == user_id).first()
    if deck:
        db.delete(deck)
        db.commit()
    return {"ok": True}
