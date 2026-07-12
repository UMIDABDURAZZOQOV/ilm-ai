import json
import os
from datetime import date, datetime, timedelta
from typing import Any, Optional

from services.users import USE_DB
from services.db import SessionLocal
from services.models import ReviewItem

DATA_DIR = "data/review_items"
os.makedirs(DATA_DIR, exist_ok=True)

REVIEW_INTERVALS = [1, 3, 7, 14, 30]
PASS_THRESHOLD = 0.7


def _path(user_id: int) -> str:
    return f"{DATA_DIR}/user_{user_id}.json"


def _row_to_dict(row: ReviewItem) -> dict[str, Any]:
    return {
        "id": row.id,
        "user_id": row.user_id,
        "topic": row.topic,
        "source_material": row.source_material,
        "next_review_date": row.next_review_date,
        "interval_stage": row.interval_stage,
        "last_result": row.last_result,
    }


def _load_file(user_id: int) -> list[dict[str, Any]]:
    path = _path(user_id)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        return json.loads(content) if content else []


def _save_file(user_id: int, items: list[dict[str, Any]]) -> None:
    with open(_path(user_id), "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def upsert_weak_topics(user_id: int, topics: list[str], source_material: Optional[str] = None) -> None:
    """Schedule newly-identified weak topics for review. Leaves any topic that
    already has a pending review item alone — don't reset an in-progress schedule
    just because it shows up in another Gaps Report."""
    if not topics:
        return
    today = date.today().isoformat()

    if USE_DB:
        db = SessionLocal()
        try:
            existing = {
                r.topic.strip().lower()
                for r in db.query(ReviewItem).filter(ReviewItem.user_id == user_id).all()
            }
            for topic in topics:
                if not topic or topic.strip().lower() in existing:
                    continue
                db.add(ReviewItem(
                    user_id=user_id,
                    topic=topic,
                    source_material=source_material,
                    next_review_date=today,
                    interval_stage=0,
                ))
            db.commit()
        finally:
            db.close()
        return

    items = _load_file(user_id)
    existing = {i["topic"].strip().lower() for i in items}
    next_id = max((i["id"] for i in items), default=0) + 1
    for topic in topics:
        if not topic or topic.strip().lower() in existing:
            continue
        items.append({
            "id": next_id,
            "user_id": user_id,
            "topic": topic,
            "source_material": source_material,
            "next_review_date": today,
            "interval_stage": 0,
            "last_result": None,
        })
        next_id += 1
    _save_file(user_id, items)


def list_due(user_id: int) -> list[dict[str, Any]]:
    today = date.today().isoformat()
    if USE_DB:
        db = SessionLocal()
        try:
            rows = (
                db.query(ReviewItem)
                .filter(ReviewItem.user_id == user_id, ReviewItem.next_review_date <= today)
                .order_by(ReviewItem.next_review_date.asc())
                .all()
            )
            return [_row_to_dict(r) for r in rows]
        finally:
            db.close()

    return [i for i in _load_file(user_id) if i["next_review_date"] <= today]


def complete_review(item_id: int, user_id: int, score: int, total: int) -> Optional[dict[str, Any]]:
    passed = total > 0 and (score / total) >= PASS_THRESHOLD
    today = date.today()

    if USE_DB:
        db = SessionLocal()
        try:
            row = db.query(ReviewItem).filter(ReviewItem.id == item_id, ReviewItem.user_id == user_id).first()
            if not row:
                return None
            if passed:
                row.interval_stage = min(row.interval_stage + 1, len(REVIEW_INTERVALS) - 1)
            else:
                row.interval_stage = 0
            interval_days = REVIEW_INTERVALS[row.interval_stage]
            row.next_review_date = (today + timedelta(days=interval_days)).isoformat()
            row.last_result = "correct" if passed else "incorrect"
            row.last_reviewed_at = datetime.utcnow()
            db.add(row)
            db.commit()
            db.refresh(row)
            return _row_to_dict(row)
        finally:
            db.close()

    items = _load_file(user_id)
    item = next((i for i in items if i["id"] == item_id), None)
    if not item:
        return None
    if passed:
        item["interval_stage"] = min(item["interval_stage"] + 1, len(REVIEW_INTERVALS) - 1)
    else:
        item["interval_stage"] = 0
    interval_days = REVIEW_INTERVALS[item["interval_stage"]]
    item["next_review_date"] = (today + timedelta(days=interval_days)).isoformat()
    item["last_result"] = "correct" if passed else "incorrect"
    _save_file(user_id, items)
    return item


def count_due_by_user() -> dict[int, int]:
    """Used by the push-notification scheduler: {user_id: due_count} for every
    user with at least one review item due today."""
    today = date.today().isoformat()
    counts: dict[int, int] = {}

    if USE_DB:
        db = SessionLocal()
        try:
            rows = db.query(ReviewItem).filter(ReviewItem.next_review_date <= today).all()
            for r in rows:
                counts[r.user_id] = counts.get(r.user_id, 0) + 1
            return counts
        finally:
            db.close()

    for fname in os.listdir(DATA_DIR):
        if not fname.startswith("user_") or not fname.endswith(".json"):
            continue
        try:
            user_id = int(fname[len("user_"):-len(".json")])
        except ValueError:
            continue
        due = [i for i in _load_file(user_id) if i["next_review_date"] <= today]
        if due:
            counts[user_id] = len(due)
    return counts
