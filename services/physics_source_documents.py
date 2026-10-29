"""Pinned textbook identity: a segment manifest is never a whole-PDF digest."""

import hashlib
import json
import re
from pathlib import Path


def source_identity(book):
    if book.get("source_kind") != "ordered_pdf_segments":
        if not re.fullmatch(r"[0-9a-f]{64}", book.get("sha256", "")):
            raise ValueError("single_pdf_source_digest")
        return {"sha256": book["sha256"]}
    segments = book["segments"]
    if not segments:
        raise ValueError("source_segments_required")
    expected = 1
    for segment in segments:
        if (
            segment["start"] != expected
            or segment["pages"] < 1
            or segment["end"] - segment["start"] + 1 != segment["pages"]
            or Path(segment["file_name"]).name != segment["file_name"]
            or not re.fullmatch(r"[0-9a-f]{64}", segment["sha256"])
        ):
            raise ValueError("source_segments_not_contiguous")
        expected = segment["end"] + 1
    digest = hashlib.sha256(json.dumps(segments, sort_keys=True).encode()).hexdigest()
    if (
        "sha256" in book
        or expected - 1 != book["pdf_page_count"]
        or digest != book["source_set_sha256"]
    ):
        raise ValueError("source_segment_manifest_identity")
    return {"source_kind": "ordered_pdf_segments", "source_set_sha256": digest}


def segment_page(book, pdf_page):
    source_identity(book)
    segment = next(
        (s for s in book["segments"] if s["start"] <= pdf_page <= s["end"]), None
    )
    if segment is None:
        raise ValueError("source_page_outside_segments")
    return {
        "pdf_page": pdf_page,
        "segment_file_name": segment["file_name"],
        "segment_local_pdf_page": pdf_page - segment["start"] + 1,
        "segment_sha256": segment["sha256"],
    }
