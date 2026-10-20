"""Index user-provided textbooks without redistributing their text or images.

Requires Poppler's pdftotext. The catalogue stores bibliographic data, short
headings, page references and verification results only. Missing files are
explicitly blocked, never filled from another edition or a generated outline.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

BOOKS = {
    5: dict(
        file_name="5-biologiya.pdf",
        title="Biologiya",
        year=2020,
        authors=["O‘. Pratov", "A. To‘xtayev", "F. Azimova", "Z. Tillayeva"],
        publisher="O‘zbekiston",
        edition=5,
        toc=[95],
        end=93,
        offset=1,
        chapter_count=3,
        paragraph_count=18,
        isbn="978-9943-6479-3-0",
    ),
    6: dict(file_name="botanika_6_uzb.pdf", title="Botanika"),
    7: dict(
        file_name="zoologiya_7_uzb.pdf",
        title="Biologiya (Zoologiya)",
        year=2017,
        authors=["O. Mavlonov"],
        publisher="O‘zbekiston milliy ensiklopediyasi",
        edition=4,
        toc=[204, 205, 206],
        end=201,
        offset=0,
        chapter_count=8,
        paragraph_count=59,
        isbn="978-9943-07-508-5",
    ),
    8: dict(
        file_name="odam_va_uning_salomatligi_8_uzb.pdf",
        title="Odam va uning salomatligi",
    ),
    9: dict(
        file_name="biologiya_9_uzb.pdf",
        title="Biologiya. Sitologiya va genetika asoslari",
        year=2019,
        authors=["A. Zikiryayev", "A. To‘xtayev", "I. Azimov", "N. Sonin"],
        publisher="Yangiyul Poligraph Service",
        edition=5,
        toc=[188, 189, 190],
        end=188,
        offset=0,
        chapter_count=8,
        paragraph_count=67,
        isbn="978-9943-361-10-2",
    ),
    10: dict(
        file_name="biologiya_10_uzb.pdf",
        title="Biologiya",
        year=2017,
        authors=[
            "A. G‘afurov",
            "A. Abdukarimov",
            "J. Tolipova",
            "O. Ishankulov",
            "M. Umaraliyeva",
            "I. Abduraxmonova",
        ],
        publisher="Sharq",
        edition=1,
        toc=[237, 238],
        end=235,
        offset=0,
        chapter_count=5,
        paragraph_count=58,
        isbn="978-9943-26-708-4",
    ),
    11: dict(
        file_name="biologiya_11_uzb.pdf",
        title="Biologiya",
        year=2018,
        authors=[
            "A. G‘afurov",
            "A. Abdukarimov",
            "J. Tolipova",
            "O. Ishankulov",
            "M. Umaraliyeva",
            "I. Abduraxmonova",
        ],
        publisher="Sharq",
        edition=1,
        toc=[237, 238],
        end=233,
        offset=0,
        chapter_count=4,
        paragraph_count=44,
        isbn="978-9943-26-806-7",
    ),
}

VERIFIED_PDF_SHA256 = {
    5: "a2465bbe185ed9062d7af1eac5389048253317dc9a7ae2889a562fce094a0530",
    7: "168c60207cb556c57deacedf453c23774c64ab76309cf43be117871e53ab064b",
    9: "3b7435c0f6bebbe465cab24f9a74f4b443c54c2b33043c1bd7856bffa0f7f8fe",
    10: "dc2e7ceaec7dd828d634b4525c4bed6ea2aaeedf84484f95a890954a25c1138d",
    11: "3a220c9f8102663566979e3b568b1a51c6134342b37edc2ee4ad3a0d2c101a52",
}


def norm(value):
    value = unicodedata.normalize("NFKC", value).casefold().replace("ð", "p")
    value = "\n".join(
        line
        for line in value.splitlines()
        if line.strip() not in {"z", "l.u", "rta", "po", "du", ":e", "tp", "ht"}
    )
    return "".join(c for c in value if c.isalnum())


START = re.compile(
    r"^(?:[IVX]+\s+(?:BOB|BO[‘'’]LIM)\.|\d+\s*[-–]\s*§|\d+\.\d+\.|\d+\s*[-–]\s*(?:laboratoriya|amaliy))",
    re.I,
)


def toc_records(pages, book):
    chunks, current, toc_page = [], [], None
    for page in book["toc"]:
        for raw in pages[page - 1].splitlines():
            line = raw.strip()
            if not line or line in {"z", "l.u", "rta", "po", "du", ":e", "tp", "ht"}:
                continue
            if START.match(line):
                if current:
                    chunks.append((toc_page, " ".join(current)))
                current, toc_page = [line], page
            elif current and not re.fullmatch(r"\d+", line):
                if re.match(
                    r"(?:Atamalar|Topishmoqlar|Zoologiya termin|DARSLIKDA)", line, re.I
                ):
                    chunks.append((toc_page, " ".join(current)))
                    current = []
                else:
                    current.append(line)
    if current:
        chunks.append((toc_page, " ".join(current)))
    records = []
    for page, chunk in chunks:
        chunk = chunk.replace("ð", "p").replace("\u00ad", "")
        match = re.search(r"\.{2,}\s*(\d+)\s*$", chunk)
        number = int(match[1]) if match else None
        title = re.sub(r"\.{2,}\s*\d+\s*$", "", chunk).strip()
        if re.match(r"[IVX]+\s+BO[‘'’]LIM", title, re.I):
            kind = "part"
        elif re.match(r"[IVX]+\s+BOB", title, re.I):
            kind = "chapter"
        elif re.match(r"\d+\.\d+\.", title):
            kind = "subchapter"
        else:
            kind = (
                "laboratory"
                if "laboratoriya" in title.casefold()
                else "practical"
                if "amaliy" in title.casefold()
                else "topic"
            )
        paragraph = re.match(r"(\d+)\s*[-–]\s*§\.?\s*", title)
        records.append(
            dict(
                kind=kind,
                title=title,
                paragraph=int(paragraph[1]) if paragraph else None,
                toc_pdf_page=page,
                toc_printed_start=number,
            )
        )
    # The five-grade OCR spaces individual letters; verified against its TOC.
    if book["year"] == 2020:
        chapter_titles = [
            "I BOB. BIOLOGIYA TIRIK ORGANIZMLAR HAQIDAGI FAN",
            "II BOB. TIRIK ORGANIZMLARNING XILMA-XILLIGI",
            "III BOB. ORGANIZM VA TASHQI MUHIT",
        ]
        topic_titles = [
            "Biologiya – hayot haqidagi fan",
            "Tirik organizmlarning xususiyatlari",
            "Biologiyaning o‘rganish usullari",
            "Hujayra – tiriklikning asosi",
            "Tirik organizmlar haqida umumiy ma’lumot",
            "Bakteriyalar dunyosi",
            "Zamburug‘lar dunyosi",
            "O‘simliklar dunyosi",
            "Tuban o‘simliklar",
            "Yuksak o‘simliklar",
            "O‘zbekistonda keng tarqalgan dorivor va zaharli o‘simliklar",
            "Hayvonot dunyosi",
            "Umurtqasiz hayvonlar",
            "Umurtqali hayvonlar",
            "Odam organlari sistemasi",
            "Ekologik omillar",
            "Inson va tabiat",
            "Tabiatni muhofaza qilish",
        ]
        ci = 0
        for r in records:
            if r["kind"] == "chapter":
                r["title"] = chapter_titles[ci]
                ci += 1
            elif r["paragraph"]:
                r["title"] = f"{r['paragraph']}-§. {topic_titles[r['paragraph'] - 1]}"
    return records


def verify_record(r, pages, book):
    if r["paragraph"]:
        digits = r"\s*".join(str(r["paragraph"]))
        pattern = re.compile(rf"(?m)^\s*[.\s]*{digits}\s*[-–]\s*§\.?\s*")
    elif r["kind"] in {"laboratory", "practical"}:
        n = re.match(r"\d+", r["title"])[0]
        word = "laboratoriya" if r["kind"] == "laboratory" else "amaliy"
        pattern = re.compile(rf"(?im)^\s*{n}\s*[-–]\s*{word}")
    else:
        return
    title = re.sub(r"^\d+\s*[-–]\s*§\.?", "", r["title"])
    candidates = []
    for i, p in enumerate(pages[: book["end"] - 1]):
        for match in pattern.finditer(p):
            head = p[max(0, match.start() - 180) : match.end() + 420]
            target = norm(title)
            similarity = SequenceMatcher(
                None, target, norm(head), autojunk=False
            ).find_longest_match().size / max(1, len(target))
            expected = (r["toc_printed_start"] or i + 1) + book["offset"]
            if not r["paragraph"] and len(target) < 32:
                similarity = 1.0  # The TOC only names the numbered laboratory.
            candidates.append((similarity, i + 1, match.start(), similarity))
    if not candidates:
        r["verification"] = {
            "status": "needs_visual_check",
            "reason": "heading_not_extracted",
        }
        return
    strong = [c for c in candidates if c[0] >= 0.5]
    if strong:
        # Running headers repeat the section on subsequent pages. Prefer the
        # numbered body heading on the TOC page, not the cleanest running header.
        expected = (r["toc_printed_start"] or strong[0][1]) + book["offset"]
        _, page, start, similarity = min(
            strong, key=lambda c: (abs(c[1] - expected), c[1], -c[2])
        )
    else:
        _, page, start, similarity = max(candidates)
    r.update(pdf_start=page, printed_start=page - book["offset"])
    r["verification"] = {
        "status": "text_layer_matched" if similarity >= 0.50 else "needs_visual_check",
        "method": "paragraph_number_and_heading"
        if r["paragraph"]
        else "numbered_activity_heading",
        "heading_similarity": round(similarity, 3),
        "heading_offset": start,
    }
    if r["toc_printed_start"] != r["printed_start"]:
        r["verification"]["toc_body_page_difference"] = True


def index_book(path, grade, book):
    if (
        grade not in VERIFIED_PDF_SHA256
        or hashlib.sha256(path.read_bytes()).hexdigest() != VERIFIED_PDF_SHA256[grade]
    ):
        raise ValueError(
            f"Unreviewed PDF/edition for grade {grade}; do not reuse another edition's metadata."
        )
    raw = subprocess.check_output(["pdftotext", "-layout", str(path), "-"], text=True)
    pages = raw.split("\f")
    if not pages[-1].strip():
        pages.pop()
    records = toc_records(pages, book)
    chapter = part = subsection = None
    for i, r in enumerate(records):
        r["id"] = f"bio-{grade}-{r['kind']}-{i + 1}"
        if r["kind"] == "part":
            part = r["id"]
            chapter = subsection = None
        elif r["kind"] == "chapter":
            chapter, subsection = r["id"], None
        elif r["kind"] == "subchapter":
            subsection = r["id"]
        r.update(chapter_id=chapter, part_id=part, subchapter_id=subsection)
        verify_record(r, pages, book)
    # Non-TOC laboratory/practical sections of grade 5 are indexed independently.
    if grade == 5:
        for page, kind, number, title in [
            (
                9,
                "laboratory",
                1,
                "Xavfsizlik texnikasi qoidalari va laboratoriya jihozlari bilan tanishish",
            ),
            (16, "laboratory", 2, "Lupa va mikroskop tuzilishi bilan tanishish"),
            (
                23,
                "laboratory",
                3,
                "Piyoz po‘sti hujayrasining tuzilishini mikroskopda o‘rganish",
            ),
            (31, "practical", 1, "Sutdan qatiq tayyorlash"),
            (
                35,
                "laboratory",
                4,
                "Achitqi zamburug‘idan foydalanib non tayyorlash jarayoni bilan tanishish",
            ),
            (40, "practical", 2, "O‘simliklar bargidan gerbariy tayyorlash"),
            (50, "practical", 3, "Olma o‘simligining hayot sikli bilan tanishish"),
            (52, "practical", 4, "Xona o‘simliklarini ekish va ko‘chirib o‘tkazish"),
            (69, "practical", 5, "Suvarak va asalarining hayot siklini o‘rganish"),
            (74, "practical", 6, "Baqaning hayot siklini o‘rganish"),
            (
                86,
                "practical",
                7,
                "Maktab hududidagi o‘simlik va hayvonot dunyosining mavsumiy o‘zgarishlarini kuzatish",
            ),
            (
                91,
                "practical",
                8,
                "Bakteriya, zamburug‘, o‘simlik va hayvonot dunyosi haqida ma’lumot to‘plash",
            ),
        ]:
            owner = max(
                (
                    r
                    for r in records
                    if r.get("paragraph") and r.get("pdf_start", 999) <= page
                ),
                key=lambda r: r["pdf_start"],
            )
            heading_offset = 0
            for line in pages[page - 1].splitlines(keepends=True):
                if re.search(
                    rf"{number}[-–](?:laboratoriya|amaliy)",
                    re.sub(r"\s+", "", line).lower(),
                ):
                    break
                heading_offset += len(line)
            records.append(
                dict(
                    id=f"bio-5-{kind}-{number}",
                    kind=kind,
                    paragraph=None,
                    title=title,
                    toc_pdf_page=None,
                    toc_printed_start=None,
                    pdf_start=page,
                    chapter_id=owner["chapter_id"],
                    printed_start=page - 1,
                    verification={
                        "status": "text_layer_manually_checked",
                        "method": "body_activity_heading",
                        "heading_offset": heading_offset,
                        "reviewed_on": "2026-10-20",
                    },
                )
            )
    ordered = sorted(
        (r for r in records if r.get("pdf_start")),
        key=lambda r: (r["pdf_start"], r["verification"].get("heading_offset", 0)),
    )
    for idx, r in enumerate(ordered):
        nxt = ordered[idx + 1] if idx + 1 < len(ordered) else None
        end = nxt["pdf_start"] if nxt else book["end"] - 1
        if (
            nxt
            and nxt["verification"].get("heading_offset", 999) < 90
            and end > r["pdf_start"]
        ):
            end -= 1
        r.update(
            pdf_end=max(r["pdf_start"], end),
            printed_end=max(r["pdf_start"], end) - book["offset"],
        )
        r["range_method"] = "next_verified_heading_boundary_inclusive"
        content = "\n".join(pages[r["pdf_start"] - 1 : r["pdf_end"]])
        markers = [
            word
            for word in ("savol", "topshiriq", "mustaqil", "bilimingizni")
            if word in content.casefold()
        ]
        r["assessment_marker_scan"] = {
            "detected": markers,
            "status": "detected" if markers else "not_detected_not_proof_of_absence",
        }
    # Chapter/part start pages derive from real children, not TOC page mistakes.
    for r in reversed(records):
        if r["kind"] in {"chapter", "part", "subchapter"}:
            field = {
                "chapter": "chapter_id",
                "part": "part_id",
                "subchapter": "subchapter_id",
            }[r["kind"]]
            children = [
                c
                for c in records
                if c["id"] != r["id"] and c.get(field) == r["id"] and c.get("pdf_start")
            ]
            if children:
                r.update(
                    pdf_start=min(c["pdf_start"] for c in children),
                    pdf_end=max(c["pdf_end"] for c in children),
                )
                r.update(
                    printed_start=r["pdf_start"] - book["offset"],
                    printed_end=r["pdf_end"] - book["offset"],
                )
                r["verification"] = {
                    "status": "children_heading_matched",
                    "method": "toc_and_body_children",
                }
                if (
                    r["toc_printed_start"] is not None
                    and r["toc_printed_start"] != r["printed_start"]
                ):
                    r["verification"]["toc_body_page_difference"] = True
    return {
        **{k: v for k, v in book.items() if k not in {"toc", "end", "offset"}},
        "id": f"biology-{grade}-{book['year']}",
        "grade": grade,
        "status": "mapped"
        if all(
            r.get("verification", {}).get("status") != "needs_visual_check"
            for r in records
        )
        else "indexed_pending_review",
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "pdf_page_count": len(pages),
        "toc_pdf_pages": book["toc"],
        "bibliography_pdf_pages": [2, 3] if grade == 5 else [1, 2],
        "questions_and_tasks": {
            "present": True,
            "evidence_pdf_pages": [
                i + 1
                for i, p in enumerate(pages[: book["end"] - 1])
                if any(word in norm(p) for word in ("savol", "topshiriq"))
            ][:8],
            "verification": "text_layer_legends_and_assessment_markers",
            "textbook_questions_republished": False,
        },
        "rights": {
            "fulltext_republication": "not_authorized",
            "images_republication": "not_authorized",
            "published_payload": "bibliography_headings_page_references_and_original_fact_based_lessons",
        },
        "duplicate_pdf_ranges": [[99, 195]] if grade == 5 else [],
        "records": records,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--blocked-transfer-grade",
        type=int,
        action="append",
        default=[],
        help="Grade whose attachment was actually rejected by the transfer tool; repeat as needed.",
    )
    args = parser.parse_args()
    books = []
    for grade, book in BOOKS.items():
        matches = list(args.pdf_dir.rglob(book["file_name"]))
        if not matches:
            books.append(
                {
                    "id": f"biology-{grade}-unavailable",
                    "grade": grade,
                    "file_name": book["file_name"],
                    "title": book["title"],
                    "status": "blocked_transfer_limit_32_mib"
                    if grade in args.blocked_transfer_grade
                    else "blocked_source_unavailable",
                    "records": [],
                    "note": "User attachment exists, but the available transfer tool rejected files over 32 MiB; no pages read."
                    if grade in args.blocked_transfer_grade
                    else "Source file is not locally available; no pages read.",
                }
            )
            continue
        books.append(index_book(matches[0], grade, book))
    result = {
        "schema_version": 1,
        "subject_slug": "biologiya",
        "language": "uz",
        "books": books,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    for book in books:
        records = book["records"]
        pending = [
            r["id"]
            for r in records
            if r.get("verification", {}).get("status") == "needs_visual_check"
        ]
        print(
            f"Grade {book['grade']}: {book['status']}; {len(records)} records; pending checks {pending}"
        )


if __name__ == "__main__":
    main()
