"""CPU utilization measurement for local training processes."""

from __future__ import annotations

import subprocess
import time
from subprocess import SubprocessError
from typing import Optional

from mlte._private.platform import is_windows
from mlte.measurement.common import CommonStatistics
from mlte.measurement.process_measurement import ProcessMeasurement
from mlte.measurement.units import Unit, Units

# -----------------------------------------------------------------------------
# CPUStatistics
# -----------------------------------------------------------------------------


class CPUStatistics(CommonStatistics):
    """
    The CPUStatistics class encapsulates data
    and functionality for tracking and updating
    CPU utilization statistics for a running process.
    """

    DEFAULT_UNIT = Units.percent

    def __init__(
        self,
        avg: float,
        min: float,
        max: float,
        unit: Unit = DEFAULT_UNIT,
    ):
        """
        Initialize a CPUStatistics instance.

        :param avg: The average utilization
        :param min: The minimum utilization
        :param max: The maximum utilization
        :param unit: the unit the values comes in, as a value from Units; defaults to Units.percent
        """
        super().__init__(avg, min, max, unit)


# -----------------------------------------------------------------------------
# LocalProcessCPUUtilization
# -----------------------------------------------------------------------------


class LocalProcessCPUUtilization(ProcessMeasurement):
    """Measures CPU utilization for a local process."""

    def __init__(
        self, identifier: Optional[str] = None, group: Optional[str] = None
    ):
        """
        Initialize a new LocalProcessCPUUtilization measurement.

        :param identifier: A unique identifier for the measurement
        :param group: An optional group id, if we want to group this measurement with others.
        """
        super().__init__(identifier, group)
        if is_windows():
            raise RuntimeError(
                f"Measurement for {self.evidence_metadata.test_case_id if self.evidence_metadata else 'this'} is not supported on Windows."
            )

    # Overriden.
    def __call__(self, pid: int, poll_interval: int = 1) -> CPUStatistics:
        """
        Monitor the CPU utilization of process at `pid` until exit.

        :param pid: The process identifier
        :param poll_interval: The poll interval in seconds

        :return: The collection of CPU usage statistics
        """
        stats = []
        while True:
            util = _get_cpu_usage(pid)
            if util < 0.0:
                break
            stats.append(util / 100.0)
            time.sleep(poll_interval)

        return CPUStatistics(
            avg=sum(stats) / len(stats),
            min=min(stats),
            max=max(stats),
            unit=Units.percent,
        )

    # Overriden.
    @classmethod
    def get_output_type(cls) -> type[CPUStatistics]:
        return CPUStatistics


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def _get_cpu_usage(pid: int) -> float:
    """
    Get the current CPU usage for the process with `pid`.

    :param pid: The identifier of the process

    :return: The current CPU utilization as percent
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
    except FileNotFoundError as e:
        raise RuntimeError(
            f"External program needed to get CPU usage was not found: {e}"
        )
