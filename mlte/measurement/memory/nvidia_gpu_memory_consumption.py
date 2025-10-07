"""
mlte/measurement/memory/nvidia_gpu_memory_consumption.py

Memory consumption measurement for gpu processes.

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
from typing import Any, Callable, Optional

import psutil

from mlte.evidence.external import ExternalEvidence
from mlte.measurement.process_measurement import ProcessMeasurement
from mlte.measurement.units import (
    Quantity,
    Unit,
    Units,
    str_to_unit,
    unit_to_str,
)
from mlte.validation.validator import Validator

# -----------------------------------------------------------------------------
#   ___
#  / __|___ _ __  _ __  ___ _ _
# | (__/ _ \ '  \| '  \/ _ \ ' \
#  \___\___/_|_|_|_|_|_\___/_||_|
# -----------------------------------------------------------------------------


class CommonStatistics(ExternalEvidence):
    DEFAULT_UNIT: Optional[Unit] = None

    def __init__(self, avg: int, min: int, max: int, unit: Optional[Unit]):
        """

        :param avg: The average value
        :param min: The minimum value
        :param max: The maximum value
        :param unit: the unit the values comes in, as a value from Units
        """
        super().__init__()

        self.avg = Quantity(avg, unit)
        """The average value."""

        self.min = Quantity(min, unit)
        """The minimum values."""

        self.max = Quantity(max, unit)
        """The maximum value."""

        self.unit = unit
        """The unit being used for all values."""

    def serialize(self) -> dict[str, Any]:
        """
        Serialize to a JSON object.

        :return: The JSON object
        """
        return {
            "avg": self.avg.magnitude,
            "min": self.min.magnitude,
            "max": self.max.magnitude,
            "unit": unit_to_str(self.unit),
        }

    @classmethod
    def deserialize(cls, data: dict[str, Any]) -> Any:
        """
        Deserialize from a JSON object.

        :param data: The JSON object

        :return: The deserialized instance
        """
        unit = str_to_unit(data["unit"])
        return cls(
            avg=data["avg"],
            min=data["min"],
            max=data["max"],
            unit=unit if unit else cls.DEFAULT_UNIT,
        )

    def __str__(self) -> str:
        """Return a string representation."""
        return (
            f"Average: {self.avg}\n"
            + f"Minimum: {self.min}\n"
            + f"Maximum: {self.max}"
        )

    def __repr__(self) -> str:
        """Return a string representation for debugging."""
        return (
            f"avg={self.avg}, min={self.min}, max={self.max}, unit={self.unit}"
        )

    @classmethod
    def max_consumption_less_than(
        cls, threshold: int, unit: Optional[Unit] = None
    ) -> Validator:
        """
        Construct and invoke a validator for maximum memory consumption.

        :param threshold: The threshold value for maximum consumption
        :param unit: the unit the threshold comes in, as a value from Units; defaults to DEFAULT_UNIT

        :return: The Validator that can be used to validate a Value.
        """
        # This allows us to get the unit from a subclass
        if unit is None:
            unit = cls.DEFAULT_UNIT

        threshold_w_unit = Quantity(threshold, unit)
        bool_exp: Callable[[Any], bool] = (
            lambda stats: stats.max < threshold_w_unit
        )
        validator: Validator = Validator.build_validator(
            bool_exp=bool_exp,
            thresholds=[threshold_w_unit],
            success=f"Maximum consumption below threshold {threshold_w_unit}",
            failure=f"Maximum consumption exceeds threshold {threshold_w_unit}",
            input_types=[cls],
        )
        return validator

    @classmethod
    def average_consumption_less_than(
        cls, threshold: float, unit: Optional[Unit] = None
    ) -> Validator:
        """
        Construct and invoke a validator for average memory consumption.

        :param threshold: The threshold value for average consumption, in KB
        :param unit: the unit the threshold comes in, as a value from Units; defaults to Units.kilobyte

        :return: The Validator that can be used to validate a Value.
        """

        # This allows us to get the unit from a subclass
        if unit is None:
            unit = cls.DEFAULT_UNIT

        threshold_w_unit = Quantity(threshold, unit)
        bool_exp: Callable[[Any], bool] = (
            lambda stats: stats.avg < threshold_w_unit
        )
        validator: Validator = Validator.build_validator(
            bool_exp=bool_exp,
            thresholds=[threshold_w_unit],
            success=f"Average consumption below threshold {threshold_w_unit}",
            failure=f"Average consumption exceeds threshold {threshold_w_unit}",
            input_types=[cls],
        )
        return validator


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
    consumption statistics for an NVIDIA GPU.
    """

    def __init__(self, avg: int, min: int, max: int, unit: Unit = DEFAULT_UNIT):
        """
        Initialize a NvidiaGPUMemoryStatistics instance.

        :param avg: The average memory consumption
        :param min: The minimum memory consumption
        :param max: The maximum memory consumption
        :param unit: the unit the values comes in, as a value from Units; defaults to DEFAULT_UNIT
        """
        super().__init__(avg, min, max, unit)


# -----------------------------------------------------------------------------
#  __  __                                        _
# |  \/  |___ __ _ ____  _ _ _ ___ _ __  ___ _ _| |_
# | |\/| / -_) _` (_-< || | '_/ -_) '  \/ -_) ' \  _|
# |_|  |_\___\__,_/__/\_,_|_| \___|_|_|_\___|_||_\__|
# -----------------------------------------------------------------------------


class NvidiaGPUMemoryConsumption(ProcessMeasurement):
    """Measure memory consumption for a specific gpu."""

    def __init__(
        self,
        identifier: Optional[str] = None,
        group: Optional[str] = None,
        gpu_id: int = 0,
    ):
        """
        Initialize a LocalProcessMemoryConsumption instance.

        :param identifier: A unique identifier for the measurement
        :param group: An optional group id, if we want to group this measurement with others.
        :param gpu_id: The id of the gpu
        """
        super().__init__(identifier)
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

        # Keep collecting stats untl the controlling process goes away.
        # It might actualy take the controlling process a while to start up the memory consumption
        # so just collect the entire time whether we have consumption or not.
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
