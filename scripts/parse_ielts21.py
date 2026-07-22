"""
parse_ielts21.py — extract Cambridge IELTS 21 Academic from the official PDF.

The owner holds a licence for the book + audio (see scripts/IELTS21_EXTRACTION_NOTES.md).

Every page in this PDF is /Rotate 90, so pypdf's plain `extract_text()` emits tokens in
an order that scrambles two-column layouts (worst in the audioscripts, where the speaker
labels form their own column). We therefore collect each glyph run with its text-matrix
position and rebuild the lines ourselves: with the 90° rotation the *x* coordinate runs
down the page (line order) and *y* runs across it (column order).

Output: scripts/seeds/ielts21.json  — consumed by scripts/seed_ielts_21.py
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict

from pypdf import PdfReader

# Which book: `--book 20` (or IELTS_BOOK) picks the paths and the title prefix, so a
# newly bought Cambridge volume needs no edit here.
BOOK = int(os.environ.get("IELTS_BOOK", "21"))
PDF_PATH = os.environ.get("IELTS_PDF") or os.environ.get(
    "IELTS21_PDF", rf"C:/Users/Page/Downloads/IELTS_{BOOK}.pdf")
OUT_PATH = os.path.join(os.path.dirname(__file__), "seeds", f"ielts{BOOK}.json")

# Filled from the book's own Contents page by `locate_back_matter()`; the ranges differ
# between volumes, and the Contents lists them ("Audioscripts 97 / Listening and Reading
# answer keys 117 / Sample Writing answers 125").
AUDIOSCRIPT_PAGES: range = range(0)
ANSWER_KEY_PAGES: range = range(0)

LINE_TOL = 6.0          # two runs within this many units of x are on the same visual line
FOOTER_X = 812.0        # everything below the last text baseline is running-foot junk
NAV_RE = re.compile(r"[➔➜]|p\.\s*1\d\d")
# Matched case-sensitively: the running heads are Title Case, while the section
# headings that we must keep ("LISTENING", "READING", …) are printed in full caps.
RUNNING_HEAD = {"Test 1", "Test 2", "Test 3", "Test 4", "Reading", "Listening",
                "Writing", "Speaking", "Audioscripts", "Listening and Reading answer keys"}

# Two very different physical layouts ship under this series, and the difference is not
# cosmetic. Book 21 is the publisher's own typesetting: every page carries /Rotate 90,
# so visual lines have to be rebuilt from glyph coordinates. Book 20 arrived re-typeset
# — upright pages, no audioscripts, no Writing or Speaking papers, and answer keys laid
# out in two columns separated by wide runs of spaces.
#
# Detected in main() from /Rotate rather than from the book number, because it is a
# property of the file, not of the edition. Everything downstream of `load_pages` —
# cutting a page into question blocks, collecting options, numbering gaps — is shared.
PLAIN_LAYOUT = False

# A scanned volume has no text layer at all, so its pages come from
# `scripts/ocr_pages.py` instead of from pypdf. Set in main() when the cache exists.
OCR_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seeds", "ocr", f"c{BOOK}")
OCR_PAGES = False
# A word starts a new visual line when its centre sits this far from the current one,
# as a fraction of its own height.
OCR_ROW_TOL = 0.6
# Two columns of an answer key share one printed line. The gap between them is many
# times a word space, so it is re-emitted as four — `parse_answer_keys_plain` splits on
# runs of four, and without this the two columns merge into one unreadable row.
OCR_COLUMN_GAP = 34.0
# Neither engine returns the dot leader that marks an answer space — the dots are too
# faint to be read as text — so a note came back as "Area: 1    hectares" and not one of
# the ten gaps in a Listening Part 1 was found. The leader is put back from the width of
# the hole it left. A part heading ("PART 1    Questions 1-10") leaves a 66px gap and a
# real leader 95-186px, so the threshold sits between them, and headings are skipped
# outright rather than trusted to the number.
OCR_LEADER_GAP = 90.0
# A heading ends in a number too. "READING PASSAGE 1" became "READING PASSAGE 1 ........."
# and stopped matching PASSAGE_RE, which cost every reading passage in the book.
# Two marks that only an audioscript page carries: the speaker label, and the "Q26" the
# margin prints where the answer is spoken. Part 4 is one uninterrupted lecture, so it
# has no speaker labels at all — going by those alone stopped the walk on the first
# Part 4 page and left the section empty.
# "Questions II and 12" — OCR reads 11 as two capital I's, so the block header was not
# recognised, the block was never split, and the "Choose TWO letters" fallback filled
# the whole 13-20 range with one shared stem: eight duplicate questions.
OCR_QRANGE_RE = re.compile(
    r"\b(Questions?)\s+([\dIlO|]{1,2})\s*([-–—]|and)\s*([\dIlO|]{1,2})\b", re.I)
SPEAKER_RE = re.compile(r"^[A-Z][A-Z'. ]{1,14}\s*:")
SCRIPT_MARK_RE = re.compile(r"\bQ\d{1,2}\b")


def is_script_page(lines: list[str]) -> bool:
    return any(SPEAKER_RE.match(l) or SCRIPT_MARK_RE.search(l) for l in lines)
OCR_HEADING_RE = re.compile(
    r"^(READING PASSAGE|PART|TEST|SECTION|WRITING TASK|Questions?)\b", re.I)


# ─── low-level page reconstruction ────────────────────────────────────────────

def ocr_lines(page_no: int) -> list[str]:
    """Visual lines rebuilt from the OCR word boxes of a scanned page.

    The engine returns lines in its own order, which is not the page's: on a Listening
    page the five question numbers come back as five lines of their own, detached from
    the sentences they belong to. Grouping words by vertical position puts "11" back in
    front of its question, which is what every downstream regex expects.
    """
    with open(os.path.join(OCR_DIR, f"{page_no}.json"), encoding="utf-8") as fh:
        page = json.load(fh)
    return lines_from_boxes(page["words"], page_height=page.get("height"))


def lines_from_boxes(words: list[dict], leaders: bool = True,
                     page_height: float | None = None) -> list[str]:
    """Group boxed words into visual lines, keeping a column gap as four spaces.

    With `leaders`, a wide hole after a question number is re-emitted as the dot leader
    the page actually prints. Answer-key pages pass False: there the wide gap separates
    the two columns of the key, and a number followed by one is a question number
    followed by its answer, not a gap.
    """
    if not words:
        return []

    # A leader is sometimes half-read, leaving a stray "." or "„" in the middle of it.
    # Those tokens are not text, and left in place they break the hole into two gaps too
    # narrow to recognise — question 31 of Test 2 came out as "31 . and".
    if leaders:
        words = [w for w in words if not re.fullmatch(r"[.·…„,']{1,4}", w["t"])]

    rows: list[list[dict]] = []
    for w in sorted(words, key=lambda w: w["y"] + w["h"] / 2):
        centre = w["y"] + w["h"] / 2
        if rows:
            last = rows[-1][-1]
            if abs(centre - (last["y"] + last["h"] / 2)) <= last["h"] * OCR_ROW_TOL:
                rows[-1].append(w)
                continue
        rows.append([w])

    lines: list[str] = []
    for row in rows:
        row.sort(key=lambda w: w["x"])
        plain = " ".join(w["t"] for w in row)
        # A Contents entry is also a short line ending in a number ("Audioscripts 100"),
        # and appending a leader to it hid the Contents page from locate_back_matter.
        heading = bool(Q_HEADER.match(plain) or Q_HEADER_ONE.match(plain)
                       or OCR_HEADING_RE.match(plain) or CONTENTS_RE.match(plain))

        # Asked before the text is assembled, because it rewrites a letter-shaped number
        # in place: checking afterwards left the line reading "the movement of the I ....",
        # with the leader restored but the number still a capital I.
        trailing = leaders and not heading and ends_with_gap(row, page_height)

        parts: list[str] = []
        for i, w in enumerate(row):
            if i:
                prev = row[i - 1]
                gap = w["x"] - (prev["x"] + prev["w"])
                if (leaders and not heading and gap > OCR_LEADER_GAP
                        and is_gap_number(row, i - 1)):
                    parts.append(" ......... ")
                else:
                    parts.append("    " if gap > OCR_COLUMN_GAP else " ")
            parts.append(w["t"])
        text = "".join(parts).strip()
        if trailing:
            text += " ........."

        text = OCR_QRANGE_RE.sub(
            lambda m: f"{m.group(1)} {m.group(2).translate(OCR_NUM_TRANS)} "
                      f"{m.group(3)} {m.group(4).translate(OCR_NUM_TRANS)}", text)
        if text and text not in RUNNING_HEAD:
            lines.append(text)
    return lines


def as_number(text: str) -> str | None:
    """The digits this token reads as, allowing OCR's I for 1, l for 1 and O for 0.

    A trailing stop is part of the leader, not of the number: where only the first dot
    of the leader survived, the token came back as "7." and the gap went unrecognised.
    """
    text = text.rstrip(".,·…")
    if re.fullmatch(r"\d{1,2}", text):
        return text
    if re.fullmatch(r"[IlO|]{1,2}", text):
        digits = text.translate(OCR_NUM_TRANS)
        return digits if digits.isdigit() and digits != "0" else None
    return None


def is_gap_number(row: list[dict], i: int, ocr_shapes: bool = False) -> bool:
    """Is `row[i]` the printed number of an answer space?

    A currency sign is part of the answer, not of the number ("Cost per child: 9 £ ...").
    The number is rewritten in place when OCR gave it as letters, because everything
    downstream looks for a digit.
    """
    if re.fullmatch(r"[£$€]", row[i]["t"]) and i:
        i -= 1
    # Letter shapes are only trusted at the end of a line. Mid-line, "I" is far more
    # often the word than the number, and accepting it there invented gaps that pushed
    # real ones out — twelve questions were lost that way.
    digits = as_number(row[i]["t"]) if ocr_shapes else (
        row[i]["t"] if re.fullmatch(r"\d{1,2}", row[i]["t"]) else None)
    if digits is None:
        return False
    row[i]["t"] = digits
    return True


def ends_with_gap(row: list[dict], page_height: float | None) -> bool:
    """A leader running to the end of the line leaves only its number behind.

    One guard, arrived at by measuring the whole book rather than by reasoning: the page
    number is a lone number too, so the bottom sliver of the page is ignored.

    Everything else that looked prudent cost questions. Capping the line length to keep
    prose out lost eighteen — notes and table rows run longer than they look, and the
    number has to be the last token anyway. Requiring two tokens lost three more: a
    table cell is often nothing but its number.
    """
    if not row:
        return False
    # Measured, not guessed: the running foot sits at 0.92-0.93 of the page height and
    # the last line of content at 0.75. A 0.94 cut-off left the page number in, and the
    # leader appended to it produced a phantom "22 ........." on the page whose printed
    # number is 22.
    if page_height and row[0]["y"] > page_height * 0.90:
        return False
    return is_gap_number(row, len(row) - 1, ocr_shapes=True)


OCR_NUM_TRANS = str.maketrans({"I": "1", "l": "1", "|": "1", "O": "0"})


def fix_leading_number(text: str) -> str:
    """"I Mathieson" → "1 Mathieson", "IO alone" → "10 alone", "4() flooding" → "40 …".

    OCR reads the 1 of a question number as a capital I, the 10 as IO and the 0 as "()"
    often enough that whole columns of answers went unrecognised. Only a leading token
    made purely of those shapes is touched, and only when it reads as a number after.
    """
    text = re.sub(r"^(\d)\(\)", r"\g<1>0", text)
    # "22Visualisation" — the space between the number and its answer is not always
    # returned, and the answer is then lost with the number attached to it.
    text = re.sub(r"^(\d{1,2})([A-Za-z][A-Za-z/() -]*)$", r"\1 \2", text)
    m = re.match(r"^([IlO|\d]{1,2})(\s+\S.*)$", text)
    if not m or m.group(1).isdigit():
        return text
    digits = m.group(1).translate(OCR_NUM_TRANS)
    return digits + m.group(2) if digits.isdigit() else text


MERGED_KEY_RE = re.compile(r"^(\d{1,2}(?:\s+\d{1,2})+)\s+(\S+(?:\s+\S+)*)$")


def split_merged_key(cell: str) -> list[str]:
    """"10 8 9 topspin training paint" → "8 topspin", "9 training", "10 paint".

    rapidocr sometimes takes several rows of a key as one box, and then emits the whole
    number column before the whole answer column. The numbers come out in the order the
    box was scanned, not in the order of the answers, so they are sorted; the answers
    are already in reading order.

    Only fires on two or more leading numbers with exactly as many words after them, and
    never when one of those words is itself a number — "3 250 / two hundred and fifty"
    must not be torn apart.
    """
    m = MERGED_KEY_RE.match(cell)
    if not m:
        return [cell]
    nums, rest = m.group(1).split(), m.group(2).split()
    if len(nums) != len(rest) or len(nums) < 2:
        return [cell]
    if any(re.fullmatch(r"\d+", r) for r in rest):
        return [cell]
    return [f"{n} {a}" for n, a in zip(sorted(nums, key=int), rest)]


def ocr_key_segments(page_no: int) -> list[str]:
    """One string per printed answer on a scanned answer-key page.

    The two halves of the key are one printed line ("2 beginners    22 B"), so they are
    cut at the wide gap that `lines_from_boxes` preserves. That is the same shape
    `page_segments` produces for the rotated book, so `parse_answer_keys` reads either.
    """
    # Both engines, in that order. rapidocr is the one that sees the isolated capitals
    # and so must have the last word, but it drops the occasional whole answer — Test 4's
    # question 40 was simply absent from it, and Windows OCR had it all along.
    lines = ocr_lines(page_no)
    path = os.path.join(OCR_DIR, "keys", f"{page_no}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            lines = lines + lines_from_boxes(json.load(fh)["words"], leaders=False)

    out: list[str] = []
    for line in lines:
        for cell in re.split(r"\s{4,}", line):
            cell = fix_leading_number(cell.strip())
            if cell:
                out.extend(split_merged_key(cell))
    return out


def plain_lines(page) -> list[str]:
    """Upright page: pypdf's own line breaks are already the visual ones.

    Leading and trailing space is trimmed but *interior* runs are kept — they are the
    only thing separating the two columns of an answer-key page.
    """
    return [line for raw in (page.extract_text() or "").split("\n")
            if (line := raw.strip()) and line not in RUNNING_HEAD]


def page_lines(page) -> list[str]:
    """Rebuild a rotated page's visual lines, dropping running heads and footers."""
    if PLAIN_LAYOUT:
        return plain_lines(page)
    runs: list[tuple[float, float, str]] = []

    def visit(text, cm, tm, font, size):
        if text and text.strip():
            runs.append((tm[4], tm[5], text.strip()))

    page.extract_text(visitor_text=visit)

    buckets: dict[float, list[tuple[float, str]]] = defaultdict(list)
    for x, y, t in sorted(runs, key=lambda r: r[0]):
        key = next((k for k in buckets if abs(k - x) <= LINE_TOL), x)
        buckets[key].append((y, t))

    lines: list[str] = []
    for x in sorted(buckets):
        if x >= FOOTER_X:
            continue
        text = " ".join(t for _, t in sorted(buckets[x], key=lambda p: p[0]))
        text = re.sub(r"\s+", " ", text).strip()
        if not text or NAV_RE.search(text):
            continue
        if text.strip(" .") in RUNNING_HEAD:
            continue
        if re.fullmatch(r"[\dIl|]{1,4}", text):        # bare page number / stray rule
            continue
        lines.append(text)
    return lines


def page_segments(page) -> list[str]:
    """Split an answer-key page into one string per printed answer.

    Questions 1-20 and 21-40 are printed side by side, and the gap between the two
    columns is narrower than the gap between a question number and its own answer, so
    clustering by position is unreliable. Instead we exploit the fact that the question
    number is always its own glyph run: within a visual line, every run that is a bare
    1-2 digit number starts a new answer segment.
    """
    runs: list[tuple[float, float, str]] = []

    def visit(text, cm, tm, font, size):
        if text and text.strip():
            runs.append((tm[4], tm[5], text.strip()))

    page.extract_text(visitor_text=visit)

    buckets: dict[float, list[tuple[float, str]]] = defaultdict(list)
    for x, y, t in sorted(runs, key=lambda r: r[0]):
        if x >= FOOTER_X:
            continue
        key = next((k for k in buckets if abs(k - x) <= LINE_TOL), x)
        buckets[key].append((y, t))

    # Numeric answers ("3 250 / two hundred and fifty") must not be mistaken for question
    # numbers, so only split at the handful of across-page positions where bare numbers
    # occur often enough to be a printed question-number column.
    tally: dict[float, int] = defaultdict(int)
    for x in buckets:
        for y, t in buckets[x]:
            if re.fullmatch(r"\d{1,2}\s*&?\s*\d{0,2}", t):
                key = next((k for k in tally if abs(k - y) <= 8), y)
                tally[key] += 1
    number_cols = [y for y, n in tally.items() if n >= 5]

    out: list[str] = []
    for x in sorted(buckets):
        segments: list[list[str]] = [[]]
        for y, t in sorted(buckets[x], key=lambda p: p[0]):
            is_number_col = any(abs(y - c) <= 8 for c in number_cols)
            if is_number_col and re.fullmatch(r"\d{1,2}\s*&?\s*\d{0,2}", t) and segments[-1]:
                segments.append([])
            segments[-1].append(t)
        for seg in segments:
            text = re.sub(r"\s+", " ", " ".join(seg)).strip()
            if text and not NAV_RE.search(text) and text.strip(" .") not in RUNNING_HEAD:
                out.append(text)
    return out


CONTENTS_RE = re.compile(r"^(Audioscripts|Listening and Reading answer keys|"
                         r"Sample Writing answers)\s+(\d{1,3})\s*$", re.I)


def page_reader(reader):
    """How to get the visual lines of page `n` (1-based) for this PDF.

    Three sources now: OCR word boxes for a scan, pypdf's own line breaks for an upright
    file, and coordinate reconstruction for a rotated one.
    """
    if OCR_PAGES:
        return ocr_lines
    if PLAIN_LAYOUT:
        return lambda n: plain_lines(reader.pages[n - 1])
    return lambda n: page_lines(reader.pages[n - 1])


def locate_back_matter(reader) -> None:
    """Read the Contents page for where the audioscripts and answer keys start.

    These were hard-coded to book 21's pages. Every volume paginates differently, so a
    new book would have parsed its front matter as answer keys and found nothing. The
    Contents lists all three sections; the printed numbers run a page or two behind the
    PDF's own indices (front matter), so the offset is measured from where the
    "Audioscripts" heading actually appears.
    """
    global AUDIOSCRIPT_PAGES, ANSWER_KEY_PAGES

    read = page_reader(reader)
    total = len(reader.pages)

    listed: dict[str, int] = {}
    for n in range(1, min(12, total) + 1):
        for line in read(n):
            if m := CONTENTS_RE.match(line):
                listed[m.group(1).lower()] = int(m.group(2))
        if len(listed) >= 3:
            break

    scripts_at = listed.get("audioscripts")
    keys_at = listed.get("listening and reading answer keys")
    writing_at = listed.get("sample writing answers")

    if not (scripts_at and keys_at and writing_at):
        # A re-typeset edition prints no Contents and no audioscripts at all; the keys
        # are then everything from the first "... ANSWERS" heading to the end.
        first = next((n for n in range(1, total + 1)
                      if any(ANSWER_HEAD.search(l) for l in read(n)[:3])), None)
        if first is None:
            raise RuntimeError("No Contents page and no answer-key heading in this PDF.")
        AUDIOSCRIPT_PAGES = range(0)
        ANSWER_KEY_PAGES = range(first, total + 1)
        print(f"back matter: no audioscripts, answer keys {first}-{total}", flush=True)
        return

    # The printed numbers run a page or two behind the PDF's own indices because of the
    # front matter, so the offset is measured from where the heading actually falls.
    offset = 1
    for n in range(max(1, scripts_at - 2), min(total, scripts_at + 4) + 1):
        if any(l.strip() == "Audioscripts" for l in read(n)):
            offset = n - scripts_at
            break

    AUDIOSCRIPT_PAGES = range(scripts_at + offset, keys_at + offset)
    ANSWER_KEY_PAGES = range(keys_at + offset, writing_at + offset)

    # The Contents gives the printed numbers and the offset is inferred from one
    # heading, which put Cambridge 19's keys two pages late — the whole of Test 1 fell
    # outside the range and its forty answers were silently absent. An answer-key page
    # is unmistakable in itself: a "TEST n" banner and a bare skill heading. Where those
    # pages are found, they win over the arithmetic.
    found = [n for n in range(scripts_at + offset, total + 1)
             if any(re.fullmatch(r"[Il|]?\s*TEST\s*[\dIlO|]{1,2}", l, re.I) for l in read(n))
             and any(re.fullmatch(r"LISTENING|READING", l) for l in read(n))]
    if found:
        ANSWER_KEY_PAGES = range(min(found), max(found) + 1)

        # Same two-page drift as the keys, and it cost more: the audioscripts were held
        # to start two pages late, so Test 1's transcript fell outside the range while
        # Test 4's Speaking paper ran on into the scripts and produced five parts and
        # forty-eight questions for forty slots.
        #
        # A script page is the only kind that carries speaker labels, so the section is
        # the run of them that ends where the keys begin. Looking instead for the page
        # that reopens at "TEST 1 / PART 1" matched a Speaking paper, which prints both.
        n = min(found) - 1
        while n > 1 and is_script_page(read(n)):
            n -= 1
        # Only when the walk actually found script pages. The rotated book's scripts
        # carry neither margin marks nor speaker labels in a form this recognises, so
        # the walk stops immediately there and would leave the section empty — losing
        # all sixteen of its transcripts and running Test 4's Speaking paper on into
        # the scripts. Where it finds nothing, the Contents arithmetic stands.
        if n + 1 < min(found):
            AUDIOSCRIPT_PAGES = range(n + 1, min(found))
        else:
            AUDIOSCRIPT_PAGES = range(scripts_at + offset, min(found))

    print(f"back matter: audioscripts {AUDIOSCRIPT_PAGES.start}-{AUDIOSCRIPT_PAGES.stop - 1}, "
          f"answer keys {ANSWER_KEY_PAGES.start}-{ANSWER_KEY_PAGES.stop - 1}", flush=True)


def load_pages(reader) -> list[list[str]]:
    if OCR_PAGES:
        return [ocr_key_segments(n) if n in ANSWER_KEY_PAGES else ocr_lines(n)
                for n in range(1, len(reader.pages) + 1)]
    if PLAIN_LAYOUT:
        return [plain_lines(p) for p in reader.pages]
    return [page_segments(p) if (i + 1) in ANSWER_KEY_PAGES else page_lines(p)
            for i, p in enumerate(reader.pages)]


# ─── answer keys ──────────────────────────────────────────────────────────────

BAND_NOISE = re.compile(
    r"you are (unlikely|likely) to get|acceptable score|If you score|"
    r"more practice or lessons|institutions will find|examination conditions|"
    r"improving your English|Answer key with extra|Resource Bank|in Resource"
)
ANSWER_LINE = re.compile(r"^(\d{1,2})\s+(.+)$")
# rapidocr, which reads the scanned keys, drops the spaces between words — the
# heading comes back as "17&18INEITHERORDER". Every two-mark answer in the book was
# lost to that: forty questions with no key at all.
# The ampersand is misread too — "23&24" came back as "238.24" — so anything short
# between the two numbers is accepted. "IN EITHER ORDER" following it is what makes
# the line unambiguous.
PAIR_HEAD = re.compile(
    r"^(\d{1,2})[&8.,\s]{1,3}(\d{1,2})[\s1lI|]{0,3}IN\s*EITHER\s*ORDER", re.I)


def parse_answer_keys(pages: list[list[str]]) -> dict[tuple[int, str], dict[int, str]]:
    """→ {(test_no, 'listening'|'reading'): {question_no: answer}}"""
    keys: dict[tuple[int, str], dict[int, str]] = {}

    for pno in ANSWER_KEY_PAGES:
        lines = [l.strip() for l in pages[pno - 1]]
        # One page holds exactly one (test, skill) key, but column-order reading can put
        # the "TEST n" banner after the skill heading — so resolve both up front.
        # The banner is sometimes preceded by a stray rule glyph ("I TEST 1").
        # A scan's "TEST 1" comes back as "TEST I" often enough that a whole test's key
        # was skipped; the leading stray glyph of the rotated book still has to be
        # allowed too, which is what the optional group at the front is for.
        test_no = next(
            (int(m.group(1).translate(OCR_NUM_TRANS)) for l in lines
             if (m := re.fullmatch(r"[Il|]?\s*TEST\s*([\dIlO|]{1,2})", l, re.I))
             and m.group(1).translate(OCR_NUM_TRANS).isdigit()),
            None)
        skill = next((l.lower() for l in lines if re.fullmatch(r"LISTENING|READING", l)), None)
        if test_no is None or skill is None:
            continue
        cur = keys.setdefault((test_no, skill), {})
        pending_pair: list[int] = []

        for line in lines:
            if BAND_NOISE.search(line) or re.fullmatch(r"[Il|]?\s*TEST\s*\d|LISTENING|READING", line, re.I):
                continue
            if re.match(r"^(Part|Reading Passage|Questions)\b", line, re.I):
                continue

            m_pair = PAIR_HEAD.match(line)
            if m_pair:
                pending_pair = [int(m_pair.group(1)), int(m_pair.group(2))]
                continue
            # The two letters of an "IN EITHER ORDER" pair are printed on their own lines.
            if pending_pair and (m_solo := re.fullmatch(
                    r"([A-Ha-h])(?:\s+(?:Part|Reading Passage|Questions)\b.*)?", line)):
                cur[pending_pair.pop(0)] = m_solo.group(1).upper()
                continue

            m = ANSWER_LINE.match(line)
            if m:
                num, ans = int(m.group(1)), m.group(2).strip()
                # …but they are just as often typeset alongside the other column's
                # answers ("2 weather B"), where the trailing letter is the pair's.
                if pending_pair and (tail := re.search(r"\s([A-H])$", ans)):
                    cur[pending_pair.pop(0)] = tail.group(1)
                    ans = ans[:tail.start()].strip()
                if 1 <= num <= 40 and ans:
                    cur[num] = normalise_answer(ans)
    return keys


ANSWER_HEAD = re.compile(r"(LISTENING|READING)\s+ANSWERS", re.I)
COLUMN_GAP = re.compile(r"\s{4,}")
# "21-22 C.E" — one two-mark question, either letter accepted in either box.
PAIR_PLAIN = re.compile(r"^(\d{1,2})\s*[-–—]\s*(\d{1,2})\s+([A-J])\s*[.,/&]\s*([A-J])$")


def record_plain_answer(cur: dict[int, str], cell: str) -> None:
    if not cell:
        return
    if m := PAIR_PLAIN.match(cell):
        cur[int(m.group(1))] = cur[int(m.group(2))] = f"{m.group(3)}/{m.group(4)}"
        return
    # The space after the number is usually there but not always ("40C"), and demanding
    # nothing at all would read a bare year like "1980" as question 19 answer "80".
    m = re.match(r"^(\d{1,2})\s+(.+)$", cell) or re.match(r"^(\d{1,2})([A-Z]{1,2})$", cell)
    if m and 1 <= int(m.group(1)) <= 40:
        cur[int(m.group(1))] = normalise_answer(m.group(2))


def parse_answer_keys_plain(pages: list[list[str]]) -> dict[tuple[int, str], dict[int, str]]:
    """Book 20's keys: two columns a page, separated by a wide run of spaces.

    Only the Listening page names its test ("TEST 1 LISTENING ANSWERS"); the Reading
    page that follows says just "READING ANSWERS", so the number carries over from the
    page before it.
    """
    keys: dict[tuple[int, str], dict[int, str]] = {}
    test_no: int | None = None

    for pno in ANSWER_KEY_PAGES:
        lines = pages[pno - 1]
        head = next((l for l in lines[:3] if ANSWER_HEAD.search(l)), None)
        if not head:
            continue
        if m := re.search(r"TEST\s*(\d)", head, re.I):
            test_no = int(m.group(1))
        if test_no is None:
            continue
        skill = "listening" if re.search(r"LISTENING", head, re.I) else "reading"
        cur = keys.setdefault((test_no, skill), {})
        for line in lines:
            if ANSWER_HEAD.search(line):
                continue
            for cell in COLUMN_GAP.split(line):
                record_plain_answer(cur, cell.strip())
    return keys


def normalise_answer(ans: str) -> str:
    # A neighbouring column's heading can trail the answer when no number separates them.
    ans = re.split(r"\b(?:Reading Passage|Questions?|Part\b|If you score)", ans)[0]
    ans = ans.replace(" I ", " / ").replace("NOTGIVEN", "NOT GIVEN")
    ans = re.sub(r"\s+", " ", ans).strip(" .")
    # OCR returns some of the lettered answers in lower case ("28 c").
    if re.fullmatch(r"[a-h]", ans):
        ans = ans.upper()
    return ans


# ─── test body: locate sections ───────────────────────────────────────────────

def find_test_pages(pages: list[list[str]]) -> list[dict]:
    """Locate, per test, the page index (0-based) of each skill heading."""
    tests: list[dict] = []
    cur: dict | None = None
    last = (AUDIOSCRIPT_PAGES.start or ANSWER_KEY_PAGES.start) - 1
    for i, lines in enumerate(pages[:last]):
        joined = lines[:4]
        for tag in ("LISTENING", "READING", "WRITING", "SPEAKING"):
            if tag in joined:
                if tag == "LISTENING":
                    cur = {"test": len(tests) + 1, "listening": i}
                    tests.append(cur)
                elif cur is not None:
                    cur.setdefault(tag.lower(), i)
    for t, nxt in zip(tests, tests[1:] + [{"listening": last}]):
        t["end"] = nxt["listening"]
    return tests


TEST_BANNER = re.compile(r"^TEST\s*(\d)$", re.I)


def find_test_pages_plain(pages: list[list[str]]) -> list[dict]:
    """Upright layout: a test opens with a bare "TEST n" banner, not a LISTENING head.

    Writing and Speaking are absent from this edition, so both are pinned to the end of
    the test — `flatten` then hands their parsers an empty list and they yield nothing,
    which is the honest result rather than a crash.
    """
    tests = [{"test": int(m.group(1)), "listening": i}
             for i, lines in enumerate(pages)
             if lines and (m := TEST_BANNER.match(lines[0]))]

    last = ANSWER_KEY_PAGES.start - 1
    for t, nxt in zip(tests, tests[1:] + [{"listening": last}]):
        t["end"] = t["writing"] = t["speaking"] = nxt["listening"]
        t["reading"] = next(
            (p for p in range(t["listening"], t["end"])
             if any(PASSAGE_RE.match(l) for l in pages[p][:2])), t["end"])
    return tests


def flatten(pages: list[list[str]], start: int, end: int) -> list[str]:
    out: list[str] = []
    for p in range(start, end):
        out.extend(pages[p])
    return out


# ─── question blocks ──────────────────────────────────────────────────────────

# A block header is normally its own line, but Listening prints the first one on the
# part heading ("PART 4 Questions 31-40"), so allow that prefix too.
# The part heading carries the first block's range, and the two layouts label the part
# differently ("PART 4 Questions 31-40" vs "Section 4 Question 31-40").
_PART_PREFIX = r"(?:(?:P\s?A\s?R\s?T|Section)\s*\d\s+)?"
Q_HEADER = re.compile(_PART_PREFIX + r"Questions?\s+(\d{1,2})\s*(?:[-–—]|and)\s*(\d{1,2})\s*$", re.I)
Q_HEADER_ONE = re.compile(_PART_PREFIX + r"Questions?\s+(\d{1,2})\s*$", re.I)
# The gap leader is typeset with dots on most pages but with middots on a few.
# The number is sometimes followed by its own full stop before the currency sign
# ("Set lunch costs 9.£………… per person"), which otherwise eats one dot of the leader
# and leaves the gap unrecognised.
GAP = re.compile(r"(\d{1,2})\s*\.?\s*[£$€]?\s*[.·…]{4,}")
# "A the clay it was made with" in one edition, "A.the clay it was made with" — no space
# at all — in the other, so the letter may be followed by punctuation or by space, but
# something must separate it from the text or every capitalised word starts an option.
OPTION_LINE = re.compile(r"^([A-J])(?:[.)]\s*|\s+)(\S.*)$")
# One edition numbers its items "14 reference to…", the other "14. reference to…" and
# sometimes "14.Paragraph A". A separator is required either way: without one, "2015
# researchers reported" reads as item 20 answering "15 researchers reported".
NUM_LINE = re.compile(r"^(\d{1,2})(?:[.)]\s*|\s+)(\S.*)$")

# "21 -22Which TWO things…" — a two-mark question that prints its own range inline and
# runs straight into the stem. Left alone it yields question 21 and silently drops 22.
RANGE_PREFIX = re.compile(r"^(\d{1,2})\s*[-–—]\s*(\d{1,2})\s*(?=[A-Z])")

INSTRUCTION_HINTS = (
    "complete the", "choose", "do the following", "write the correct",
    "match each", "look at the following", "which section", "which paragraph",
    "reading passage", "write your answers", "in boxes", "nb you may",
    "label the", "answer the questions", "write no more than", "select",
)


def detect_type(text: str) -> str:
    low = text.lower()
    if "true" in low and "false" in low and "not given" in low:
        return "tfng"
    if re.search(r"\byes\b", low) and re.search(r"\bno\b", low) and "not given" in low:
        return "ynng"
    if "list of headings" in low or "choose the correct heading" in low:
        return "heading"
    if "choose the correct letter" in low or "choose two letters" in low or "choose three letters" in low:
        return "mcq"
    # "Complete each sentence with the correct ending, A-G" is worded as a completion
    # but answered from a lettered box, and it prints no dot leader for the completion
    # branch to find — so it must be classified before the "complete" test below, or the
    # whole block yields nothing at all.
    if "correct ending" in low or "list of phrases" in low:
        return "matching"
    if ("match each" in low or "which section" in low or "which paragraph" in low
            or "look at the following" in low or "choose six answers" in low
            or "choose five answers" in low or "write the correct letter" in low
            or "what ability is required" in low or "which " in low and "box" in low):
        return "matching"
    if "complete" in low or "one word" in low or "no more than" in low:
        return "completion"
    return "completion"


def split_blocks(lines: list[str]) -> list[dict]:
    """Split a skill section into `Questions N-M` blocks."""
    blocks: list[dict] = []
    cur: dict | None = None
    for line in lines:
        m = Q_HEADER.match(line) or Q_HEADER_ONE.match(line)
        if m:
            lo = int(m.group(1))
            hi = int(m.group(2)) if m.lastindex and m.lastindex >= 2 else lo
            cur = {"lo": lo, "hi": hi, "lines": []}
            blocks.append(cur)
        elif cur is not None:
            cur["lines"].append(line)
    return blocks


def split_instruction(block_lines: list[str], lo: int, hi: int) -> tuple[list[str], list[str]]:
    """Separate the leading rubric from the block's actual content."""
    instr: list[str] = []
    for i, line in enumerate(block_lines):
        low = line.lower()
        starts_item = bool(NUM_LINE.match(line) and lo <= int(NUM_LINE.match(line).group(1)) <= hi)
        if starts_item or GAP.search(line):
            return instr, block_lines[i:]
        instr.append(line)
        # Rubrics never run past a handful of lines; once we've seen a hint and the
        # next line no longer looks like one, the content has started.
        if i >= 1 and not any(h in low for h in INSTRUCTION_HINTS) and len(instr) > 6:
            return instr, block_lines[i + 1:]
    return instr, []


# The option text may start lower case ("A national …") or upper ("A This is …"), but a
# lone capital is a neighbouring option's letter rather than the start of a word.
MULTI_OPTION = re.compile(r"\b([A-J])\s+(?=[a-z0-9]|[A-Z][a-z])")


def collect_options(content: list[str]) -> list[str]:
    """Options printed as a lettered box (A .. I), shared by every item in the block."""
    opts: dict[str, str] = {}
    for line in content:
        if not OPTION_LINE.match(line):
            continue
        # A few boxes are typeset across two or three columns, so one visual line can
        # carry several options ("A national B agricultural C less wealthy nations").
        marks = list(MULTI_OPTION.finditer(line))
        for m, nxt in zip(marks, marks[1:] + [None]):
            letter = m.group(1)
            text = line[m.end(): nxt.start() if nxt else len(line)].strip()
            if letter not in opts and text:
                opts[letter] = text
    letters = sorted(opts)
    # A couple of boxes lose a letter in the text layer (the glyph for "I" is simply not
    # encoded), so require a run starting at A rather than a gapless sequence.
    if len(letters) < 3 or letters[0] != "A":
        return []
    return [f"{k}. {opts[k]}" for k in letters]


def join_wrapped_gaps(lines: list[str]) -> list[str]:
    """Re-join lines that the typesetter wrapped in the middle of a gapped sentence.

    Two cases: the gap's number ends one line and its dot leader begins the next, and a
    gapped sentence that simply runs on ("… came from 1 ..... and transportation" /
    "businesses"). Without this the run-on becomes a bogus sub-heading.
    """
    out: list[str] = []
    for line in lines:
        prev = out[-1] if out else ""
        wraps_leader = re.search(r"\b\d{1,2}\s*$", prev) and re.match(r"^[.·…]{4,}", line)
        # Re-flow the paragraph: a lower-case line continues the one above, whereas a
        # capitalised one starts the next sub-heading and a bulleted one starts the next
        # note — both are excluded by the lower-case test, since a bullet line begins
        # with "•". The gap can fall on either side of the wrap, hence GAP.match too.
        runs_on = ((line[:1].islower() or GAP.match(line))
                   and not prev.rstrip().endswith((".", ":", "?")))
        if prev and (wraps_leader or runs_on):
            out[-1] = f"{prev} {line}"
        else:
            out.append(line)
    return out


def has_numbered(lines: list[str], lo: int, hi: int) -> bool:
    """True when the block lists its questions as numbered items.

    A summary-completion gap that happens to wrap onto a new line ("16 ......... or have
    travelled from ...") looks identical to a numbered item, so those are excluded.
    """
    return any((m := NUM_LINE.match(l)) and lo <= int(m.group(1)) <= hi
               and not GAP.match(l) for l in lines)


def block_instruction(block: dict) -> str:
    """The rubric only — stop at the first option, numbered item or gap."""
    out: list[str] = []
    for line in block["lines"]:
        if OPTION_LINE.match(line) or GAP.search(line) or NUM_LINE.match(line):
            break
        out.append(line)
    return " ".join(out).strip()


def repair_item_numbers(lines: list[str], lo: int, hi: int) -> list[str]:
    """"I a reference to…" → "1 a reference to…", inside this block only.

    OCR gives a lone 1 as I and a 10 as IO. Repairing that anywhere would rewrite prose
    that begins with "I", so it is done here, where the block's range says whether the
    reading is even possible.
    """
    out = []
    for line in lines:
        # "2() There are more worthwhile things…" — the 0 of a 20 is read as a bracket
        # pair. Repaired here rather than globally, for the same reason as the letters.
        m0 = re.match(r"^(\d)\(\)(\s+\S.*)$", line)
        if m0 and lo <= int(m0.group(1) + "0") <= hi:
            line = m0.group(1) + "0" + m0.group(2)
        m = re.match(r"^([IlO|]{1,2})(\s+\S.*)$", line)
        if m:
            digits = m.group(1).translate(OCR_NUM_TRANS)
            if digits.isdigit() and lo <= int(digits) <= hi:
                line = digits + m.group(2)
        out.append(line)
    return out


def build_questions(block: dict, qtype: str) -> list[dict]:
    lo, hi = block["lo"], block["hi"]
    if OCR_PAGES:
        block = {**block, "lines": repair_item_numbers(block["lines"], lo, hi)}
    instr, content = split_instruction(block["lines"], lo, hi)
    out: list[dict] = []

    # A "Choose TWO letters, A-E" block has no numbered items at all — its stem and
    # options are the whole block — so there is nothing for split_instruction to cut.
    if qtype == "mcq" and not has_numbered(block["lines"], lo, hi):
        content = block["lines"]

    # Summary-completion blocks that answer from a word list are worded like a matching
    # task ("Write the correct letter, A-I") but are laid out with inline gaps.
    if qtype in ("matching", "heading") and not has_numbered(content, lo, hi):
        options = collect_options(block["lines"])
        for q in build_questions({**block, "lines": block["lines"]}, "completion"):
            q["options"] = options or None
            out.append(q)
        return dedupe(out, lo, hi, block_instruction(block))

    if qtype == "completion":
        heading = ""
        # When a summary's very first gap falls at the start of a line, its lead-in sits
        # on the last rubric line; pull it back so the sentence stays whole.
        if (content and instr and GAP.match(content[0])
                and not instr[-1].rstrip().endswith((".", ":", "?"))):
            content = instr[-1:] + content
        for line in join_wrapped_gaps(content):
            hits = list(GAP.finditer(line))
            if not hits:
                # Notes and summaries are broken up by short sub-headings; anything
                # longer, or ending in a full stop, is prose rather than a heading.
                if len(line) < 80 and not line.endswith(".") and not line.startswith("•"):
                    heading = line
                continue
            display = GAP.sub("________", line).strip(" •·-")
            display = re.sub(r"\s+([,.;])", r"\1", display)
            for h in hits:
                num = int(h.group(1))
                if lo <= num <= hi:
                    text = f"{heading}: {display}" if heading else display
                    if text.strip("_ ") == "":
                        # A bullet that is nothing but a gap; the only context is the
                        # sub-heading that the rubric swallowed.
                        text = f"{instr[-1]}: {display}" if instr else display
                    out.append({"number": num, "question_text": text, "options": None})

        # "Complete the sentences" prints the number at the head of the sentence and the
        # blank at its end, often on the wrapped line below — so there is no leader
        # beside the number for the loop above to find, and Test 2's questions 19 to 21
        # were lost while 22, whose blank happens to fall first, came through.
        found = {q["number"] for q in out}
        if len(found) < hi - lo + 1:
            out.extend(trailing_blank_items(content, lo, hi, found))
        return dedupe(out, lo, hi, block_instruction(block))

    if qtype == "mcq":
        if re.search(r"TWO letters", " ".join(instr), re.I):
            content = [RANGE_PREFIX.sub("", l) for l in content]
        stem: list[str] = []
        opts: list[str] = []
        num: int | None = None
        for line in content:
            m_num = NUM_LINE.match(line)
            m_opt = OPTION_LINE.match(line)
            if m_num and lo <= int(m_num.group(1)) <= hi:
                flush_mcq(out, num, stem, opts)
                num, stem, opts = int(m_num.group(1)), [m_num.group(2)], []
            elif m_opt and num is not None:
                opts.append(f"{m_opt.group(1)}. {m_opt.group(2).strip()}")
            elif num is None:
                stem.append(line)      # "Choose TWO letters" blocks have an unnumbered stem
            elif opts:
                opts[-1] += " " + line
            else:
                stem.append(line)
        flush_mcq(out, num, stem, opts)

        if not out and stem:
            # "Questions 21 and 22 — Choose TWO letters, A-E": one stem, two answer slots.
            shared_stem = " ".join(s for s in stem if not OPTION_LINE.match(s)).strip()
            shared_opts = collect_options(content)
            for n in range(lo, hi + 1):
                out.append({"number": n, "question_text": shared_stem, "options": shared_opts})
        return dedupe(out, lo, hi, block_instruction(block))

    # tfng / ynng / matching / heading — numbered statements, options from the box
    # The lettered box sits above the items as often as below them, so scan the
    # whole block rather than just the part after the rubric.
    options = collect_options(block["lines"]) if qtype in ("matching", "heading") else None
    num = None
    parts: list[str] = []
    for line in content:
        m_num = NUM_LINE.match(line)
        if m_num and lo <= int(m_num.group(1)) <= hi:
            flush_plain(out, num, parts, options)
            num, parts = int(m_num.group(1)), [m_num.group(2)]
        elif num is not None and not OPTION_LINE.match(line):
            parts.append(line)
    flush_plain(out, num, parts, options)
    return dedupe(out, lo, hi, block_instruction(block))


def trailing_blank_items(content: list[str], lo: int, hi: int,
                         found: set[int]) -> list[dict]:
    """Numbered sentences whose blank is at the end, with their wrapped continuation."""
    items: list[dict] = []
    num: int | None = None
    parts: list[str] = []

    def flush():
        if num is not None and num not in found:
            text = re.sub(r"\s+", " ", " ".join(parts)).strip(" .")
            items.append({"number": num, "question_text": f"{text} ________",
                          "options": None})

    for line in content:
        m = NUM_LINE.match(line)
        if m and lo <= int(m.group(1)) <= hi:
            flush()
            num, parts = int(m.group(1)), [m.group(2)]
        elif num is not None and not line.lower().startswith(INSTRUCTION_HINTS):
            parts.append(line)
    flush()
    return items


def flush_mcq(out, num, stem, opts):
    if num is None:
        return
    out.append({
        "number": num,
        "question_text": " ".join(stem).strip(),
        "options": opts or None,
    })


def flush_plain(out, num, parts, options):
    if num is None:
        return
    out.append({
        "number": num,
        "question_text": " ".join(parts).strip(),
        "options": options,
    })


FIGURE_RE = re.compile(r"Label the (map|plan|diagram|chart)", re.I)


def dedupe(items: list[dict], lo: int, hi: int, rubric: str = "") -> list[dict]:
    seen: dict[int, dict] = {}
    for it in items:
        if lo <= it["number"] <= hi and it["question_text"]:
            seen.setdefault(it["number"], it)
    # Map-labelling tasks print some of their labels inside the artwork, where there is
    # no text layer to read. Keep the numbering intact and flag what needs the figure.
    if (m := FIGURE_RE.search(rubric)):
        for n in range(lo, hi + 1):
            seen.setdefault(n, {
                "number": n,
                "question_text": f"Label {n} on the {m.group(1)}",
                "options": None,
                "needs_figure": True,
            })
    return [seen[n] for n in sorted(seen)]


# ─── reading ──────────────────────────────────────────────────────────────────

PASSAGE_RE = re.compile(r"^READING PASSAGE\s*(\d)\s*$")   # caps only: the sentence
                                                            # "Reading Passage 2 has seven
                                                            # sections" is not a heading
SPEND_RE = re.compile(r"^You should spend|^Passage \d+ below", re.I)
FOOTNOTE_RE = re.compile(r"^\*+")


MIN_PASSAGE_WORDS = 300


def passage_segment(region: list[str]) -> list[str]:
    """The article does not always come before its questions.

    Test 3's Passage 2 prints the heading and the "choose a heading" task first, then the
    article, then the remaining questions. Slicing at the first "Questions" header left
    that passage empty while all thirteen of its questions parsed cleanly — so every
    count was green and the exam would have shipped with nothing to read.

    The region is cut at its "Questions" headers and the wordiest slice wins; the rubric
    and lettered box that open that slice are dropped by skipping to the first full line
    of prose. Chasing an unbroken run of long lines instead does not work — a paragraph's
    last line is usually short, so the article breaks into fragments.
    """
    cuts = [i for i, l in enumerate(region)
            if Q_HEADER.match(l) or Q_HEADER_ONE.match(l)]
    slices = list(zip([0] + cuts, cuts + [len(region)]))
    lo, hi = max(slices, key=lambda b: sum(len(l.split()) for l in region[b[0]:b[1]]))
    lines = region[lo:hi]
    # A rubric can be longer than the length test ("Choose the correct heading for each
    # section from the list of headings below." is 75 characters), and starting the
    # article there also makes the line above it — "Reading Passage 2 has six sections"
    # — look like the title.
    first = next((i for i, l in enumerate(lines)
                  if len(l) >= 60 and not NUM_LINE.match(l) and not SPEND_RE.match(l)
                  and not l.lower().startswith(INSTRUCTION_HINTS)), 0)
    return lines[first:]


def parse_reading(lines: list[str], test_no: int, answers: dict[int, str]) -> list[dict]:
    # Cut the section into three passage regions.
    starts = [i for i, l in enumerate(lines) if PASSAGE_RE.match(l)]
    regions = [(s, e) for s, e in zip(starts, starts[1:] + [len(lines)])]

    out: list[dict] = []
    for idx, (s, e) in enumerate(regions, start=1):
        region = lines[s:e]
        first_q = next((i for i, l in enumerate(region)
                        if Q_HEADER.match(l) or Q_HEADER_ONE.match(l)), len(region))
        body = region[1:first_q]
        body = [l for l in body if not SPEND_RE.match(l) and not FOOTNOTE_RE.match(l)]
        if sum(len(l.split()) for l in body) < MIN_PASSAGE_WORDS:
            if run := passage_segment(region):
                # The title is the short line immediately above the article.
                head = region[:region.index(run[0])]
                lead = next((l for l in reversed(head) if len(l) < 80
                             and not SPEND_RE.match(l) and not Q_HEADER.match(l)
                             and not Q_HEADER_ONE.match(l)), None)
                body = ([lead] if lead else []) + run
        title = body[0] if body else f"Reading Passage {idx}"
        paragraphs = rebuild_paragraphs(body[1:])

        blocks = split_blocks(region[first_q:])
        questions: list[dict] = []
        for b in blocks:
            qtype = detect_type(" ".join(b["lines"][:8]))
            for q in build_questions(b, qtype):
                q["question_type"] = qtype
                q["group_instruction"] = block_instruction(b)
                q["correct_answer"] = answers.get(q["number"], "")
                questions.append(q)
        questions.sort(key=lambda q: q["number"])

        out.append({
            "test": test_no,
            "section": idx,
            "title": title,
            "passage_text": "\n\n".join(paragraphs),
            "word_count": sum(len(p.split()) for p in paragraphs),
            "questions": questions,
        })
    return out


def rebuild_paragraphs(body: list[str]) -> list[str]:
    """Join wrapped lines; a new paragraph starts at a section letter or a blank-ish break."""
    paras: list[str] = []
    cur: list[str] = []
    for line in body:
        if re.match(r"^[A-J]\s+[A-Z]", line) and len(line) > 40:
            if cur:
                paras.append(" ".join(cur))
            cur = [line]
        elif cur and cur[-1].rstrip().endswith((".", "!", "?", "'", "’")) and line[:1].isupper() and len(" ".join(cur)) > 400:
            paras.append(" ".join(cur))
            cur = [line]
        else:
            cur.append(line)
    if cur:
        paras.append(" ".join(cur))
    return [re.sub(r"\s+", " ", p).strip() for p in paras if p.strip()]


# ─── listening ────────────────────────────────────────────────────────────────

# The scan's OCR breaks a word wherever the letter spacing widens, so the heading of
# Test 2 Part 4 came back as "PAR T 4" — the part was never recognised and all ten of
# its questions were lost.
PART_RE = re.compile(r"^(?:P\s?A\s?R\s?T|Section)\s*(\d)\s*"
                     r"(?:Questions?\s*(\d{1,2})\s*(?:[-–]|and)\s*(\d{1,2}))?", re.I)

# The recordings live in the frontend's public/ dir, which only exists on a dev machine —
# so the file list is resolved here, at parse time, and baked into the fixture. The
# seeder then works unchanged on Render, where those files are not present.
AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "..", "ilm-ai-frontend", "public", "audio", "listening")
FIGURE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "..", "ilm-ai-frontend", "public", "ielts")


def audio_urls(test_no: int, part: int) -> list[str]:
    """Ordered URLs for a part; nine of the sixteen were ripped as two files."""
    stem = f"C{BOOK}T{test_no}P{part}"
    try:
        names = sorted(n for n in os.listdir(AUDIO_DIR)
                       if n.endswith((".mp3", ".m4a"))
                       and os.path.splitext(n)[0].split(".")[0] == stem)
    except FileNotFoundError:
        return []
    return [f"/audio/listening/{n}" for n in names]


def parse_listening(lines: list[str], test_no: int, answers: dict[int, str],
                    transcripts: dict[int, str]) -> list[dict]:
    starts = [i for i, l in enumerate(lines) if PART_RE.match(l)]
    regions = [(s, e) for s, e in zip(starts, starts[1:] + [len(lines)])]

    out: list[dict] = []
    for part, (s, e) in enumerate(regions, start=1):
        region = lines[s:e]
        blocks = split_blocks(region)
        questions: list[dict] = []
        for b in blocks:
            qtype = detect_type(" ".join(b["lines"][:8]))
            for q in build_questions(b, qtype):
                q["question_type"] = qtype
                q["group_instruction"] = block_instruction(b)
                q["correct_answer"] = answers.get(q["number"], "")
                questions.append(q)
        questions.sort(key=lambda q: q["number"])

        # The part's own caption if it prints one ("Reclaiming urban rivers"), else the
        # part number. Anything numbered, lettered or interrogative is a question, and a
        # very short line is a stray table-header cell ("Name of" / "restaurant") — both
        # were being shown to students as the title of the paper.
        title = next(
            (l for l in region[1:6]
             if len(l) >= 12 and not l.endswith("?")
             and not Q_HEADER.match(l) and not Q_HEADER_ONE.match(l)
             and not NUM_LINE.match(l) and not OPTION_LINE.match(l)
             and not l.lower().startswith(INSTRUCTION_HINTS)
             and not l.lower().startswith(("write ", "which ", "what ", "who ", "how "))),
            f"Part {part}")
        out.append({
            "test": test_no,
            "section": part,
            "title": title,
            "audio_parts": audio_urls(test_no, part),
            "transcript": transcripts.get(part, ""),
            "questions": questions,
        })
    return out


def parse_audioscripts(pages: list[list[str]]) -> dict[int, dict[int, str]]:
    """→ {test_no: {part_no: transcript}} — no truncation."""
    scripts: dict[int, dict[int, str]] = defaultdict(dict)
    test_no = None
    part_no = None
    buf: list[str] = []

    def flush():
        if test_no and part_no and buf:
            scripts[test_no][part_no] = "\n".join(buf).strip()

    for pno in AUDIOSCRIPT_PAGES:
        for line in pages[pno - 1]:
            m_test = re.fullmatch(r"TEST\s*(\d)", line, re.I)
            # The heading occasionally absorbs the first word of the script ("PART 4 No.").
            m_part = re.match(r"PART\s*(\d)\b", line, re.I)
            if m_test:
                flush()
                buf = []
                test_no, part_no = int(m_test.group(1)), None
                continue
            if m_part:
                flush()
                buf = []
                part_no = int(m_part.group(1))
                continue
            if re.fullmatch(r"[\dIl|]{1,3}", line):    # column of audio-track numbers
                continue
            buf.append(line)
    flush()
    return scripts


# ─── writing & speaking ───────────────────────────────────────────────────────

def parse_writing(lines: list[str], test_no: int) -> list[dict]:
    starts = [(i, int(m.group(1))) for i, l in enumerate(lines)
              if (m := re.match(r"^WRITING TASK\s*(\d)", l, re.I))]
    out = []
    for (s, task), (e, _) in zip(starts, starts[1:] + [(len(lines), 0)]):
        body = [l for l in lines[s + 1:e] if not re.match(r"^You should spend", l, re.I)]
        # Task 1's chart is a vector figure; its axis labels leak in as short fragments.
        prompt_lines, stop = [], False
        for l in body:
            if re.match(r"^Write at least", l, re.I):
                prompt_lines.append(l)
                stop = True
                continue
            if not stop:
                prompt_lines.append(l)
        # The paper prints "Write at least 150 words." under the box, and the exam
        # screen prints it again below the prompt — so it was shown twice. The rubric
        # is also its own paragraph, not a continuation of the topic sentence.
        prompt_lines = [l for l in prompt_lines if not re.match(r"^Write at least", l, re.I)]
        prompt = " ".join(prompt_lines).strip()
        prompt = re.sub(r"\s+(Summarise the information|Do the following|Give reasons)",
                        lambda m: "\n\n" + m.group(1), prompt, count=1)

        out.append({
            "test": test_no,
            "task": task,
            "task_type": f"Task{task}",
            "prompt": prompt,
            # Task 1 asks the candidate to describe a figure, so the essay cannot be
            # attempted without it. Book 21 draws its figures as vector art, so they had
            # to be rendered and cropped (see the commit that added public/ielts/c21).
            "image_url": figure_url(test_no) if task == 1 else None,
            "min_words": 150 if task == 1 else 250,
            "duration_minutes": 20 if task == 1 else 40,
        })
    return out


def figure_url(test_no: int) -> str | None:
    name = f"t{test_no}-task1.png"
    if os.path.exists(os.path.join(FIGURE_DIR, f"c{BOOK}", name)):
        return f"/ielts/c{BOOK}/{name}"
    return None


BULLET = re.compile(r"^[•·▪◦*\-•�]\s*")

# Part 2 prints this fixed rubric in a sidebar beside the cue card. Because the sidebar
# shares its baselines with the cue card, every visual line ends with a fragment of it.
PART2_SIDEBAR = ("You will have to talk about the topic for 1 to 2 minutes. You have "
                 "1 minute to think about what you are going to say. You can make some "
                 "notes to help you if you wish.")


def strip_sidebar(line: str) -> str:
    words = line.split()
    for i in range(len(words) - 2):        # a one- or two-word tail is a coincidence
        if " ".join(words[i:]) in PART2_SIDEBAR:
            return " ".join(words[:i]).strip()
    return line


def parse_speaking(lines: list[str], test_no: int) -> list[dict]:
    starts = [(i, int(m.group(1))) for i, l in enumerate(lines)
              if (m := re.fullmatch(r"PART\s*(\d)", l, re.I))]
    out = []
    for (s, part), (e, _) in zip(starts, starts[1:] + [(len(lines), 0)]):
        body = [BULLET.sub("", l).strip() for l in lines[s + 1:e]]
        body = [l for l in body if l and "�" not in l]
        if part == 2:
            cue_lines = [c for l in body if (c := strip_sidebar(l))]
            out.append({
                "test": test_no, "part": 2,
                "topic": cue_lines[0] if cue_lines else "Part 2 cue card",
                "cue_card": " ".join(cue_lines), "questions": [],
                "prep_seconds": 60, "speak_seconds": 120,
            })
            continue
        topic = ""
        questions: list[str] = []
        for l in body:
            if l.endswith("?"):
                questions.append(l)
            elif (len(l) < 60 and not l.lower().startswith(
                    ("the examiner", "example", "discussion", "topics"))
                    and l[:1].isupper()):
                topic = topic or l
        out.append({
            "test": test_no, "part": part,
            "topic": topic or f"Part {part}",
            "cue_card": None, "questions": questions,
            "prep_seconds": None, "speak_seconds": None,
        })
    return out


# ─── main ─────────────────────────────────────────────────────────────────────

TABLE_MARK = re.compile(r"\[\[(\d{1,2})\]\]")


def attach_tables(pages: list[list[str]], sections: list[dict],
                  first_page: int, last_page: int) -> None:
    """Give a section its printed table, where the paper prints one.

    pypdf returns a table row as one run, so the grid has to come from pdfplumber
    (services… see scripts/ielts_tables.py). The grid is matched to a section by the
    question numbers inside it rather than by position — but only within one skill's
    pages, because Listening and Reading both number from 1, so a Reading table would
    otherwise match a Listening part just as well.
    """
    from ielts_tables import tables_on_page

    for page_no in range(first_page + 1, last_page + 1):
        if not any("Complete the table" in l for l in pages[page_no - 1]):
            continue
        for grid in tables_on_page(PDF_PATH, page_no):
            numbers = {int(m) for row in grid for cell in row for m in TABLE_MARK.findall(cell)}
            if not numbers:
                continue
            for section in sections:
                owned = {q["number"] for q in section["questions"]}
                if numbers & owned == numbers:
                    section.setdefault("tables", []).append(grid)
                    break


def manual_papers() -> dict:
    """Papers that cannot be parsed out of this book's PDF, transcribed by hand.

    Cambridge 20 was sold as two files: a re-typeset one carrying only Listening and
    Reading, and the full 130-page edition, which is a scan with no text layer at all.
    The Writing prompts and Speaking questions exist only in the scan, so they were read
    off the page and committed as `ielts20_manual.json`. Merged rather than pasted into
    the fixture so that re-running the parser cannot quietly drop them.
    """
    path = os.path.join(os.path.dirname(__file__), "seeds", f"ielts{BOOK}_manual.json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    global PLAIN_LAYOUT, OCR_PAGES
    reader = PdfReader(PDF_PATH)
    PLAIN_LAYOUT = all(int(p.get("/Rotate", 0) or 0) == 0 for p in reader.pages)
    # A scan's pages come from the OCR cache instead. "Has a text layer" is measured by
    # how much text, not whether there is any: Cambridge 19 returns 410 characters over
    # 138 pages — stray marks, enough to make an any() test say the book is readable.
    sampled = sum(len((p.extract_text() or "").strip()) for p in reader.pages[:20])
    OCR_PAGES = sampled < 20 * 40
    if OCR_PAGES and not os.path.isdir(OCR_DIR):
        raise SystemExit(f"This PDF has no text layer and {OCR_DIR} is missing.\n"
                         f'Run: python scripts/ocr_pages.py "{PDF_PATH}" {BOOK}')
    print("layout: " + ("scanned + OCR" if OCR_PAGES
                        else "upright" if PLAIN_LAYOUT else "rotated"), flush=True)

    locate_back_matter(reader)
    pages = load_pages(reader)
    # Cambridge 19 is upright like book 20 but prints its keys in book 21's format, so
    # neither of these can be chosen by /Rotate. Try the publisher's layout first and
    # fall back to the re-typeset one when it yields nothing.
    keys = parse_answer_keys(pages) or parse_answer_keys_plain(pages)
    scripts = parse_audioscripts(pages) if AUDIOSCRIPT_PAGES else {}
    # Which finder applies is not a property of the rotation. Cambridge 19 is upright
    # like book 20 but typeset like book 21, with LISTENING / READING / WRITING /
    # SPEAKING headings; choosing by /Rotate looked for book 20's bare "TEST n" banner
    # and found one test in a book that has four. So: headings first, banner as fallback.
    tests = find_test_pages(pages) or find_test_pages_plain(pages)

    manual = manual_papers()
    data = {"source": f"Cambridge IELTS {BOOK} Academic", "book": BOOK, "tests": []}
    for t in tests:
        n = t["test"]
        listening = parse_listening(
            flatten(pages, t["listening"], t["reading"]), n,
            keys.get((n, "listening"), {}), scripts.get(n, {}))
        reading = parse_reading(
            flatten(pages, t["reading"], t["writing"]), n, keys.get((n, "reading"), {}))
        writing = parse_writing(flatten(pages, t["writing"], t["speaking"]), n)
        speaking = parse_speaking(flatten(pages, t["speaking"], t["end"]), n)
        # Only where the PDF yielded nothing — a book whose papers do parse is never
        # overridden by a hand-written file that may have gone stale.
        writing = writing or [
            {"test": n, "task": 1 if w["task_type"] == "Task1" else 2, **w}
            for w in manual.get("writing", {}).get(str(n), [])
        ]
        speaking = speaking or [{"test": n, **sp} for sp in manual.get("speaking", {}).get(str(n), [])]
        add_manual_questions(manual, n, listening, reading, keys)
        attach_tables(pages, listening, t["listening"], t["reading"])
        attach_tables(pages, reading, t["reading"], t["writing"])

        data["tests"].append({
            "test": n, "listening": listening, "reading": reading,
            "writing": writing, "speaking": speaking,
        })

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)

    report(data)
    print(f"\nwrote {OUT_PATH}")
    return 0


def add_manual_questions(manual: dict, test_no: int, listening: list[dict],
                         reading: list[dict], keys: dict) -> None:
    """Insert questions the page could not be read for at all.

    Only for a scan, and only where both OCR engines lost the same cell — Test 3's
    "a 10 ................ tart" is absent from each of them, not merely garbled. The
    answer still comes from the parsed key, so a hand-written file can never disagree
    with the book about what is correct.
    """
    for item in manual.get("questions", []):
        if item["test"] != test_no:
            continue
        sections = listening if item["skill"] == "listening" else reading
        section = next((s for s in sections if s["section"] == item["section"]), None)
        if section is None:
            print(f"  manual question {item['number']}: no section "
                  f"{item['skill']} {item['section']}", flush=True)
            continue
        if any(q["number"] == item["number"] for q in section["questions"]):
            continue
        section["questions"].append({
            "number": item["number"],
            "question_type": item.get("question_type", "completion"),
            "question_text": item["question_text"],
            "options": item.get("options"),
            "group_instruction": item.get("group_instruction"),
            "correct_answer": keys.get((test_no, item["skill"]), {}).get(item["number"], ""),
        })
        section["questions"].sort(key=lambda q: q["number"])


def report(data: dict) -> None:
    for t in data["tests"]:
        n = t["test"]
        lq = sum(len(s["questions"]) for s in t["listening"])
        rq = sum(len(s["questions"]) for s in t["reading"])
        l_missing = sorted(set(range(1, 41)) - {q["number"] for s in t["listening"] for q in s["questions"]})
        r_missing = sorted(set(range(1, 41)) - {q["number"] for s in t["reading"] for q in s["questions"]})
        no_ans = [q["number"] for s in t["listening"] + t["reading"] for q in s["questions"]
                  if not q["correct_answer"]]
        print(f"TEST {n}")
        print(f"  listening  {lq}/40 q   missing={l_missing}")
        print(f"  reading    {rq}/40 q   missing={r_missing}")
        print(f"  passages   {[s['word_count'] for s in t['reading']]}")
        print(f"  transcripts{[len(s['transcript']) for s in t['listening']]}")
        print(f"  writing    {[(w['task'], len(w['prompt'])) for w in t['writing']]}")
        print(f"  speaking   {[(s['part'], len(s['questions']), len(s['cue_card'] or '')) for s in t['speaking']]}")
        if no_ans:
            print(f"  ⚠ no answer key for {no_ans}")


if __name__ == "__main__":
    sys.exit(main())
