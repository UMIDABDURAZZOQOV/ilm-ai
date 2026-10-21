"""Read-only chapter/topic/source audit; completeness is not production approval.

No database or PDF is opened. Source bounds and recorded review evidence are
validated; biological truth still requires source review and subject expertise.
"""

import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.curriculum_validation import (  # noqa: E402
    load_documents,
    load_lesson_set,
    readiness_report,
)


def completion_audit(catalog, lessons):
    identities = [(lesson["book_id"], lesson["topic_id"]) for lesson in lessons]
    if len(set(identities)) != len(identities):
        raise ValueError("duplicate_source_topic_lesson")
    grades = readiness_report(catalog, lessons)
    covered = set(identities)
    chapters = []
    for book in catalog["books"]:
        for chapter in book["records"]:
            if chapter["kind"] not in {"chapter", "introduction"}:
                continue
            records = [
                r for r in book["records"]
                if r["kind"] in {"topic", "laboratory", "practical"}
                and r["chapter_id"] == chapter["id"]
            ]
            missing = [r["id"] for r in records if (book["id"], r["id"]) not in covered]
            chapters.append({
                "grade": book["grade"],
                "chapter_id": chapter["id"],
                "title": chapter["title"],
                "kind": chapter["kind"],
                "pdf_range": [chapter["pdf_start"], chapter["pdf_end"]],
                "printed_range": [chapter["printed_start"], chapter["printed_end"]],
                "theory_topics": sum(r["kind"] == "topic" for r in records),
                "activities": sum(r["kind"] != "topic" for r in records),
                "missing_record_ids": missing,
                "complete": bool(records) and not missing,
            })
    fingerprint = hashlib.sha256(json.dumps(
        {"catalog": catalog, "lessons": sorted(lessons, key=lambda l: l["key"])},
        ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode()).hexdigest()
    return {
        "schema_version": 1,
        "scope": "reviewed_content_coverage_not_production_or_physical_lab_approval",
        "content_sha256": fingerprint,
        "complete": all(g["course_ready"] for g in grades)
        and all(c["complete"] for c in chapters),
        "totals": {
            "books": len(grades),
            "chapters": sum(g["chapters"] for g in grades),
            "introductions": sum(g["introductions"] for g in grades),
            "theory_lessons": sum(g["ready_theory_lessons"] for g in grades),
            "digital_activities": sum(g["ready_activities"] for g in grades),
            "cards": sum(len(l["theory"]) for l in lessons),
            "questions": sum(len(l["questions"]) for l in lessons),
        },
        "grades": grades,
        "chapters": chapters,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    catalog, _ = load_documents()
    report = completion_audit(catalog, load_lesson_set())
    if args.output:
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"complete": report["complete"], **report["totals"]}))
    return 0 if report["complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
