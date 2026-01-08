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


def _handle_error(msg: str, e: Optional[Exception] = None):
    logger = logging.getLogger(__name__)
    logger.error(msg)
    traceback.print_exc()
    if e is not None:
        raise e
    else:
        raise ValueError(msg)


def aggregate_measurements_from_process(
    pid: int,
    poll_interval: float,
    gpu_ids: list[int],
    fn: Callable[[types.ModuleType, int], float],
) -> Tuple[float, float, float]:
    """
    :param pid: The process identifier
    :param poll_interval: The poll interval, in seconds
    :param gpu_ids: List of 1 or more gpu_ids to read and aggregate.
    :param fn: The pynvml function to call that actually extracts the value. See get_pynvml_statistic
    for details.
    :return: minimum, maximum, average
    """

    minimum: float = sys.maxsize
    maximum: float = 0
    total: float = 0
    count: int = 0

    while True:
        try:

            # This is just so that we check to see if our task is running
            # psutil.Process(pid)
            if not psutil.pid_exists(pid):
                break

            return_values: list[float] = get_pynvml_statistic(
                gpu_ids=gpu_ids, fn=fn
            )

            minimum = min(minimum, min(return_values))
            maximum = max(maximum, max(return_values))
            total += sum(return_values)
            count += len(return_values)

            time.sleep(poll_interval)
        except psutil.NoSuchProcess:
            # This is by design as the process went away
            break

    average: float = 0
    if count > 0:
        average = total / count

    return minimum, maximum, average


def get_pynvml_statistic(
    gpu_ids: list[int], fn: Callable[[types.ModuleType, int], float]
) -> list[float]:
    """
    Dynamically loads the pynvml library, initializes it, makes the call
    on the library and returns the value.

    The callable is provided with a loaded pynvml as the first argument and the handle
    to the device as a second argument, so that a call can be made directly to pynvml with
    the handle. For example:

    fn(pynvml, handle) -> float:
        memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        return float(memory_info.used)

    NOTE: The pynvml "handle" type is unavailable to the typing system.

    :param gpu_ids: One or more gpu.
    :param fn: The function to be called to get the value.
    :return: The value returned by the function.
    """

    # This is outside the try so that we always appear to return something.
    results: list[float] = []
    try:
        pynvml = import_module("pynvml")

        # TODO: Check to see if re-initing this takes time or we can do it at will
        # This may generate a pynvml.NVMLError_LibraryNotFound if pynvml exists but no drivers exist
        pynvml.nvmlInit()

        try:
            # Get the number of NVIDIA devices
            device_count = pynvml.nvmlDeviceGetCount()

            # We take a stringent approach at this pount. If they request a gpu that doesn't exist, bail out completely.
            for gpu_id in gpu_ids:
                if gpu_id > device_count - 1:
                    raise ValueError(
                        f"GPU monitor requested for gpu {gpu_id} but there are only {device_count} gpus available.",
                    )

            for gpu_id in gpu_ids:
                # Aggregate all results
                handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
                tmp = fn(pynvml, handle)
                results.append(tmp)

        except pynvml.NVMLError as error:
            _handle_error("NVML supporting library not installed.", error)

    except ModuleNotFoundError as e:
        # TODO: Switch to new logging/error handling system
        _handle_error("Warning: pynvml not found.", e)
    except AttributeError as e:
        # TODO: Switch to new logging/error handling system
        _handle_error("Error: Attribute not found in module 'pynvml'.", e)
    except Exception as e:
        # TODO: Switch to new logging/error handling system
        # This is for things such as pynvml.NVMLError_LibraryNotFound - "NVML Shared Library Not Found"
        # This is when we can find pynvml but we don't actually have the underlying platform library which
        # will be triggered by a call to init.
        _handle_error(f"Other exception '{e}'", e)

    return results
