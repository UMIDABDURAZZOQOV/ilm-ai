"""Import European universities from the open Hipolabs universities dataset.

Source: http://universities.hipolabs.com  (open list of world universities:
name, country, domains, web_pages). It has no admission stats — European systems
don't use SAT/acceptance-rate the same way — but it gives real names and domains,
which drive the logos. Writes ../ilm-ai-frontend/public/colleges-eu.json.
"""

import json
import os
import re
import urllib.parse
import urllib.request

BASE = "http://universities.hipolabs.com/search"
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ilm-ai-frontend", "public", "colleges-eu.json")

# Major European higher-ed countries (broad, not a proprietary ranking).
COUNTRIES = [
    "United Kingdom", "Germany", "France", "Italy", "Spain", "Netherlands",
    "Switzerland", "Sweden", "Belgium", "Austria", "Denmark", "Finland",
    "Norway", "Ireland", "Poland", "Portugal", "Czech Republic", "Greece",
    "Hungary", "Romania",
]
CAP = 500


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return "eu-" + s[:56]


def fetch(country: str):
    url = f"{BASE}?{urllib.parse.urlencode({'country': country})}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except Exception as e:  # noqa: BLE001
        print(f"  {country}: {e}")
        return []


def main():
    rows = []
    seen = set()
    for country in COUNTRIES:
        data = fetch(country)
        print(f"{country}: {len(data)}")
        for u in data:
            name = u.get("name")
            if not name:
                continue
            cid = slugify(name)
            if cid in seen:
                continue
            seen.add(cid)
            web = (u.get("web_pages") or [""])[0]
            state = (u.get("state-province") or country)
            rows.append({
                "id": cid,
                "name": name,
                "city": "",
                "state": state,
                "country": country,
                "region": "Europe",
                "type": "Public",
                "website": web,
            })

    rows.sort(key=lambda c: c["name"])
    rows = rows[:CAP]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False)
    print(f"Wrote {len(rows)} European universities -> {os.path.abspath(OUT)}")


if __name__ == "__main__":
    main()
