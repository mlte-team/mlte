"""
Memory utilization measurement for gpu processes.

It relies on the pynvml package for status. We dynamically import it, so that we can can return useful
results when it isn't available.

We are using the 'nvidia-ml-py' version of the library. Thus: 'pip install nvidia-ml-py'

API DOCS:

NVIDIA Management Library (NVML) - https://developer.nvidia.com/management-library-nvml

Links at bottom:
API Docs - https://docs.nvidia.com/deploy/nvml-api/index.html
Python Binding Docs - https://pypi.org/project/nvidia-ml-py/

Example for getting memory utilization (nvmlDeviceGetMemoryInfo):

https://docs.nvidia.com/deploy/nvml-api/group__nvmlDeviceQueries.html#group__nvmlDeviceQueries_1g2dfeb1db82aa1de91aa6edf941c85ca8

"""

from __future__ import annotations

import sys
import time
from importlib import import_module
from typing import Optional

import psutil

from mlte.measurement.common import CommonStatistics
from mlte.measurement.process_measurement import ProcessMeasurement
from mlte.measurement.units import Quantity, Unit, Units

# -----------------------------------------------------------------------------
#  ___ _        _   _    _   _
# / __| |_ __ _| |_(_)__| |_(_)__ ___
# \__ \  _/ _` |  _| (_-<  _| / _(_-<
# |___/\__\__,_|\__|_/__/\__|_\__/__/
# -----------------------------------------------------------------------------


class NvidiaGPUMemoryStatistics(CommonStatistics):
    # Nvidia-smi cli uses MiB so we use that make it easy to visually compare
    # and we suspect this is what people are calibrated to.
    DEFAULT_UNIT = Units.mebibyte

    """
    The NvidiaGPUMemoryStatistics class encapsulates data
    and functionality for tracking and updating memory
    utilization statistics for an NVIDIA GPU.
    """

    def __init__(
        self, avg: float, min: float, max: float, unit: Unit = DEFAULT_UNIT
    ):
        """
        Initialize a NvidiaGPUMemoryStatistics instance.

        :param avg: The average memory utilization
        :param min: The minimum memory utilization
        :param max: The maximum memory utilization
        :param unit: the unit the values comes in, as a value from Units; defaults to DEFAULT_UNIT
        """
        super().__init__(avg, min, max, unit)


# -----------------------------------------------------------------------------
#  __  __                                        _
# |  \/  |___ __ _ ____  _ _ _ ___ _ __  ___ _ _| |_
# | |\/| / -_) _` (_-< || | '_/ -_) '  \/ -_) ' \  _|
# |_|  |_\___\__,_/__/\_,_|_| \___|_|_|_\___|_||_\__|
# -----------------------------------------------------------------------------


class NvidiaGPUMemoryUtilization(ProcessMeasurement):
    """Measure memory utilizatio for a specific gpu."""

    def __init__(
        self,
        identifier: Optional[str] = None,
        group: Optional[str] = None,
        gpu_id: int = 0,
    ):
        """
        Initialize a LocalProcessMemoryUtilization instance.

        :param identifier: A unique identifier for the measurement
        :param group: An optional group id, if we want to group this measurement with others.
        :param gpu_id: The id of the gpu
        """
        super().__init__(identifier, group)
        self.gpu_id = gpu_id

    # Overriden.
    def __call__(
        self,
        pid: int,
        unit: Unit = NvidiaGPUMemoryStatistics.DEFAULT_UNIT,
        poll_interval: int = 1,
    ) -> NvidiaGPUMemoryStatistics:
        """
        Monitor memory usage on a specific gpu.

        :param pid: The process identifier
        :param poll_interval: The poll interval, in seconds
        :param unit: The unit to return the memory size in, defaults to statistics default unit.
        :return: The captured statistics
        """
        maximum = 0
        minimum = sys.maxsize
        total = 0
        count = 0

        # Keep collecting stats until the controlling process goes away.
        # It might actually take the controlling process a while to start up the memory utilization
        # so just collect the entire time whether we have utilization or not.
        while True:
            try:
                # This is just so that we check to see if our task is running
                psutil.Process(pid)
                size_in_bytes = _get_nvml_memory_usage_bytes(self.gpu_id)

                # If invalid, then we get this. We might want to keep track of how many we get.
                if size_in_bytes == -1:
                    break

                minimum = min(minimum, size_in_bytes)
                maximum = max(maximum, size_in_bytes)
                total += size_in_bytes
                count += 1

                time.sleep(poll_interval)
            except psutil.NoSuchProcess:
                # This is by design as the process went away
                break

        # Coerce to the quantity type with bytes then convert to target
        avg_unit = Quantity(0, Units.bytes).to(unit)
        if count > 0:
            avg_unit = Quantity(total // count, Units.bytes).to(unit)
        min_unit = Quantity(minimum, Units.bytes).to(unit)
        max_unit = Quantity(maximum, Units.bytes).to(unit)
        return NvidiaGPUMemoryStatistics(
            avg_unit.magnitude,
            min_unit.magnitude,
            max_unit.magnitude,
            unit=unit,
        )

    # Overriden.

    @classmethod
    def get_output_type(cls) -> type[NvidiaGPUMemoryStatistics]:
        return NvidiaGPUMemoryStatistics


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def _get_nvml_memory_usage_bytes(gpu_id: int) -> int:
    """
    Gets the memory usage for the INDEX specified gpu. NOTE: This is for
    the entire GPU not just a single process.
    :param gpu_id: The id (index) of the gpu.
    :return: The memory usage in bytes.
    """
    try:
        pynvml = import_module("pynvml")

        # TODO: Check to see if re-initing this takes time or we can do it at will
        pynvml.nvmlInit()

        try:
            # Get the number of NVIDIA devices
            device_count = pynvml.nvmlDeviceGetCount()

            if gpu_id > device_count - 1:
                # TODO: Switch to new logging/error handling system
                print(
                    f"GPU monitor requested for {gpu_id} gpu but there are only {device_count} gpus available."
                )
                return -1

            # Error checking to see if they have too many.
            handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)

            # NOTE: Pynvml exposes version 1 of the structure which has:
            # total, used, free
            memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            return int(memory_info.used)

        except pynvml.NVMLError as error:
            # TODO: Switch to new logging/error handling system
            print(error)
            return -1

    except ModuleNotFoundError:
        # TODO: Switch to new logging/error handling system
        print("Warning: pynvml not found.")
        return -1
    except AttributeError as e:
        # TODO: Switch to new logging/error handling system
        print(f"Error: {e} Attribute not found in module 'pynvml'.")
        return -1
    except Exception as e:
        # TODO: Switch to new logging/error handling system
        # This is for things such as pynvml.NVMLError_LibraryNotFound
        print(f"Other exception {e}")
        return -1
