"""
CPU utilization measurement for local training processes.
"""

import time
import subprocess
from typing import Dict, Any
from subprocess import SubprocessError

from ..measurement import Measurement
from ..evaluation import EvaluationResult
from ..validation import Validator, Success, Failure
from ..._private.platform import is_windows


class CPUStatistics(EvaluationResult):
    """
    The CPUStatistics class encapsulates data
    and functionality for tracking and updating
    CPU consumption statistics for a running process.
    """

    def __init__(
        self, measurement: Measurement, avg: float, min: float, max: float
    ):
        """
        Initialize a CPUStatistics instance.

        :param measurement: The generating measurement
        :type measurement: Measurement
        :param avg: The average utilization
        :type avg: float
        :param min: The minimum utilization
        :type min: float
        :param max: The maximum utilization
        :type max: float
        """
        super().__init__(measurement)

        self.avg = avg
        """The average CPU utilization, as a proportion."""

        self.min = min
        """The minimum CPU utilization, as a proportion."""

        self.max = max
        """The maximum CPU utilization, as a proportion."""

    def __str__(self) -> str:
        """Return a string representation of CPUStatistics."""
        s = ""
        s += f"Average: {self.avg:.2f}%\n"
        s += f"Minimum: {self.min:.2f}%\n"
        s += f"Maximum: {self.max:.2f}%"
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
            ["ps", "-p", f"{pid}", "-o", "%cpu"], stderr=subprocess.DEVNULL
        ).decode("utf-8")
        return float(stdout.strip().split("\n")[1].strip())
    except SubprocessError:
        return -1.0
    except ValueError:
        return -1.0


class LocalProcessCPUUtilization(Measurement):
    """Measures CPU utilization for a local process."""

    def __init__(self):
        """Initialize a new LocalProcessCPUUtilization measurement."""
        super().__init__("LocalProcessCPUUtilization")
        if is_windows():
            raise RuntimeError(
                f"Measurement {self.name} is not supported on Windows."
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
            stats.append(util / 100.0)
            time.sleep(poll_interval)

        return {
            "avg_utilization": sum(stats) / len(stats),
            "min_utilization": min(stats),
            "max_utilization": max(stats),
        }

    def semantics(self, data: Dict[str, Any]) -> CPUStatistics:
        """
        Provide semantics for measurement output.

        :param data: Measurement output data
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

    def with_validator_max_utilization_not_greater_than(
        self, threshold: float
    ) -> Measurement:
        """
        Add a validator for maximum CPU utilization.

        :param threshold: The threshold value for maximum utilization
        :type threshold: float

        :return: The measurement instance (`self`)
        :rtype: Measurement
        """
        return self.with_validator(
            Validator(
                "MaximumUtilization",
                lambda stats: Success(
                    f"Maximum utilization {stats.max:.2f} "
                    f"below threshold {threshold:.2f}"
                )
                if stats.max <= threshold
                else Failure(
                    (
                        f"Maximum utilization {stats.max:.2f} "
                        f"exceeds threshold {threshold:.2f}"
                    )
                ),
            )
        )

    def with_validator_avg_utilization_not_greater_than(
        self, threshold: float
    ) -> Measurement:
        """
        Add a validator for average CPU utilization.

        :param threshold: The threshold value for average utilization
        :type threshold: float

        :return: The measurement instance (`self`)
        :rtype: Measurement
        """
        return self.with_validator(
            Validator(
                "AverageUtilization",
                lambda stats: Success(
                    f"Average utilization {stats.max:.2f} "
                    f"below threshold {threshold:.2f}"
                )
                if stats.avg <= threshold
                else Failure(
                    (
                        f"Average utilization {stats.avg:.2f} "
                        "exceeds threshold {threshold:.2f}"
                    )
                ),
            )
        )
