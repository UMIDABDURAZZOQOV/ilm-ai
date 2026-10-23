"""Bounded deterministic concept grading for the first source-reviewed batch.

Chemical formula/equation/numeric tasks are not silently treated as prose.
Their parsers are added only with reviewed topic-specific rules and tests.
"""
import re
import unicodedata


def normalized_text(value):
    if type(value) is not str or len(value) > 80:
        raise ValueError("invalid_answer")
    value = unicodedata.normalize("NFKC", value).strip()
    if not value:
        raise ValueError("answer_required")
    value = value.translate(str.maketrans({"‘": "'", "’": "'", "ʻ": "'", "ʼ": "'"}))
    if any(not (ch.isalpha() or ch in " '-.") for ch in value):
        raise ValueError("invalid_answer")
    return re.sub(r" +", " ", value.casefold()).rstrip(".").strip()


def grade_answer(spec, answer):
    if type(answer) is not dict:
        return "invalid_answer"
    kind = spec["kind"]
    if kind == "concept_selection":
        if set(answer) != {"choice_id"} or type(answer["choice_id"]) is not str:
            return "invalid_answer"
        choice = answer["choice_id"]
        if choice not in spec["choice_ids"]:
            return "invalid_answer"
        return "correct" if choice == spec["expected"] else "incorrect"
    if kind == "short_text":
        if set(answer) != {"value"}:
            return "invalid_answer"
        try:
            value = normalized_text(answer["value"])
        except ValueError as exc:
            return str(exc)
        aliases = {normalized_text(a) for a in spec["aliases"]}
        return "correct" if value in aliases else "incorrect"
    return "invalid_answer"
