from __future__ import annotations

import inspect
from types import FrameType
from typing import Any, Optional, Type


class ClassMethodInfo:
    """
    Class to extract info about current class, method and arguments.
    """

    def __init__(
        self, method_name: str, arguments: list[Any], method_class: str
    ):
        """
        Initialize a ClassMethodInfo instance.

        :param method_name: The name of the method that called us.
        :param arguments: The list of arguments passed to the method.
        :param method_class: The full module + class name of the object that contains the method.
        """

        self.method_name: str = method_name
        """The human-readable string for the name method."""

        self.arguments: list[Any] = arguments
        """The arguments used when calling the method."""

        self.method_class: str = method_class
        """Class where this method was called came from."""

    @staticmethod
    def get_class_method_data(
        caller_function: Optional[FrameType],
    ) -> ClassMethodInfo:
        """
        Extracting context info from current class method that called us.

        :param caller_function: The frame of the function to review, if any. If not provided, we inspect to get our caller.

        :return: A ClassMethodInfo with information about the method.
        """
        # Get context info about the caller from inspection.
        if caller_function is None:
            curr_frame = inspect.currentframe()
            if curr_frame is None:
                raise Exception(
                    "Unexpected error reading caller method data: empty frame."
                )
            caller_function = curr_frame.f_back
            if caller_function is None:
                raise Exception(
                    "Unexpected error reading caller method data: empty function."
                )

        # Get function name of caller.
        method_name = caller_function.f_code.co_name

        # Get args. Args include all caller arguments except for the value class type.
        arguments = caller_function.f_locals
        filtered_args = []
        for arg_key, arg_value in arguments.items():
            if arg_key != "cls":
                filtered_args.append(arg_value)

        # Build the class info as a string.
        if "cls" not in arguments:
            raise Exception("'cls' argument is needed in method arguments.")
        cls: Type[object] = arguments["cls"]
        cls_str = f"{cls.__module__}.{cls.__name__}"

        # Return the full info.
        info = ClassMethodInfo(method_name, filtered_args, cls_str)
        return info
