"""
Unit tests for Metaclasses helpers.
"""

from typing import Any, Callable

import pytest

from mlte._private import meta

# -------------------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------------------


class ClassForTesting:
    """Just used for testing."""

    def method_for_test(self, a):
        return a

    @classmethod
    def a_class_method(cls):
        return

    @staticmethod
    def a_static_method():
        return


def function_for_testing(b):
    """Just for testing."""
    return b


# -------------------------------------------------------------------------------------
# Tests
# -------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "test_object, callables, expected",
    [
        (ClassForTesting, ["method_for_test"], True),
        (ClassForTesting, ["not_method_for_test"], False),
        (ClassForTesting, ["method_for_test", "a_class_method"], True),
    ],
)
def test_has_callables(test_object: type, callables: list[str], expected: bool):
    """Check if it has the given callables."""

    success = meta.has_callables(test_object, *callables)

    assert success == expected


@pytest.mark.parametrize(
    "test_object, expected",
    [
        (function_for_testing, "test._private.test_meta.function_for_testing"),
        (ClassForTesting, "test._private.test_meta.ClassForTesting"),
        (
            ClassForTesting.method_for_test,
            "test._private.test_meta.ClassForTesting.method_for_test",
        ),
        (
            ClassForTesting.a_class_method,
            "test._private.test_meta.ClassForTesting.a_class_method",
        ),
        (
            ClassForTesting.a_static_method,
            "test._private.test_meta.ClassForTesting.a_static_method",
        ),
    ],
)
def test_qualified_name(test_object: type | Callable[[], Any], expected: str):
    """Check if qulified name is properly obtained for a function."""

    qual_name = meta.get_qualified_name(test_object)

    assert qual_name == expected
