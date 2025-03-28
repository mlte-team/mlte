"""
Unit test for the function info util module.
"""

import inspect
from types import FrameType
from typing import Optional

from mlte._private.function_info import FunctionInfo

# -------------------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------------------


top_frame = inspect.currentframe()
"""Used for tests."""


class TestFuncClass:
    """Sample test class to test getting its info."""

    def func_to_test(self, a: str) -> Optional[FrameType]:
        """This test function returns the frame being called from here."""
        curr_frame = inspect.currentframe()
        return curr_frame


def simple_test_func(b):
    curr_frame = inspect.currentframe()
    return curr_frame


# -------------------------------------------------------------------------------------
# Tests
# -------------------------------------------------------------------------------------


def test_function_info_this_module():
    """Tests properly returning info from the current function."""
    curr_frame = inspect.currentframe()

    func_info = FunctionInfo.get_function_info(curr_frame)

    assert func_info.function_name == "test_function_info_this_module"
    assert func_info.function_parent == "test._private.test_function_info"
    assert func_info.arguments == []


def test_function_info_from_class():
    """Tests properly returning info from the a class."""
    test_class = TestFuncClass()

    func_info = FunctionInfo.get_function_info(test_class.func_to_test(a="a"))

    assert func_info.function_name == "func_to_test"
    assert (
        func_info.function_parent
        == "test._private.test_function_info.TestFuncClass"
    )
    assert func_info.arguments == ["a"]


def test_function_info_lone_function():
    """Tests properly returning info from a lone function."""

    func_info = FunctionInfo.get_function_info(simple_test_func(b="b"))

    assert func_info.function_name == "simple_test_func"
    assert func_info.function_parent == "test._private.test_function_info"
    assert func_info.arguments == ["b"]


def test_function_info_no_parent():
    """Tests properly returning info from a no parent function."""

    func_info = FunctionInfo.get_function_info(top_frame)

    assert func_info.function_name is None
    assert func_info.function_parent == "test._private.test_function_info"
    assert func_info.arguments == []
