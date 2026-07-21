"""
seed_placement.py — build the calibrated placement-test bank.

Each question is authored AT a level (CEFR A1-C2 for languages, daraja_1..5 for the
academic subjects) with an explicit description of what that level means, so the
resulting level is something the learner has actually demonstrated rather than a
percentage of an uncalibrated lesson bank. See services/placement.py for the scoring.

Resumable: it only asks Gemini for the (subject, level, skill) buckets that are still
short, so re-running fills the gaps. Dumps scripts/seeds/placement_bank.json.

    PYTHONIOENCODING=utf-8 python scripts/seed_placement.py [--subject ingliz_tili]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.db import SessionLocal, engine, Base                      # noqa: E402
from services.models import PlacementQuestion, SkillSubject             # noqa: E402
from services.placement import (                                        # noqa: E402
    CEFR_LEVELS, LANGUAGE_SUBJECT_SLUGS, SUBJECT_LEVELS, levels_for,
)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seed_skilltree import _generate_round_robin, _parse_json           # noqa: E402

SEED_PATH = os.path.join(os.path.dirname(__file__), "seeds", "placement_bank.json")

# Per (level, skill) bucket. 6 CEFR levels × 3 skills × 12 = 216 questions per
# language; the test itself asks 7 per level, so a retake is a different paper.
PER_BUCKET = 12
LANGUAGE_SKILLS = ["grammar", "vocabulary", "reading"]
SUBJECT_SKILLS = ["bilim", "qollash"]

# What each band means, in the words a question writer needs. Without this the model
# drifts and writes B1-ish questions for every level, which is exactly the failure the
# old test had.
CEFR_BRIEF = {
    "A1": "eng boshlang'ich: alifbo, olmoshlar, to be, sonlar, ranglar, oila, kundalik 500 ta eng keng tarqalgan so'z. Gaplar juda qisqa.",
    "A2": "boshlang'ich+: Past Simple, kelasi zamon (going to), sifatlarning qiyosiy darajasi, predloglar, oddiy kundalik matnlar.",
    "B1": "o'rta: Present Perfect, 1- va 2-shart gaplar, majhul nisbat (oddiy), phrasal verb'larning keng tarqalganlari, 1000-2000 so'z.",
    "B2": "o'rta+: Past Perfect, 3-shart gap, o'zlashtirma gap, murakkab ergash gaplar, idiomalar, abstrakt mavzudagi matn.",
    "C1": "yuqori: nozik ma'no farqlari, inversiya, formal/informal registr, kam uchraydigan idioma va kollokatsiyalar, uzun analitik matn.",
    "C2": "ona tilida so'zlashuvchiga yaqin: stilistik nuanslar, kam qo'llanadigan grammatik konstruksiyalar, ilmiy/badiiy matn tahlili.",
}

SUBJECT_BRIEF = {
    "daraja_1": "maktab bazaviy darajasi: ta'rif, atama, eng asosiy faktlarni bilish.",
    "daraja_2": "maktab o'rta darajasi: qoidani oddiy, bir bosqichli holatda qo'llash.",
    "daraja_3": "Milliy Sertifikat B daraja: bir necha bosqichli masala, qiyoslash va tahlil.",
    "daraja_4": "Milliy Sertifikat A daraja: murakkab, nostandart masala, bir necha mavzuni birlashtirish.",
    "daraja_5": "olimpiada darajasi: chuqur tahlil, isbot, noan'anaviy yechim talab qiladi.",
}

SKILL_BRIEF = {
    "grammar": "grammatika qoidasini tekshiruvchi savol (gapdagi bo'sh joyni to'ldirish yoki to'g'ri shaklni tanlash)",
    "vocabulary": "so'z boyligini tekshiruvchi savol (so'z ma'nosi, kollokatsiya, sinonim)",
    "reading": "2-4 gapli qisqa matn va uni tushunishni tekshiruvchi savol",
    "bilim": "nazariy bilimni tekshiruvchi savol (ta'rif, fakt, qoida)",
    "qollash": "bilimni amalda qo'llashni tekshiruvchi savol (masala, misol, tahlil)",
}


def build_prompt(subject_name: str, subject_slug: str, level: str, skill: str, count: int) -> str:
    is_lang = subject_slug in LANGUAGE_SUBJECT_SLUGS
    brief = (CEFR_BRIEF if is_lang else SUBJECT_BRIEF)[level]
    scale = "CEFR" if is_lang else "Milliy Sertifikat"
    lang_note = ""
    if is_lang:
        lang_note = (
            f"\nSavol va variantlar {subject_name.upper()} tilida bo'lsin "
            f"(o'rganilayotgan tilda), tushuntirish esa o'zbek tilida."
        )

    return f"""Siz til/fan darajasini aniqlovchi (placement test) savollarini yozuvchi tajribali testolog siz.
Fan: {subject_name}
Shkala: {scale}
DARAJA: {level} — {brief}
Savol turi: {SKILL_BRIEF[skill]}
{lang_note}

Aynan {count} ta savol yozing.

ENG MUHIM QOIDA: har bir savol ANIQ {level} darajasiga mos bo'lishi SHART.
- {level} dan PAST darajadagi o'quvchi bu savolga javob bera olmasligi kerak.
- {level} darajasini egallagan o'quvchi esa uni ishonch bilan yechishi kerak.
- Savolni ataylab chalg'ituvchi yoki "hiyla" qilib yubormang — daraja o'lchanadi, ziyraklik emas.

Boshqa talablar:
- Aniq 4 ta variant, faqat bittasi to'g'ri.
- Chalg'ituvchi variantlar ishonarli bo'lsin (tasodifan topib bo'lmasin).
- correct_answer variantlardan biri bilan SO'ZMA-SO'Z bir xil.
- explanation: o'zbek tilida, 1-2 gap.
- Barcha {count} savol bir-biridan farq qilsin.

Faqat quyidagi JSON massivini qaytaring:
[
  {{"question_text": "...", "options": ["...","...","...","..."], "correct_answer": "...", "explanation": "..."}}
]"""


def valid(item: dict) -> bool:
    opts = item.get("options")
    return (
        isinstance(item.get("question_text"), str) and len(item["question_text"].strip()) > 5
        and isinstance(opts, list) and len(opts) == 4
        and all(isinstance(o, str) and o.strip() for o in opts)
        and item.get("correct_answer") in opts
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", action="append", help="limit to these subject slugs")
    ap.add_argument("--per-bucket", type=int, default=PER_BUCKET)
    args = ap.parse_args()

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        subjects = db.query(SkillSubject).order_by(SkillSubject.order_index).all()
        if args.subject:
            subjects = [s for s in subjects if s.slug in args.subject]

        for subj in subjects:
            skills = LANGUAGE_SKILLS if subj.slug in LANGUAGE_SUBJECT_SLUGS else SUBJECT_SKILLS
            for level in levels_for(subj.slug):
                for skill in skills:
                    have = (
                        db.query(PlacementQuestion)
                        .filter(PlacementQuestion.subject_slug == subj.slug,
                                PlacementQuestion.level == level,
                                PlacementQuestion.skill == skill)
                        .count()
                    )
                    need = args.per_bucket - have
                    if need <= 0:
                        continue
                    print(f"{subj.slug:16} {level:9} {skill:11} need {need}", flush=True)
                    try:
                        resp = _generate_round_robin(
                            build_prompt(subj.name_uz, subj.slug, level, skill, need))
                        items = _parse_json(resp.text)
                        if isinstance(items, dict):
                            items = items.get("questions", [])
                    except Exception as exc:
                        print(f"  FAILED: {exc}", flush=True)
                        continue

                    added = 0
                    for it in items:
                        if not valid(it):
                            continue
                        db.add(PlacementQuestion(
                            subject_slug=subj.slug,
                            level=level,
                            skill=skill,
                            question_text=it["question_text"].strip(),
                            options=it["options"],
                            correct_answer=it["correct_answer"],
                            explanation=(it.get("explanation") or "").strip() or None,
                        ))
                        added += 1
                    db.commit()
                    print(f"  +{added}", flush=True)

        dump(db)
    finally:
        db.close()
    return 0


def dump(db) -> None:
    rows = db.query(PlacementQuestion).order_by(
        PlacementQuestion.subject_slug, PlacementQuestion.level, PlacementQuestion.id).all()
    data = [{
        "subject_slug": r.subject_slug, "level": r.level, "skill": r.skill,
        "question_text": r.question_text, "options": r.options,
        "correct_answer": r.correct_answer, "explanation": r.explanation,
    } for r in rows]
    os.makedirs(os.path.dirname(SEED_PATH), exist_ok=True)
    with open(SEED_PATH, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    print(f"\ndumped {len(data)} questions → {SEED_PATH}")


if __name__ == "__main__":
    sys.exit(main())
