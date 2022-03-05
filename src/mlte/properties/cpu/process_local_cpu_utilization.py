"""
CPU utilization measurement for local training processes.
"""

import time
import subprocess
from subprocess import SubprocessError

from ..property import Property


class CPUStatistics:
    """
    The CPUStatistics class encapsulates data
    and functionality for tracking and updating
    CPU consumption statistics for a running process.
    """

    def __init__(self, avg: float, min: float, max: float):
        """
        Initialize a CPUStatistics instance
        :param avg The average utilization
        :param min The minimum utilization
        :param max The maximum utilization
        """
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
    :param pid The identifier of the process
    :return The current CPU utilization as percentage
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


class ProcessLocalCpuUtilization(Property):
    """
    TODO
    """

    def __init__(self):
        super().__init__("ProcessLocalCPUUtilization")

    def __call__(self, pid: int, poll_interval: int = 1) -> CPUStatistics:
        """
        Monitor the CPU utilization of process at `pid` until exit.
        :param pid The process identifier
        :param poll_interval The poll interval in seconds
        :return The collection of CPU usage statistics
        """
        stats = []
        while True:
            util = _get_cpu_usage(pid)
            if util < 0.0:
                break
            stats.append(util)
            time.sleep(poll_interval)

        return CPUStatistics(sum(stats) / len(stats), min(stats), max(stats))
