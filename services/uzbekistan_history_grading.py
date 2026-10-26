"""Bounded objective history grading; no fuzzy matching, dates inference or essay grading."""

import re
import unicodedata


def normalized_text(value):
    if type(value) is not str or len(value) > 120:
        raise ValueError("invalid_answer")
    value = unicodedata.normalize("NFKC", value).strip()
    if not value:
        raise ValueError("answer_required")
    value = value.translate(
        str.maketrans({"‘": "'", "’": "'", "ʻ": "'", "ʼ": "'", "`": "'"})
    )
    if any(not (c.isalpha() or c.isdecimal() or c in " '-.") for c in value):
        raise ValueError("invalid_answer")
    # Apostrophe is normalized, never removed: o‘ and o are different letters.
    return re.sub(r" +", " ", value.casefold()).rstrip(".").strip()


def grade_answer(spec, answer):
    if type(answer) is not dict:
        return "invalid_answer"
    kind = spec["kind"]
    if kind == "concept_selection":
        if (
            set(answer) != {"choice_id"}
            or type(answer["choice_id"]) is not str
            or answer["choice_id"] not in spec["choice_ids"]
        ):
            return "invalid_answer"
        return "correct" if answer["choice_id"] == spec["expected"] else "incorrect"
    if kind == "ordering":
        order = answer.get("order")
        if (
            set(answer) != {"order"}
            or type(order) is not list
            or any(type(v) is not str for v in order)
            or len(order) != len(spec["expected"])
            or len(set(order)) != len(order)
            or set(order) != set(spec["expected"])
        ):
            return "invalid_answer"
        return "correct" if order == spec["expected"] else "incorrect"
    if kind == "short_text":
        if set(answer) != {"value"}:
            return "invalid_answer"
        try:
            value = normalized_text(answer["value"])
        except ValueError as exc:
            return str(exc)
        return (
            "correct"
            if value in {normalized_text(a) for a in spec["aliases"]}
            else "incorrect"
        )
    return "invalid_answer"
