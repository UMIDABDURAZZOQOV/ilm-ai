"""Purge only fixed, ownership-checked paths. Never recursive directory deletion."""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import secrets

from fastapi import HTTPException
from services.account_ownership import USER_FILES
from services.private_file_lock import exclusive_file_lock


def _safe(path, root):
    if root != path and root not in path.parents:
        raise ValueError("account_storage_path_outside_root")
    for parent in [path, *path.parents]:
        if parent.is_symlink() or (
            parent.exists()
            and bool(getattr(parent.lstat(), "st_file_attributes", 0) & 0x400)
        ):
            raise ValueError("account_storage_symlink_forbidden")
    return path


def storage_root():
    raw = os.getenv("ACCOUNT_DELETION_STORAGE_ROOT", "")
    path = Path(raw).absolute()
    if not raw or not Path(raw).is_absolute() or not path.is_dir():
        raise HTTPException(503, "account_deletion_storage_not_configured")
    if os.getenv("ENVIRONMENT") == "production" and path != Path.cwd().absolute():
        raise HTTPException(503, "account_deletion_storage_root_mismatch")
    _safe(path, path)
    return path


def _replace(path, value):
    temporary = path.with_name(path.name + ".deletion-" + secrets.token_hex(8))
    try:
        with os.fdopen(
            os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600),
            "w",
            encoding="utf8",
        ) as output:
            output.write(value)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def purge_account_files(user_id, email_hash, requested_at):
    from services.account_deletion import digest
    from services.study import aware

    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("invalid_account_identity")
    root = storage_root()
    # Writers are serialized by the active-account DB lock; after revocation
    # they cannot recreate these user files. Missing paths are idempotent.
    for directory in USER_FILES:
        path = _safe(root / directory / f"user_{user_id}.json", root)
        path.unlink(missing_ok=True)
    feedback = _safe(root / "data/feedback/feedback.jsonl", root)
    if feedback.exists():
        lock = _safe(feedback.with_suffix(".lock"), root)
        with exclusive_file_lock(lock):
            if feedback.stat().st_size > 100 * 1024 * 1024:
                raise ValueError("feedback_cleanup_requires_operator")
            temporary = feedback.with_name(
                feedback.name + ".deletion-" + secrets.token_hex(8)
            )
            try:
                with (
                    feedback.open(encoding="utf8") as source,
                    os.fdopen(
                        os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600),
                        "w",
                        encoding="utf8",
                    ) as output,
                ):
                    while line := source.readline(1024 * 1024 + 1):
                        if len(line) > 1024 * 1024:
                            raise ValueError("feedback_record_requires_review")
                        entry = json.loads(line)
                        if not isinstance(entry, dict):
                            raise ValueError("feedback_layout_requires_review")
                        email = entry.get("email")
                        if (
                            isinstance(email, str)
                            and digest("email:" + email.strip().lower()) == email_hash
                        ):
                            if not isinstance(entry.get("submitted_at"), str):
                                raise ValueError("feedback_timestamp_requires_review")
                            submitted = datetime.fromisoformat(entry["submitted_at"])
                            if submitted.tzinfo is None:
                                submitted = submitted.replace(tzinfo=timezone.utc)
                            if submitted <= aware(requested_at):
                                continue
                        output.write(line)
                os.replace(temporary, feedback)
            finally:
                temporary.unlink(missing_ok=True)
    # Database mode may still have legacy snapshots. Remove only this UID;
    # unknown layouts fail pending cleanup rather than erasing another account.
    layouts = [
        ("users.json", "list"),
        ("data/payments/checkout_sessions.json", "dict"),
        ("data/refresh_tokens.json", "dict"),
    ]
    for relative, kind in layouts:
        path = _safe(root / relative, root)
        if not path.exists():
            continue
        with exclusive_file_lock(_safe(path.with_suffix(".deletion.lock"), root)):
            if path.stat().st_size > 10 * 1024 * 1024:
                raise ValueError("legacy_cleanup_requires_operator")
            data = json.loads(path.read_text(encoding="utf8"))
            if kind == "list":
                if not isinstance(data, list) or any(
                    not isinstance(r, dict) or "id" not in r for r in data
                ):
                    raise ValueError("legacy_users_layout_requires_review")
                kept = [r for r in data if str(r["id"]) != str(user_id)]
            else:
                if not isinstance(data, dict) or any(
                    not isinstance(r, dict) or "user_id" not in r for r in data.values()
                ):
                    raise ValueError("legacy_owner_layout_requires_review")
                kept = {
                    k: r for k, r in data.items() if str(r["user_id"]) != str(user_id)
                }
            _replace(path, json.dumps(kept, ensure_ascii=False))
