"""
mlte/measurement/memory/local_process_memory_consumption.py

Memory consumption measurement for local training processes.
"""

from __future__ import annotations

import subprocess
import time
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
# Memory Statistics
# -----------------------------------------------------------------------------


class MemoryStatistics(ExternalEvidence):
    """
    The MemoryStatistics class encapsulates data
    and functionality for tracking and updating memory
    consumption statistics for a running process.
    """

    def __init__(
        self, avg: int, min: int, max: int, unit: Unit = Units.kilobyte
    ):
        """
        Initialize a MemoryStatistics instance.

        :param avg: The average memory consumption
        :param min: The minimum memory consumption
        :param max: The maximum memory consumption
        :param unit: the unit the values comes in, as a value from Units; defaults to Units.kilobyte
        """
        super().__init__()

        self.avg = Quantity(avg, unit)
        """The average memory consumption."""

        self.min = Quantity(min, unit)
        """The minimum memory consumption."""

        self.max = Quantity(max, unit)
        """The maximum memory consumption."""

        self.unit = unit
        """The unit being used for all values."""

    def serialize(self) -> dict[str, Any]:
        """
        Serialize an MemoryStatistics to a JSON object.

        :return: The JSON object
        """
        return {
            "avg": self.avg.magnitude,
            "min": self.min.magnitude,
            "max": self.max.magnitude,
            "unit": unit_to_str(self.unit),
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> MemoryStatistics:
        """
        Deserialize an MemoryStatistics from a JSON object.

        :param data: The JSON object

        :return: The deserialized instance
        """
        unit = str_to_unit(data["unit"])
        return MemoryStatistics(
            avg=data["avg"],
            min=data["min"],
            max=data["max"],
            unit=unit if unit else Units.kilobyte,
        )

    def __str__(self) -> str:
        """Return a string representation of MemoryStatistics."""
        s = ""
        s += f"Average: {self.avg}\n"
        s += f"Minimum: {self.min}\n"
        s += f"Maximum: {self.max}"
        return s

    @classmethod
    def max_consumption_less_than(
        cls, threshold: int, unit: Unit = Units.kilobyte
    ) -> Validator:
        """
        Construct and invoke a validator for maximum memory consumption.

        :param threshold: The threshold value for maximum consumption
        :param unit: the unit the threshold comes in, as a value from Units; defaults to Units.kilobyte

        :return: The Validator that can be used to validate a Value.
        """
        threshold_w_unit = Quantity(threshold, unit)
        bool_exp: Callable[[MemoryStatistics], bool] = (
            lambda stats: stats.max < threshold_w_unit
        )
        validator: Validator = Validator.build_validator(
            bool_exp=bool_exp,
            thresholds=[threshold_w_unit],
            success=f"Maximum consumption below threshold {threshold_w_unit}",
            failure=f"Maximum consumption exceeds threshold {threshold_w_unit}",
            input_types=[MemoryStatistics],
        )
        return validator

    @classmethod
    def average_consumption_less_than(
        cls, threshold: float, unit: Unit = Units.kilobyte
    ) -> Validator:
        """
        Construct and invoke a validator for average memory consumption.

        :param threshold: The threshold value for average consumption, in KB
        :param unit: the unit the threshold comes in, as a value from Units; defaults to Units.kilobyte

        :return: The Validator that can be used to validate a Value.
        """
        threshold_w_unit = Quantity(threshold, unit)
        bool_exp: Callable[[MemoryStatistics], bool] = (
            lambda stats: stats.avg < threshold_w_unit
        )
        validator: Validator = Validator.build_validator(
            bool_exp=bool_exp,
            thresholds=[threshold_w_unit],
            success=f"Average consumption below threshold {threshold_w_unit}",
            failure=f"Average consumption exceeds threshold {threshold_w_unit}",
            input_types=[MemoryStatistics],
        )
        return validator


# -----------------------------------------------------------------------------
# LocalProcessMemoryConsumption
# -----------------------------------------------------------------------------


class LocalProcessMemoryConsumption(ProcessMeasurement):
    """Measure memory consumption for a local training process."""

    def __init__(self, identifier: Optional[str] = None):
        """
        Initialize a LocalProcessMemoryConsumption instance.

        :param identifier: A unique identifier for the measurement
        """
        super().__init__(identifier)

    # Overriden.
    def __call__(self, pid: int, poll_interval: int = 1) -> MemoryStatistics:
        """
        Monitor memory consumption of process at `pid` until exit.

        :param pid: The process identifier
        :param poll_interval: The poll interval, in seconds
        :return: The captured statistics
        """
        stats = []
        while True:
            kb = _get_memory_usage_psutil(pid)
            if kb == 0:
                break
            stats.append(kb)
            time.sleep(poll_interval)

        return MemoryStatistics(
            avg=int(sum(stats) / len(stats)),
            min=min(stats),
            max=max(stats),
            unit=Units.kilobyte,
        )

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
