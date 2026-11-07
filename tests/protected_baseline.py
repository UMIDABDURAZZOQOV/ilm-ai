"""Portable frozen baselines plus three explicitly reviewed integration files.

No lesson/catalogue/source evidence file may use the runtime review exception.
Original manifests are never rewritten. Unknown byte changes fail closed.
"""
import hashlib
import json

REVIEW_SHA256 = "1e608f43ba6b17e35eb2359e6b08ee319a95243f351518d84c36319d818f4bfd"
REVIEW_PATH = "docs/beta/shared_runtime_review_20261107.json"
RUNTIME_PATHS = {"services/curriculum.py", "services/db.py", "main.py"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def assert_protected_file(root, name, expected, baseline):
    data = (root / name).read_bytes()
    variants = {digest(data)}
    # The historical manifests include Windows CRLF Python file hashes. Only
    # Python/JSON text newline representation is portable. PDF/image evidence
    # stays byte-exact. No trimming, BOM stripping or JSON reserialization.
    if name.endswith((".py", ".json")):
        lf = data.replace(b"\r\n", b"\n")
        variants.update({digest(lf), digest(lf.replace(b"\n", b"\r\n"))})
    if expected in variants:
        return
    assert name in RUNTIME_PATHS, name
    review_bytes = (root / REVIEW_PATH).read_bytes().replace(b"\r\n", b"\n")
    assert digest(review_bytes) == REVIEW_SHA256, "integration_review_manifest_changed"
    review = json.loads(review_bytes)
    assert review["schema_version"] == 1
    assert {row["path"] for row in review["files"]} == RUNTIME_PATHS
    row = next(row for row in review["files"] if row["path"] == name)
    assert row["original_baselines"].get(baseline) == expected, name
    assert digest(data.replace(b"\r\n", b"\n")) == row["current_lf_sha256"], name
