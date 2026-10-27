"""Bounded exact arithmetic and explicit elementary concepts, server-only.

This is not a general symbolic algebra engine. Unsupported expression families
are rejected, never accepted from a handful of numeric samples. No eval/exec,
Python AST execution, sympify, arbitrary identifiers, calls or floating point.
"""

import re
import unicodedata
from fractions import Fraction


class MathInputError(ValueError):
    pass


def text_answer(value):
    if type(value) is not str or not 0 < len(value) <= 80:
        raise MathInputError("invalid_answer")
    value = unicodedata.normalize("NFKC", value).strip().casefold()
    value = value.translate(str.maketrans({c: "'" for c in "‘’ʻʼ`"}))
    if not value or any(not (c.isalpha() or c in " '-") for c in value):
        raise MathInputError("invalid_answer")
    return " ".join(value.split())


def exact_number(value):
    """Closed recursive-descent arithmetic. <=80 tokens, depth12, 256-bit ratios.

    Decimal comma is a decimal separator, never a tuple or thousands separator.
    Powers/functions/implicit multiplication/variables deliberately unsupported.
    Mixed fraction notation will require a separately versioned grammar.
    """
    if type(value) is not str or not 0 < len(value) <= 160:
        raise MathInputError("invalid_expression")
    value = value.translate(str.maketrans({"−": "-", "×": "*", "÷": "/", ",": "."}))
    if re.search(r"[^0-9.()+*/\-\s]", value):
        raise MathInputError("invalid_expression")
    tokens = re.findall(r"[0-9]+(?:\.[0-9]+)?|[()+*/-]", value)
    if not tokens or len(tokens) > 80 or "".join(tokens) != re.sub(r"\s", "", value):
        raise MathInputError("invalid_expression")
    index = 0

    def bounded(number):
        if (
            max(abs(number.numerator).bit_length(), number.denominator.bit_length())
            > 256
        ):
            raise MathInputError("expression_too_complex")
        return number

    def expression(depth):
        nonlocal index
        result = term(depth)
        while index < len(tokens) and tokens[index] in {"+", "-"}:
            operator = tokens[index]
            index += 1
            right = term(depth)
            result = bounded(result + right if operator == "+" else result - right)
        return result

    def term(depth):
        nonlocal index
        result = atom(depth)
        while index < len(tokens) and tokens[index] in {"*", "/"}:
            operator = tokens[index]
            index += 1
            right = atom(depth)
            if operator == "/" and right == 0:
                raise MathInputError("division_by_zero")
            result = bounded(result * right if operator == "*" else result / right)
        return result

    def atom(depth):
        nonlocal index
        if depth > 12 or index == len(tokens):
            raise MathInputError("invalid_expression")
        token = tokens[index]
        index += 1
        if token in {"+", "-"}:
            result = atom(depth + 1)
            return result if token == "+" else -result
        if token == "(":
            result = expression(depth + 1)
            if index == len(tokens) or tokens[index] != ")":
                raise MathInputError("invalid_expression")
            index += 1
            return result
        if not re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", token) or len(token) > 40:
            raise MathInputError("invalid_expression")
        return bounded(Fraction(token))

    result = expression(0)
    if index != len(tokens):
        raise MathInputError("invalid_expression")
    return result


def grade_answer(spec, answer):
    """Return code only. Keys and feedback remain in the immutable server snapshot."""
    if type(answer) is not dict:
        raise MathInputError("invalid_answer")
    if spec["kind"] == "choice":
        if set(answer) != {"choice_id"} or type(answer["choice_id"]) is not str:
            raise MathInputError("invalid_answer")
        if answer["choice_id"] not in spec["choice_ids"]:
            raise MathInputError("invalid_answer")
        return "correct" if answer["choice_id"] == spec["expected"] else "incorrect"
    if set(answer) != {"value"}:
        raise MathInputError("invalid_answer")
    if spec["kind"] == "short_text":
        actual = text_answer(answer["value"])
        expected = {text_answer(a) for a in spec["aliases"]}
        return "correct" if actual in expected else "incorrect"
    if spec["kind"] == "exact_number":
        return (
            "correct"
            if exact_number(answer["value"]) == Fraction(spec["expected"])
            else "incorrect"
        )
    raise MathInputError("unsupported_response_kind")
