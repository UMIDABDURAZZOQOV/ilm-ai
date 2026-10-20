"""Decode every page of the pinned user PDFs into a PRIVATE, local OCR cache.

Requires Poppler and Tesseract (eng). OCR is for heading lookup only; teaching
facts still require visual review. Never commit this cache or the source PDFs.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

REVIEW = Path(__file__).with_name("curriculum") / "biology_scanned_review.json"


def source_paths(root, book):
    paths = []
    cursor = 1
    for segment in book["segments"]:
        matches = list(root.rglob(segment["file_name"]))
        if len(matches) != 1:
            raise ValueError(
                "Missing/ambiguous source segment: " + segment["file_name"]
            )
        path = matches[0]
        if hashlib.sha256(path.read_bytes()).hexdigest() != segment["sha256"]:
            raise ValueError("Unreviewed source segment: " + segment["file_name"])
        if (
            segment["start"] != cursor
            or segment["pages"] != segment["end"] - cursor + 1
        ):
            raise ValueError("Non-contiguous source segments")
        cursor = segment["end"] + 1
        paths.append((segment, path))
    return paths


def decode(job):
    path, local_page = job
    with tempfile.TemporaryDirectory(prefix="biology-ocr-") as temp:
        stem = Path(temp) / "page"
        subprocess.run(
            [
                "pdftoppm",
                "-f",
                str(local_page),
                "-l",
                str(local_page),
                "-scale-to",
                "1800",
                "-singlefile",
                "-png",
                str(path),
                str(stem),
            ],
            check=True,
            capture_output=True,
        )
        return subprocess.check_output(
            [
                "tesseract",
                str(stem.with_suffix(".png")),
                "stdout",
                "-l",
                "eng",
                "--psm",
                "3",
            ],
            text=True,
            stderr=subprocess.DEVNULL,
            env={**os.environ, "OMP_THREAD_LIMIT": "1"},
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-dir", required=True, type=Path)
    parser.add_argument("--cache", required=True, type=Path)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if not 1 <= args.workers <= 8:
        parser.error("workers must be between 1 and 8")
    args.cache.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": 1,
        "engine": "tesseract eng psm3 / Poppler 1800px",
        "books": [],
    }
    for book in json.loads(REVIEW.read_text())["books"]:
        paths = source_paths(args.pdf_dir, book)
        jobs = [
            (path, n) for segment, path in paths for n in range(1, segment["pages"] + 1)
        ]
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            pages = list(pool.map(decode, jobs))
        raw = json.dumps(pages, ensure_ascii=False)
        (args.cache / f"grade-{book['grade']}-ocr-pages.json").write_text(raw)
        manifest["books"].append(
            {
                "grade": book["grade"],
                "segments": book["segments"],
                "ocr_sha256": hashlib.sha256(raw.encode()).hexdigest(),
                "decoded_pages": len(pages),
            }
        )
        print(f"Grade {book['grade']}: {len(pages)} pages decoded")
    (args.cache / "ocr_cache_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
