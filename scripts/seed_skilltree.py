"""Seed the Milliy Sertifikat skill tree: upsert the hand-authored unit/lesson
structure, then bulk-generate question content per lesson via Gemini.

Usage (from the ilm-ai/ directory):
    python scripts/seed_skilltree.py                       # all subjects
    python scripts/seed_skilltree.py --subject ona_tili
    python scripts/seed_skilltree.py --subject tarix --per-lesson 10

Content is generated in Uzbek only for v1: Ona tili questions are inherently
about the Uzbek language itself (a synonym/grammar question doesn't translate
meaningfully), and Tarix is taught in Uzbek in this app's curriculum context.
The `language` column on SkillQuestion is ready for ru/en content later
without a schema change.

Writes directly to the DB AND dumps a reviewable JSON fixture per subject to
scripts/seeds/skilltree_<subject>.json -- seed_skilltree_bank.py loads that
fixture at production startup so prod never calls Gemini live.
"""
import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from google import genai
from google.genai import types as genai_types

from services.db import SessionLocal, engine, Base
from services.models import SkillLesson, SkillLessonPrerequisite, SkillQuestion, SkillSubject, SkillUnit
from services.skilltree_bank import add_question, validate_question
from services.skilltree_taxonomy import SKILLTREE_OUTLINE

Base.metadata.create_all(bind=engine)

MODEL = os.environ.get("SEED_GEMINI_MODEL", "gemini-flash-latest")
SEEDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seeds")

# Explicit round-robin across all configured keys (rather than gemini.py's
# sticky-until-failure rotation) -- a bulk batch job like this concentrates
# far more requests per minute than normal traffic, so spreading load evenly
# across every key from the start avoids repeatedly hammering one key's 5rpm
# free-tier limit before rotating off it.
_KEYS = [k.strip() for k in (os.environ.get("GEMINI_API_KEYS") or os.environ.get("GEMINI_API_KEY", "")).split(",") if k.strip()]
# 60s timeout: without it a single stalled connection hangs the whole batch
# forever instead of failing over to the next key.
_CLIENTS = [genai.Client(api_key=k, http_options=genai_types.HttpOptions(timeout=60_000)) for k in _KEYS]
_key_index = 0


def _generate_round_robin(prompt: str):
    global _key_index
    if not _CLIENTS:
        raise RuntimeError("No GEMINI_API_KEYS / GEMINI_API_KEY configured")
    last_err = None
    for _ in range(len(_CLIENTS)):
        client = _CLIENTS[_key_index]
        idx = _key_index
        _key_index = (_key_index + 1) % len(_CLIENTS)
        try:
            return client.models.generate_content(model=MODEL, contents=prompt)
        except Exception as e:
            print(f"  key #{idx} failed: {e}")
            last_err = e
            continue
    raise last_err


def _parse_json(text: str):
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    return json.loads(cleaned)


def upsert_structure(db, subject_slug: str, subject_def: dict) -> SkillSubject:
    subject = db.query(SkillSubject).filter(SkillSubject.slug == subject_slug).first()
    if not subject:
        subject = SkillSubject(
            slug=subject_slug,
            name_uz=subject_def["name"]["uz"],
            name_ru=subject_def["name"]["ru"],
            name_en=subject_def["name"]["en"],
            icon=subject_def.get("icon"),
            color=subject_def.get("color"),
            order_index=len(SKILLTREE_OUTLINE.keys()) if subject_slug not in SKILLTREE_OUTLINE else list(SKILLTREE_OUTLINE.keys()).index(subject_slug),
        )
        db.add(subject)
        db.commit()
        db.refresh(subject)

    previous_lesson = None  # last lesson of the previous unit, for cross-unit chaining
    for u_idx, unit_def in enumerate(subject_def["units"]):
        unit = (
            db.query(SkillUnit)
            .filter(SkillUnit.subject_id == subject.id, SkillUnit.slug == unit_def["slug"])
            .first()
        )
        if not unit:
            unit = SkillUnit(
                subject_id=subject.id,
                slug=unit_def["slug"],
                title_uz=unit_def["title"]["uz"],
                title_ru=unit_def["title"]["ru"],
                title_en=unit_def["title"]["en"],
                order_index=u_idx,
            )
            db.add(unit)
            db.commit()
            db.refresh(unit)

        for l_idx, lesson_def in enumerate(unit_def["lessons"]):
            lesson = (
                db.query(SkillLesson)
                .filter(SkillLesson.unit_id == unit.id, SkillLesson.slug == lesson_def["slug"])
                .first()
            )
            if not lesson:
                lesson = SkillLesson(
                    unit_id=unit.id,
                    slug=lesson_def["slug"],
                    title_uz=lesson_def["title"]["uz"],
                    title_ru=lesson_def["title"]["ru"],
                    title_en=lesson_def["title"]["en"],
                    order_index=l_idx,
                    xp_reward=10,
                )
                db.add(lesson)
                db.commit()
                db.refresh(lesson)

            if previous_lesson is not None:
                exists = (
                    db.query(SkillLessonPrerequisite)
                    .filter(
                        SkillLessonPrerequisite.lesson_id == lesson.id,
                        SkillLessonPrerequisite.requires_lesson_id == previous_lesson.id,
                    )
                    .first()
                )
                if not exists:
                    db.add(SkillLessonPrerequisite(lesson_id=lesson.id, requires_lesson_id=previous_lesson.id))
                    db.commit()
            previous_lesson = lesson

    return subject


def generate_for_lesson(subject_name_uz: str, unit_title_uz: str, lesson_title_uz: str, count: int, theory: list[dict] | None = None) -> list[dict]:
    # Duolingo principle: never test what wasn't taught. The lesson's teaching
    # cards are embedded in the prompt so every question is answerable from them.
    theory_block = ""
    if theory:
        cards_text = "\n\n".join(
            f"KARTOCHKA {i + 1}: {c.get('title', '')}\n{c.get('body', '')}"
            + (f"\nMisol: {c['example']}" if c.get("example") else "")
            for i, c in enumerate(theory)
        )
        theory_block = f"""
O'quvchiga test oldidan FAQAT quyidagi o'quv kartochkalari o'rgatilgan:

{cards_text}

ENG MUHIM QOIDA (Duolingo tamoyili): har bir savolga javobni o'quvchi FAQAT
yuqoridagi kartochkalarda berilgan ma'lumotdan topa olishi SHART. Kartochkalarda
aytilmagan fakt, atama, sana yoki tushunchani so'ramang. Kartochkalardagi
misollarga o'xshash, lekin ayni ular emas, yangi holatlar tuzsangiz bo'ladi.
"""

    prompt = f"""Siz O'zbekiston Milliy Sertifikat imtihoniga savol yozuvchi tajribali metodistsiz.
Fan: {subject_name_uz}
Bo'lim: {unit_title_uz}
Mavzu (dars): {lesson_title_uz}
{theory_block}
Ushbu mavzu bo'yicha aynan {count} ta original test savolini yozing.

Qat'iy talablar:
- Har bir savol mustaqil va tushunarli bo'lishi kerak.
- Aniq 4 ta variant, faqat bittasi to'g'ri.
- Qiyinlik taqsimoti: taxminan 40% oson, 40% o'rta, 20% qiyin.
- correct_answer variantlardan biri bilan SO'ZMA-SO'Z bir xil bo'lishi kerak.
- explanation: to'g'ri javob nima uchun to'g'ri ekanini 1-3 gapda tushuntiring
  (o'quvchi darsni tugatgach shu tushuntirishni ko'radi).
- Barcha {count} savol bir-biridan farq qilishi kerak.

Faqat quyidagi JSON massivini qaytaring, boshqa hech narsa yozmang:
[
  {{
    "difficulty": "easy" | "medium" | "hard",
    "question_text": "...",
    "options": ["...", "...", "...", "..."],
    "correct_answer": "...",
    "explanation": "..."
  }}
]"""

    response = _generate_round_robin(prompt)
    items = _parse_json(response.text)
    if isinstance(items, dict):
        items = items.get("questions", [])
    return items


def generate_theory_for_lesson(subject_name_uz: str, unit_title_uz: str, lesson_title_uz: str) -> list[dict]:
    """Duolingo-style teaching cards shown BEFORE the quiz questions -- first
    the app teaches, then it tests."""
    prompt = f"""Siz O'zbekiston Milliy Sertifikat imtihoniga tayyorlovchi tajribali o'qituvchisiz.
Fan: {subject_name_uz}
Bo'lim: {unit_title_uz}
Mavzu (dars): {lesson_title_uz}

Ushbu mavzuni o'quvchiga NOLDAN o'rgatadigan 3-4 ta qisqa o'quv kartochkasini yozing
(Duolingo darslaridagi kabi: avval tushuncha o'rgatiladi, keyin test beriladi).

Qat'iy talablar:
- Har bir kartochka BITTA aniq tushunchani o'rgatsin.
- title: 2-5 so'zli sarlavha.
- body: tushunchani sodda, ravon tilda tushuntiring (2-4 gap). Ilmiy-quruq emas,
  o'quvchi bilan suhbatlashgandek yozing.
- example: shu tushunchaga aniq, yodda qoladigan 1-2 ta misol.
- Kartochkalar mantiqiy ketma-ketlikda bo'lsin: soddadan murakkabga.
- Keyin beriladigan test savollari aynan shu kartochkalarda o'rgatilgan
  bilimga tayanadi, shuning uchun mavzuning eng muhim qismlarini qamrab oling.

Faqat quyidagi JSON massivini qaytaring, boshqa hech narsa yozmang:
[
  {{
    "title": "...",
    "body": "...",
    "example": "..."
  }}
]"""

    response = _generate_round_robin(prompt)
    items = _parse_json(response.text)
    if isinstance(items, dict):
        items = items.get("cards", [])
    return items


def _valid_theory(cards) -> bool:
    if not isinstance(cards, list) or not (2 <= len(cards) <= 6):
        return False
    return all(isinstance(c, dict) and c.get("title") and c.get("body") for c in cards)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-lesson", type=int, default=10)
    parser.add_argument("--subject", type=str, default=None, choices=list(SKILLTREE_OUTLINE.keys()) + [None])
    parser.add_argument("--regen-questions", action="store_true",
                        help="Regenerate questions even for lessons that already have them (grounded in theory cards)")
    args = parser.parse_args()

    os.makedirs(SEEDS_DIR, exist_ok=True)

    db = SessionLocal()
    total = 0
    try:
        for subject_slug, subject_def in SKILLTREE_OUTLINE.items():
            if args.subject and subject_slug != args.subject:
                continue

            subject = upsert_structure(db, subject_slug, subject_def)
            fixture_rows = []
            theory_rows = []

            units = db.query(SkillUnit).filter(SkillUnit.subject_id == subject.id).order_by(SkillUnit.order_index).all()
            for unit in units:
                lessons = db.query(SkillLesson).filter(SkillLesson.unit_id == unit.id).order_by(SkillLesson.order_index).all()
                for lesson in lessons:
                    # Teaching cards (learn-first phase) -- generate once per lesson.
                    if not lesson.theory:
                        try:
                            cards = generate_theory_for_lesson(subject_def["name"]["uz"], unit.title_uz, lesson.title_uz)
                            if _valid_theory(cards):
                                lesson.theory = cards
                                db.add(lesson)
                                db.commit()
                                print(f"THEORY {unit.title_uz} / {lesson.title_uz}: +{len(cards)} cards")
                            else:
                                print(f"THEORY INVALID {unit.title_uz} / {lesson.title_uz}: skipped")
                        except Exception as exc:
                            print(f"THEORY FAILED {unit.title_uz} / {lesson.title_uz}: {exc}")
                        time.sleep(3)
                    if lesson.theory:
                        theory_rows.append({
                            "subject_slug": subject_slug,
                            "unit_slug": unit.slug,
                            "lesson_slug": lesson.slug,
                            "theory": lesson.theory,
                        })

                    existing = db.query(SkillQuestion).filter(SkillQuestion.lesson_id == lesson.id).order_by(SkillQuestion.order_index).all()
                    if existing and not args.regen_questions:
                        print(f"SKIP {unit.title_uz} / {lesson.title_uz}: already has {len(existing)} questions")
                        for q in existing:
                            fixture_rows.append({
                                "subject_slug": subject_slug,
                                "unit_slug": unit.slug,
                                "lesson_slug": lesson.slug,
                                "lesson_id": lesson.id,
                                "order_index": q.order_index,
                                "language": q.language,
                                "question_text": q.question_text,
                                "options": q.options,
                                "correct_answer": q.correct_answer,
                                "explanation": q.explanation,
                                "difficulty": q.difficulty,
                            })
                        continue

                    try:
                        items = generate_for_lesson(subject_def["name"]["uz"], unit.title_uz, lesson.title_uz, args.per_lesson, theory=lesson.theory)
                    except Exception as exc:
                        print(f"FAILED {unit.title_uz} / {lesson.title_uz}: {exc}")
                        continue

                    if existing:
                        # --regen-questions: replace only after a successful regeneration,
                        # so a failed Gemini call never leaves a lesson empty.
                        db.query(SkillQuestion).filter(SkillQuestion.lesson_id == lesson.id).delete()
                        db.commit()

                    inserted = 0
                    for idx, item in enumerate(items):
                        q_in = {
                            "lesson_id": lesson.id,
                            "order_index": idx,
                            "language": "uz",
                            "question_text": (item.get("question_text") or "").strip(),
                            "options": item.get("options"),
                            "correct_answer": item.get("correct_answer"),
                            "explanation": item.get("explanation"),
                            "difficulty": item.get("difficulty", "medium"),
                        }
                        ok, err = validate_question(q_in)
                        if not ok:
                            print(f"  invalid item skipped: {err}")
                            continue
                        add_question(db, q_in)
                        fixture_rows.append({
                            "subject_slug": subject_slug,
                            "unit_slug": unit.slug,
                            "lesson_slug": lesson.slug,
                            **q_in,
                        })
                        inserted += 1
                    total += inserted
                    print(f"{unit.title_uz} / {lesson.title_uz}: +{inserted}")
                    time.sleep(3)  # round-robin across all keys already keeps any single key well under its RPM limit

            fixture_path = os.path.join(SEEDS_DIR, f"skilltree_{subject_slug}.json")
            with open(fixture_path, "w", encoding="utf-8") as f:
                json.dump(fixture_rows, f, ensure_ascii=False, indent=2)
            print(f"Wrote fixture: {fixture_path} ({len(fixture_rows)} questions)")

            theory_path = os.path.join(SEEDS_DIR, f"skilltree_theory_{subject_slug}.json")
            with open(theory_path, "w", encoding="utf-8") as f:
                json.dump(theory_rows, f, ensure_ascii=False, indent=2)
            print(f"Wrote theory fixture: {theory_path} ({len(theory_rows)} lessons)")
    finally:
        db.close()
    print(f"Done. Inserted {total} questions total.")


if __name__ == "__main__":
    main()
