"""Audit the reviewed five-book map; never derives approval from OCR.

Optional --pdf-dir verifies the exact private originals and decodes all pages.
Only short source metadata/maps/review status can be written to the repository.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from services.chemistry_validation import load_catalog, readiness, ROOT


def audit_originals(catalog, directory):
    from pypdf import PdfReader
    import pypdfium2 as pdfium

    total = 0
    for book in catalog["books"]:
        path = directory / book["file_name"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != book["sha256"]:
            raise ValueError("source_digest_mismatch:" + book["file_name"])
        if len(PdfReader(path).pages) != book["pdf_page_count"]:
            raise ValueError("source_page_count_mismatch")
        with pdfium.PdfDocument(path) as document:
            for page in document:
                bitmap = page.render(scale=120 / max(page.get_size()))
                bitmap.close()
                page.close()
                total += 1
    return total


def write_maps(catalog, progress, lessons=()):
    folder = ROOT / "docs/chemistry"
    folder.mkdir(parents=True, exist_ok=True)
    activities = {identifier: lesson['key'] for lesson in lessons
                  for identifier in lesson.get('source_activity_ids', [])}
    for book, state in zip(catalog["books"], progress):
        grade = book["grade"]
        lines = [f"# {grade}-sinf: {book['title']} ({book['year']})", "",
                 "Source map; catalogue entries are not implemented lessons.", "",
                 f"File: `{book['file_name']}`; SHA-256: `{book['sha256']}`.", "",
                 "End pages include the shared boundary before the next heading.",
                 "Individual lesson claims require their own reviewed source refs.", "",
                 "| ID | Kind / number | Original heading | Printed | PDF / region | TOC start | Content | Prerequisite |",
                 "| --- | --- | --- | --- | --- | --- | --- | --- |"]
        remaining = set(state["remaining_ids"])
        for r in book["records"]:
            start, end = r["start_locator"], r["end_locator"]
            location = f"{start['pdf_page']}:{start['region']} – {end['pdf_page']}:{end['region']}"
            status = "reviewed local lesson" if r["kind"] in {"paragraph", "laboratory", "practical"} and r["id"] not in remaining else r["content_status"]
            if r['id'] in activities:
                status = 'integrated source activity in ' + activities[r['id']]
            if r.get('editorial_review_issues'):
                status += '; scoped editorial review remains open'
            if r.get('source_review_hold',{}).get('status') == 'open':
                status = 'blocked: source review ' + r['source_review_hold']['id']
            lines.append(f"| `{r['id']}` | {r['kind']} {r.get('number') or ''} | {r['title'].replace('|', '/')} | {r['printed_start']}–{r['printed_end']} | {location} | {r.get('toc_printed_start') or 'body only'} | {status} | {', '.join(r['prerequisite_ids']) or '—'} |")
        (folder / f"grade_{grade}_map.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-dir", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--write-maps", action="store_true")
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    catalog = load_catalog()
    # The explicit reviewed index will be used after authorship; draft globbing
    # is deliberately prohibited.
    index_path = ROOT / "scripts/curriculum/chemistry/chemistry_lessons.json"
    lessons = []
    if index_path.exists():
        from services.chemistry_validation import load_lessons
        lessons = load_lessons(catalog)
    progress = readiness(catalog, lessons)
    result = {"mapped_grades": len(catalog["books"]),
              "catalogue_records": sum(len(b["records"]) for b in catalog["books"]),
              "source_teaching_entries": sum(s["source_teaching_entries"] for s in progress),
              "implemented_lessons": len(lessons), "grades": progress,
              "integrated_source_activities": len({i for l in lessons for i in l.get('source_activity_ids', [])}),
              "open_source_review_holds": sum(r.get('source_review_hold',{}).get('status') == 'open'
                                               for b in catalog['books'] for r in b['records']),
              "open_editorial_review_issues": sum(i.get('status') == 'open_review'
                                                 for b in catalog['books'] for r in b['records']
                                                 for i in r.get('editorial_review_issues', [])),
              "full_fact_formula_review_complete": False}
    if args.pdf_dir:
        result["original_pdf_pages_decoded"] = audit_originals(catalog, args.pdf_dir)
    if args.write_maps:
        write_maps(catalog, progress, lessons)
    if args.report:
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "grades"}, indent=2))
    for row in progress:
        print(f"Grade {row['grade']}: {row['implemented_lessons']}/{row['source_teaching_entries']} local lessons")
    if args.require_complete and not all(r["course_ready"] for r in progress):
        parser.exit(2, "course_incomplete: mapped sources are not authored lessons\n")


if __name__ == "__main__":
    main()
