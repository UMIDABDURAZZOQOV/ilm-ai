"""
fill_syllabus_gaps.py — go unit by unit and add whatever the syllabus still expects.

expand_taxonomy.py padded every unit to a fixed eleven lessons, which is a quota, not
a syllabus: a unit that needed fourteen stopped at eleven, and one that needed eight
got three lessons of filler. This asks, per unit, what the DTM / Milliy Sertifikat
programme covers there that the current lessons do not — with the unit's existing
lessons in the prompt, since asking without them produced "missing" topics that were
already taught (Conditionals, Passive Voice and Reported Speech were all reported
missing from Ingliz tili while sitting in "Gap tuzilishi").

Proposals are appended to services/skilltree_outline.json, which
skilltree_taxonomy.py merges over the hand-authored spine. Append-only, keyed by
slug: an existing lesson is never renamed or reordered, because UserLessonProgress
rows point at those slugs.

    PYTHONIOENCODING=utf-8 python scripts/fill_syllabus_gaps.py [--subject tarix]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.llm_provider import generate, provider_name          # noqa: E402
from services.skilltree_taxonomy import SKILLTREE_OUTLINE          # noqa: E402

OUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "services", "skilltree_outline.json")
MAX_PER_UNIT = 8


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()[:60] or "dars"


def normalise(text: str) -> str:
    """For duplicate detection: strip punctuation and the usual Uzbek spelling drift."""
    t = text.lower().replace("'", "").replace("`", "").replace("‘", "").replace("’", "")
    return re.sub(r"[^a-z0-9 ]+", " ", t)


def build_prompt(subject_uz: str, unit_uz: str, unit_lessons: list[str],
                 other_lessons: list[str]) -> str:
    have = "\n".join(f"- {t}" for t in unit_lessons) or "(bo'sh)"
    elsewhere = "\n".join(f"- {t}" for t in other_lessons[:120])
    return f"""Siz O'zbekiston DTM / Milliy Sertifikat imtihoni uchun o'quv dasturi tuzuvchi metodistsiz.

Fan: {subject_uz}
BO'LIM: {unit_uz}

Shu bo'limdagi MAVJUD darslar:
{have}

Shu fanning BOSHQA bo'limlaridagi darslar (bularni takrorlamang):
{elsewhere}

Savol: rasmiy DTM / Milliy Sertifikat dasturida SHU BO'LIMGA tegishli bo'lgan, lekin
yuqoridagi ro'yxatlarda YO'Q mavzularni sanang.

Qat'iy talablar:
- Yuqorida bor mavzuni boshqacha nom bilan QAYTA yozmang. Diqqat bilan solishtiring.
- Faqat SHU bo'limga tegishli mavzular. Boshqa bo'limning mavzusini bu yerga tiqmang.
- MAKTAB darajasi. Universitet mavzularini taklif qilmang.
- Agar bo'lim allaqachon to'liq bo'lsa — bo'sh massiv [] qaytaring. Bu TO'G'RI javob
  va ko'p hollarda kutilgan javob.
- Ko'pi bilan {MAX_PER_UNIT} ta.

Faqat JSON massiv qaytaring:
[{{"uz": "...", "ru": "...", "en": "..."}}]"""


def parse(text: str):
    t = text.strip()
    if t.startswith("```"):
        t = t.split("```")[1]
        if t.startswith("json"):
            t = t[4:]
    return json.loads(t)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", action="append")
    args = ap.parse_args()

    print(f"provider: {provider_name()}\n", flush=True)

    outline: dict = {}
    if os.path.exists(OUT_PATH):
        with open(OUT_PATH, encoding="utf-8") as fh:
            outline = json.load(fh)

    added_total = 0
    for slug in (args.subject or list(SKILLTREE_OUTLINE)):
        subject = SKILLTREE_OUTLINE[slug]
        done = outline.setdefault(slug, {})
        all_titles = [l["title"]["uz"] for u in subject["units"] for l in u["lessons"]]

        for unit in subject["units"]:
            unit_titles = [l["title"]["uz"] for l in unit["lessons"]]
            others = [t for t in all_titles if t not in unit_titles]
            try:
                items = parse(generate(build_prompt(
                    subject["name"]["uz"], unit["title"]["uz"], unit_titles, others)).text)
                if isinstance(items, dict):
                    items = items.get("lessons", [])
            except Exception as exc:
                print(f"{slug:16} {unit['slug']:24} FAILED: {str(exc)[:70]}", flush=True)
                continue

            seen = {normalise(t) for t in all_titles}
            taken = {slugify(t) for t in all_titles}
            fresh = []
            for it in items[:MAX_PER_UNIT]:
                if not isinstance(it, dict) or not it.get("uz"):
                    continue
                title = it["uz"].strip()
                if normalise(title) in seen:
                    continue
                s = slugify(title)
                if s in taken:
                    continue
                seen.add(normalise(title))
                taken.add(s)
                fresh.append({"slug": s, "uz": title,
                              "ru": (it.get("ru") or title).strip(),
                              "en": (it.get("en") or title).strip()})

            if fresh:
                done[unit["slug"]] = done.get(unit["slug"], []) + fresh
                all_titles.extend(f["uz"] for f in fresh)
                added_total += len(fresh)
                print(f"{slug:16} {unit['slug']:24} +{len(fresh)}", flush=True)
                for f in fresh:
                    print(f"      · {f['uz']}", flush=True)
            else:
                print(f"{slug:16} {unit['slug']:24} to'liq", flush=True)

            with open(OUT_PATH, "w", encoding="utf-8") as fh:
                json.dump(outline, fh, ensure_ascii=False, indent=1)

    print(f"\n{added_total} new lessons proposed → {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
