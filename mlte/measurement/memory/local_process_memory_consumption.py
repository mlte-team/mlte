"""
mlte/measurement/memory/local_process_memory_consumption.py

Memory consumption measurement for local training processes.
"""

from __future__ import annotations

import subprocess
import time
from typing import Any, Dict, Type

import psutil

from mlte.evidence.metadata import EvidenceMetadata
from mlte.measurement.process_measurement import ProcessMeasurement
from mlte.spec.condition import Condition
from mlte.validation.result import Failure, Success
from mlte.value.base import ValueBase

# -----------------------------------------------------------------------------
# Memory Statistics
# -----------------------------------------------------------------------------


class MemoryStatistics(ValueBase):
    """
    The MemoryStatistics class encapsulates data
    and functionality for tracking and updating memory
    consumption statistics for a running process.
    """

    def __init__(
        self,
        evidence_metadata: EvidenceMetadata,
        avg: int,
        min: int,
        max: int,
    ):
        """
        Initialize a MemoryStatistics instance.

        :param evidence_metadata: The generating measurement's metadata
        :param avg: The average memory consumption, in KB
        :param min: The minimum memory consumption, in KB
        :param max: The maximum memory consumption, in KB
        """
        super().__init__(self, evidence_metadata)

        self.avg = avg
        """The average memory consumption (KB)."""

        self.min = min
        """The minimum memory consumption (KB)."""

        self.max = max
        """The maximum memory consumption (KB)."""

    def serialize(self) -> Dict[str, Any]:
        """
        Serialize an MemoryStatistics to a JSON object.

        :return: The JSON object
        """
        return {"avg": self.avg, "min": self.min, "max": self.max}

    @staticmethod
    def deserialize(
        evidence_metadata: EvidenceMetadata, data: Dict[str, Any]
    ) -> MemoryStatistics:
        """
        Deserialize an MemoryStatistics from a JSON object.

        :param evidence_metadata: The generating measurement's metadata
        :param data: The JSON object

        :return: The deserialized instance
        """
        return MemoryStatistics(
            evidence_metadata,
            avg=data["avg"],
            min=data["min"],
            max=data["max"],
        )

    def __str__(self) -> str:
        """Return a string representation of MemoryStatistics."""
        s = ""
        s += f"Average: {self.avg}\n"
        s += f"Minimum: {self.min}\n"
        s += f"Maximum: {self.max}"
        return s

    @classmethod
    def max_consumption_less_than(cls, threshold: int) -> Condition:
        """
        Construct and invoke a condition for maximum memory consumption.

        :param threshold: The threshold value for maximum consumption, in KB

        :return: The Condition that can be used to validate a Value.
        """
        condition: Condition = Condition.build_condition(
            lambda stats: Success(
                f"Maximum consumption {stats.max} "
                f"below threshold {threshold}"
            )
            if stats.max < threshold
            else Failure(
                (
                    f"Maximum consumption {stats.max} "
                    f"exceeds threshold {threshold}"
                )
            ),
        )
        return condition

    @classmethod
    def average_consumption_less_than(cls, threshold: float) -> Condition:
        """
        Construct and invoke a condition for average memory consumption.

        :param threshold: The threshold value for average consumption, in KB

        :return: The Condition that can be used to validate a Value.
        """
        condition: Condition = Condition.build_condition(
            lambda stats: Success(
                f"Average consumption {stats.avg} "
                f"below threshold {threshold}"
            )
            if stats.avg <= threshold
            else Failure(
                (
                    f"Average consumption {stats.avg} "
                    f"exceeds threshold {threshold}"
                )
            ),
        )
        return condition


# -----------------------------------------------------------------------------
# LocalProcessMemoryConsumption
# -----------------------------------------------------------------------------


class LocalProcessMemoryConsumption(ProcessMeasurement):
    """Measure memory consumption for a local training process."""

    def __init__(self, identifier: str):
        """
        Initialize a LocalProcessMemoryConsumption instance.

        :param identifier: A unique identifier for the measurement
        """
        super().__init__(self, identifier)

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
            self.metadata,
            avg=int(sum(stats) / len(stats)),
            min=min(stats),
            max=max(stats),
        )

    @classmethod
    def value(self) -> Type[MemoryStatistics]:
        """Returns the class type object for the Value produced by the Measurement."""
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
