from __future__ import annotations

import gc
import inspect
from types import FrameType, FunctionType
from typing import Any, Mapping, Optional

from mlte._private import meta


class FunctionInfo:
    """
    Class to extract info about current class, function and arguments.
    """

    def __init__(
        self,
        function_name: Optional[str],
        arguments: list[Any],
        function_parent: Optional[str],
    ):
        """
        Initialize a FunctionInfo instance.

        :param function_name: The name of the function that called us.
        :param arguments: The list of arguments passed to the function.
        :param function_parent: The full module + class name of the object that contains the function, if any.
        """

        self.function_name = function_name
        """The human-readable string for the name function."""

        self.arguments: list[Any] = arguments
        """The arguments used when calling the function."""

        self.function_parent = function_parent
        """Class or module where this function was called came from."""

    @staticmethod
    def get_function_info(
        caller_function: Optional[FrameType] = None,
    ) -> FunctionInfo:
        """
        Extracting context info from current function that called us.

        :param caller_function: The frame of the function to review, if any. If not provided, we inspect to get our caller.
        :return: A FunctionInfo with information about the calling function.
        """
        # Get context info about the caller from inspection.
        if caller_function is None:
            curr_frame = inspect.currentframe()
            if curr_frame is None:
                raise Exception(
                    "Unexpected error reading caller function data: empty frame."
                )
            caller_function = curr_frame.f_back
            if caller_function is None:
                raise Exception(
                    "Unexpected error reading caller function data: empty function."
                )

        # Get function name of caller. Handle case when called from top script.
        function_name: Optional[str] = caller_function.f_code.co_name
        if function_name == "<module>":
            function_name = None

        # Get args. Args will include all caller arguments except for caller class or object.
        arg_keys, _, _, arg_values = inspect.getargvalues(caller_function)
        filtered_args = []
        for arg_key in arg_keys:
            if arg_key != "cls" and arg_key != "self":
                filtered_args.append(arg_values[arg_key])

        # Build the class info as a string, or module if there is no class.
        class_type = get_class_from_func(get_func_from_frame(caller_function))
        if not class_type:
            module = inspect.getmodule(caller_function)
            parent_str = f"{module.__name__}" if module else None
        else:
            parent_str = f"{meta.get_qualified_name(class_type)}"

        # Return the full info.
        info = FunctionInfo(function_name, filtered_args, parent_str)
        return info

    def __str__(self) -> str:
        return f"FunctionInfo: Func Name - {self.function_name}; Args - {self.arguments}; Parent - {self.function_parent}"


# -------------------------------------------------------------------------
# Helper functions to get metadata.
# -------------------------------------------------------------------------


def get_func_from_frame(frame: FrameType) -> Optional[FunctionType]:
    # Nifty trick - get the function from the reference to its code object
    refs = gc.get_referrers(frame.f_code)
    for ref in refs:
        if isinstance(ref, FunctionType):
            return ref
    return None


def get_class_from_func(func: Optional[FunctionType]) -> Optional[type]:
    if not func or "." not in func.__qualname__:
        return None

    cls_qual_name, func_name = func.__qualname__.rsplit(".", 1)
    if func_name != func.__name__:
        raise RuntimeError(
            f"Error parsing function name, expected name and frame do not match: {func_name}, {func.__name__}"
        )

    # Recursively check GC references
    visited_ids = set()
    items_to_check = [func]

    # The function is referenced within the type's dict, or its descriptor
    while len(items_to_check) > 0:
        obj = items_to_check[0]
        items_to_check = items_to_check[1:]

        obj_id = id(obj)
        if obj_id in visited_ids:
            continue
        visited_ids.add(obj_id)

        refs = gc.get_referrers(obj)
        for ref in refs:
            if isinstance(ref, type) and ref.__qualname__ == cls_qual_name:
                return ref

            if hasattr(ref, "__get__") or isinstance(ref, Mapping):
                items_to_check.append(ref)

    return None
