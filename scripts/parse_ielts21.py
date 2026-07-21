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

PDF_PATH = os.environ.get("IELTS21_PDF", r"C:/Users/Page/Downloads/IELTS_21.pdf")
OUT_PATH = os.path.join(os.path.dirname(__file__), "seeds", "ielts21.json")

# Page numbers below are 1-based, matching the "===== PAGE n =====" dumps used while
# reverse-engineering the layout. They come from the book's own table of contents.
AUDIOSCRIPT_PAGES = range(98, 118)
ANSWER_KEY_PAGES = range(118, 126)

LINE_TOL = 6.0          # two runs within this many units of x are on the same visual line
FOOTER_X = 812.0        # everything below the last text baseline is running-foot junk
NAV_RE = re.compile(r"[➔➜]|p\.\s*1\d\d")
# Matched case-sensitively: the running heads are Title Case, while the section
# headings that we must keep ("LISTENING", "READING", …) are printed in full caps.
RUNNING_HEAD = {"Test 1", "Test 2", "Test 3", "Test 4", "Reading", "Listening",
                "Writing", "Speaking", "Audioscripts", "Listening and Reading answer keys"}


# ─── low-level page reconstruction ────────────────────────────────────────────

def page_lines(page) -> list[str]:
    """Rebuild a rotated page's visual lines, dropping running heads and footers."""
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


def load_pages(reader) -> list[list[str]]:
    return [page_segments(p) if (i + 1) in ANSWER_KEY_PAGES else page_lines(p)
            for i, p in enumerate(reader.pages)]


# ─── answer keys ──────────────────────────────────────────────────────────────

BAND_NOISE = re.compile(
    r"you are (unlikely|likely) to get|acceptable score|If you score|"
    r"more practice or lessons|institutions will find|examination conditions|"
    r"improving your English|Answer key with extra|Resource Bank|in Resource"
)
ANSWER_LINE = re.compile(r"^(\d{1,2})\s+(.+)$")
PAIR_HEAD = re.compile(r"^(\d{1,2})\s*&\s*(\d{1,2})\s+IN EITHER ORDER", re.I)


def parse_answer_keys(pages: list[list[str]]) -> dict[tuple[int, str], dict[int, str]]:
    """→ {(test_no, 'listening'|'reading'): {question_no: answer}}"""
    keys: dict[tuple[int, str], dict[int, str]] = {}

    for pno in ANSWER_KEY_PAGES:
        lines = [l.strip() for l in pages[pno - 1]]
        # One page holds exactly one (test, skill) key, but column-order reading can put
        # the "TEST n" banner after the skill heading — so resolve both up front.
        # The banner is sometimes preceded by a stray rule glyph ("I TEST 1").
        test_no = next((int(m.group(1)) for l in lines
                        if (m := re.fullmatch(r"[Il|]?\s*TEST\s*(\d)", l, re.I))), None)
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
                    r"([A-H])(?:\s+(?:Part|Reading Passage|Questions)\b.*)?", line)):
                cur[pending_pair.pop(0)] = m_solo.group(1)
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


def normalise_answer(ans: str) -> str:
    # A neighbouring column's heading can trail the answer when no number separates them.
    ans = re.split(r"\b(?:Reading Passage|Questions?|Part\b|If you score)", ans)[0]
    ans = ans.replace(" I ", " / ").replace("NOTGIVEN", "NOT GIVEN")
    ans = re.sub(r"\s+", " ", ans).strip(" .")
    return ans


# ─── test body: locate sections ───────────────────────────────────────────────

def find_test_pages(pages: list[list[str]]) -> list[dict]:
    """Locate, per test, the page index (0-based) of each skill heading."""
    tests: list[dict] = []
    cur: dict | None = None
    for i, lines in enumerate(pages[:97]):
        joined = lines[:4]
        for tag in ("LISTENING", "READING", "WRITING", "SPEAKING"):
            if tag in joined:
                if tag == "LISTENING":
                    cur = {"test": len(tests) + 1, "listening": i}
                    tests.append(cur)
                elif cur is not None:
                    cur.setdefault(tag.lower(), i)
    for t, nxt in zip(tests, tests[1:] + [{"listening": 97}]):
        t["end"] = nxt["listening"]
    return tests


def flatten(pages: list[list[str]], start: int, end: int) -> list[str]:
    out: list[str] = []
    for p in range(start, end):
        out.extend(pages[p])
    return out


# ─── question blocks ──────────────────────────────────────────────────────────

# A block header is normally its own line, but Listening prints the first one on the
# part heading ("PART 4 Questions 31-40"), so allow that prefix too.
Q_HEADER = re.compile(r"^(?:PART\s*\d\s+)?Questions?\s+(\d{1,2})\s*(?:[-–—]|and)\s*(\d{1,2})\s*$", re.I)
Q_HEADER_ONE = re.compile(r"^(?:PART\s*\d\s+)?Questions?\s+(\d{1,2})\s*$", re.I)
# The gap leader is typeset with dots on most pages but with middots on a few.
GAP = re.compile(r"(\d{1,2})\s*[£$€]?\s*[.·…]{4,}")
OPTION_LINE = re.compile(r"^([A-J])\s+(\S.*)$")
NUM_LINE = re.compile(r"^(\d{1,2})\s+(\S.*)$")

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


def build_questions(block: dict, qtype: str) -> list[dict]:
    lo, hi = block["lo"], block["hi"]
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
        return dedupe(out, lo, hi, block_instruction(block))

    if qtype == "mcq":
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

PART_RE = re.compile(r"^PART\s*(\d)\s*(?:Questions?\s*(\d{1,2})\s*[-–]\s*(\d{1,2}))?", re.I)

# The recordings live in the frontend's public/ dir, which only exists on a dev machine —
# so the file list is resolved here, at parse time, and baked into the fixture. The
# seeder then works unchanged on Render, where those files are not present.
AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "..", "ilm-ai-frontend", "public", "audio", "listening")


def audio_urls(test_no: int, part: int) -> list[str]:
    """Ordered URLs for a part; nine of the sixteen were ripped as two files."""
    stem = f"C21T{test_no}P{part}"
    try:
        names = sorted(n for n in os.listdir(AUDIO_DIR)
                       if n.endswith(".mp3") and n[:-len(".mp3")].split(".")[0] == stem)
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

        title = next((l for l in region[1:6]
                      if not Q_HEADER.match(l) and not l.lower().startswith(
                          ("complete", "choose", "write", "questions"))), f"Part {part}")
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
        out.append({
            "test": test_no,
            "task": task,
            "task_type": f"Task{task}",
            "prompt": " ".join(prompt_lines).strip(),
            "min_words": 150 if task == 1 else 250,
            "duration_minutes": 20 if task == 1 else 40,
        })
    return out


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

def main() -> int:
    reader = PdfReader(PDF_PATH)
    pages = load_pages(reader)
    keys = parse_answer_keys(pages)
    scripts = parse_audioscripts(pages)
    tests = find_test_pages(pages)

    data = {"source": "Cambridge IELTS 21 Academic", "tests": []}
    for t in tests:
        n = t["test"]
        listening = parse_listening(
            flatten(pages, t["listening"], t["reading"]), n,
            keys.get((n, "listening"), {}), scripts.get(n, {}))
        reading = parse_reading(
            flatten(pages, t["reading"], t["writing"]), n, keys.get((n, "reading"), {}))
        writing = parse_writing(flatten(pages, t["writing"], t["speaking"]), n)
        speaking = parse_speaking(flatten(pages, t["speaking"], t["end"]), n)
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
