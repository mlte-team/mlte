"""
Memory consumption measurement for local training processes.
"""

import time
import subprocess
from typing import Dict, Any

from ..property import Property
from ..evaluation import EvaluationResult
from ..validation import Validator, Success, Failure
from ...platform.os import is_windows


class MemoryStatistics(EvaluationResult):
    """
    The MemoryStatistics class encapsulates data
    and functionality for tracking and updating memory
    consumption statistics for a running process.
    """

    def __init__(self, property: Property, avg: float, min: int, max: int):
        """
        Initialize a MemoryStatistics instance.

        :param property: The generating property
        :type property: Property
        :param avg: The average memory consumption
        :type avg: float
        :param min: The minimum memory consumption
        :type avg: float
        :param max: The maximum memory consumption
        :type max: float
        """
        super().__init__(property)

        self.avg = avg
        """The average memory consumption (KB)."""

        self.min = min
        """The minimum memory consumption (KB)."""

        self.max = max
        """The maximum memory consumption (KB)."""

    def __str__(self) -> str:
        """Return a string representation of MemoryStatistics."""
        s = ""
        s += f"Average: {int(self.avg)}\n"
        s += f"Minimum: {self.min}\n"
        s += f"Maximum: {self.max}"
        return s


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
            ["pmap", f"{pid}"], stdout=subprocess.PIPE
        ) as pmap, subprocess.Popen(
            ["tail", "-n", "1"], stdin=pmap.stdout, stdout=subprocess.PIPE
        ) as tail:
            used = subprocess.check_output(
                ["awk", "/[0-9]K/{print $2}"], stdin=tail.stdout
            )
        return int(used.decode("utf-8").strip()[:-1])
    except ValueError:
        return 0


class LocalProcessMemoryConsumption(Property):
    """Measure memory consumption for a local training process."""

    def __init__(self):
        """Initialize a LocalProcessMemoryConsumption instance."""
        super().__init__("LocalProcessMemoryConsumption")
        if is_windows():
            raise RuntimeError(
                f"Property {self.name} is not supported on Windows."
            )

    def __call__(self, pid: int, poll_interval: int = 1) -> Dict[str, Any]:
        """
        Monitor memory consumption of process at `pid` until exit.

        :param pid: The process identifier
        :type pid: int
        :param poll_interval: The poll interval, in seconds
        :type poll_interval: int

        :return The collection of memory usage statistics
        :rtype: Dict
        """
        stats = []
        while True:
            kb = _get_memory_usage(pid)
            if kb == 0:
                break
            stats.append(kb)
            time.sleep(poll_interval)

        return {
            "avg_consumption": sum(stats) / len(stats),
            "min_consumption": min(stats),
            "max_consumption": max(stats),
        }

    def semantics(self, data: Dict[str, Any]) -> MemoryStatistics:
        """
        Provide semantics for property output.

        :param data: Property output data
        :type data: Dict

        :return: Memory consumption statistics
        :rtype: MemoryStatistics
        """
        assert "avg_consumption" in data, "Broken invariant."
        assert "min_consumption" in data, "Broken invariant."
        assert "max_consumption" in data, "Broken invariant."
        return MemoryStatistics(
            self,
            avg=data["avg_consumption"],
            min=data["min_consumption"],
            max=data["max_consumption"],
        )

    def add_validator_max_consumption_not_greater_than(self, threshold: int):
        """
        Add a validator for maximum memory consumption.

        :param threshold: The threshold value for maximum consumption
        :type threshold: int
        """
        self.add_validator(
            Validator(
                "MaximumConsumption",
                lambda stats: Success()
                if stats.max <= threshold
                else Failure(
                    (
                        f"Maximum consumption {stats.max}"
                        "exceeds threshold {threshold}"
                    )
                ),
            )
        )

    def add_validator_avg_consumption_not_greater_than(self, threshold: float):
        """
        Add a validator for average memory consumption.

        :param threshold: The threshold value for average consumption
        :type threshold: int
        """
        self.add_validator(
            Validator(
                "AverageConsumption",
                lambda stats: Success()
                if stats.avg <= threshold
                else Failure(
                    (
                        f"Average utilization {stats.avg}"
                        "exceeds threshold {threshold}"
                    )
                ),
            )
        )
