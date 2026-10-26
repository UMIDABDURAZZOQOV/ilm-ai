"""Bounded deterministic v2 grading. No eval, CAS, AI or client correctness flags.

Formula equivalence is an authored whitelist of closed ASTs, with commutative
sum/product normalization. It deliberately makes no general symbolic-proof claim.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from math import isqrt


class AnswerError(ValueError):
    pass


@dataclass(frozen=True)
class PositiveSquareRoot:
    """Private exact irrational quantity, represented by its rational square."""

    radicand: Fraction


def square_root_quantity(radicand):
    """No floating-point approximation or expression evaluation."""
    if (
        not isinstance(radicand, Fraction)
        or radicand < 0
        or radicand.numerator.bit_length() > 4096
        or radicand.denominator.bit_length() > 4096
    ):
        raise AnswerError("invalid_expected_root")
    top, bottom = isqrt(radicand.numerator), isqrt(radicand.denominator)
    if top * top == radicand.numerator and bottom * bottom == radicand.denominator:
        return Fraction(top, bottom)
    return PositiveSquareRoot(radicand)


def expected_quantity(spec):
    """Private optional exact ratio; legacy decimal rubrics retain their value.

    A repeating rational (for example M/(ZF)) must not be silently rounded
    before deciding the authored rounding interval. Neither field is public.
    """
    root_mode = "expected_root_rational" in spec
    if root_mode and "expected_rational" in spec:
        raise AnswerError("ambiguous_expected_quantity")
    if "expected_rational" not in spec and not root_mode:
        return Fraction(Decimal(spec["expected_si"]))
    error = "invalid_expected_root" if root_mode else "invalid_expected_rational"
    ratio = spec["expected_root_rational" if root_mode else "expected_rational"]
    if not isinstance(ratio, dict) or set(ratio) != {"numerator", "denominator"}:
        raise AnswerError(error)
    for value in ratio.values():
        if (
            not isinstance(value, str)
            or len(value) > 128
            or not re.fullmatch(r"[+-]?[0-9]+", value)
        ):
            raise AnswerError(error)
    numerator, denominator = int(ratio["numerator"]), int(ratio["denominator"])
    if denominator <= 0:
        raise AnswerError(error)
    result = Fraction(numerator, denominator)
    return square_root_quantity(result) if root_mode else result


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
    "g/m3": ("density", Fraction(1, 1000)),
    # Degrees are separate from radian magnitudes; no inexact pi conversion.
    "°": ("angle_degrees", Fraction(1)),
    "deg": ("angle_degrees", Fraction(1)),
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
    "MPa": ("pressure", Fraction(10**6)),
    "GPa": ("pressure", Fraction(10**9)),
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
    "Hz": ("frequency", Fraction(1)),
    # Grade7 PDF53: revolutions per second, distinct from rad/s.
    "1/s": ("frequency", Fraction(1)),
    "kHz": ("frequency", Fraction(1000)),
    "m/s2": ("acceleration", Fraction(1)),
    "cm/s2": ("acceleration", Fraction(1, 100)),
    "rad": ("angle", Fraction(1)),
    "rad/s": ("angular_speed", Fraction(1)),
    # Grade10 PDF12: angular acceleration, distinct from rad/s and Hz.
    "rad/s2": ("angular_acceleration", Fraction(1)),
    # Grade7 PDF84: spring stiffness and original SI-scaled answers.
    "N/m": ("stiffness", Fraction(1)),
    # Same physical force/length dimension: surface coefficient and energy/area.
    "mN/m": ("stiffness", Fraction(1, 1000)),
    "J/m2": ("stiffness", Fraction(1)),
    "mJ/m2": ("stiffness", Fraction(1, 1000)),
    "kN/m": ("stiffness", Fraction(1000)),
    # Grade7 PDF91: explicit supplied G, not dimensionless.
    "N*m2/kg2": ("gravitation_constant", Fraction(1)),
    "kg*m/s": ("momentum", Fraction(1)),
    "N*s": ("momentum", Fraction(1)),
    # Grade7 PDF141: megajoule is explicitly taught.
    "MJ": ("energy", Fraction(1000000)),
    # Grade7 PDF157: correct case-sensitive SI prefixes, not gW.
    "mW": ("power", Fraction(1, 1000)),
    "MW": ("power", Fraction(1000000)),
    "W*s": ("energy", Fraction(1)),
    # Grade8 PDF10–21: charge, Coulomb coefficient and electric field.
    "C": ("charge", Fraction(1)),
    "µC": ("charge", Fraction(1, 10**6)),
    "nC": ("charge", Fraction(1, 10**9)),
    "µN": ("force", Fraction(1, 10**6)),
    "nN": ("force", Fraction(1, 10**9)),
    "pN": ("force", Fraction(1, 10**12)),
    "N*m2/C2": ("coulomb_constant", Fraction(1)),
    "N/C": ("electric_field", Fraction(1)),
    # Grade8 PDF42/48/51: current, resistance, resistivity and square millimetres.
    "A": ("current", Fraction(1)),
    "mA": ("current", Fraction(1, 1000)),
    "µA": ("current", Fraction(1, 10**6)),
    "Ω": ("resistance", Fraction(1)),
    "mΩ": ("resistance", Fraction(1, 1000)),
    "kΩ": ("resistance", Fraction(1000)),
    "MΩ": ("resistance", Fraction(10**6)),
    "Ω*m": ("resistivity", Fraction(1)),
    "mm2": ("area", Fraction(1, 10**6)),
    # Grade8 PDF79: capacitance and explicit permittivity constant.
    "F": ("capacitance", Fraction(1)),
    "µF": ("capacitance", Fraction(1, 10**6)),
    "nF": ("capacitance", Fraction(1, 10**9)),
    "pF": ("capacitance", Fraction(1, 10**12)),
    "F/m": ("permittivity", Fraction(1)),
    # Grade8 PDF91–92: power and metered energy; prefixes remain case-sensitive.
    "hW": ("power", Fraction(100)),
    "Wh": ("energy", Fraction(3600)),
    "kWh": ("energy", Fraction(3600000)),
    "hWh": ("energy", Fraction(360000)),
    "MWh": ("energy", Fraction(3600000000)),
    "GJ": ("energy", Fraction(1000000000)),
    # Grade8 PDF121/123/124: molar quantities, not dimensionless atomic weights.
    "kg/C": ("electrochemical_equivalent", Fraction(1)),
    "mg/C": ("electrochemical_equivalent", Fraction(1, 10**6)),
    "kg/mol": ("molar_mass", Fraction(1)),
    "g/mol": ("molar_mass", Fraction(1, 1000)),
    "C/mol": ("faraday_constant", Fraction(1)),
    "mol": ("amount", Fraction(1)),
    # Grade9 PDF8/12/14: volume, inverse-mol constant and NUMBER concentration.
    "mm3": ("volume", Fraction(1, 10**9)),
    "1/mol": ("avogadro_constant", Fraction(1)),
    "1/m3": ("number_density", Fraction(1)),
    # Separate labelled scales: Celsius givens never silently become kelvins.
    "K": ("temperature", Fraction(1)),
    "°C": ("celsius_reading", Fraction(1)),
    "J/K": ("boltzmann_constant", Fraction(1)),
    "J/(mol*K)": ("gas_constant", Fraction(1)),
    "J/(kg*K)": ("specific_heat", Fraction(1)),
    "kJ/(kg*K)": ("specific_heat", Fraction(1000)),
    "J/kg": ("specific_energy", Fraction(1)),
    "kJ/kg": ("specific_energy", Fraction(1000)),
    "MJ/kg": ("specific_energy", Fraction(10**6)),
    # Grade8 PDF150/152: magnetic induction (not temperature).
    "T": ("magnetic_induction", Fraction(1)),
    "mT": ("magnetic_induction", Fraction(1, 1000)),
    "µT": ("magnetic_induction", Fraction(1, 10**6)),
}
UNIT_ALIASES = {
    "J/(kg·K)": "J/(kg*K)",
    "J/(kg K)": "J/(kg*K)",
    "J/(kg*°C)": "J/(kg*K)",
    "J/(kg·°C)": "J/(kg*K)",
    "mol^-1": "1/mol",
    "mol⁻¹": "1/mol",
    "m^-3": "1/m3",
    "m⁻³": "1/m3",
    "m⁻3": "1/m3",
    "μT": "µT",
    "uT": "µT",
    "ohm": "Ω",
    "kohm": "kΩ",
    "ohm*m": "Ω*m",
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
    "μC": "µC",
    "uC": "µC",
    "μN": "µN",
    "uN": "µN",
    "μA": "µA",
    "uA": "µA",
    "μF": "µF",
    "uF": "µF",
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


def exact_square_root(value):
    """Exact rational roots only; irrational rounding is not silently guessed."""
    if value < 0:
        raise AnswerError("domain_error")
    top, bottom = isqrt(value.numerator), isqrt(value.denominator)
    if top * top != value.numerator or bottom * bottom != value.denominator:
        raise AnswerError("domain_error")
    return bounded(Fraction(top, bottom))


def numeric(text, *, allow_square_root=False):
    text, root = tree(text)

    def visit(node, depth=0):
        if depth > 12:
            raise AnswerError("invalid_expression")
        if isinstance(node, ast.Constant):
            return literal(node, text)
        if (
            allow_square_root
            and isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "sqrt"
            and len(node.args) == 1
            and not node.keywords
        ):
            return exact_square_root(visit(node.args[0], depth + 1))
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
                if allow_square_root and right == Fraction(1, 2):
                    return exact_square_root(left)
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
        if (
            spec.get("allow_square_root") is True
            and isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "sqrt"
            and len(node.args) == 1
            and not node.keywords
        ):
            return ("power", visit(node.args[0], depth + 1), ("number", "1/2"))
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
            if spec.get("allow_square_root") is True:
                try:
                    exponent = numeric(ast.get_source_segment(text, node.right))
                except AnswerError:
                    raise AnswerError("domain_error") from None
                if exponent == Fraction(1, 2):
                    return ("power", left, ("number", "1/2"))
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
        value = numeric(
            answer["value"],
            allow_square_root=(spec.get("formula") or {}).get("allow_square_root")
            is True,
        )
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
        expected = expected_quantity(spec)
        if "expected_root_rational" in spec:
            # New authored roots require explicit nearest-grid rounding. Do not
            # substitute an approximate decimal as the grading truth. A rational
            # learner answer a is valid iff sqrt(r) lies inside [a-h, a+h].
            try:
                grid = numeric(spec["rounding_increment_si"])
                tolerance = numeric(spec["abs_tol_si"])
                relative = numeric(spec["rel_tol"])
                if grid <= 0 or tolerance != grid / 2 or relative != 0:
                    raise AnswerError("invalid_root_rounding")
            except (KeyError, ValueError, InvalidOperation, ZeroDivisionError):
                raise AnswerError("invalid_root_rounding") from None
        else:
            tolerance = max(
                Fraction(Decimal(spec["abs_tol_si"])),
                abs(expected) * Fraction(Decimal(spec["rel_tol"])),
            )
        if spec.get("rounding_increment_si"):
            if "expected_root_rational" not in spec:
                grid = Fraction(Decimal(spec["rounding_increment_si"]))
            if (actual_si / grid).denominator != 1:
                return "rounding_requirement"
        if isinstance(expected, PositiveSquareRoot):
            if actual_si < 0:
                return "sign_error"
            lower, upper = max(Fraction(), actual_si - tolerance), actual_si + tolerance
            return (
                "correct"
                if lower * lower <= expected.radicand <= upper * upper
                else "out_of_tolerance"
            )
        if abs(actual_si - expected) > tolerance:
            return (
                "sign_error"
                if actual_si == -expected and expected
                else "out_of_tolerance"
            )
        return "correct"
    except AnswerError as exc:
        return str(exc)
