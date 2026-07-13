"""Re-tag under-labelled SAT questions onto real taxonomy skills.

Imported/seeded questions frequently arrive with a placeholder skill — "General"
(the Reading & Writing import fallback), the domain name itself (the Math import
fallback, e.g. skill "Algebra" inside domain "Algebra"), or null. Such questions
never show up under any topic in the Question Bank. This assigns every one of
them a real taxonomy skill:

  • Math questions are classified by their CONTENT (keywords: "circle" -> Circles,
    "percent" -> Percentages, "sin/cos/tan" -> Right triangles and trigonometry …),
    so they land in the topic they actually belong to.
  • Anything a keyword rule doesn't catch (all Reading & Writing "General", plus
    unmatched Math) is spread round-robin across its domain's skills so the topic
    counts stay balanced and no question is unreachable.

Deterministic (ordered by id) and idempotent — once every question carries a
valid skill for its domain it's a no-op.
"""
import logging

from services.db import SessionLocal
from services.models import SatIeltsQuestion
from services.sat_taxonomy import SAT_TAXONOMY

logger = logging.getLogger(__name__)


def clean_question_text() -> None:
    """Strip the stray leading "null" many seeded questions carry (a passage
    placeholder that got stringified), e.g. 'null\\n\\nIf $x...$' -> 'If $x...$'."""
    db = SessionLocal()
    fixed = 0
    try:
        rows = (
            db.query(SatIeltsQuestion)
            .filter(SatIeltsQuestion.question_text.like("null%"))
            .all()
        )
        for q in rows:
            cleaned = q.question_text
            if cleaned[:4].lower() == "null":
                cleaned = cleaned[4:].lstrip("\r\n \t")
            if cleaned and cleaned != q.question_text:
                q.question_text = cleaned
                fixed += 1
        if fixed:
            db.commit()
            logger.info("Cleaned leading 'null' from %d question texts.", fixed)
    except Exception as e:  # noqa: BLE001 — never block startup
        db.rollback()
        logger.warning("Question-text cleanup failed: %s", e)
    finally:
        db.close()


def _domain_skills() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for entries in SAT_TAXONOMY.values():
        for e in entries:
            if e["skills"]:
                out[e["domain"]] = list(e["skills"])
    return out


# Content keyword -> skill, per Math domain. Ordered MOST-SPECIFIC FIRST: the
# first rule whose any keyword appears in the (lower-cased) question text wins.
# Skill names here must exactly match services/sat_taxonomy.py.
_MATH_RULES: dict[str, list[tuple[list[str], str]]] = {
    "Geometry & Trigonometry": [
        (["circle", "radius", "radii", "diameter", "circumference", "arc length", " arc "], "Circles"),
        (["sin", "cos", "tan", "hypotenuse", "right triangle", "trigonom", "pythagor"], "Right triangles and trigonometry"),
        (["volume", "surface area", "cylinder", "sphere", "cube", "prism", "cone", "cubic"], "Area and volume"),
        (["angle", "triangle", "parallel", "perpendicular", "transversal", "congruent", "polygon", "quadrilateral", "vertices"], "Lines, angles, and triangles"),
    ],
    "Problem Solving & Data Analysis": [
        (["percent", "%", "discount", " tax", "markup"], "Percentages"),
        (["probability", "at random", "likelihood", " odds", "chance that"], "Probability"),
        (["margin of error", "randomly selected", "sample of", "survey", "population", "poll"], "Inference from statistics"),
        (["scatter", "line of best fit", "best fits", "correlat", "trend line"], "Two-variable data"),
        (["mean", "median", "mode", "standard deviation", "histogram", "box plot", "data set", "distribution", "average of"], "One-variable data"),
        (["ratio", " rate", "proportion", "per ", "for every", "miles per", "unit rate"], "Ratios, rates, and proportions"),
        (["claim", "experiment", "concluded that", "cause", "generaliz"], "Evaluating statistical claims"),
    ],
    "Advanced Math": [
        (["parabola", "quadratic", "x^2", "x²", "vertex of", "roots of"], "Nonlinear functions"),
        (["exponential", "^x", "polynomial", "cubic", "radical", "square root of", "system of nonlinear"], "Nonlinear equations and systems"),
        (["equivalent", "simplif", "factor", "expand", "rewrite the expression"], "Equivalent expressions"),
    ],
    "Algebra": [
        (["inequalit", "≤", "≥", "at least", "at most", "less than or equal", "greater than or equal"], "Linear inequalities"),
        (["system of", "two equations", "system of equations"], "Systems of two linear equations"),
        (["slope", "f(x)", "y-intercept", "rate of change", "the function"], "Linear functions"),
        (["two variables", "ax + by", "line passes through", "x and y"], "Linear equations in two variables"),
    ],
}


def _classify_math(text: str, domain: str, valid: set[str]) -> str | None:
    """Return the taxonomy skill whose keyword rule the text matches, or None."""
    rules = _MATH_RULES.get(domain)
    if not rules:
        return None
    low = (text or "").lower()
    for keywords, skill in rules:
        if skill in valid and any(k in low for k in keywords):
            return skill
    return None


def retag_general_questions() -> None:
    """Assign every placeholder-skill SAT question a real taxonomy skill —
    Math by content, everything else round-robin across the domain's skills."""
    skills_by_domain = _domain_skills()
    db = SessionLocal()
    updated = 0
    try:
        for domain, skills in skills_by_domain.items():
            valid = set(skills)
            rows = (
                db.query(SatIeltsQuestion)
                .filter(SatIeltsQuestion.exam_type == "SAT")
                .filter(SatIeltsQuestion.domain == domain)
                .order_by(SatIeltsQuestion.id)
                .all()
            )
            # "Unassigned" = skill isn't one of this domain's real skills
            # (null, blank, "General", or the domain name used as a skill).
            unassigned = [q for q in rows if (q.skill or "") not in valid]
            rr = 0  # round-robin cursor for questions no keyword rule catches
            for q in unassigned:
                skill = _classify_math(q.question_text, domain, valid)
                if skill is None:
                    skill = skills[rr % len(skills)]
                    rr += 1
                q.skill = skill
                updated += 1
        if updated:
            db.commit()
            logger.info("Re-tagged %d placeholder-skill questions onto taxonomy skills.", updated)
    except Exception as e:  # noqa: BLE001 — never block startup
        db.rollback()
        logger.warning("Question re-tag failed: %s", e)
    finally:
        db.close()
