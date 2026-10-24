"""Bounded deterministic concept grading for the first source-reviewed batch.

Chemical formula/equation/numeric tasks are not silently treated as prose.
Their parsers are added only with reviewed topic-specific rules and tests.
"""
import re
import unicodedata
from decimal import Decimal, InvalidOperation


def normalized_number(value):
    """Bounded decimal input, including comma decimals and e notation. No eval."""
    if type(value) is not str or len(value) > 80:
        raise ValueError('invalid_answer')
    value = value.strip().replace('\u2212', '-')
    if not value:
        raise ValueError('answer_required')
    if not re.fullmatch(r'[+-]?(?:[0-9]{1,50}(?:[.,][0-9]{1,50})?|[.,][0-9]{1,50})(?:[eE][+-]?[0-9]{1,2})?', value):
        raise ValueError('invalid_answer')
    try:
        number = Decimal(value.replace(',', '.'))
    except InvalidOperation:
        raise ValueError('invalid_answer') from None
    if not number.is_finite() or abs(number.adjusted()) > 50:
        raise ValueError('invalid_answer')
    return number


def canonical_number(value):
    number = normalized_number(value)
    if number == 0:
        return '0'
    # Decimal.normalize() uses the ambient precision and can round distinct
    # incorrect answers into one fingerprint. Fixed formatting is exact here.
    text = format(number, 'f')
    return text.rstrip('0').rstrip('.') if '.' in text else text


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
    if kind == 'numeric_value':
        if set(answer) != {'value'}:
            return 'invalid_answer'
        try:
            value = normalized_number(answer['value'])
        except ValueError as exc:
            return str(exc)
        # The reviewed task fixes the unit in its prompt. Arbitrary units and
        # expressions cannot be appended or converted silently.
        return 'correct' if value == normalized_number(spec['expected']) else 'incorrect'
    if kind in {'chemical_formula', 'chemical_equation'}:
        if set(answer) != {'value'}:
            return 'invalid_answer'
        from services.chemistry_notation import formula, equation
        try:
            if kind == 'chemical_formula':
                value, _ = formula(answer['value'])
                approved = [spec['expected'], *spec.get('aliases', [])]
                return 'correct' if value in {formula(a)[0] for a in approved} else 'incorrect'
            sides, atoms, canonical = equation(answer['value'])
        except ValueError as exc:
            return str(exc)
        expected_sides, _, expected = equation(spec['expected'])
        if any(set(a) != set(b) for a,b in zip(sides, expected_sides)):
            return 'incorrect_species'
        if atoms[0] != atoms[1]:
            return 'atom_imbalance'
        return 'correct' if canonical == expected else 'incorrect_ratio'
    return "invalid_answer"
