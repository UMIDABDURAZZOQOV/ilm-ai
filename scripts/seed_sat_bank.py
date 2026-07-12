"""Bulk-generate SAT questions per skill via Gemini and store them in the bank.

Usage (from the ilm-ai/ directory, when Gemini quota/billing allows):
    python scripts/seed_sat_bank.py                 # 10 per skill, all skills
    python scripts/seed_sat_bank.py --per-skill 25  # more per skill
    python scripts/seed_sat_bank.py --domain Algebra

Questions are validated before insert; duplicates are not detected, so run
sparingly or clear the bank first. Progress is printed per skill so an
interrupted run can be resumed with --domain.
"""

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from services.db import SessionLocal, engine, Base
from services.question_bank import validate_question, add_question
from services.sat_taxonomy import SAT_TAXONOMY

Base.metadata.create_all(bind=engine)

MODEL = os.environ.get("SEED_GEMINI_MODEL", "gemini-2.5-flash")


def _parse_json(text: str):
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    return json.loads(cleaned)


def generate_for_skill(client, domain: str, skill: str, count: int) -> list[dict]:
    prompt = f"""You are a senior item writer for the College Board Digital SAT.
Write exactly {count} ORIGINAL, exam-quality Digital SAT multiple-choice questions.

Target:
- Section/Domain: {domain}
- Skill: {skill}

Strict requirements — match a real Digital SAT question, not a textbook exercise:
- Difficulty spread: about 30% easy, 45% medium, 25% hard. Hard items must be
  genuinely hard (multi-step reasoning, subtle distractors), not just longer.
- Every question must be fully self-contained. For Reading & Writing skills,
  embed the short passage/stimulus (25-150 words) INSIDE question_text, then the
  question stem, exactly as the digital exam presents it.
- For Math, use realistic numbers and, where natural, real-world contexts
  (rates, data, geometry). Use plain text math notation (x^2, sqrt(), <=, >=,
  fractions as a/b). Do NOT use LaTeX or image references.
- Exactly 4 options, labelled "A) ", "B) ", "C) ", "D) ". Distractors must be
  plausible and reflect common student errors — never obviously wrong throwaways.
- correct_answer must be copied VERBATIM from one of the options (full "X) ..." string).
- rubric: a clear, step-by-step explanation of WHY the correct answer is right AND
  why the key distractors are wrong. This is what our AI tutor shows students, so
  make it genuinely instructive (2-5 sentences).
- All {count} questions must be distinct from one another (different numbers,
  contexts, and stems).

Return ONLY a valid JSON array, no prose, no markdown fences:
[
  {{
    "difficulty": "easy" | "medium" | "hard",
    "question_text": "...",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "correct_answer": "A) ...",
    "rubric": "..."
  }}
]"""

    response = client.models.generate_content(model=MODEL, contents=prompt)
    items = _parse_json(response.text)
    if isinstance(items, dict):
        items = items.get("questions", [])
    return items


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-skill", type=int, default=10)
    parser.add_argument("--domain", type=str, default=None)
    args = parser.parse_args()

    from google import genai
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    db = SessionLocal()
    # Pre-load existing question stems so re-runs don't create duplicates.
    from services.models import SatIeltsQuestion
    seen = {
        (qt or "").strip().lower()[:120]
        for (qt,) in db.query(SatIeltsQuestion.question_text)
        .filter(SatIeltsQuestion.exam_type == "SAT")
        .all()
    }
    total = 0
    try:
        for section, domains in SAT_TAXONOMY.items():
            for d in domains:
                if args.domain and d["domain"] != args.domain:
                    continue
                for skill in d["skills"]:
                    try:
                        items = generate_for_skill(client, d["domain"], skill, args.per_skill)
                    except Exception as exc:
                        print(f"FAILED {d['domain']} / {skill}: {exc}")
                        continue
                    inserted = 0
                    dupes = 0
                    for item in items:
                        text = (item.get("question_text") or "").strip()
                        key = text.lower()[:120]
                        if key in seen:
                            dupes += 1
                            continue
                        q_in = {
                            "exam_type": "SAT",
                            "domain": d["domain"],
                            "skill": skill,
                            "difficulty": item.get("difficulty", "medium"),
                            "question_type": "mcq",
                            "question_text": text,
                            "options": item.get("options"),
                            "correct_answer": item.get("correct_answer"),
                            "rubric": item.get("rubric"),
                            "source_filename": "gemini_seed",
                            "tags": ["SAT", d["domain"], skill],
                        }
                        ok, _ = validate_question(q_in)
                        if ok:
                            try:
                                add_question(db, q_in)
                                seen.add(key)
                                inserted += 1
                            except Exception:
                                continue
                    total += inserted
                    dupe_note = f" ({dupes} dupes skipped)" if dupes else ""
                    print(f"{d['domain']} / {skill}: +{inserted}{dupe_note}")
                    time.sleep(2)  # be gentle with rate limits
    finally:
        db.close()
    print(f"Done. Inserted {total} questions total.")


if __name__ == "__main__":
    main()
