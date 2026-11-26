"""Laboratory work and practical sessions are not taught in the app.

Owner decision, 2026-11-26: the app is for gaining knowledge at home, where
nobody can run a school laboratory, so every textbook "laboratoriya ishi" and
"amaliy mashg‘ulot" is withheld in every subject. Withheld lessons never block the next lesson, are never started, are
not counted in progress, and the tutor does not quote them. Their reviewed
content, imported rows and any earlier learner progress stay untouched, so the
decision can be reversed by emptying ``WITHHELD_KINDS``. The rule applies to the
published app routes (``routers/beta_mobile.py`` marks their session); local
authoring previews and course-coverage checks still see every lesson.

The textbooks' own catalogues mark these topics with ``kind`` "laboratory",
"practical" or "home_practical": Biology 40 + 11, Physics 31 + 4 + 1 and
Chemistry 49 + 15, i.e. 151 authored lessons. History has none. Problem-solving
sections (Physics "problem_practice") are knowledge work and stay.
"""
import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "scripts" / "curriculum"
CATALOGS = (
    "physics/physics_sources.json",
    "chemistry/chemistry_sources.json",
    "biology_sources.json",
)
WITHHELD_KINDS = frozenset({"laboratory", "practical", "home_practical"})


def _records(node):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from _records(value)
    elif isinstance(node, list):
        for value in node:
            yield from _records(value)


@lru_cache(maxsize=1)
def withheld_topic_ids():
    ids = set()
    for relative in CATALOGS:
        catalog = json.loads((ROOT / relative).read_text(encoding="utf8"))
        for record in _records(catalog):
            if isinstance(record.get("id"), str) and record.get("kind") in WITHHELD_KINDS:
                ids.add(record["id"])
    return frozenset(ids)


FLAG = "withhold_laboratory"


def is_withheld(topic_id, db):
    """Only the published app withholds labs; authoring previews still see them."""
    return bool(db.info.get(FLAG)) and topic_id in withheld_topic_ids()


def withholding(db_dependency):
    """Router dependency that marks the request's session as the published app."""
    from fastapi import Depends

    def dependency(db=Depends(db_dependency)):
        db.info[FLAG] = True
        try:
            yield
        finally:
            db.info.pop(FLAG, None)

    return dependency
