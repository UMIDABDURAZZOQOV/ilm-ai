#!/bin/bash
# Generate question + theory content for the two subjects added on 2026-07-26,
# Geometriya and Geografiya, and their placement buckets. Resumable: both seeders
# skip lessons and buckets that already have content, so re-running after a quota
# stop or a machine restart picks up exactly where it left off.
#
#   bash scripts/fill_new_subjects.sh
cd "$(dirname "$0")/.."
set -a; . ./.env; set +a
export PYTHONIOENCODING=utf-8
export SEED_SLEEP=${SEED_SLEEP:-0.4}

log() { echo "[$(date +%H:%M:%S)] $*"; }

for subject in geometriya geografiya; do
  log "=== $subject: questions + theory"
  python scripts/seed_skilltree.py --subject "$subject" --per-lesson 10
  log "=== $subject: placement bucket"
  python scripts/seed_placement.py --subject "$subject" 2>/dev/null || \
    log "seed_placement.py not run for $subject (check its interface)"
done

log "done — dump fixtures next: python scripts/dump_skilltree_fixtures.py"
