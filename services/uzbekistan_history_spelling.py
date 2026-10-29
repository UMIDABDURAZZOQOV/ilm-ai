"""Source-reviewed orthographic alternatives for NEW attempts; frozen r1 stays intact."""

import json
from copy import deepcopy

from services.uzbekistan_history_grading import normalized_text
from services.uzbekistan_history_sources import DIRECTORY, digest, load_catalog, require


def load_reviews():
    document = json.loads((DIRECTORY / "spelling_reviews.json").read_text())
    require(document["schema_version"] == 1, "spelling_schema")
    return document["reviews"]


def compact(value):
    return normalized_text(value).replace(" ", "").replace("-", "")


def validate_reviews(documents, reviews=None):
    # Only whitespace/hyphen alternatives, never new people, years or fuzzy keys.
    reviews = load_reviews() if reviews is None else reviews
    lessons = {l["key"]: l for d in documents for l in d["lessons"]}
    books = {b["id"]: b for b in load_catalog()["books"]}
    seen = set()
    for review in reviews:
        require(review["assessment_key"] not in seen, "duplicate_spelling_review")
        seen.add(review["assessment_key"])
        lesson = lessons.get(review["lesson_key"])
        require(
            lesson is not None and digest(lesson) == review["lesson_content_sha256"],
            "spelling_base_content_changed",
        )
        q = next(
            (q for q in lesson["assessments"] if q["key"] == review["assessment_key"]),
            None,
        )
        require(
            q is not None and q["response_kind"] == "short_text",
            "spelling_question_kind",
        )
        require(
            review["verification"] == "original_image_checked_ocr_locator_only"
            and bool(review["review_note"]),
            "spelling_review_missing",
        )
        refs = review["source_refs"]
        require(
            refs and all(r in q["source_refs"] for r in refs),
            "spelling_source_not_question_source",
        )
        for ref in refs:
            book = books[ref["book_id"]]
            require(
                ref.get("page_image_sha256")
                == [book["pages"][p - 1]["image_sha256"] for p in ref["pdf_pages"]],
                "spelling_image_evidence",
            )
        aliases = review["aliases"]
        require(0 < len(aliases) <= 8, "spelling_alias_count")
        allowed = {compact(a) for a in q["grading_spec"]["aliases"]}
        require(
            all(
                compact(a) in allowed and not any(c.isdecimal() for c in a)
                for a in aliases
            ),
            "spelling_is_new_fact_not_orthography",
        )
    return reviews


def new_attempt_spec(lesson_key, content_sha, question_key, spec, source_refs):
    result = deepcopy(spec)
    if result["kind"] != "short_text":
        return result
    result["normalization_revision"] = 2
    matches = [r for r in load_reviews() if r["assessment_key"] == question_key]
    for review in matches:
        require(
            review["lesson_key"] == lesson_key
            and review["lesson_content_sha256"] == content_sha,
            "spelling_snapshot_content_conflict",
        )
        require(
            review["verification"] == "original_image_checked_ocr_locator_only"
            and bool(review["review_note"])
            and review["source_refs"]
            and all(ref in source_refs for ref in review["source_refs"]),
            "spelling_snapshot_source_not_reviewed",
        )
        allowed = {compact(a) for a in result["aliases"]}
        require(
            all(compact(a) in allowed for a in review["aliases"]),
            "spelling_snapshot_not_orthographic",
        )
        result["aliases"] = list(
            dict.fromkeys([*result["aliases"], *review["aliases"]])
        )
        result["spelling_review_sha256"] = digest(review)
    return result
