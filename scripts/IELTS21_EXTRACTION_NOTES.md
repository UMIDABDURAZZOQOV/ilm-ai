# Cambridge IELTS 21 Academic — extraction notes (2026-07-21)

> **STATUS: DONE.** `scripts/parse_ielts21.py` + `scripts/seed_ielts21.py` replaced everything
> described below; the fixture `scripts/seeds/ielts21.json` holds 320/320 questions with 320/320
> answer keys and is live in production. This file is kept as the record of *why* the first pass
> failed. The decisive fact — every page is `/Rotate 90`, so pypdf's default reading order
> interleaves columns — is the thing to remember if the parser ever needs changing.

The owner has a **licence** for the official book + audio, so ingesting them is fine.

Source files
- Book:  `C:/Users/Page/Downloads/IELTS_21.pdf`  (146 pages, 43 MB, text layer is clean)
- Audio: `C:/Users/Page/Desktop/Projects/IELTS 21 AUDIO.zip`
         (already extracted → `ilm-ai-frontend/public/audio/listening/C21T*.mp3`, 26 files)
- Library available in this env: **`pypdf`** (pdfplumber / PyMuPDF are NOT installed).

## What the FIRST extraction pass got wrong (verified against the DB)

| Table | Rows | Reality |
|---|---|---|
| `ielts_questions` | **0** | ❌ nothing extracted — **this is why no test actually works** |
| `ielts_reading` | 16 | ❌ only 4 real (5.4k–6k chars); the other 12 hold just `"You should spend about 20 minutes on"` (30–36 chars) |
| `ielts_listening` | 16 | ⚠️ audio links fine; every transcript is **exactly 800 chars** → hard-truncated |
| `ielts_writing` | 16 | ⚠️ prompts look right (~591 chars) but `task` is `None` (should be 1 or 2) |
| `ielts_speaking` | 16 | ⚠️ mojibake — bullets decoded as `�` (`'� Where do you go to get a haircut?'`) |

So: audio ✅, everything else needs redoing.

## Page map discovered (regular, 4 tests × ~22 pages)

```
p10  Test 1 LISTENING  PART 1            p16  Test 1 READING
p11                    PART 2  Q11-20    p19         Questions 8-13
p13                    PART 3  Q21-30
p15                    PART 4  Q31-40
p32  Test 2 LISTENING                    p38  Test 2 READING
```
Tests 3 and 4 follow the same offsets (~+22 pages each). Answer keys and the
audioscripts live at the back of the book — locate them by scanning for
`Audioscript` / `Answer key` headings before parsing.

## Plan for the rewrite

1. **Questions first** — this is the blocker. Parse the `Questions N-M` blocks; each block's
   instruction line becomes `group_instruction`. Detect the type from the instruction wording:
   `TRUE/FALSE/NOT GIVEN` → `tfng`, `YES/NO/NOT GIVEN` → `ynng`, `Choose the correct letter` →
   `mcq`, `Choose ONE WORD` / `Complete the notes` → `completion`, `list of headings` → `heading`,
   `Which section` / matching → `matching`. Pair each with the answer key at the back →
   `ielts_questions.correct_answer`. Keep `order_index` = the printed question number (1–40).
2. **Reading passages** — extract the pages between `READING PASSAGE n` and the first
   `Questions` block; strip running headers/footers ("Test 1", page numbers). Expect 5–6k chars.
   Do NOT truncate.
3. **Transcripts** — from the Audioscript section, per test/part. Remove the 800-char cap that
   the first pass applied.
4. **Speaking** — decode with `errors="replace"` removed; strip the bullet glyph instead of
   letting it become `�`. Split into Part 1 / 2 / 3.
5. **Writing** — set `task` = 1 or 2 from the `WRITING TASK n` heading; keep the figure page
   reference for Task 1 (image needs exporting separately — pypdf can pull embedded images).

## Frontend status (already built, content-agnostic)

`src/components/ielts/` has `ReadingExam`, `ListeningExam`, `WritingExam`, `SpeakingExam`,
`ExamShell` + `TestBrowser`; `src/lib/ieltsBand.ts` has the official raw→band tables.
`/sat/ielts/reading` and `/sat/ielts/dictionary` are wired. **Listening / Writing / Speaking
pages are still unwired on purpose** — their grading endpoints need a real `task_id`, so wire
them once the tables above hold correct rows.
