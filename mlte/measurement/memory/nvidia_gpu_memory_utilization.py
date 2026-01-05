"""
Memory utilization measurement for gpu processes.

This relies on the pynvml package for status. We dynamically import it, so that we can return useful
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

from typing import Optional, Union

import mlte.measurement.utility.pynvml_utils as pynvml_utils
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
    # Nvidia-smi cli uses MiB so we use that for consistency.
    DEFAULT_UNIT: Unit = Units.mebibyte

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
    """Measure memory utilization for a specific gpu."""

    def __init__(
        self,
        identifier: Optional[str] = None,
        group: Optional[str] = None,
        gpu_ids: Union[int, list[int]] = 0,
    ):
        """
        Initialize a NvidiaGPUMemoryUtilization instance.

        :param identifier: A unique identifier for the measurement
        :param group: An optional group id, if we want to group this measurement with others.
        :param gpu_ids: A list of 1 or more gpu ids to use.
        """
        super().__init__(identifier, group)

        self.gpu_ids: list[int] = (
            [gpu_ids] if isinstance(gpu_ids, int) else gpu_ids
        )
        assert len(self.gpu_ids) > 0

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
        :param unit: The unit to return the memory size in, defaults to statistics default unit.
        :param poll_interval: The poll interval, in seconds
        :return: The captured statistics
        """

        # Keep collecting stats until the controlling process goes away.
        # It might actually take the controlling process a while to start up the memory utilization
        # so just collect the entire time whether we have utilization or not.

        minimum, maximum, average = (
            pynvml_utils.aggregate_measurements_from_process(
                pid,
                poll_interval,
                gpu_ids=self.gpu_ids,
                fn=_get_nvml_memory_usage_bytes,
            )
        )

        # Coerce to the desired target units
        return NvidiaGPUMemoryStatistics(
            Quantity(average, Units.bytes).to(unit).magnitude,
            Quantity(minimum, Units.bytes).to(unit).magnitude,
            Quantity(maximum, Units.bytes).to(unit).magnitude,
            unit=unit,
        )

    # Overriden.

    @classmethod
    def get_output_type(cls) -> type[NvidiaGPUMemoryStatistics]:
        return NvidiaGPUMemoryStatistics


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def _get_nvml_memory_usage_bytes(pynvml, handle) -> float:
    """
    Function to be passed to the pynvml utility to get the memory usage in bytes.
    :param pynvml: The pynvml module
    :param handle: A handle to the gpy
    :return: The memory usage in watts
    """
    # NOTE: Pynvml exposes version 1 of the structure which has:
    # total, used, free
    memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    return float(memory_info.used)
