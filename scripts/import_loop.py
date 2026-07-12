"""Keep running the resumable College Scorecard import until the full set is in.

DEMO_KEY is rate-limited (~1,000 rows/hour), so this runs the importer, and if it
hasn't finished, waits out the hourly window and runs again — until every
degree-granting US institution is imported. Launch in the background:
    python scripts/import_loop.py
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(__file__)
STATE = os.path.join(HERE, ".import_colleges_state.json")
IMPORT = os.path.join(HERE, "import_colleges.py")
WAIT = 3720  # 62 minutes — just past the hourly rate-limit window

for attempt in range(1, 13):  # safety cap: ~12 hours
    print(f"=== import run {attempt} ===", flush=True)
    subprocess.run([sys.executable, IMPORT])
    try:
        st = json.load(open(STATE, encoding="utf-8"))
    except Exception:  # noqa: BLE001
        st = {"next_page": 0}
    if st.get("next_page", 0) == 0:
        print("IMPORT COMPLETE — full US set imported.", flush=True)
        break
    print(f"not finished (next page {st.get('next_page')}/{st.get('total')}); waiting {WAIT}s…", flush=True)
    time.sleep(WAIT)
