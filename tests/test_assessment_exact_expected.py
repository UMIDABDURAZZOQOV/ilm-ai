"""Exact server truth with learner-facing decimal rounding, without an API change."""

from copy import deepcopy
from fractions import Fraction

import pytest

from services.assessment_grading import AnswerError, expected_quantity, grade_answer

THIRD = {
    "kind": "numeric_quantity",
    "dimension": "dimensionless",
    "expected_si": "0.33",
    "expected_rational": {"numerator": "1", "denominator": "3"},
    "abs_tol_si": "0.005",
    "rel_tol": "0",
    "rounding_increment_si": "0.01",
}


def test_round_a_repeating_rational_without_moving_the_truth_to_rounded_decimal():
    assert expected_quantity(THIRD) == Fraction(1, 3)
    assert grade_answer(THIRD, {"value": "0.33", "unit": "1"}) == "correct"
    assert grade_answer(THIRD, {"value": "33", "unit": "%"}) == "correct"
    assert grade_answer(THIRD, {"value": "0.34", "unit": "1"}) == "out_of_tolerance"
    assert (
        grade_answer(THIRD, {"value": "0.333", "unit": "1"}) == "rounding_requirement"
    )
    assert grade_answer(THIRD, {"value": "1/3", "unit": "1"}) == "rounding_requirement"
    # The existing rounded decimal canonical solution is still usable by old internal tooling.
    assert (
        grade_answer(THIRD, {"value": THIRD["expected_si"], "unit": "1"}) == "correct"
    )


def test_existing_decimal_rubric_remains_exact_and_does_not_opt_in():
    legacy = deepcopy(THIRD)
    legacy.pop("expected_rational")
    legacy.pop("rounding_increment_si")
    legacy["abs_tol_si"] = "0"
    assert expected_quantity(legacy) == Fraction(33, 100)
    assert grade_answer(legacy, {"value": "0.33", "unit": "1"}) == "correct"
    assert grade_answer(legacy, {"value": "1/3", "unit": "1"}) == "out_of_tolerance"
    assert (
        grade_answer(legacy, {"value": "sqrt(0.1089)", "unit": "1"})
        == "invalid_expression"
    )


@pytest.mark.parametrize(
    "ratio",
    [
        None,
        [],
        {"numerator": "1"},
        {"numerator": "1", "denominator": "0"},
        {"numerator": "1", "denominator": "-3"},
        {"numerator": 1, "denominator": "3"},
        {"numerator": True, "denominator": "3"},
        {"numerator": "1.0", "denominator": "3"},
        {"numerator": "1e9", "denominator": "3"},
        {"numerator": "1", "denominator": "3", "code": "ignored"},
        {"numerator": "__import__('os')", "denominator": "3"},
        {"numerator": "1" * 129, "denominator": "3"},
    ],
)
def test_corrupt_or_unbounded_private_ratio_is_rejected(ratio):
    bad = {**THIRD, "expected_rational": ratio}
    with pytest.raises(AnswerError, match="invalid_expected_rational"):
        expected_quantity(bad)
    assert (
        grade_answer(bad, {"value": "0.33", "unit": "1"}) == "invalid_expected_rational"
    )
