"""
coverage_check.py — does the tree actually teach the topics the exam asks about?

Written after a wrong call: reading the seven unit titles of Matematika, I told the
owner it was missing trigonometry, logarithms, progressions and vectors. All four are
there — as *lessons* inside existing units, added by expand_taxonomy.py. Unit titles
are a summary, and a summary cannot be checked against a syllabus.

So this looks at lesson titles, and each topic is matched by several spellings,
because a single keyword produces false alarms of its own ("article" misses the lesson
called "Otlar va artikllar").

Keyword matching still only proves a title mentions a topic. Treat a ❌ as "worth
looking at", never as proof, and a ✓ as "named", not "taught well".

    PYTHONIOENCODING=utf-8 python scripts/coverage_check.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.skilltree_taxonomy import SKILLTREE_OUTLINE       # noqa: E402

# topic → the spellings that would satisfy it
CHECKS: dict[str, list[tuple[str, list[str]]]] = {
    "matematika": [
        ("Hosila", ["hosila", "differensial"]),
        ("Integral", ["integral"]),
        ("Statistika", ["statistik", "o'rtacha", "diagramma", "ehtimol"]),
        ("Stereometriya", ["prizma", "piramida", "shar", "silindr", "konus", "ko'pyoq"]),
        ("Trigonometriya", ["trigonometr", "sinus", "kosinus"]),
        ("Logarifm", ["logarifm"]),
        ("Progressiya", ["progressiya"]),
        ("Vektorlar", ["vektor"]),
    ],
    "fizika": [
        ("Statika", ["statika", "muvozanat", "richag"]),
        ("Gidrostatika", ["bosim", "arximed", "suyuqlik"]),
        ("Elektrostatika", ["zaryad", "kulon", "elektr maydon"]),
        ("Magnit maydon", ["magnit"]),
        ("Optika", ["optik", "linza", "yorug'lik"]),
        ("Yadro fizikasi", ["yadro", "radioaktiv"]),
    ],
    "kimyo": [
        ("Galogenlar", ["galogen", "xlor"]),
        ("Elektroliz", ["elektroliz"]),
        ("Kimyoviy muvozanat", ["muvozanat"]),
        ("Reaksiya tezligi", ["tezlig", "kinetik"]),
        ("Oqsil / uglevod", ["oqsil", "uglevod", "yog'"]),
    ],
    "biologiya": [
        ("Immunitet", ["immun", "kasallik", "qon"]),
        ("Ekosistema", ["ekosistem", "biotsenoz", "biogeotsenoz", "ekolog"]),
        ("Seleksiya", ["seleksiya", "naslchilik", "duragay"]),
        ("Fotosintez", ["fotosintez"]),
        ("Gormonlar", ["gormon", "endokrin", "bez"]),
    ],
    "ona_tili": [
        ("Qo'shma gap", ["qo'shma gap", "ergash gap"]),
        ("So'z yasalishi", ["yasal", "affiks", "so'z tarkib"]),
        ("Imlo", ["imlo", "orfograf"]),
        ("Tinish belgilari", ["tinish", "vergul", "nuqta"]),
        ("Frazeologizm", ["frazeolog", "ibora"]),
    ],
    "tarix": [
        ("Ahamoniylar", ["ahamoniy", "iskandar"]),
        ("Kushon", ["kushon"]),
        ("Arab istilosi", ["arab istilo", "arab"]),
        ("Somoniylar", ["somoniy"]),
        ("Qoraxoniylar", ["qoraxoniy"]),
        ("Xorazmshohlar", ["xorazmshoh"]),
        ("Mo'g'ul istilosi", ["mo'g'ul", "chingiz"]),
        ("Amir Temur", ["amir temur", "temur"]),
        ("Ulug'bek", ["ulug'bek"]),
        ("Shayboniylar", ["shayboniy"]),
        ("Buxoro xonligi", ["buxoro"]),
        ("Xiva xonligi", ["xiva"]),
        ("Qo'qon xonligi", ["qo'qon"]),
        ("Jadidchilik", ["jadid"]),
        ("1916-yil qo'zg'oloni", ["1916", "qo'zg'olon"]),
        ("Mustaqillik", ["mustaqillik"]),
        ("Konstitutsiya", ["konstitutsiya"]),
    ],
    "jahon_tarixi": [
        ("Qadimgi Misr", ["misr"]),
        ("Yunoniston", ["yunon", "gretsiya"]),
        ("Rim", ["rim"]),
        ("Uyg'onish davri", ["uyg'onish", "renessans"]),
        ("Buyuk geografik kashfiyotlar", ["kashfiyot", "kolumb"]),
        ("Fransuz inqilobi", ["fransuz inqilob", "inqilob"]),
        ("Sanoat to'ntarishi", ["sanoat"]),
        ("Birinchi jahon urushi", ["birinchi jahon"]),
        ("Ikkinchi jahon urushi", ["ikkinchi jahon"]),
        ("Sovuq urush", ["sovuq urush"]),
    ],
    "ozbek_adabiyoti": [
        ("Alpomish / doston", ["alpomish", "doston"]),
        ("Yusuf Xos Hojib", ["yusuf xos", "qutadg'u"]),
        ("Alisher Navoiy", ["navoiy"]),
        ("Bobur", ["bobur"]),
        ("Mashrab / Ogahiy", ["mashrab", "ogahiy", "munis"]),
        ("Cho'lpon", ["cho'lpon"]),
        ("Abdulla Qodiriy", ["qodiriy"]),
        ("Fitrat", ["fitrat"]),
        ("Oybek", ["oybek"]),
        ("G'afur G'ulom", ["g'afur", "g'ulom"]),
        ("She'r vaznlari", ["vazn", "aruz", "barmoq"]),
    ],
    "jahon_adabiyoti": [
        ("Gomer", ["gomer", "iliada", "odisse"]),
        ("Shekspir", ["shekspir"]),
        ("Servantes", ["servantes", "don kixot"]),
        ("Gyote", ["gyote", "faust"]),
        ("Pushkin", ["pushkin"]),
        ("Tolstoy", ["tolstoy"]),
        ("Dostoyevskiy", ["dostoyevskiy"]),
        ("Hemingway", ["hemingu", "hemingway"]),
        ("Romantizm", ["romantizm"]),
        ("Realizm", ["realizm"]),
    ],
    "koreys_tili": [
        ("Hangul alifbosi", ["hangul", "alifbo"]),
        ("Sonlar", ["son"]),
        ("Fe'l zamonlari", ["zamon"]),
        ("Hurmat shakllari", ["hurmat", "nutq uslub"]),
        ("Kelishiklar", ["kelishik", "qo'shimcha"]),
        ("Sifat", ["sifat"]),
    ],
    "fransuz_tili": [
        ("Artikllar", ["artikl"]),
        ("Être va avoir", ["etre", "avoir", "être"]),
        ("Hozirgi zamon", ["hozirgi zamon", "present"]),
        ("O'tgan zamon", ["o'tgan zamon", "passe", "passé"]),
        ("Kelasi zamon", ["kelasi zamon", "futur"]),
        ("Sonlar", ["son"]),
        ("Olmoshlar", ["olmosh"]),
    ],
    "ingliz_tili": [
        ("Artikllar", ["artikl", "article"]),
        ("Relative clauses", ["relative", "aniqlovchi ergash"]),
        ("Conditionals", ["conditional", "shart gap"]),
        ("Passive voice", ["passive", "majhul"]),
        ("Reported speech", ["reported", "o'zlashtirma"]),
        ("Phrasal verbs", ["phrasal", "frazeologik fe'l"]),
    ],
}


def main() -> int:
    missing: list[str] = []
    for slug, topics in CHECKS.items():
        subject = SKILLTREE_OUTLINE.get(slug)
        if not subject:
            continue
        lessons = [l["title"]["uz"].lower() for u in subject["units"] for l in u["lessons"]]
        print(f"\n{slug}  ({len(lessons)} lessons)")
        for name, spellings in topics:
            hit = next((l for t in spellings for l in lessons if t in l), None)
            if hit:
                print(f"   OK  {name:18} → {hit[:58]}")
            else:
                print(f"   --  {name:18} not named in any lesson title")
                missing.append(f"{slug}: {name}")

    print("\n" + "=" * 60)
    if missing:
        print("Worth a look (a title may still cover it under another name):")
        for m in missing:
            print(f"   {m}")
    else:
        print("Every checked topic is named somewhere.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
