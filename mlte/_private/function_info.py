from __future__ import annotations

import inspect
from types import FrameType
from typing import Any, Optional, Type


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

        # Get args. Args include all caller arguments except for the value class type.
        arguments = caller_function.f_locals
        filtered_args = []
        for arg_key, arg_value in arguments.items():
            if arg_key != "cls":
                filtered_args.append(arg_value)

        # Build the class info as a string.
        if "cls" not in arguments:
            cls_str = ""
        else:
            cls: Type[object] = arguments["cls"]
            cls_str = f"{cls.__module__}.{cls.__name__}"

        # Return the full info.
        info = FunctionInfo(function_name, filtered_args, cls_str)
        return info
