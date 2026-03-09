import pytest


def test_addition(calculator):
    """
    Test addition.
    """

    assert calculator.calculate("2+3") == 5


def test_subtraction(calculator):
    """
    Test subtraction.
    """

    assert calculator.calculate("10-4") == 6


def test_multiplication(calculator):
    """
    Test multiplication.
    """

    assert calculator.calculate("8*5") == 40


def test_division(calculator):
    """
    Test division.
    """

    assert calculator.calculate("20/5") == 4


def test_modulus(calculator):
    """
    Test modulus.
    """

    assert calculator.calculate("10%3") == 1


def test_power(calculator):
    """
    Test exponent.
    """

    assert calculator.calculate("2**4") == 16


def test_negative_number(calculator):
    """
    Test unary minus.
    """

    assert calculator.calculate("-10") == -10


def test_complex_expression(calculator):
    """
    Test multiple operators.
    """

    assert calculator.calculate("(10+5)*2") == 30


def test_invalid_expression(calculator):
    """
    Invalid expressions should raise ValueError.
    """

    with pytest.raises(ValueError):

        calculator.calculate(
            "__import__('os').system('ls')"
        )