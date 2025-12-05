"""
A series of utilities to simply getting NVIDIA GPU information.

This uses 'nvidia-ml-py' version of the library. Thus: 'pip install nvidia-ml-py'

API DOCS:

NVIDIA Management Library (NVML) - https://developer.nvidia.com/management-library-nvml

Links at bottom:
API Docs - https://docs.nvidia.com/deploy/nvml-api/index.html
Python Binding Docs - https://pypi.org/project/nvidia-ml-py/

"""

import logging
import sys
import time
import traceback
import types
from importlib import import_module
from typing import Callable, Optional, Tuple

import psutil

# 0 = Info logging (default)
# 1 = Warning logging
# 2 = Error logging
# 3 = Raise exceptions
ERROR_LEVEL = 0


def _handle_error(msg: str, e: Optional[Exception] = None):
    logger = logging.getLogger(__name__)
    if ERROR_LEVEL == 0:
        logger.info(f"{msg}, {e}")
    elif ERROR_LEVEL == 1:
        logger.warning(f"{msg}, {e}")
    elif ERROR_LEVEL == 2:
        logger.error(f"{msg}, {e}")
        traceback.print_exc()
    elif ERROR_LEVEL == 3:
        logger.error(msg)
        traceback.print_exc()
        if e is not None:
            raise e


def aggregate_measurements_from_process(
    pid: int,
    poll_interval: float,
    gpu_id: int,
    fn: Callable[[types.ModuleType, int], float],
    default: float = 0.0,
) -> Tuple[float, float, float]:
    """
    :param pid: The process identifier
    :param poll_interval: The poll interval, in seconds
    :param gpu_id: The id of the gpu for which to collect
    :param fn: The pynvml function to call that actually extracts the value. See get_pynvml_statistic
    for details.
    :param default: The value to use for a sample if we fail to get value for any reason such as the module
    could not be loaded or the gpu could not be found.
    :return: minimum, maximum, average
    """

    maximum: float = 0
    minimum: float = sys.maxsize
    total: float = 0
    count: int = 0

    while True:
        try:

            # This is just so that we check to see if our task is running
            # psutil.Process(pid)
            if not psutil.pid_exists(pid):
                break

            return_value = get_pynvml_statistic(
                gpu_id=gpu_id, fn=fn, default=default
            )

            # If invalid, then we get this. We might want to keep track of how many we get.
            if return_value == -1:
                break

            minimum = min(minimum, return_value)
            maximum = max(maximum, return_value)
            total += return_value
            count += 1

            time.sleep(poll_interval)
        except psutil.NoSuchProcess:
            # This is by design as the process went away
            break

    average: float = 0
    if count > 0:
        average = total / count

    return minimum, maximum, average


def get_pynvml_statistic(
    gpu_id: int,
    fn: Callable[[types.ModuleType, int], float],
    default: float = 0.0,
) -> float:
    """
    Dynamically loads the pynvml library, initializes it, makes the call
    on the library and returns the value.

    The callable is provided with a loaded pynvml as the first argument and the handle
    to the device as a second argument, so that a call can be made directly to pynvml with
    the handle. For example:

    fn(pynvml, handle) -> float:
        # NOTE: Pynvml exposes version 1 of the structure which has:
        # total, used, free
        memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        return float(memory_info.used)

    NOTE: The pynvml "handle" type is unavailable to the typing system.

    :param gpu_id: The id (index) of the gpu.
    :param fn: The function to be called to get the value.
    :param default: The value to return if we fail to get value for any reason such as the module
    could not be loaded or the gpu could not be found.
    :return: The value returned by the function.
    """
    try:
        pynvml = import_module("pynvml")

        # TODO: Check to see if re-initing this takes time or we can do it at will
        # This may generate a pynvml.NVMLError_LibraryNotFound if pynvml exists but no drivers exist
        pynvml.nvmlInit()

        try:
            # Get the number of NVIDIA devices
            device_count = pynvml.nvmlDeviceGetCount()

            if gpu_id > device_count - 1:
                # TODO: Switch to new logging/error handling system
                _handle_error(
                    f"GPU monitor requested for {gpu_id} gpu but there are only {device_count} gpus available.",
                    None,
                )
                return default

            # Error checking to see if they have too many.
            handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)

            # Now, make their call passing back the value as-is
            return fn(pynvml, handle)

        except pynvml.NVMLError as error:
            # TODO: Switch to new logging/error handling system
            print(error)
            return default

    except ModuleNotFoundError as e:
        # TODO: Switch to new logging/error handling system
        _handle_error("Warning: pynvml not found.", e)
        return default
    except AttributeError as e:
        # TODO: Switch to new logging/error handling system
        _handle_error("Error: Attribute not found in module 'pynvml'.", e)
        return default
    except Exception as e:
        # TODO: Switch to new logging/error handling system
        # This is for things such as pynvml.NVMLError_LibraryNotFound - "NVML Shared Library Not Found"
        # This is when we can find pynvml but we don't actually have the underlying platform library which
        # will be triggered by a call to init.
        _handle_error(f"Other exception '{e}'", e)
        return default
