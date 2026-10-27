"""Literal independent arithmetic oracles and bounded-input rejection."""

from fractions import Fraction

import pytest

from services.mathematics_grading import (
    MathInputError,
    exact_number,
    grade_answer,
    text_answer,
)


@pytest.mark.parametrize(
    "value,expected",
    [
        ("1/2", Fraction(1, 2)),
        ("2/4", Fraction(1, 2)),
        ("0,5", Fraction(1, 2)),
        ("0.5", Fraction(1, 2)),
        ("2+3*4", 14),
        ("(2+3)*4", 20),
        ("−3/(-6)", Fraction(1, 2)),
        ("8÷4×2", 4),
        ("1-2-3", -4),
        ("-(-3)", 3),
    ],
)
def test_exact_arithmetic(value, expected):
    assert exact_number(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "",
        " ",
        "1/0",
        "2/(3-3)",
        "1e999",
        "9**9999999",
        "x",
        "sqrt(4)",
        "__import__('os')",
        "[1]",
        "1;2",
        "1=1",
        "1 2",
        "1..2",
        "(1",
        "1)",
        "1/2/",
        "0x10",
        "True",
        "∞",
        "2^3",
        "2(3)",
        "9" * 41,
        "(" * 13 + "1" + ")" * 13,
        "1+" * 41 + "1",
    ],
)
def test_unsupported_and_unsafe_input_is_rejected(value):
    with pytest.raises(MathInputError):
        exact_number(value)


def test_no_float_tolerance_or_fuzzy_text_claim():
    assert (
        grade_answer({"kind": "exact_number", "expected": "1/3"}, {"value": "2/6"})
        == "correct"
    )
    assert (
        grade_answer({"kind": "exact_number", "expected": "1/3"}, {"value": "0.333"})
        == "incorrect"
    )
    assert text_answer(" O’LCHAM ") == text_answer("o‘lcham")
    assert text_answer("o'lcham") != text_answer("olcham")
    with pytest.raises(MathInputError):
        grade_answer({"kind": "exact_number", "expected": "3"}, {"value": True})


def test_each_objective_choice_is_explicit_not_client_correctness():
    spec = {"kind": "choice", "expected": "a", "choice_ids": ["a", "b"]}
    assert grade_answer(spec, {"choice_id": "b"}) == "incorrect"
    with pytest.raises(MathInputError):
        grade_answer(spec, {"choice_id": "b", "is_correct": True})
    with pytest.raises(MathInputError):
        grade_answer(spec, {"choice_id": "unissued"})
