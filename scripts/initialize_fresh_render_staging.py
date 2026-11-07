"""Explicit one-time Free staging build action, never a production startup hook.

Requires the exact freshly provisioned Render DB ID and an empty account/content
database. Does not accept arbitrary URLs/hosts, production identities or existing
learner data. All secrets stay in environment; failures print fixed labels only.
"""
import argparse
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def require_fresh_staging_target(env, database_id):
    from services.deployment_config import staging_errors
    if staging_errors(env) or env.get("STAGING_AUTH_SETUP_PENDING") != "true":
        raise ValueError("isolated_pending_staging_required")
    if not re.fullmatch(r"dpg-[a-z0-9]{20}-[a-z]", database_id):
        raise ValueError("explicit_render_database_id_required")
    uri = urlsplit(env["DATABASE_URL"])
    if uri.hostname != database_id or env["STAGING_DATABASE_HOST"] != database_id:
        raise ValueError("exact_new_internal_database_required")
    if not env.get("RENDER_SERVICE_ID", "").startswith("srv-"):
        raise ValueError("render_build_environment_required")
    if env.get("RENDER_SERVICE_ID") == "srv-d99id4mcjfls738a8l80":
        raise ValueError("production_service_forbidden")


def initialize(database_id):
    require_fresh_staging_target(os.environ, database_id)
    from alembic import command
    from alembic.config import Config
    from sqlalchemy import inspect, text
    from sqlalchemy.orm import Session
    from services.db import engine

    # The only previously allowed state is a schema-only rehearsal with no
    # account or lesson content. No arbitrary destructive cleanup is performed.
    content = {"users", "skilltree_lessons", "curriculum_v2_lessons",
               "chemistry_preview_lessons", "world_history_preview_lessons",
               "uzbekistan_history_preview_lessons"}
    with engine.connect() as conn:
        uri = urlsplit(os.environ["DATABASE_URL"])
        if conn.execute(text("SELECT current_database(), current_user")).one() != (
            uri.path[1:], uri.username,
        ):
            raise ValueError("database_identity_mismatch")
        names = set(inspect(conn).get_table_names())
        for table in sorted(names & content):
            if conn.execute(text('SELECT COUNT(*) FROM "' + table + '"')).scalar_one():
                raise ValueError("nonempty_database_requires_review")
        if names and "alembic_version" not in names:
            raise ValueError("unknown_existing_schema_requires_review")
    cfg = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
    with engine.begin() as conn:
        cfg.attributes["connection"] = conn
        command.upgrade(cfg, "head")
    from services.reviewed_publication_import import import_reviewed_publication
    with Session(engine) as db, db.begin():
        result = import_reviewed_publication(db)
    with engine.connect() as conn:
        counts = {table: conn.execute(text('SELECT COUNT(*) FROM "' + table + '"')).scalar_one()
                  for table in sorted(content)}
        head = conn.execute(text("SELECT version_num FROM alembic_version")).scalar_one()
    if counts["users"] != 0 or sum(v for k, v in counts.items() if k != "users") != 1381:
        raise ValueError("publication_count_requires_review")
    return {"isolated_staging_initialized": True, "alembic_head": head,
            "counts": counts, "publication": result, "production_signoff": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--new-database-id", required=True)
    parser.add_argument("--apply", action="store_true", required=True)
    args = parser.parse_args()
    try:
        result = initialize(args.new_database_id)
    except Exception:
        print('{"isolated_staging_initialized":false,"error":"fresh_staging_initialization_rejected_or_failed"}')
        return 1
    print(json.dumps(result), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
