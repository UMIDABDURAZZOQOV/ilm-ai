"""Import the full US college directory from the public College Scorecard API.

Data source: U.S. Department of Education, College Scorecard
(https://collegescorecard.ed.gov/data/) — a U.S. government work in the public
domain. This pulls ~6,000 degree-granting institutions with the fields the
College App platform needs (name, location, ownership, admission rate, median
SAT, size, website) and writes them to a JSON file the frontend can load.

Usage
-----
1. Get a free API key at https://api.data.gov/signup/  (instant, no cost).
2. Set it:   export COLLEGE_SCORECARD_API_KEY=your_key   (Windows: $env:...)
3. Run:      python scripts/import_colleges.py
   -> writes ../ilm-ai-frontend/public/colleges-us.json

The frontend's curated list (with famous professors) is merged on top by id, so
richer detail for the top universities is preserved.
"""

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

API = "https://api.data.gov/ed/collegescorecard/v1/schools"
FIELDS = ",".join([
    "id",
    "school.name",
    "school.city",
    "school.state",
    "school.ownership",
    "school.school_url",
    "latest.admissions.admission_rate.overall",
    "latest.admissions.sat_scores.average.overall",
    "latest.student.size",
])
OWNERSHIP = {1: "Public", 2: "Private Nonprofit", 3: "Private Nonprofit"}
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "ilm-ai-frontend", "public", "colleges-us.json")


def slugify(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s[:60]


STATE = os.path.join(os.path.dirname(__file__), ".import_colleges_state.json")


def fetch_page(key: str, page: int, per_page: int = 100):
    params = {
        "api_key": key,
        "fields": FIELDS,
        "per_page": per_page,
        "page": page,
        "school.degrees_awarded.predominant__range": "1..4",  # certificate through graduate (~6,000)
        "sort": "latest.student.size:desc",
    }
    url = f"{API}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def row_to_college(row):
    name = row.get("school.name")
    if not name:
        return None
    acc = row.get("latest.admissions.admission_rate.overall")
    sat = row.get("latest.admissions.sat_scores.average.overall")
    url = row.get("school.school_url") or ""
    if url and not url.startswith("http"):
        url = "https://" + url
    return {
        "id": f"{slugify(name)}-{row.get('id')}",
        "name": name,
        "city": row.get("school.city") or "",
        "state": row.get("school.state") or "",
        "country": "United States",
        "region": "US",
        "type": OWNERSHIP.get(row.get("school.ownership"), "Private Nonprofit"),
        "acceptanceRate": round(acc * 100, 1) if acc else None,
        "medianSAT": int(sat) if sat else None,
        "size": f"{int(row['latest.student.size']):,}" if row.get("latest.student.size") else None,
        "website": url,
    }


def main():
    # DEMO_KEY works out of the box (rate-limited to ~30/hour, so this script is
    # resumable — re-run it each hour and it continues where it left off until
    # the full ~6,000 are imported). Set your own key for higher limits.
    key = os.environ.get("COLLEGE_SCORECARD_API_KEY") or "DEMO_KEY"

    # Resume from prior progress.
    by_id = {}
    if os.path.exists(OUT):
        try:
            for c in json.load(open(OUT, encoding="utf-8")):
                by_id[c["id"]] = c
        except Exception:  # noqa: BLE001
            pass
    state = {"next_page": 0, "total": None}
    if os.path.exists(STATE):
        try:
            state.update(json.load(open(STATE, encoding="utf-8")))
        except Exception:  # noqa: BLE001
            pass

    per_page = 100
    page = state["next_page"]
    fetched_this_run = 0
    while True:
        try:
            data = fetch_page(key, page, per_page)
        except Exception as e:  # noqa: BLE001
            print(f"stopped at page {page}: {e} (re-run later to continue)")
            break
        meta = data["metadata"]
        state["total"] = meta["total"]
        pages = (meta["total"] + per_page - 1) // per_page
        for row in data["results"]:
            c = row_to_college(row)
            if c:
                by_id[c["id"]] = c
        fetched_this_run += len(data["results"])
        page += 1
        state["next_page"] = page
        if page >= pages:
            state["next_page"] = 0  # finished — next run refreshes from the top
            print("reached the last page — full set imported.")
            break
        time.sleep(0.4)

    colleges = sorted(by_id.values(), key=lambda c: c["name"])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(colleges, f, ensure_ascii=False)
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(state, f)
    print(f"+{fetched_this_run} this run · {len(colleges)} total / {state['total']} · next page {state['next_page']}")
    print(f"Wrote -> {os.path.abspath(OUT)}")


if __name__ == "__main__":
    main()
