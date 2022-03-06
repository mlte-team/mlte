"""
Memory consumption measurement for local training processes.
"""

import time
import subprocess

from ..property import Property
from ...platform.os import is_windows


class MemoryStatistics:
    """
    The MemoryStatistics class encapsulates data
    and functionality for tracking and updating memory
    consumption statistics for a running process.
    """

    def __init__(self, avg: float, min: int, max: int):
        """
        Initialize a MemoryStatistics instance.

        :param avg: The average memory consumtion (bytes)
        :type avg: float
        :param min: The minimum memory consumption (bytes)
        :type avg: float
        :param max: The maximum memory consumption (bytes)
        :type max: float
        """
        # The statistics
        self.avg = avg
        self.min = min
        self.max = max

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
    :param pid The identifier of the process
    :return The current memory usage in KB
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


class ProcessLocalMemoryConsumption(Property):
    """Measure memory consumption for a local training process."""

    def __init__(self):
        """Initialize a ProcessLocalMemoryConsumption instance."""
        super().__init__("ProcessLocalMemoryConsumption")
        if is_windows():
            raise RuntimeError(
                f"Property {self.name} is not supported on Windows."
            )

    def __call__(self, pid: int, poll_interval: int = 1) -> MemoryStatistics:
        """
        Monitor memory consumption of process at `pid` until exit.

        :param pid: The process identifier
        :type pid: int
        :param poll_interval: The poll interval, in seconds
        :type poll_interval: int

        :return The collection of memory usage statistics
        :rtype: MemoryStatistics
        """
        stats = []
        while True:
            kb = _get_memory_usage(pid)
            if kb == 0:
                break
            stats.append(kb)
            time.sleep(poll_interval)

        return MemoryStatistics(sum(stats) / len(stats), min(stats), max(stats))
