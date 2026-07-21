#!/bin/bash
# Fill the skill tree from wherever it left off, then STOP as soon as the Gemini
# free tier is exhausted.
#
# The machine this runs on is not always on, so an overnight idle loop is useless:
# a pass that generates nothing means every key is out of daily quota, and the only
# useful thing left to do is exit and print how far it got. Re-run it tomorrow (or
# after adding keys to GEMINI_API_KEYS) and it picks up exactly where it stopped --
# both seeders skip lessons and buckets that are already complete.
#
#   bash scripts/fill_content.sh
cd "$(dirname "$0")/.."
set -a; . ./.env; set +a
export PYTHONIOENCODING=utf-8
export SEED_GEMINI_MODEL=${SEED_GEMINI_MODEL:-gemini-flash-lite-latest}
export SEED_SLEEP=${SEED_SLEEP:-0.4}

count() {
  python -c "
import sys; sys.path.insert(0,'.')
from services.db import SessionLocal
from services.models import SkillQuestion, PlacementQuestion
db = SessionLocal()
print(db.query(SkillQuestion).count() + db.query(PlacementQuestion).count())" 2>/dev/null | tail -1
}

progress() {
  python -c "
import sys; sys.path.insert(0,'.')
from services.db import SessionLocal
from services.models import SkillLesson, SkillQuestion, PlacementQuestion
db = SessionLocal()
done = db.query(SkillQuestion.lesson_id).distinct().count()
print(f'{done}/{db.query(SkillLesson).count()} lessons ready, '
      f'{db.query(SkillQuestion).count()} questions, '
      f'{db.query(PlacementQuestion).count()} placement')" 2>/dev/null | tail -1
}

for pass in $(seq 1 100); do
  BEFORE=$(count)
  echo "=== pass $pass  $(date '+%H:%M:%S')  ($(progress)) ==="

  python -u scripts/expand_taxonomy.py                >> /tmp/expand.log    2>&1
  python -u scripts/seed_skilltree.py                 >> /tmp/content.log   2>&1
  python -u scripts/seed_placement.py --per-bucket 12 >> /tmp/placement.log 2>&1

  AFTER=$(count)
  echo "pass $pass added $((AFTER - BEFORE))"

  if [ "$AFTER" = "$BEFORE" ]; then
    echo
    echo "=== STOPPING: every API key is out of quota ==="
    echo "progress: $(progress)"
    echo "re-run this script tomorrow, or add keys to GEMINI_API_KEYS first."
    exit 3
  fi
done
echo "=== ALL DONE: $(progress) ==="
