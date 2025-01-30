"""
Unit test for the reflection util module.
"""

from typing import Any

from mlte._private.reflection import get_lambda_code


def test_get_lambda_code_simple():
    my_lambda = lambda x: x * 2  # noqa: E731
    lambda_code = get_lambda_code(my_lambda)
    assert lambda_code == "lambda x: (x * 2)"


def test_get_lambda_code_multiple_args():
    another_lambda = lambda a, b: a + b  # noqa: E731
    code = get_lambda_code(another_lambda)
    assert code == "lambda a, b: (a + b)"


def test_get_lambda_code_inner_function():
    def outer_function():
        inner_lambda = lambda y: y**2  # noqa: E731
        return get_lambda_code(inner_lambda)

    inner_code = outer_function()
    assert inner_code == "lambda y: (y ** 2)"


def test_get_lambda_code_not_a_lambda():
    not_a_lambda = "not a lambda"  # noqa: E731
    not_lambda_code = get_lambda_code(not_a_lambda)
    assert not_lambda_code is None


def test_get_lambda_code_complex_body():
    lambda_with_complex_body = lambda z: z * 3 if z > 0 else -z  # noqa: E731
    complex_code = get_lambda_code(lambda_with_complex_body)
    assert complex_code == "lambda z: ((z * 3) if (z > 0) else (- z))"


def test_get_lambda_code_multiline():
    multiline_lambda = lambda a, b: a + b  # noqa: E731
    multiline_code = get_lambda_code(multiline_lambda)
    assert multiline_code == "lambda a, b: (a + b)"


def test_get_lambda_code_with_defaults():
    lambda_with_defaults = lambda x=1, y=2: x + y  # noqa: E731
    code = get_lambda_code(lambda_with_defaults)
    assert code == "lambda x=1, y=2: (x + y)"


def test_comma_lambda() -> None:
    """Function generates proper lambda string from a lambda with other symbols."""
    test_lambda = lambda a_string: a_string.split(",", 2)  # noqa: E731
    lambda_str = get_lambda_code(test_lambda)
    assert lambda_str == "lambda a_string: a_string.split(',', 2)"


def test_lambda_and_comment():
    lambda_with_lambda_in_comment = (
        lambda w: w + 5
    )  # this is a lambda  # noqa: E731
    lambda_str = get_lambda_code(lambda_with_lambda_in_comment)
    assert lambda_str == "lambda w: (w + 5)"


def test_complex_source_line():
    """
    This case tests a specific edge case, which is handled but not very well.
    If the line the lambda was defined in is complex and can't be parsed due
    to it being a partial line, the funciton will get confused, and as a
    last attempt will just get the whole line after where the lambda def
    started, verbatim.
    """

    class Complex:
        number: int
        lambda_exp: Any
        something: str

        def set_values(self, new_number: int, new_lambda: Any, new_str: str):
            self.number = new_number
            self.lambda_exp = new_lambda
            self.something = new_str

    test = Complex()
    test.set_values(
        new_number=123, new_lambda=lambda z: z * 3 if z > 0 else -z, new_str="a"
    )

    lambda_str = get_lambda_code(test.lambda_exp)
    assert lambda_str == 'lambda z: z*3 if z > 0 else -z, new_str="a")'
