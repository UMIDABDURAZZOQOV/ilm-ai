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
DOT_RUN = re.compile(r"[.·…]{4,}")     # a leader long enough to be an answer space
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
    if DOT_RUN.search(text):
        # The token must keep its original order. One edition prints the number and its
        # leader as separate words ("2" then "……"), the other as one ("2……………."), and
        # moving the marker to the front turned the second into "░ 2" — which
        # `mark_gaps` cannot read, so the whole grid came back with no gaps in it and
        # was discarded as "not a table".
        return DOT_RUN.sub(f" {GAP_TOKEN} ", text).strip()
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
        ordered = sorted(row, key=lambda w: w["x0"])
        skip = set()
        for j, w in enumerate(ordered):
            if j in skip:
                continue
            text = w["text"]
            # A gap is printed as "3" followed by its dot leader, and the leader is wide
            # enough to reach into the next column — which put the number in one cell and
            # its marker in another, so question 3 of Test 1 simply had no box. Pair them
            # here, while the reading order is still intact, and place the result in the
            # NUMBER's cell, which is where the paper prints it.
            if re.fullmatch(r"\d{1,2}", text) and j + 1 < len(ordered):
                nxt = ordered[j + 1]["text"]
                if len(DOTTY.findall(nxt)) >= 4:
                    skip.add(j + 1)
                    text = f"{text} {GAP_TOKEN} {DOTTY.sub('', nxt)}".strip()
                else:
                    text = clean_token(text)
            else:
                text = clean_token(text)

            idx = 0
            for i, s in enumerate(starts):
                if w["x0"] + 2 >= s:
                    idx = i
            cells[idx] = (cells[idx] + " " + text).strip()
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
    return grid_from_words(words)


def grid_from_words(words: list[dict]) -> list[list[str]] | None:
    if not words:
        return None
    starts = column_starts(words)
    if len(starts) < 2:
        return None
    return mark_gaps(build_grid(words, starts))


# The rubric that always precedes a table, and the heading that always ends it.
_RUBRIC = re.compile(r"^(Write|Choose)\b.*(\bfor each answer|on your answer sheet)", re.I)
_NEXT_BLOCK = re.compile(r"^Questions?\s+\d", re.I)


def tables_on_page(pdf_path: str, page_no: int) -> list[list[list[str]]]:
    """Every table printed on a page, found by its surrounding text.

    A table sits between the "Write ONE WORD AND/OR A NUMBER for each answer" rubric
    and whatever heading comes next, so the bounds are read off the page rather than
    hard-coded — the three tables in this book are on pages 11, 33 and 41, but a
    different book would put them elsewhere.
    """
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_no - 1]
        words = page.extract_words()
        lines: dict[float, list[dict]] = {}
        for w in words:
            key = next((k for k in lines if abs(k - w["top"]) <= ROW_TOL), w["top"])
            lines.setdefault(key, []).append(w)

        starts, ends = [], []
        for top in sorted(lines):
            text = " ".join(x["text"] for x in sorted(lines[top], key=lambda x: x["x0"]))
            if _RUBRIC.match(text):
                starts.append(top + 8)          # just past the rubric's own baseline
            elif _NEXT_BLOCK.match(text):
                ends.append(top - 4)

        # Rubric lines stack up ("Choose ONE WORD ONLY…" then "Write your answers in
        # boxes 1-5…"), and the table begins after the last of a stack — but a page can
        # also hold two separate tables, so only collapse starts that are adjacent.
        starts = [s for s, nxt in zip(starts, starts[1:] + [1e9]) if nxt - s > 40]

        out = []
        for start in starts:
            stop = next((e for e in ends if e > start), page.height)
            grid = grid_from_words([w for w in words if start <= w["top"] <= stop])
            if grid and any("[[" in c for row in grid for c in row):
                out.append(grid)
        return out


if __name__ == "__main__":       # quick check against Test 1 Part 1
    import json
    import sys
    grid = extract_table(r"C:/Users/Page/Downloads/IELTS_21.pdf", 11, 435, 620)
    json.dump(grid, sys.stdout, ensure_ascii=False, indent=1)
