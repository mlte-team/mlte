"""
CPU utilization measurement for local training processes.
"""

import time
import subprocess
from typing import Dict, Any
from subprocess import SubprocessError

from ..property import Property
from ..result import EvaluationResult
from ...platform.os import is_windows


class CPUStatistics(EvaluationResult):
    """
    The CPUStatistics class encapsulates data
    and functionality for tracking and updating
    CPU consumption statistics for a running process.
    """

    def __init__(self, property: Property, avg: float, min: float, max: float):
        """
        Initialize a CPUStatistics instance.

        :param property: The generating property
        :type property: Property
        :param avg: The average utilization
        :type avg: float
        :param min: The minimum utilization
        :type min: float
        :param max: The maximum utilization
        :type max: float
        """
        super().__init__(property)

        self.avg = avg
        self.min = min
        self.max = max

    def __str__(self) -> str:
        """Return a string representation of CPUStatistics."""
        s = ""
        s += f"Average: {self.avg:.1f}%\n"
        s += f"Minimum: {self.min:.1f}%\n"
        s += f"Maximum: {self.max:.1f}%"
        return s


def _get_cpu_usage(pid: int) -> float:
    """
    Get the current CPU usage for the process with `pid`.

    :param pid: The identifier of the process
    :type pid: int

    :return: The current CPU utilization as percentage
    :rtype: float
    """
    try:
        stdout = subprocess.check_output(
            ["ps", "-p", f"{pid}", "-o", "%cpu"]
        ).decode("utf-8")
        return float(stdout.strip().split("\n")[1].strip())
    except SubprocessError:
        return -1.0
    except ValueError:
        return -1.0


class LocalProcessCPUUtilization(Property):
    """Measures CPU utilization for a local training process."""

    def __init__(self):
        """Initialize a new LocalProcessCPUUtilization property."""
        super().__init__("LocalProcessCPUUtilization")
        if is_windows():
            raise RuntimeError(
                f"Property {self.name} is not supported on Windows."
            )

    def __call__(self, pid: int, poll_interval: int = 1) -> Dict[str, Any]:
        """
        Monitor the CPU utilization of process at `pid` until exit.

        :param pid: The process identifier
        :type pid: int
        :param poll_interval: The poll interval in seconds
        :type poll_interval: int

        :return: The collection of CPU usage statistics
        :rtype: Dict
        """
        stats = []
        while True:
            util = _get_cpu_usage(pid)
            if util < 0.0:
                break
            stats.append(util)
            time.sleep(poll_interval)

        return {
            "avg_utilization": sum(stats) / len(stats),
            "min_utilization": min(stats),
            "max_utilization": max(stats),
        }

    def semantics(self, data: Dict[str, Any]) -> CPUStatistics:
        """
        Provide semantics for property output.

        :param data: Property output data
        :type data: Dict

        :return: CPU utilization statistics
        :rtype: CPUStatistics
        """
        assert "avg_utilization" in data, "Broken invariant."
        assert "min_utilization" in data, "Broken invariant."
        assert "max_utilization" in data, "Broken invariant."
        return CPUStatistics(
            self,
            avg=data["avg_utilization"],
            min=data["min_utilization"],
            max=data["max_utilization"],
        )
