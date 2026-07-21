"""
audit_units.py — find the units each subject is missing against the real syllabus.

expand_taxonomy.py filled every existing unit out to 11 lessons, which made the tree
look finished: 813 of 814 lessons answerable. But it only ever deepened units that
were already there, and the unit list itself is the original hand-authored spine —
Matematika, for instance, has no Trigonometriya, no logarithms, no progressions, no
vectors and no calculus, all of which are squarely on the DTM syllabus. A count of
lessons-per-unit cannot see that kind of gap.

This asks the model to compare each subject's unit list with the Milliy Sertifikat /
DTM programme and report only what is missing. It writes a proposal to
services/skilltree_missing_units.json for a human to review — it deliberately does
NOT touch the taxonomy, because a wrong unit here becomes dozens of wrong lessons.

    PYTHONIOENCODING=utf-8 python scripts/audit_units.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.llm_provider import generate, provider_name        # noqa: E402
from services.skilltree_taxonomy import SKILLTREE_OUTLINE        # noqa: E402

OUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "services", "skilltree_missing_units.json")


def build_prompt(subject_uz: str, units: list[str]) -> str:
    have = "\n".join(f"- {u}" for u in units)
    return f"""Siz O'zbekiston DTM / Milliy Sertifikat imtihoni bo'yicha o'quv dasturi mutaxassisisiz.

Fan: {subject_uz}

Hozirgi bo'limlar va ularning ICHIDAGI DARSLAR:
{have}

Savol: shu fanning RASMIY Milliy Sertifikat / DTM dasturida bor, lekin yuqoridagi
ro'yxatda YO'Q bo'lgan bo'limlarni sanang.

Qat'iy talablar:
- Faqat HAQIQATAN yetishmayotganini yozing. Yuqoridagi DARSLAR ro'yxatini diqqat
  bilan o'qing: agar mavzu biror bo'lim ichida DARS sifatida bor bo'lsa, uni
  "yetishmayapti" demang (masalan "Shart gaplar (Conditionals)" darsi bor bo'lsa,
  "Conditionals" ni qo'shmang).
- Bu MAKTAB darajasidagi imtihon. Universitet fanlarini taklif qilmang
  (masalan gistologiya, etologiya, matritsalar nazariyasi).
- Agar ro'yxat allaqachon to'liq bo'lsa, bo'sh massiv [] qaytaring. Bu normal javob.
- Har bir bo'lim imtihonda haqiqatan so'raladigan, jiddiy mavzu bo'lsin.
- Ko'pi bilan 6 ta.
- "reason" da nima uchun kerakligini bir jumlada yozing (o'zbekcha).

Faqat quyidagi JSON massivini qaytaring:
[
  {{"uz": "o'zbekcha nomi", "ru": "русское название", "en": "English name", "reason": "..."}}
]"""


def parse(text: str):
    t = text.strip()
    if t.startswith("```"):
        t = t.split("```")[1]
        if t.startswith("json"):
            t = t[4:]
    return json.loads(t)


def main() -> int:
    print(f"provider: {provider_name()}\n", flush=True)
    proposal: dict[str, list[dict]] = {}

    for slug, subject in SKILLTREE_OUTLINE.items():
        units = subject["units"]
        try:
            items = parse(generate(build_prompt(subject["name"]["uz"], units)).text)
            if isinstance(items, dict):
                items = items.get("units", [])
        except Exception as exc:
            print(f"{slug:18} FAILED: {str(exc)[:90]}", flush=True)
            continue

        clean = [i for i in items if isinstance(i, dict) and i.get("uz")][:6]
        proposal[slug] = clean
        print(f"{slug:18} +{len(clean)}", flush=True)
        for i in clean:
            print(f"    · {i['uz']}  — {i.get('reason','')[:70]}", flush=True)

    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(proposal, fh, ensure_ascii=False, indent=1)
    total = sum(len(v) for v in proposal.values())
    print(f"\n{total} proposed units → {OUT_PATH}")
    print("REVIEW THIS BEFORE GENERATING — a wrong unit becomes 11 wrong lessons.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
