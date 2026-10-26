"""Exact square-interval rounding truth without float/CAS or answer-key leakage."""

from copy import deepcopy
from decimal import Decimal, localcontext
from fractions import Fraction

import pytest

from services.assessment_grading import (
    AnswerError,
    PositiveSquareRoot,
    expected_quantity,
    grade_answer,
    square_root_quantity,
)

ROOT = {
    "kind": "numeric_quantity",
    "dimension": "speed",
    "expected_si": "1.41",
    "expected_root_rational": {"numerator": "2", "denominator": "1"},
    "rounding_increment_si": "0.01",
    "abs_tol_si": "0.005",
    "rel_tol": "0",
}


def test_truth_is_exact_root_and_not_the_rounded_canonical_decimal():
    assert expected_quantity(ROOT) == PositiveSquareRoot(Fraction(2))
    assert grade_answer(ROOT, {"value": "1.41", "unit": "m/s"}) == "correct"
    assert grade_answer(ROOT, {"value": "5.076", "unit": "km/h"}) == "correct"
    assert grade_answer(ROOT, {"value": "1.42", "unit": "m/s"}) == "out_of_tolerance"
    assert (
        grade_answer(ROOT, {"value": "1.414", "unit": "m/s"}) == "rounding_requirement"
    )
    assert grade_answer(ROOT, {"value": "-1.41", "unit": "m/s"}) == "sign_error"
    assert grade_answer(ROOT, {"value": "1.41", "unit": "kg"}) == "dimension_mismatch"
    assert (
        grade_answer(ROOT, {"value": "sqrt(2)", "unit": "m/s"}) == "invalid_expression"
    )
    # Changing the display fallback never changes the mathematical truth.
    changed = {**ROOT, "expected_si": "123"}
    assert grade_answer(changed, {"value": "1.41", "unit": "m/s"}) == "correct"
    assert grade_answer(changed, {"value": "123", "unit": "m/s"}) == "out_of_tolerance"


@pytest.mark.parametrize(
    "num,denom,grid,candidates",
    [
        (2, 1, "0.01", ["1.40", "1.41", "1.42"]),
        (249300, 1, "0.1", ["499.2", "499.3", "499.4"]),
        (23371875, 100, "0.1", ["483.3", "483.4", "483.5"]),
        (1, 3, "0.001", ["0.576", "0.577", "0.578"]),
        (99999, 100000, "0.01", ["0.99", "1", "1.01"]),
    ],
)
def test_independent_high_precision_decimal_reference(num, denom, grid, candidates):
    spec = {
        **ROOT,
        "expected_root_rational": {"numerator": str(num), "denominator": str(denom)},
        "rounding_increment_si": grid,
        "abs_tol_si": str(Decimal(grid) / 2),
    }
    with localcontext() as ctx:
        ctx.prec = 90
        truth = (Decimal(num) / Decimal(denom)).sqrt()
        for a in candidates:
            expected = abs(Decimal(a) - truth) <= Decimal(grid) / 2
            assert (
                grade_answer(spec, {"value": a, "unit": "m/s"}) == "correct"
            ) is expected


def test_root_canonicalizes_perfect_rational_and_zero_without_general_cas():
    assert square_root_quantity(Fraction(81, 16)) == Fraction(9, 4)
    assert square_root_quantity(Fraction()) == Fraction()
    assert square_root_quantity(Fraction(8)) == PositiveSquareRoot(Fraction(8))
    perfect = {
        **ROOT,
        "expected_root_rational": {"numerator": "81", "denominator": "16"},
    }
    assert grade_answer(perfect, {"value": "2.25", "unit": "m/s"}) == "correct"


@pytest.mark.parametrize(
    "ratio",
    [
        None,
        [],
        {"numerator": "2"},
        {"numerator": "2", "denominator": "0"},
        {"numerator": "2", "denominator": "-1"},
        {"numerator": "-2", "denominator": "1"},
        {"numerator": True, "denominator": "1"},
        {"numerator": "2.0", "denominator": "1"},
        {"numerator": "sqrt(2)", "denominator": "1"},
        {"numerator": "2", "denominator": "1", "extra": "no"},
        {"numerator": "1" * 129, "denominator": "1"},
    ],
)
def test_corrupt_unbounded_or_negative_private_root_rejected(ratio):
    spec = {**ROOT, "expected_root_rational": ratio}
    with pytest.raises(AnswerError, match="invalid_expected_root"):
        expected_quantity(spec)
    assert (
        grade_answer(spec, {"value": "1.41", "unit": "m/s"}) == "invalid_expected_root"
    )


@pytest.mark.parametrize(
    "updates",
    [
        {"rel_tol": "0.01"},
        {"abs_tol_si": "0.006"},
        {"rounding_increment_si": "0"},
        {"rounding_increment_si": "-1"},
        {"rounding_increment_si": "NaN"},
        {"rounding_increment_si": "1e1000000"},
        {"rounding_increment_si": None},
    ],
)
def test_new_root_requires_bounded_nearest_grid_policy(updates):
    spec = {**ROOT, **updates}
    assert (
        grade_answer(spec, {"value": "1.41", "unit": "m/s"}) == "invalid_root_rounding"
    )


def test_missing_grid_ambiguous_truth_and_client_key_injection_rejected():
    spec = deepcopy(ROOT)
    spec.pop("rounding_increment_si")
    assert (
        grade_answer(spec, {"value": "1.41", "unit": "m/s"}) == "invalid_root_rounding"
    )
    spec = {**ROOT, "expected_rational": {"numerator": "141", "denominator": "100"}}
    with pytest.raises(AnswerError, match="ambiguous_expected_quantity"):
        expected_quantity(spec)
    assert (
        grade_answer(spec, {"value": "1.41", "unit": "m/s"})
        == "ambiguous_expected_quantity"
    )
    assert (
        grade_answer(
            ROOT,
            {
                "value": "1.41",
                "unit": "m/s",
                "expected_root_rational": {"numerator": "1", "denominator": "1"},
            },
        )
        == "answer_required"
    )


def test_extreme_radicand_exact_integer_interval_has_no_float_overflow():
    spec = {
        **ROOT,
        "expected_root_rational": {"numerator": str(10**100 + 1), "denominator": "1"},
        "rounding_increment_si": "1",
        "abs_tol_si": "0.5",
    }
    assert grade_answer(spec, {"value": "1e50", "unit": "m/s"}) == "correct"
    assert grade_answer(spec, {"value": "1e50+1", "unit": "m/s"}) == "out_of_tolerance"
    with pytest.raises(AnswerError):
        square_root_quantity(Fraction(1 << 5000))
