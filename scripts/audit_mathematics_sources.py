"""Private-file audit, emitting only hashes/counts: no PDF/OCR copying to Git."""

import argparse
import hashlib
import json
from pathlib import Path

from services.mathematics_curriculum import ROOT, load_course, manifest, require


def audit(source_directory):
    import fitz

    catalog = manifest()
    index = json.loads((ROOT / "page_inventory.json").read_text())
    supplied = list(Path(source_directory).rglob("*.pdf"))
    paths = {}
    for book in catalog["books"]:
        matches = [p for p in supplied if p.name == book["original_filename"]]
        require(
            len(matches) == 1, "math_missing_or_duplicate_source:" + book["book_id"]
        )
        path = paths[book["book_id"]] = matches[0]
        require(
            hashlib.sha256(path.read_bytes()).hexdigest() == book["sha256"],
            "math_pdf_hash_changed",
        )
        with fitz.open(path) as pdf:
            require(
                len(pdf) == book["pdf_pages"] == len(index[book["book_id"]]),
                "math_pdf_page_count_changed",
            )
            for page, saved in zip(pdf, index[book["book_id"]]):
                require(page.number + 1 == saved["pdf_page"], "math_pdf_page_gap")
                require(
                    hashlib.sha256(page.get_text().encode()).hexdigest()
                    == saved["native_text_sha256"],
                    "math_page_text_changed",
                )
    review = json.loads((ROOT / "grade1_part1_review.json").read_text())
    from services.mathematics_curriculum import BATCHES

    reviews = [json.loads((ROOT / filename).read_text()) for _, filename in BATCHES]
    review["topics"] = [
        topic
        for entry in reviews
        if entry["book_id"] == review["book_id"]
        for topic in entry["topics"]
    ]
    for entry in reviews:
        if entry["book_id"] == review["book_id"]:
            continue
        with fitz.open(paths[entry["book_id"]]) as pdf:
            for topic in entry["topics"]:
                for saved in topic["pages"]:
                    page = pdf[saved["pdf_page"] - 1]
                    require(
                        hashlib.sha256(page.get_text().encode()).hexdigest()
                        == saved["native_text_sha256"],
                        "math_reviewed_text_changed",
                    )
                    require(
                        hashlib.sha256(
                            page.get_pixmap(matrix=fitz.Matrix(1.3, 1.3)).tobytes("png")
                        ).hexdigest()
                        == saved["image_sha256"],
                        "math_reviewed_image_changed",
                    )
    with fitz.open(paths[review["book_id"]]) as pdf:
        for topic in review["topics"]:
            for page in topic["pages"]:
                actual = (
                    pdf[page["pdf_page"] - 1]
                    .get_pixmap(matrix=fitz.Matrix(1.3, 1.3))
                    .tobytes("png")
                )
                require(
                    hashlib.sha256(actual).hexdigest() == page["image_sha256"],
                    "math_reviewed_image_changed",
                )
        mapping = json.loads((ROOT / "grade1_part1_map.json").read_text())
        require(
            [t["source_number"] for t in mapping["topics"]] == list(range(1, 42)),
            "math_toc_topic_gap_or_duplicate",
        )
        require(
            mapping["topics"][24]["duplicate_pdf_pages"] == [55, 56],
            "math_duplicate_pages_not_recorded",
        )
        for saved in mapping["additional_image_checks"]:
            page = pdf[saved["pdf_page"] - 1]
            require(
                hashlib.sha256(page.get_text().encode()).hexdigest()
                == saved["native_sha256"],
                "math_mapping_native_changed",
            )
            actual = page.get_pixmap(matrix=fitz.Matrix(1.3, 1.3)).tobytes("png")
            require(
                hashlib.sha256(actual).hexdigest() == saved["png_sha256"],
                "math_mapping_image_changed",
            )
    lessons = load_course()
    reviewed_book_pages = {
        page["pdf_page"] for topic in review["topics"] for page in topic["pages"]
    } | {page["pdf_page"] for page in mapping["additional_image_checks"]}
    pending = json.loads((ROOT / "grade1_part2_map.json").read_text())
    require(
        pending["authored_lessons"]
        == sum(l["source_refs"][0]["book_id"] == pending["book_id"] for l in lessons),
        "math_map_authored_count_changed",
    )
    with fitz.open(paths[pending["book_id"]]) as pdf:
        for saved in pending["additional_image_checks"]:
            page = pdf[saved["pdf_page"] - 1]
            require(
                hashlib.sha256(page.get_text().encode()).hexdigest()
                == saved["native_sha256"],
                "math_part2_review_text_changed",
            )
            require(
                hashlib.sha256(
                    page.get_pixmap(matrix=fitz.Matrix(1.3, 1.3)).tobytes("png")
                ).hexdigest()
                == saved["png_sha256"],
                "math_part2_review_image_changed",
            )
        require(
            pending["topics"][-1]["source_number"] == 74
            and pending["topics"][-1]["body_pdf_locator"] is None
            and pending["source_gaps"][0]["missing_printed_pages"] == [68, 69],
            "math_missing_part2_pages_invented",
        )
    third = json.loads((ROOT / "grade1_part3_map.json").read_text())
    require(
        third["book_sha256"]
        == next(
            b["sha256"] for b in catalog["books"] if b["book_id"] == third["book_id"]
        )
        and [t["source_number"] for t in third["topics"]]
        == list(range(1, 12)) + list(range(14, 27)) + list(range(30, 43))
        and [t["path_sequence"] for t in third["topics"]] == list(range(1, 38))
        and [p for t in third["topics"] for p in t["body_pdf_locator"]]
        == list(range(6, 80)),
        "math_part3_body_map_gap_or_duplicate",
    )
    require(
        third["authored_lessons"]
        == sum(l["source_refs"][0]["book_id"] == third["book_id"] for l in lessons)
        and sum(t["interactive_lesson_created"] for t in third["topics"])
        == third["authored_lessons"]
        and not any(
            t["ready"] or t["body_pdf_locator"]
            for t in third["scheduled_activities_without_body"]
        ),
        "math_part3_unreviewed_or_scheduled_content_invented",
    )
    game = next(
        t
        for t in third["scheduled_activities_without_body"]
        if t["kind"] == "game" and t["source_numbers"] == [28]
    )
    require(
        game.get("body_footer_source_numbers") == [29]
        and game.get("body_footer_pdf_page") == 53
        and game.get("body_footer_printed_page") == 51
        and not game["ready"]
        and game["body_pdf_locator"] is None,
        "math_publisher_game_label_discrepancy_hidden",
    )
    with fitz.open(paths[third["book_id"]]) as pdf:
        checks = third["additional_image_checks"] + [
            p for t in third["topics"] for p in t["boundary_pins"]
        ]
        for saved in checks:
            page = pdf[saved["pdf_page"] - 1]
            require(
                hashlib.sha256(page.get_text().encode()).hexdigest()
                == saved["native_text_sha256"]
                and hashlib.sha256(
                    page.get_pixmap(matrix=fitz.Matrix(1.3, 1.3)).tobytes("png")
                ).hexdigest()
                == saved["image_sha256"],
                "math_part3_mapping_source_changed",
            )
    return {
        "available_pdfs": len(paths),
        "available_pages": sum(b["pdf_pages"] for b in catalog["books"]),
        "body_image_reviewed_topics": sum(len(r["topics"]) for r in reviews),
        "reviewed_body_pages": sum(
            len(t["pages"]) for r in reviews for t in r["topics"]
        ),
        "interactive_lessons": len(lessons),
        "theory_cards": sum(len(l["cards"]) for l in lessons),
        "questions": sum(len(l["questions"]) for l in lessons),
        "grade1_part1_all_source_images_reviewed": len(reviewed_book_pages),
        "grade1_part2_toc_units": len(pending["topics"]),
        "grade1_part2_authored_lessons": pending["authored_lessons"],
        "grade1_part2_pending_toc_units": len(pending["topics"])
        - pending["authored_lessons"],
        "grade1_part2_remaining_available_bodies": pending[
            "native_body_heading_locators"
        ]
        - pending["authored_lessons"],
        "grade1_part2_missing_printed_pages": [68, 69],
        "grade1_part3_mapped_body_topics": len(third["topics"]),
        "grade1_part3_authored_lessons": third["authored_lessons"],
        "grade1_part3_schedule_only_rows_not_ready": len(
            third["scheduled_activities_without_body"]
        ),
        "blocked_sources": catalog["blocked_sources"],
        "full_curriculum_topic_count": None,
        "course_ready": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", required=True)
    args = parser.parse_args()
    print(json.dumps(audit(args.sources), ensure_ascii=False, indent=2))
