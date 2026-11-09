"""Portable frozen baselines plus six explicitly reviewed integration files.

No lesson/catalogue/source evidence file may use the runtime review exception.
Original manifests are never rewritten. Unknown byte changes fail closed.
"""
import hashlib
import json

REVIEW_SHA256 = "83b9693dca223905b9b5ba3370da9622b4b0a9b0e1e5971904ee44b3b5906cbd"
REVIEW_PATH = "docs/beta/shared_runtime_review_20261107.json"
RUNTIME_PATHS = {
    "services/curriculum.py", "services/db.py", "main.py",
    "services/assessment_runtime.py", "services/chemistry_runtime.py",
    "services/study.py",
}


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
