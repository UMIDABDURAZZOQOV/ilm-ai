"""Segment/OCR provenance remains distinct from whole-PDF and native-text hashes."""

import hashlib
import json
from copy import deepcopy

import pytest

from scripts.audit_physics_source_pages import check_book_pages
from services.physics_curriculum import DIRECTORY
from services.physics_source_documents import segment_page, source_identity


def digest(data):
    return hashlib.sha256(data).hexdigest()


@pytest.mark.parametrize("grade", [8, 9])
def test_existing_split_catalogue_identity_and_boundary_pages(grade):
    book = next(
        b
        for b in json.loads((DIRECTORY / "physics_sources.json").read_text())["books"]
        if b["grade"] == grade
    )
    identity = source_identity(book)
    assert "sha256" not in identity
    assert identity["source_set_sha256"] == book["source_set_sha256"]
    for part in book["segments"]:
        assert segment_page(book, part["start"])["segment_local_pdf_page"] == 1
        assert (
            segment_page(book, part["end"])["segment_local_pdf_page"] == part["pages"]
        )
    with pytest.raises(ValueError):
        segment_page(book, book["pdf_page_count"] + 1)


@pytest.fixture
def split_book(tmp_path):
    fitz = pytest.importorskip(
        "fitz",
        reason="Install requirements-source-review.txt for PDF/OCR evidence checks",
    )

    parts = []
    pages = []
    evidence = []
    ocr_root = tmp_path / "ocr" / "g8-ocr"
    ocr_root.mkdir(parents=True)
    for n in [1, 2]:
        path = tmp_path / f"part{n}.pdf"
        with fitz.open() as doc:
            page = doc.new_page(width=180, height=200)
            page.insert_text((20, 40), f"test source page {n}")
            doc.save(path)
        part = {
            "file_name": path.name,
            "start": n,
            "end": n,
            "pages": 1,
            "sha256": digest(path.read_bytes()),
        }
        parts.append(part)
        with fitz.open(path) as doc:
            raw = digest(doc[0].get_text().encode())
            pix = doc[0].get_pixmap(matrix=fitz.Matrix(2.2, 2.2))
            render = digest(doc[0].get_pixmap(matrix=fitz.Matrix(2, 2)).tobytes("png"))
            text = f"Synthetic OCR search text {n}, not a native PDF text layer."
            (ocr_root / f"p{n:03}.txt").write_text(text)
            pages.append(
                {
                    "pdf_page": n,
                    "printed_page": n,
                    "digital_text_sha256": raw,
                    "text_sha256": digest(text.encode()),
                    "raster_sha256": digest(pix.samples),
                    "raster_size": [pix.width, pix.height],
                }
            )
            evidence.append(
                {
                    "pdf_page": n,
                    "printed_page": n,
                    "text_sha256": digest(text.encode()),
                    "digital_text_sha256": raw,
                    "reviewed_render_sha256": render,
                }
            )
    book = {
        "grade": 8,
        "source_kind": "ordered_pdf_segments",
        "source_set_sha256": digest(json.dumps(parts, sort_keys=True).encode()),
        "segments": parts,
        "pdf_page_count": 2,
        "page_audit": pages,
    }
    for e in evidence:
        e["source_segment"] = segment_page(book, e["pdf_page"])
    return book, evidence, tmp_path


@pytest.mark.parametrize(
    "change", ["gap", "reorder", "manifest", "whole_hash", "empty", "count"]
)
def test_segment_manifest_cannot_impersonate_whole_pdf_or_change_order(change):
    book = deepcopy(
        next(
            b
            for b in json.loads((DIRECTORY / "physics_sources.json").read_text())[
                "books"
            ]
            if b["grade"] == 8
        )
    )
    if change == "gap":
        book["segments"][1]["start"] = 3
    if change == "reorder":
        book["segments"].reverse()
    if change == "manifest":
        book["source_set_sha256"] = "0" * 64
    if change == "whole_hash":
        book["sha256"] = "0" * 64
    if change == "empty":
        book["segments"] = []
    if change == "count":
        book["pdf_page_count"] += 1
    with pytest.raises(ValueError):
        source_identity(book)


def test_private_split_pdf_native_raster_review_and_cached_ocr_are_all_checked(
    split_book,
):
    book, pages, directory = split_book
    assert check_book_pages(book, pages, directory, directory / "ocr") == 2
    (directory / "ocr" / "g8-ocr" / "p002.txt").write_text("Changed OCR")
    with pytest.raises(ValueError, match="ocr_hash"):
        check_book_pages(book, pages, directory, directory / "ocr")


@pytest.mark.parametrize("change", ["binding", "native", "pixels", "pdf_bytes"])
def test_original_page_and_segment_evidence_tampering_is_detected(split_book, change):
    book, pages, directory = split_book
    pages = deepcopy(pages)
    if change == "binding":
        pages[1]["source_segment"]["segment_local_pdf_page"] = 2
    if change == "native":
        pages[0]["digital_text_sha256"] = "0" * 64
    if change == "pixels":
        pages[0]["reviewed_render_sha256"] = "0" * 64
    if change == "pdf_bytes":
        path = directory / "part2.pdf"
        path.write_bytes(path.read_bytes() + b"\n% altered bytes\n")
    with pytest.raises(ValueError):
        check_book_pages(book, pages, directory, directory / "ocr")
