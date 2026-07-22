"""
ocr_pages.py — read a scanned Cambridge PDF with the OCR engine built into Windows.

Cambridge 19 arrived as a 138-page scan with no text layer at all: pypdf, pdfplumber
and pdfium all return zero characters. Unlike book 20, where a second re-typeset file
carried the Listening and Reading papers, there is no other copy — everything has to
come off the picture.

Windows' own OCR was chosen after rapidocr produced text that could not be shown to a
student: it merges words, so a question read "WhatwillhappeninStanthorpetomarkthe25th".
Windows keeps the spacing, is right about the characters, and takes 0.4s a page against
rapidocr's 38 — the whole book in under two minutes rather than an hour and a half.

Words are stored with their boxes, not as finished lines, because the engine returns
lines in its own order: on a Listening page the question numbers come back as five
lines of their own, separated from the sentences they belong to. `parse_ielts21.py`
rebuilds the visual lines from the positions instead.

Answer-key pages are the exception and are read by rapidocr instead (`--keys`). Windows
OCR does not see an isolated capital letter: on the Test 2 Listening key it returned ten
of the twenty single-letter answers, silently, at every resolution from 150 to 375 dpi.
Those pages are almost entirely isolated letters, and a missing answer marks a correct
student wrong — so accuracy there beats the speed and the spacing.

    python scripts/ocr_pages.py "<pdf>" 19 [--from 1] [--to 138]
    python scripts/ocr_pages.py "<pdf>" 19 --keys 121 128
"""
from __future__ import annotations

import argparse
import asyncio
import io
import json
import os
import sys

import pypdfium2 as pdfium
import winsdk.windows.globalization as wg
import winsdk.windows.graphics.imaging as wgi
import winsdk.windows.media.ocr as wmo
import winsdk.windows.storage.streams as wss

OUT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seeds", "ocr")
SCALE = 2.0        # 150dpi-ish; the engine is no more accurate above this


async def read_page(engine, image) -> list[dict]:
    buf = io.BytesIO()
    image.save(buf, format="PNG")

    stream = wss.InMemoryRandomAccessStream()
    writer = wss.DataWriter(stream.get_output_stream_at(0))
    writer.write_bytes(buf.getvalue())
    await writer.store_async()
    await writer.flush_async()
    stream.seek(0)

    decoder = await wgi.BitmapDecoder.create_async(stream)
    bitmap = await decoder.get_software_bitmap_async()
    result = await engine.recognize_async(bitmap)

    words: list[dict] = []
    for line in result.lines:
        for word in line.words:
            r = word.bounding_rect
            words.append({"t": word.text, "x": round(r.x, 1), "y": round(r.y, 1),
                          "w": round(r.width, 1), "h": round(r.height, 1)})
    return words


def read_keys(doc, out_dir: str, first: int, last: int) -> None:
    """rapidocr over the answer-key pages, into the same word/box shape."""
    from rapidocr_onnxruntime import RapidOCR         # noqa: PLC0415 — only needed here

    ocr = RapidOCR()
    os.makedirs(out_dir, exist_ok=True)
    for pno in range(first, last + 1):
        image = doc[pno - 1].render(scale=SCALE).to_pil()
        result, _ = ocr(image)
        words = []
        for box, text, _conf in (result or []):
            xs = [p[0] for p in box]
            ys = [p[1] for p in box]
            words.append({"t": text, "x": round(min(xs), 1), "y": round(min(ys), 1),
                          "w": round(max(xs) - min(xs), 1),
                          "h": round(max(ys) - min(ys), 1)})
        with open(os.path.join(out_dir, f"{pno}.json"), "w", encoding="utf-8") as fh:
            json.dump({"width": image.width, "height": image.height, "words": words},
                      fh, ensure_ascii=False)
        print(f"{pno:4} {len(words):5} cells (keys)", flush=True)


async def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("book", type=int)
    ap.add_argument("--from", dest="first", type=int, default=1)
    ap.add_argument("--to", dest="last", type=int, default=0)
    ap.add_argument("--keys", nargs=2, type=int, metavar=("FIRST", "LAST"),
                    help="read these pages with rapidocr into <book>/keys/")
    args = ap.parse_args()

    if args.keys:
        doc = pdfium.PdfDocument(args.pdf)
        read_keys(doc, os.path.join(OUT_ROOT, f"c{args.book}", "keys"), *args.keys)
        return 0

    engine = (wmo.OcrEngine.try_create_from_language(wg.Language("en-US"))
              or wmo.OcrEngine.try_create_from_user_profile_languages())
    if engine is None:
        print("No Windows OCR engine for English is installed.", file=sys.stderr)
        return 1

    out_dir = os.path.join(OUT_ROOT, f"c{args.book}")
    os.makedirs(out_dir, exist_ok=True)
    doc = pdfium.PdfDocument(args.pdf)
    last = args.last or len(doc)

    for pno in range(args.first, last + 1):
        image = doc[pno - 1].render(scale=SCALE).to_pil()
        words = await read_page(engine, image)
        with open(os.path.join(out_dir, f"{pno}.json"), "w", encoding="utf-8") as fh:
            json.dump({"width": image.width, "height": image.height, "words": words},
                      fh, ensure_ascii=False)
        print(f"{pno:4} {len(words):5} words", flush=True)

    print(f"done — {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
