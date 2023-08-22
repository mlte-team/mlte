"""
mlte/measurement/memory/local_process_memory_consumption.py

Memory consumption measurement for local training processes.
"""

from __future__ import annotations

import subprocess
import time
from typing import Any, Dict, Type

from mlte._private.platform import is_macos, is_windows
from mlte.evidence.metadata import EvidenceMetadata
from mlte.validation.condition import Condition
from mlte.validation.result import Failure, Success
from mlte.value.artifact import Value

from ..process_measurement import ProcessMeasurement

# -----------------------------------------------------------------------------
# Memory Statistics
# -----------------------------------------------------------------------------


class MemoryStatistics(Value):
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
        :type evidence_metadata: EvidenceMetadata
        :param avg: The average memory consumption
        :type avg: int
        :param min: The minimum memory consumption
        :type avg: int
        :param max: The maximum memory consumption
        :type max: int
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
        :rtype: Dict[str, Any]
        """
        return {"avg": self.avg, "min": self.min, "max": self.max}

    @staticmethod
    def deserialize(
        evidence_metadata: EvidenceMetadata, json: Dict[str, Any]
    ) -> MemoryStatistics:
        """
        Deserialize an MemoryStatistics from a JSON object.

        :param evidence_metadata: The generating measurement's metadata
        :type evidence_metadata: EvidenceMetadata
        :param json: The JSON object
        :type json: Dict[str, Any]

        :return: The deserialized instance
        :rtype: MemoryStatistics
        """
        return MemoryStatistics(
            evidence_metadata,
            avg=json["avg"],
            min=json["min"],
            max=json["max"],
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

        :param threshold: The threshold value for maximum consumption
        :type threshold: int

        :return: The Condition that can be used to validate a Value.
        :rtype: Condition
        """
        condition: Condition = Condition(
            "max_consumption_less_than",
            [threshold],
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

        :param threshold: The threshold value for average consumption
        :type threshold: int

        :return: The Condition that can be used to validate a Value.
        :rtype: Condition
        """
        condition: Condition = Condition(
            "average_consumption_less_than",
            [threshold],
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
        :type identifier: str
        """
        super().__init__(self, identifier)
        if is_windows() or is_macos():
            raise RuntimeError(
                f"Measurement {self.metadata.identifier} is not supported on Windows or macOS."
            )

    def __call__(self, pid: int, poll_interval: int = 1) -> MemoryStatistics:
        """
        Monitor memory consumption of process at `pid` until exit.

        :param pid: The process identifier
        :type pid: int
        :param poll_interval: The poll interval, in seconds
        :type poll_interval: int

        :return: The captured statistics
        :rtype: MemoryStatistics
        """
        stats = []
        while True:
            kb = _get_memory_usage(pid)
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


def _get_memory_usage(pid: int) -> int:
    """
    Get the current memory usage for the process with `pid`.

    :param pid: The identifier of the process
    :type pid: int

    :return: The current memory usage in KB
    :rtype: int
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
