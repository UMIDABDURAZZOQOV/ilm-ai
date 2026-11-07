import json
from pathlib import Path
import pytest
from tests.protected_baseline import assert_protected_file, digest, REVIEW_PATH


def test_only_text_line_endings_are_portable(tmp_path):
    (tmp_path / "same.py").write_bytes(b"value = 1\n")
    assert_protected_file(tmp_path, "same.py", digest(b"value = 1\r\n"), "world_history")
    (tmp_path / "same.py").write_bytes(b"value = 1\r\n")
    assert_protected_file(tmp_path, "same.py", digest(b"value = 1\n"), "world_history")
    (tmp_path / "same.py").write_bytes(b"value = 2\n")
    with pytest.raises(AssertionError):
        assert_protected_file(tmp_path, "same.py", digest(b"value = 1\n"), "world_history")


def test_source_claims_and_binary_evidence_are_still_exact(tmp_path):
    (tmp_path / "facts.json").write_bytes(b'{}\n')
    assert_protected_file(tmp_path, "facts.json", digest(b'{}\r\n'), "world_history")
    (tmp_path / "facts.json").write_bytes(b'{"forged":true}\n')
    with pytest.raises(AssertionError):
        assert_protected_file(tmp_path, "facts.json", digest(b'{}\r\n'), "world_history")
    (tmp_path / "source.pdf").write_bytes(b'%PDF\n')
    with pytest.raises(AssertionError):
        assert_protected_file(tmp_path, "source.pdf", digest(b'%PDF\r\n'), "world_history")


def test_runtime_override_is_bound_to_original_manifest_and_exact_new_bytes(tmp_path):
    root = Path(__file__).resolve().parents[1]
    review = json.loads((root / REVIEW_PATH).read_text())
    row = next(x for x in review["files"] if x["path"] == "services/curriculum.py")
    target = tmp_path / row["path"]
    target.parent.mkdir(parents=True)
    target.write_bytes((root / row["path"]).read_bytes())
    manifest = tmp_path / REVIEW_PATH
    manifest.parent.mkdir(parents=True)
    manifest.write_bytes((root / REVIEW_PATH).read_bytes())
    original = row["original_baselines"]["world_history"]
    assert_protected_file(tmp_path, row["path"], original, "world_history")
    with pytest.raises(AssertionError):
        assert_protected_file(tmp_path, row["path"], "0" * 64, "world_history")
    target.write_bytes(target.read_bytes() + b"\n# unreviewed mutation\n")
    with pytest.raises(AssertionError):
        assert_protected_file(tmp_path, row["path"], original, "world_history")
    manifest.write_bytes(b'{"unreviewed":true}')
    with pytest.raises(AssertionError, match="integration_review_manifest_changed"):
        assert_protected_file(tmp_path, row["path"], original, "world_history")
