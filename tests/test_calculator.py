"""Unit tests for the calculator logic.

GitHub Actions runs these automatically on every push / pull request.
If any test fails, the workflow goes red and (with branch protection)
the code cannot be merged or deployed.
"""
import pytest

from app.calculator import add, subtract, multiply, divide, calculate


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(10, 4) == 6


def test_multiply():
    assert multiply(3, 5) == 15


def test_divide():
    assert divide(10, 2) == 5


def test_divide_by_zero_raises():
    with pytest.raises(ValueError):
        divide(1, 0)


def test_calculate_dispatch():
    assert calculate("add", 1, 1) == 2
    assert calculate("multiply", 4, 2) == 8


def test_calculate_unknown_operation():
    with pytest.raises(ValueError):
        calculate("modulo", 5, 2)


# Parametrized test: one function, many cases.
@pytest.mark.parametrize(
    "op,a,b,expected",
    [
        ("add", 1, 2, 3),
        ("subtract", 5, 2, 3),
        ("multiply", 2, 3, 6),
        ("divide", 9, 3, 3),
    ],
)
def test_calculate_table(op, a, b, expected):
    assert calculate(op, a, b) == expected
