"""Source gaps and sandbox constraints must remain visible and fail closed."""

import json
import sys

import pytest

from scripts.audit_mathematics_sources import audit
from scripts.serve_mathematics_preview import main, sandbox_path
from services.mathematics_curriculum import ROOT, load_course, manifest


def test_missing_sources_are_not_counted_as_complete_and_duplicates_are_one_topic():
    source = manifest()
    assert len(source["books"]) == 23
    assert sum(b["pdf_pages"] for b in source["books"]) == 2958
    assert source["full_curriculum_topic_count"] is None
    assert not source["all_grades_complete"]
    blocked = {s["book_id"]: s["status"] for s in source["blocked_sources"]}
    assert (
        blocked["math-uz-g9-p1"]
        == blocked["math-uz-g11-p1"]
        == "transfer_blocked_32_MiB"
    )
    assert blocked["math-uz-g6-p2"] == "source_missing"
    assert all(
        blocked[f"math-uz-g{g}-geometry"] == "source_missing" for g in range(7, 11)
    )
    mapping = json.loads((ROOT / "grade1_part1_map.json").read_text())
    assert len(mapping["topics"]) == 41 and not mapping["full_map_verified"]
    repeated = mapping["topics"][24]
    assert repeated["canonical_pdf_pages"] == [53, 54]
    assert repeated["duplicate_pdf_pages"] == [55, 56]
    assert mapping["topics"][25]["body_pdf_pages_observed"] == [57, 58]
    assert len(load_course()) == 5  # TOC locators never become synthetic lessons.


def test_missing_pdf_fails_audit_before_any_completeness_claim(tmp_path):
    with pytest.raises(ValueError, match="missing_or_duplicate_source"):
        audit(tmp_path)


def test_git_and_symlink_sandbox_paths_are_refused(tmp_path):
    with pytest.raises(ValueError, match="outside_all_git"):
        sandbox_path(str(ROOT / "new-sandbox"), False)
    symlink = tmp_path / "link"
    symlink.symlink_to(tmp_path)
    with pytest.raises(ValueError, match="symlinks"):
        sandbox_path(str(symlink), True)


def test_production_cli_is_rejected_before_any_directory_or_database_write(
    tmp_path, monkeypatch
):
    target = tmp_path / "must-not-exist"
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setattr(
        sys,
        "argv",
        ["serve_mathematics_preview", "--directory", str(target), "--create-only"],
    )
    with pytest.raises(SystemExit) as result:
        main()
    assert result.value.code == 2 and not target.exists()
