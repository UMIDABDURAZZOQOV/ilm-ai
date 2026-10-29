"""Bounded objective history grading; no fuzzy matching, dates inference or essay grading."""

import re
import unicodedata

ROMAN = {
    tens + ones: 10 * t + o
    for t, tens in enumerate(["", "x", "xx", "xxx", "xl", "l", "lx", "lxx", "lxxx", "xc"])
    for o, ones in enumerate(["", "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix"])
    if t or o
}


def century_value(text, *, require_unit=False):
    """Bounded century notation, never dates, arithmetic or inferred history."""
    suffix = r"\s*-?\s*asr" if require_unit else r"(?:\s*-?\s*asr)?"
    match = re.fullmatch(r"([0-9]{1,2}|[ivxlcdm]+)" + suffix, text)
    if not match:
        return None
    token = match[1]
    value = int(token) if token.isascii() and token.isdecimal() else ROMAN.get(token)
    return value if value is not None and 1 <= value <= 99 else None


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
        revision = spec.get("normalization_revision", 1)
        if type(revision) is not int or revision not in {1, 2}:
            return "invalid_answer"
        aliases = {normalized_text(a) for a in spec["aliases"]}
        if value in aliases:
            return "correct"
        if revision == 2:
            # Only source-approved aliases explicitly naming the same century
            # enable bare Arabic/Roman notation. Names and years stay exact.
            values = {century_value(a, require_unit=True) for a in aliases}
            if len(values) == 1 and None not in values and century_value(value) in values:
                return "correct"
        return "incorrect"
    return "invalid_answer"
