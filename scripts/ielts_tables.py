"""
ielts_tables.py — rebuild the printed tables of the Listening papers.

pypdf, which the rest of parse_ielts21.py uses, hands back a whole table row as one
text run: "Taster day introduction to sailing £120 if booking one small groups (max".
The cell boundaries are simply not in what it returns, so a table came out as a heap
of words and questions 1-6 of Test 1 read as gibberish.

pdfplumber gives per-word bounding boxes, which is enough to put the grid back. Note
these pages are /Rotate 90 and pdfplumber reports already-rotated coordinates: `top`
runs down the page (row order) and `x0` across it (column order) — the opposite way
round from the raw text matrix pypdf exposes.

The extracted grid is emitted with gaps marked `[[7]]`, so the frontend can render a
real table and drop the answer box into the cell where the gap is printed.
"""
from __future__ import annotations

import re
from collections import Counter

import pdfplumber

GAP_RE = re.compile(r"[.·…]{4,}")
# The dot leader that marks an answer space is drawn across the cell, so pdfplumber
# ends up interleaving it with the word printed beside it:
#     "....................a..v..a..il.a" + "ble"  ==  "…… available"
# Stripping the dots out of such a token recovers the word, and the marker records
# that a gap was there.
DOTTY = re.compile(r"[.·…]")
GAP_TOKEN = "░"          # placeholder; turned into [[n]] once the number is known
ROW_TOL = 6.0            # words within this many points share a printed line
MIN_COLUMN_HITS = 3      # an x position must start this many words to be a column
# Columns in these tables are ~80pt apart; a closer cluster is a wrapped header line
# ("What you" / "learn"), not a new column.
MIN_COLUMN_GAP = 70


def column_starts(words: list[dict]) -> list[float]:
    """Left-aligned cells make the column edges the most popular word-start positions."""
    hits = Counter(round(w["x0"]) for w in words)
    starts: list[float] = []
    for x, n in sorted(hits.items()):
        if n < MIN_COLUMN_HITS:
            continue
        # Wrapped text inside a cell starts at the same x, so keep the first of a run.
        if starts and x - starts[-1] < MIN_COLUMN_GAP:
            continue
        starts.append(float(x))
    # The first column's header is often a single word, so it never reaches the
    # popularity threshold — without this everything left of column two lands in it.
    leftmost = min(w["x0"] for w in words)
    if not starts or starts[0] - leftmost > 20:
        starts.insert(0, float(round(leftmost)))
    return starts


def clean_token(text: str) -> str:
    """Pull the answer-space dots out of a token, keeping any letters caught in them."""
    if len(DOTTY.findall(text)) >= 4:
        return (GAP_TOKEN + " " + DOTTY.sub("", text)).strip()
    # The tail of a leader can also break off as its own token ("..t" of "and tides").
    if text and DOTTY.sub("", text) and len(DOTTY.findall(text)) >= 1 and text[0] in ".·…":
        return DOTTY.sub("", text)
    return text


def build_grid(words: list[dict], starts: list[float]) -> list[list[str]]:
    """Words → rows of cells, each cell a string with its gaps marked `[[n]]`."""
    rows: list[list[dict]] = []
    for w in sorted(words, key=lambda w: (w["top"], w["x0"])):
        if rows and abs(rows[-1][0]["top"] - w["top"]) <= ROW_TOL:
            rows[-1].append(w)
        else:
            rows.append([w])

    grid: list[list[str]] = []
    for row in rows:
        cells = [""] * len(starts)
        for w in row:
            # Belongs to the last column that starts at or before it.
            idx = 0
            for i, s in enumerate(starts):
                if w["x0"] + 2 >= s:
                    idx = i
            cells[idx] = (cells[idx] + " " + clean_token(w["text"])).strip()
        grid.append(cells)

    return merge_wrapped(grid)


def merge_wrapped(grid: list[list[str]]) -> list[list[str]]:
    """Fold a row that is only the continuation of the row above it.

    A cell whose text wraps produces a row with just that one column filled; the real
    table has no such row.
    """
    out: list[list[str]] = []
    for row in grid:
        filled = [i for i, c in enumerate(row) if c]
        if out and len(filled) == 1:
            i = filled[0]
            out[-1][i] = (out[-1][i] + " " + row[i]).strip()
        else:
            out.append(list(row))
    return out


def mark_gaps(grid: list[list[str]]) -> list[list[str]]:
    """"1 ..........." → "[[1]]", so the renderer knows where the input goes."""
    out = []
    for row in grid:
        cells = []
        for cell in row:
            # "7 ░" — the number printed before the leader names the answer box.
            cell = re.sub(rf"(\d{{1,2}})\s*[£$€]?\s*{GAP_TOKEN}", lambda m: f"[[{m.group(1)}]]", cell)
            cell = cell.replace(GAP_TOKEN, "")
            cells.append(re.sub(r"\s+", " ", cell).strip())
        out.append(cells)
    return out


def extract_table(pdf_path: str, page_no: int, top: float, bottom: float) -> list[list[str]] | None:
    """Grid for the table printed between `top` and `bottom` on a 1-based page."""
    with pdfplumber.open(pdf_path) as pdf:
        words = [
            w for w in pdf.pages[page_no - 1].extract_words()
            if top <= w["top"] <= bottom
        ]
    if not words:
        return None
    starts = column_starts(words)
    if len(starts) < 2:
        return None
    return mark_gaps(build_grid(words, starts))


if __name__ == "__main__":       # quick check against Test 1 Part 1
    import json
    import sys
    grid = extract_table(r"C:/Users/Page/Downloads/IELTS_21.pdf", 11, 435, 620)
    json.dump(grid, sys.stdout, ensure_ascii=False, indent=1)
