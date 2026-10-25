"""Private-PDF checks for authored evidence; no source bytes are published."""

import hashlib
from contextlib import ExitStack
from pathlib import Path

from services.physics_source_documents import segment_page, source_identity


def check_book_pages(book, pages, directory, ocr_directory=None):
    import fitz

    directory = Path(directory)
    identity = source_identity(book)
    with ExitStack() as stack:
        documents = {}
        parts = (
            book.get("segments")
            if "source_set_sha256" in identity
            else [
                {
                    "file_name": book["file_name"],
                    "sha256": book["sha256"],
                    "pages": book["pdf_page_count"],
                }
            ]
        )
        for part in parts:
            paths = list(directory.rglob(part["file_name"]))
            if (
                len(paths) != 1
                or hashlib.sha256(paths[0].read_bytes()).hexdigest() != part["sha256"]
            ):
                raise ValueError("original_pdf_or_segment_hash_mismatch")
            doc = stack.enter_context(fitz.open(paths[0]))
            if len(doc) != part["pages"]:
                raise ValueError("original_pdf_or_segment_page_count")
            documents[part["file_name"]] = doc
        for evidence in pages:
            n = evidence["pdf_page"]
            source = book["page_audit"][n - 1]
            if "source_set_sha256" in identity:
                binding = segment_page(book, n)
                if evidence["source_segment"] != binding:
                    raise ValueError("reviewed_segment_page_mismatch")
                page = documents[binding["segment_file_name"]][
                    binding["segment_local_pdf_page"] - 1
                ]
                raw_digest = hashlib.sha256(page.get_text().encode()).hexdigest()
                if (
                    raw_digest != source["digital_text_sha256"]
                    or evidence["digital_text_sha256"] != raw_digest
                ):
                    raise ValueError("original_native_text_hash_mismatch")
                pix = page.get_pixmap(matrix=fitz.Matrix(2.2, 2.2))
                if [pix.width, pix.height] != source["raster_size"] or hashlib.sha256(
                    pix.samples
                ).hexdigest() != source["raster_sha256"]:
                    raise ValueError("original_catalogue_raster_hash_mismatch")
                if ocr_directory:
                    text = (
                        Path(ocr_directory) / f"g{book['grade']}-ocr" / f"p{n:03}.txt"
                    ).read_text()
                    if (
                        hashlib.sha256(text.encode()).hexdigest()
                        != evidence["text_sha256"]
                    ):
                        raise ValueError("private_reviewed_ocr_hash_mismatch")
            else:
                page = documents[book["file_name"]][n - 1]
                if (
                    hashlib.sha256(page.get_text().encode()).hexdigest()
                    != evidence["text_sha256"]
                ):
                    raise ValueError("original_page_text_or_pixels_mismatch")
            if (
                hashlib.sha256(
                    page.get_pixmap(matrix=fitz.Matrix(2, 2)).tobytes("png")
                ).hexdigest()
                != evidence["reviewed_render_sha256"]
            ):
                raise ValueError("original_page_text_or_pixels_mismatch")
    return len(pages)
