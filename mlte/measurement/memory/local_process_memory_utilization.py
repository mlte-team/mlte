"""
mlte/measurement/memory/local_process_memory_utilization.py

Memory utilization measurement for local training processes.
"""

from __future__ import annotations

import subprocess
import time
from typing import Optional

import psutil

from mlte.measurement.common import CommonStatistics
from mlte.measurement.process_measurement import ProcessMeasurement
from mlte.measurement.units import Unit, Units

# -----------------------------------------------------------------------------
# Memory Statistics
# -----------------------------------------------------------------------------


class MemoryStatistics(CommonStatistics):
    """
    The MemoryStatistics class encapsulates data
    and functionality for tracking and updating memory
    utilization statistics for a running process.
    """

    DEFAULT_UNIT = Units.kilobyte

    def __init__(self, avg: int, min: int, max: int, unit: Unit = DEFAULT_UNIT):
        """
        Initialize a MemoryStatistics instance.

        :param avg: The average memory utilization
        :param min: The minimum memory utilization
        :param max: The maximum memory utilization
        :param unit: the unit the values comes in, as a value from Units; defaults to Units.kilobyte
        """
        super().__init__(avg, min, max, unit)


# -----------------------------------------------------------------------------
# LocalProcessMemoryUtilization
# -----------------------------------------------------------------------------


class LocalProcessMemoryUtilization(ProcessMeasurement):
    """Measure memory utilization for a local training process."""

    def __init__(
        self, identifier: Optional[str] = None, group: Optional[str] = None
    ):
        """
        Initialize a LocalProcessMemoryUtilization instance.

        :param identifier: A unique identifier for the measurement
        :param group: An optional group id, if we want to group this measurement with others.
        """
        super().__init__(identifier, group)

    # Overriden.
    def __call__(
        self, pid: int, unit: Unit = Units.kilobyte, poll_interval: int = 1
    ) -> MemoryStatistics:
        """
        Monitor memory utilization of process at `pid` until exit.

        :param pid: The process identifier
        :param poll_interval: The poll interval, in seconds
        :param unit: The unit to return the memory size in, defaults to kilobyte (Units.kilobyte).
        :return: The captured statistics
        """
        captures = []
        while True:
            size_in_kb = _get_memory_usage_psutil(pid)
            if size_in_kb == 0:
                break
            captures.append(size_in_kb)
            time.sleep(poll_interval)

        # Calculate stats, use kilobytes as the psutil function returns values in that unit.
        avg = int(sum(captures) / len(captures)) * Units.kilobyte
        minimum = min(captures) * Units.kilobyte
        maximum = max(captures) * Units.kilobyte

        # Convert to provided unit if needed.
        avg = avg.to(unit)
        minimum = minimum.to(unit)
        maximum = maximum.to(unit)

        return MemoryStatistics(avg, minimum, maximum, unit=unit)

    # Overriden.
    @classmethod
    def get_output_type(cls) -> type[MemoryStatistics]:
        return MemoryStatistics


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def _get_memory_usage_pmap(pid: int) -> int:
    """
    Get the current memory usage for the process with `pid`.

    :param pid: The identifier of the process
    :return: The current memory usage in KB
    """
    # sudo pmap 917 | tail -n 1 | awk '/[0-9]K/{print $2}'
    try:
        with subprocess.Popen(
            ["pmap", f"{pid}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        ) as pmap, subprocess.Popen(
            ["tail", "-n", "1"],
            stdin=pmap.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        ) as tail:
            used = subprocess.check_output(
                ["awk", "/[0-9]K/{print $2}"],
                stdin=tail.stdout,
                stderr=subprocess.DEVNULL,
            )
        return int(used.decode("utf-8").strip()[:-1])
    except ValueError:
        return 0
    except FileNotFoundError as e:
        raise RuntimeError(
            f"External program needed to get memory usage was not found: {e}"
        )


def _get_memory_usage_psutil(pid: int) -> int:
    """
    Get the current memory usage for the process with `pid`.

    :param pid: The identifier of the process
    :return: The current memory usage in KB
    """
    try:
        curr_proc = psutil.Process(pid)
        mem_in_kb = curr_proc.memory_info().rss / 1024
        return int(mem_in_kb)
    except psutil.NoSuchProcess:
        return 0
