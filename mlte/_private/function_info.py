from __future__ import annotations

import inspect
from types import FrameType
from typing import Any, Optional, Type

from mlte._private.meta import get_full_path


class FunctionInfo:
    """
    Class to extract info about current class, function and arguments.
    """

    def __init__(
        self, function_name: str, arguments: list[Any], function_class: str
    ):
        """
        Initialize a FunctionInfo instance.

        :param function_name: The name of the function that called us.
        :param arguments: The list of arguments passed to the function.
        :param function_class: The full module + class name of the object that contains the function, if any.
        """

        self.function_name: str = function_name
        """The human-readable string for the name function."""

        self.arguments: list[Any] = arguments
        """The arguments used when calling the function."""

        self.function_class: str = function_class
        """Class where this function was called came from."""

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

        # Get function name of caller.
        function_name = caller_function.f_code.co_name

        # Get args. Args will include all caller arguments except for caller class or object.
        arg_keys, _, _, arg_values = inspect.getargvalues(caller_function)
        filtered_args = []
        for arg_key in arg_keys:
            print(f"{arg_key}={arg_values[arg_key]}")
            if arg_key != "cls" and arg_key != "self":
                filtered_args.append(arg_values[arg_key])

        # Build the class info as a string.
        if "cls" not in arg_keys:
            cls_str = ""
        else:
            cls: Type[object] = arg_values["cls"]
            cls_str = f"{get_full_path(cls)}"

        # Return the full info.
        info = FunctionInfo(function_name, filtered_args, cls_str)
        return info
