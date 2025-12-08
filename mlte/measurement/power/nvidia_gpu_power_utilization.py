"""
Power utilization measurement in watts for NVIDIA gpu processes.

This relies on the pynvml package for status. We dynamically import it, so that we can return useful
results when it isn't available.

We are using the 'nvidia-ml-py' version of the library. Thus: 'pip install nvidia-ml-py'

API DOCS:

NVIDIA Management Library (NVML) - https://developer.nvidia.com/management-library-nvml

Links at bottom:
API Docs - https://docs.nvidia.com/deploy/nvml-api/index.html
Python Binding Docs - https://pypi.org/project/nvidia-ml-py/

Example for getting memory utilization (nvmlDeviceGetPowerUsage):

https://docs.nvidia.com/deploy/nvml-api/group__nvmlDeviceQueries.html#group__nvmlDeviceQueries_1g7ef7dff0ff14238d08a19ad7fb23fc87

This call returns milliwatts used.

"""

from __future__ import annotations

from typing import Optional

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


class NvidiaGPUPowerStatistics(CommonStatistics):
    # Nvidia-smi cli uses watts so we use that for consistency.
    DEFAULT_UNIT = Units.watt

    """
    The NvidiaGPUMemoryStatistics class encapsulates data
    and functionality for tracking and updating power usage
    statistics for an NVIDIA GPU.
    """

    def __init__(
        self, avg: float, min: float, max: float, unit: Unit = DEFAULT_UNIT
    ):
        """
        Initialize a NvidiaGPUPowerStatistics instance.

        :param avg: The average power utilization
        :param min: The minimum power utilization
        :param max: The maximum power utilization
        :param unit: the unit the values comes in, as a value from Units; defaults to DEFAULT_UNIT
        """
        super().__init__(avg, min, max, unit)


# -----------------------------------------------------------------------------
#  __  __                                        _
# |  \/  |___ __ _ ____  _ _ _ ___ _ __  ___ _ _| |_
# | |\/| / -_) _` (_-< || | '_/ -_) '  \/ -_) ' \  _|
# |_|  |_\___\__,_/__/\_,_|_| \___|_|_|_\___|_||_\__|
# -----------------------------------------------------------------------------


class NvidiaGPUPowerUtilization(ProcessMeasurement):
    """Measure power utilization for a specific gpu."""

    def __init__(
        self,
        identifier: Optional[str] = None,
        group: Optional[str] = None,
        gpu_id: int = 0,
    ):
        """
        Initialize a NvidiaGPUPowerUtilization instance.

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
        unit: Unit = NvidiaGPUPowerStatistics.DEFAULT_UNIT,
        poll_interval: int = 1,
    ) -> NvidiaGPUPowerStatistics:
        """
        Monitor memory usage on a specific gpu.

        :param pid: The process identifier
        :param poll_interval: The poll interval, in seconds
        :param unit: The unit to return the memory size in, defaults to statistics default unit.
        :return: The captured statistics
        """
        average, minimum, maximum = (
            pynvml_utils.aggregate_measurements_from_process(
                pid,
                poll_interval,
                gpu_id=self.gpu_id,
                fn=_get_nvml_power_usage_watts,
                default=-1,
            )
        )

        # Coerce to the desired target units
        return NvidiaGPUPowerStatistics(
            Quantity(average, Units.watt).to(unit).magnitude,
            Quantity(minimum, Units.watt).to(unit).magnitude,
            Quantity(maximum, Units.watt).to(unit).magnitude,
            unit=unit,
        )

    # Overriden.
    @classmethod
    def get_output_type(cls) -> type[NvidiaGPUPowerStatistics]:
        return NvidiaGPUPowerStatistics


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def _get_nvml_power_usage_watts(pynvml, handle) -> float:
    """
    Function to be passed to the pynvml utility to get the power usage in watts.
    :param pynvml: The pynvml module
    :param handle: A handle to the gpy
    :return: The power usage in watts
    """
    milliwatts_used = pynvml.nvmlDeviceGetPowerUsage(handle)
    return float(milliwatts_used / 1000)
