"""
expand_taxonomy.py — deepen the skill tree from a demo into an actual syllabus.

The hand-authored outline in services/skilltree_taxonomy.py gives each unit 3-5
lessons — 253 lessons across 12 subjects. That is a skeleton: the whole of Uzbek
history from prehistory to today was 27 lessons, the whole English language 22, and a
learner could finish a subject in under an hour. This asks Gemini for the full lesson
list each unit actually needs at Milliy Sertifikat depth and writes the result to
services/skilltree_outline.json, which the taxonomy module merges over the base.

Two rules it must never break:
  * Existing lesson slugs are kept, in their existing order, at the front of the unit.
    They are what UserLessonProgress rows point at — renaming or reordering one would
    silently move somebody's progress to a different lesson.
  * Only new slugs are appended. Nothing is ever removed here.

    PYTHONIOENCODING=utf-8 python scripts/expand_taxonomy.py [--subject tarix]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.skilltree_taxonomy import SKILLTREE_OUTLINE          # noqa: E402
from seed_skilltree import _generate_round_robin, _parse_json      # noqa: E402

OUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "services", "skilltree_outline.json")

# A unit of 9-12 lessons puts a subject at roughly 60-80 lessons, which is a term's
# work rather than an afternoon's.
TARGET_PER_UNIT = 11


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text[:60] or "dars"


def build_prompt(subject_name: str, unit_title: str, existing: list[str], need: int) -> str:
    have = "\n".join(f"- {t}" for t in existing) or "(hozircha yo'q)"
    return f"""Siz O'zbekiston Milliy Sertifikat imtihoni uchun o'quv dasturi (silabus) tuzuvchi metodistsiz.

Fan: {subject_name}
Bo'lim: {unit_title}

Bu bo'limda hozir quyidagi darslar bor:
{have}

Shu bo'limni TO'LIQ qamrab olish uchun yana {need} ta YANGI dars mavzusini yozing.

Talablar:
- Yuqorida allaqachon bor mavzularni TAKRORLAMANG.
- Mavzular oson → qiyin tartibida, mantiqiy ketma-ketlikda bo'lsin.
- Har bir dars bitta aniq mavzuni qamrasin (juda keng "hammasi haqida" mavzu bo'lmasin).
- Mavzular shu bo'lim doirasidan chiqmasin.
- Milliy Sertifikat/DTM darajasidagi haqiqiy sillabusga mos bo'lsin — maktab
  darsligidagi mavzular ketma-ketligini o'ylang.

Faqat quyidagi JSON massivini qaytaring:
[
  {{"uz": "o'zbekcha nomi", "ru": "русское название", "en": "English name"}}
]"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", action="append")
    ap.add_argument("--target", type=int, default=TARGET_PER_UNIT)
    args = ap.parse_args()

    # Resume-friendly: keep whatever previous runs already produced.
    outline: dict = {}
    if os.path.exists(OUT_PATH):
        with open(OUT_PATH, encoding="utf-8") as fh:
            outline = json.load(fh)

    slugs = args.subject or list(SKILLTREE_OUTLINE)
    for subject_slug in slugs:
        subject_def = SKILLTREE_OUTLINE[subject_slug]
        subject_name = subject_def["name"]["uz"]
        done = outline.setdefault(subject_slug, {})

        for unit in subject_def["units"]:
            base = [l["title"]["uz"] for l in unit["lessons"]]
            already = done.get(unit["slug"], [])
            have = len(base) + len(already)
            need = args.target - have
            if need <= 0:
                continue

            print(f"{subject_slug:16} {unit['slug']:22} {have} → {args.target}", flush=True)
            titles = base + [a["uz"] for a in already]
            try:
                resp = _generate_round_robin(build_prompt(subject_name, unit["title"]["uz"], titles, need))
                items = _parse_json(resp.text)
                if isinstance(items, dict):
                    items = items.get("lessons", [])
            except Exception as exc:
                print(f"  FAILED: {exc}", flush=True)
                continue

            taken = {slugify(t) for t in titles} | {a["slug"] for a in already}
            added = []
            for it in items:
                if not isinstance(it, dict) or not it.get("uz"):
                    continue
                slug = slugify(it["uz"])
                if slug in taken:
                    continue
                taken.add(slug)
                added.append({
                    "slug": slug,
                    "uz": it["uz"].strip(),
                    "ru": (it.get("ru") or it["uz"]).strip(),
                    "en": (it.get("en") or it["uz"]).strip(),
                })
            done[unit["slug"]] = already + added
            print(f"  +{len(added)}", flush=True)

            with open(OUT_PATH, "w", encoding="utf-8") as fh:
                json.dump(outline, fh, ensure_ascii=False, indent=1)

    total = sum(len(v) for s in outline.values() for v in s.values())
    print(f"\n{total} new lessons → {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
