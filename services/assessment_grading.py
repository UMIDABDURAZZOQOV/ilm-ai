"""Bounded deterministic v2 grading. No eval, CAS, AI or client correctness flags.

Formula equivalence is an authored whitelist of closed ASTs, with commutative
sum/product normalization. It deliberately makes no general symbolic-proof claim.
"""

from __future__ import annotations

import ast
import re
from decimal import Decimal, InvalidOperation
from fractions import Fraction


class AnswerError(ValueError):
    pass


# Explicit registry, not a permissive expression parser. Source: grade 6
# PDF12–14 (length/time), PDF21 (film V/S), PDF28 (front h/t),
# PDF29–35 (mass, volume and density), PDF37–38 (laboratory volumes).
UNITS = {
    "m": ("length", Fraction(1)),
    "cm": ("length", Fraction(1, 100)),
    "mm": ("length", Fraction(1, 1000)),
    "dm": ("length", Fraction(1, 10)),
    "km": ("length", Fraction(1000)),
    "µm": ("length", Fraction(1, 10**6)),
    "nm": ("length", Fraction(1, 10**9)),
    "s": ("time", Fraction(1)),
    "kg": ("mass", Fraction(1)),
    "g": ("mass", Fraction(1, 1000)),
    "mg": ("mass", Fraction(1, 10**6)),
    "t": ("mass", Fraction(1000)),
    "m2": ("area", Fraction(1)),
    "cm2": ("area", Fraction(1, 10**4)),
    "m3": ("volume", Fraction(1)),
    "dm3": ("volume", Fraction(1, 1000)),
    "cm3": ("volume", Fraction(1, 10**6)),
    "L": ("volume", Fraction(1, 1000)),
    "mL": ("volume", Fraction(1, 10**6)),
    "kg/m3": ("density", Fraction(1)),
    "g/cm3": ("density", Fraction(1000)),
    "m/s": ("speed", Fraction(1)),
    "mm/s": ("speed", Fraction(1, 1000)),
    "cm/s": ("speed", Fraction(1, 100)),
    "min": ("time", Fraction(60)),
    "h": ("time", Fraction(3600)),
    "km/h": ("speed", Fraction(5, 18)),
    "km/s": ("speed", Fraction(1000)),
    "N": ("force", Fraction(1)),
    "kN": ("force", Fraction(1000)),
    "mN": ("force", Fraction(1, 1000)),
    "N/kg": ("force_per_mass", Fraction(1)),
    "Pa": ("pressure", Fraction(1)),
    "kPa": ("pressure", Fraction(1000)),
    "N/m2": ("pressure", Fraction(1)),
    "1": ("dimensionless", Fraction(1)),
    "atm": ("pressure", Fraction(101325)),
    "J": ("energy", Fraction(1)),
    "kJ": ("energy", Fraction(1000)),
    "mJ": ("energy", Fraction(1, 1000)),
    "W": ("power", Fraction(1)),
    "kW": ("power", Fraction(1000)),
    "N*m": ("torque", Fraction(1)),
    "%": ("dimensionless", Fraction(1, 100)),
    # Grade6 PDF123–126: voltage and milli-/kilovolt notation. Case matters.
    "V": ("voltage", Fraction(1)),
    "mV": ("voltage", Fraction(1, 1000)),
    "kV": ("voltage", Fraction(1000)),
    # Grade6 PDF147: lens optical power1/F with F in metres.
    "dptr": ("optical_power", Fraction(1)),
    "1/m": ("optical_power", Fraction(1)),
}
UNIT_ALIASES = {
    "metr": "m",
    "santimetr": "cm",
    "sm": "cm",
    "millimetr": "mm",
    "detsimetr": "dm",
    "kilometr": "km",
    "μm": "µm",
    "um": "µm",
    "mikrometr": "µm",
    "nanometr": "nm",
    "sekund": "s",
    "kilogramm": "kg",
    "gramm": "g",
    "milligramm": "mg",
    "tonna": "t",
    "l": "L",
    "litr": "L",
    "ml": "mL",
    "sm3": "cm3",
    "g/sm3": "g/cm3",
    "soat": "h",
    "minut": "min",
    "km/soat": "km/h",
    "nyuton": "N",
    "paskal": "Pa",
    "joul": "J",
    "vatt": "W",
    "N·m": "N*m",
    "N m": "N*m",
    "foiz": "%",
}
TOKEN = re.compile(
    r"\s*(?:\d+(?:\.\d*)?(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?|"
    r"[A-Za-z][A-Za-z0-9_]*|\*\*|[()+*/^\-])"
)


def normalized(text):
    if not isinstance(text, str) or not text.strip() or len(text) > 128:
        raise AnswerError("invalid_expression")
    text = text.strip().translate(
        str.maketrans({"−": "-", "–": "-", "×": "*", "·": "*"})
    )
    if "," in text:
        if text.count(",") != 1 or "." in text or not re.search(r"\d,\d", text):
            raise AnswerError("invalid_expression")
        text = text.replace(",", ".")
    # Superscripts/implicit multiplication are not guessed; the UI supplies ^ and *.
    text = text.replace("^", "**")
    cursor, tokens = 0, 0
    while cursor < len(text):
        match = TOKEN.match(text, cursor)
        if not match:
            raise AnswerError("invalid_expression")
        cursor = match.end()
        tokens += 1
        if tokens > 64:
            raise AnswerError("invalid_expression")
    return text


def bounded(value):
    if value.numerator.bit_length() > 512 or value.denominator.bit_length() > 512:
        raise AnswerError("invalid_expression")
    return value


def tree(text):
    text = normalized(text)
    try:
        root = ast.parse(text, mode="eval").body
    except (SyntaxError, ValueError, RecursionError):
        raise AnswerError("invalid_expression") from None
    if sum(1 for _ in ast.walk(root)) > 100:
        raise AnswerError("invalid_expression")
    return text, root


def literal(node, text):
    if type(node.value) not in (int, float):
        raise AnswerError("invalid_expression")
    token = ast.get_source_segment(text, node)
    try:
        value = Decimal(token)
        if (
            not value.is_finite()
            or abs(value.adjusted()) > 100
            or len(value.as_tuple().digits) > 40
        ):
            raise AnswerError("invalid_expression")
        return bounded(Fraction(value))
    except (InvalidOperation, TypeError, ValueError):
        raise AnswerError("invalid_expression") from None


def numeric(text):
    text, root = tree(text)

    def visit(node, depth=0):
        if depth > 12:
            raise AnswerError("invalid_expression")
        if isinstance(node, ast.Constant):
            return literal(node, text)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = visit(node.operand, depth + 1)
            return -value if isinstance(node.op, ast.USub) else value
        if isinstance(node, ast.BinOp) and isinstance(
            node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow)
        ):
            left, right = visit(node.left, depth + 1), visit(node.right, depth + 1)
            if isinstance(node.op, ast.Add):
                result = left + right
            elif isinstance(node.op, ast.Sub):
                result = left - right
            elif isinstance(node.op, ast.Mult):
                result = left * right
            elif isinstance(node.op, ast.Div):
                if right == 0:
                    raise AnswerError("domain_error")
                result = left / right
            else:
                if (
                    right.denominator != 1
                    or abs(right) > 12
                    or (left == 0 and right < 0)
                ):
                    raise AnswerError("domain_error")
                result = left ** int(right)
            return bounded(result)
        raise AnswerError("invalid_expression")

    return visit(root)


def formula_ast(text, spec):
    if not isinstance(text, str) or len(text) > 128:
        raise AnswerError("invalid_expression")
    if "=" in text:
        if text.count("=") != 1:
            raise AnswerError("invalid_expression")
        target, text = text.split("=")
        if target.strip() != spec["target"]:
            raise AnswerError("wrong_formula")
    text, root = tree(text)
    allowed = set(spec["variables"])

    def visit(node, depth=0):
        if depth > 12:
            raise AnswerError("invalid_expression")
        if isinstance(node, ast.Constant):
            value = literal(node, text)
            return ("number", str(value))
        if isinstance(node, ast.Name):
            if node.id not in allowed:
                raise AnswerError("unknown_symbol")
            return ("symbol", node.id)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = visit(node.operand, depth + 1)
            if value[0] == "number":
                number = Fraction(value[1])
                return (
                    "number",
                    str(-number if isinstance(node.op, ast.USub) else number),
                )
            return ("negate", value) if isinstance(node.op, ast.USub) else value
        if isinstance(node, ast.BinOp) and isinstance(
            node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow)
        ):
            left, right = visit(node.left, depth + 1), visit(node.right, depth + 1)
            if isinstance(node.op, (ast.Add, ast.Mult)):
                kind = "sum" if isinstance(node.op, ast.Add) else "product"
                children = []
                for part in (left, right):
                    children.extend(part[1] if part[0] == kind else [part])
                return (kind, tuple(sorted(children, key=repr)))
            if isinstance(node.op, ast.Sub):
                return ("subtract", left, right)
            if isinstance(node.op, ast.Div):
                if right == ("number", "0"):
                    raise AnswerError("domain_error")
                return ("divide", left, right)
            if (
                right[0] != "number"
                or Fraction(right[1]).denominator != 1
                or abs(Fraction(right[1])) > 12
            ):
                raise AnswerError("domain_error")
            return ("power", left, right)
        raise AnswerError("invalid_expression")

    return visit(root)


def grade_answer(spec, answer):
    """Return a code only; private expected values/rubric never enter API payloads."""
    kind = spec["kind"]
    fields = {k for k, v in answer.items() if v is not None}
    if kind == "concept_selection":
        if fields != {"choice_id"} or answer["choice_id"] not in spec["choice_ids"]:
            return "invalid_answer"
        return (
            "correct"
            if answer["choice_id"] == spec["expected_choice"]
            else "incorrect_concept"
        )
    if kind == "ordering":
        if fields != {"order"} or not isinstance(answer["order"], list):
            return "invalid_answer"
        actual = answer["order"]
        if len(actual) != len(set(actual)) or set(actual) != set(
            spec["expected_order"]
        ):
            return "invalid_answer"
        return "correct" if actual == spec["expected_order"] else "incorrect_order"
    required = {"value", "unit"} | ({"formula"} if spec.get("formula") else set())
    if fields != required:
        return "answer_required"
    try:
        value = numeric(answer["value"])
        # Accept explicit typed exponent variants, preserving SI case. Never
        # infer an omitted exponent (cm and cm3 are different dimensions).
        unit = answer["unit"].strip().replace("²", "2").replace("³", "3")
        unit = unit.replace("^2", "2").replace("^3", "3")
        unit = UNIT_ALIASES.get(unit, unit)
        if unit not in UNITS:
            return "unknown_unit"
        dimension, factor = UNITS[unit]
        if dimension != spec["dimension"]:
            return "dimension_mismatch"
        if spec.get("formula"):
            actual = formula_ast(answer["formula"], spec["formula"])
            equivalents = [
                formula_ast(v, spec["formula"]) for v in spec["formula"]["equivalents"]
            ]
            if actual not in equivalents:
                return "wrong_formula"
        actual_si = value * factor
        expected = Fraction(Decimal(spec["expected_si"]))
        tolerance = max(
            Fraction(Decimal(spec["abs_tol_si"])),
            abs(expected) * Fraction(Decimal(spec["rel_tol"])),
        )
        if spec.get("rounding_increment_si"):
            grid = Fraction(Decimal(spec["rounding_increment_si"]))
            if (actual_si / grid).denominator != 1:
                return "rounding_requirement"
        if abs(actual_si - expected) > tolerance:
            return (
                "sign_error"
                if actual_si == -expected and expected
                else "out_of_tolerance"
            )
        return "correct"
    except AnswerError as exc:
        return str(exc)
