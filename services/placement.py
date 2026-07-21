"""Placement-test scoring.

The old test drew 15 questions from the ordinary lesson bank and mapped the raw
percentage onto a CEFR band (90 → C1, 75 → B2, …). Two things were wrong with that:

1. Lesson questions are tagged easy/medium/hard *within their own lesson*, so a "hard"
   question from the A1 unit is still an A1 question. The bank was never calibrated to
   CEFR at all, which is why the result disagreed with other placement tests.
2. A single percentage cannot separate "answered every A1 question and no B2 question"
   from "answered half of each" — yet those are very different learners.

So the test now draws from a bank authored *at* each level (`PlacementQuestion`) and
reports the highest level the learner actually demonstrates: walk up from the bottom,
and stop at the first level they fail to master. A high score at a low level can never
be traded for a level the learner has not shown.
"""
from __future__ import annotations

# Ordered easiest → hardest. The first entry is the floor: a learner who masters
# nothing is placed there rather than being left without a level.
CEFR_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]
SUBJECT_LEVELS = ["daraja_1", "daraja_2", "daraja_3", "daraja_4", "daraja_5"]

LANGUAGE_SUBJECT_SLUGS = {"ingliz_tili", "koreys_tili", "fransuz_tili"}

# A level counts as mastered at 75%: high enough that guessing a 4-option question
# (25%) cannot reach it by luck over the 6-8 questions we ask per level, low enough
# that one careless slip does not drop a whole band.
MASTERY_PCT = 75.0
# Below this at the very first level the learner is a genuine beginner.
PARTIAL_PCT = 45.0

QUESTIONS_PER_LEVEL = 7          # 6 levels × 7 = 42 questions for a language test


def levels_for(subject_slug: str) -> list[str]:
    return CEFR_LEVELS if subject_slug in LANGUAGE_SUBJECT_SLUGS else SUBJECT_LEVELS


def level_label(subject_slug: str, level: str) -> str:
    if subject_slug in LANGUAGE_SUBJECT_SLUGS:
        return level
    return f"{SUBJECT_LEVELS.index(level) + 1}-daraja"


def score_placement(subject_slug: str, per_level: dict[str, tuple[int, int]]) -> dict:
    """Decide a level from {level: (correct, asked)}.

    Returns the awarded level plus the per-level breakdown, so the UI can show *why*
    it landed there instead of a bare band.
    """
    order = levels_for(subject_slug)
    breakdown = []
    for lvl in order:
        correct, asked = per_level.get(lvl, (0, 0))
        pct = (correct / asked * 100) if asked else 0.0
        breakdown.append({
            "level": lvl,
            "label": level_label(subject_slug, lvl),
            "correct": correct,
            "asked": asked,
            "pct": round(pct, 1),
            "mastered": asked > 0 and pct >= MASTERY_PCT,
        })

    awarded = order[0]
    for i, row in enumerate(breakdown):
        if row["asked"] == 0:
            continue
        if row["mastered"]:
            awarded = row["level"]
        else:
            # Partial credit at the level directly above the last mastered one is what
            # separates "solid B1" from "B1 and reaching into B2" — but it never skips
            # a level, so it cannot inflate the result.
            if row["pct"] >= PARTIAL_PCT and i > 0 and breakdown[i - 1]["mastered"]:
                awarded = row["level"]
            break

    total_correct = sum(r["correct"] for r in breakdown)
    total_asked = sum(r["asked"] for r in breakdown)
    return {
        "level": awarded,
        "label": level_label(subject_slug, awarded),
        "score": total_correct,
        "total": total_asked,
        "score_pct": round(total_correct / total_asked * 100, 1) if total_asked else 0.0,
        "breakdown": breakdown,
    }
