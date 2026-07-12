"""Re-tag under-labelled SAT questions onto real taxonomy skills.

Most seeded questions were tagged with the placeholder skill "General" (or left
null), so they never showed up under any topic in the Question Bank — a domain
with 135 questions displayed only the ~30 that happened to carry a real skill
name. This spreads those questions evenly across their domain's taxonomy skills
so every question is reachable by topic. Deterministic (ordered by id) and
idempotent — once nothing is left as "General"/null it's a no-op.
"""
import logging

from services.db import SessionLocal
from services.models import SatIeltsQuestion
from services.sat_taxonomy import SAT_TAXONOMY

logger = logging.getLogger(__name__)


def _domain_skills() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for entries in SAT_TAXONOMY.values():
        for e in entries:
            if e["skills"]:
                out[e["domain"]] = list(e["skills"])
    return out


def retag_general_questions() -> None:
    """Distribute placeholder-skill SAT questions across their domain's skills."""
    skills_by_domain = _domain_skills()
    db = SessionLocal()
    updated = 0
    try:
        for domain, skills in skills_by_domain.items():
            # A question is "unassigned" if its skill is a placeholder — null,
            # blank, "General", or the domain name itself (Math questions were
            # seeded with skill == domain, e.g. skill "Algebra" in domain
            # "Algebra"), i.e. anything not one of the domain's real skills.
            valid = set(skills)
            rows = (
                db.query(SatIeltsQuestion)
                .filter(SatIeltsQuestion.exam_type == "SAT")
                .filter(SatIeltsQuestion.domain == domain)
                .order_by(SatIeltsQuestion.id)
                .all()
            )
            unassigned = [q for q in rows if (q.skill or "") not in valid]
            for i, q in enumerate(unassigned):
                q.skill = skills[i % len(skills)]
                updated += 1
        if updated:
            db.commit()
            logger.info("Re-tagged %d placeholder-skill questions onto taxonomy skills.", updated)
    except Exception as e:  # noqa: BLE001 — never block startup
        db.rollback()
        logger.warning("Question re-tag failed: %s", e)
    finally:
        db.close()
