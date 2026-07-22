"""
reorder_lessons.py — put each unit's lessons into teaching order.

expand_taxonomy.py appends, which protected everyone's progress but left every unit
reading "the original four, then the seven that were added later". Matematika got away
with it because the additions happened to be the harder material; Tarix did not — its
medieval unit taught the Arab conquest (8c), the Samanids (9c) and the Mongols (13c),
and only then went back to the Ephthalites and the Türk Khaganate (5-6c).

The order is written to `_order` inside services/skilltree_outline.json as a list of
slugs; `skilltree_taxonomy.py::_merge_expansion()` sorts each unit by it. Only the
sequence changes — no slug is renamed, added or dropped, so `UserLessonProgress` rows
still point at the same lessons.

    PYTHONIOENCODING=utf-8 python scripts/reorder_lessons.py [--subject tarix]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.llm_provider import generate, provider_name      # noqa: E402
from services.skilltree_taxonomy import SKILLTREE_OUTLINE      # noqa: E402

OUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "services", "skilltree_outline.json")


def build_prompt(subject_uz: str, unit_uz: str, titles: list[str]) -> str:
    listing = "\n".join(f"{i}. {t}" for i, t in enumerate(titles))
    return f"""Siz o'quv dasturi tuzuvchi metodistsiz.

Fan: {subject_uz}
Bo'lim: {unit_uz}

Quyidagi darslar hozir tasodifiy tartibda turibdi:
{listing}

Ularni O'QITISH TARTIBIGA soling:
- Tarix bo'lsa — XRONOLOGIK tartib (erta davr avval).
- Boshqa fanlarda — oson mavzudan qiyiniga; oldingi dars keyingisiga zamin bo'lsin.
- Bir mavzuning davomi bo'lgan darslar yonma-yon tursin.

MUHIM: faqat tartibni o'zgartiring. Dars qo'shmang, o'chirmang, nomini o'zgartirmang.
Javob — yuqoridagi raqamlarning yangi tartibi, JSON massiv sifatida.
Massivda {len(titles)} ta raqam bo'lishi SHART, har biri roppa-rosa bir marta.

Masalan: [3, 0, 1, 2]"""


def parse(text: str):
    """Pull the ordering out of whatever the model wrapped it in.

    Half the units came back as prose around the array ("Mana yangi tartib: [3, 0, …]")
    and were thrown away as unparseable, so only the units that happened to answer
    tersely got reordered. The first bracketed list of integers is the answer.
    """
    t = text.strip()
    if t.startswith("```"):
        t = t.split("```")[1]
        if t.startswith("json"):
            t = t[4:]
    try:
        return json.loads(t.strip())
    except json.JSONDecodeError:
        m = re.search(r"\[\s*\d+(?:\s*,\s*\d+)*\s*\]", t)
        if m:
            return json.loads(m.group(0))
        # Some answers drop the brackets entirely and give a numbered list, one index
        # per line. Every integer in the reply is the ordering; the permutation check
        # in main() is what decides whether to trust it.
        nums = [int(x) for x in re.findall(r"\d+", t)]
        if not nums:
            raise
        return nums


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", action="append")
    args = ap.parse_args()
    print(f"provider: {provider_name()}\n", flush=True)

    with open(OUT_PATH, encoding="utf-8") as fh:
        outline = json.load(fh)

    for slug in (args.subject or list(SKILLTREE_OUTLINE)):
        subject = SKILLTREE_OUTLINE[slug]
        bucket = outline.setdefault(slug, {})
        for unit in subject["units"]:
            lessons = unit["lessons"]
            titles = [l["title"]["uz"] for l in lessons]
            slugs = [l["slug"] for l in lessons]
            if len(lessons) < 3:
                continue
            try:
                order = parse(generate(build_prompt(
                    subject["name"]["uz"], unit["title"]["uz"], titles)).text)
            except Exception as exc:
                print(f"{slug:16} {unit['slug']:24} FAILED: {str(exc)[:60]}", flush=True)
                continue

            # A permutation or nothing: a truncated or duplicated list would silently
            # drop lessons out of the tree.
            if (not isinstance(order, list) or sorted(order) != list(range(len(slugs)))):
                print(f"{slug:16} {unit['slug']:24} rejected (not a permutation)", flush=True)
                continue

            new = [slugs[i] for i in order]
            moved = sum(1 for a, b in zip(slugs, new) if a != b)
            bucket.setdefault("_order", {})[unit["slug"]] = new
            print(f"{slug:16} {unit['slug']:24} {moved}/{len(new)} moved", flush=True)

            with open(OUT_PATH, "w", encoding="utf-8") as fh:
                json.dump(outline, fh, ensure_ascii=False, indent=1)

    print("\ndone — re-run seed_skilltree.py to write the new order_index")
    return 0


if __name__ == "__main__":
    sys.exit(main())
