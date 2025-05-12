"""
mlte/measurement/cpu/local_process_cpu_utilization.py

CPU utilization measurement for local training processes.
"""

from __future__ import annotations

import subprocess
import time
from subprocess import SubprocessError
from typing import Any, Callable, Optional

from mlte._private.platform import is_windows
from mlte.evidence.external import ExternalEvidence
from mlte.measurement.process_measurement import ProcessMeasurement
from mlte.measurement.units import Quantity, Unit, Units
from mlte.validation.validator import Validator

# -----------------------------------------------------------------------------
# CPUStatistics
# -----------------------------------------------------------------------------


class CPUStatistics(ExternalEvidence):
    """
    The CPUStatistics class encapsulates data
    and functionality for tracking and updating
    CPU consumption statistics for a running process.
    """

    def __init__(
        self,
        avg: float,
        min: float,
        max: float,
        unit: Unit = Units.percent,
    ):
        """
        Initialize a CPUStatistics instance.

        :param avg: The average utilization
        :param min: The minimum utilization
        :param max: The maximum utilization
        :param unit: the unit the values comes in, as a value from Units; defaults to Units.percent
        """
        super().__init__()

        self.avg = Quantity(avg, unit)
        """The average CPU utilization, as a proportion."""

        self.min = Quantity(min, unit)
        """The minimum CPU utilization, as a proportion."""

        self.max = Quantity(max, unit)
        """The maximum CPU utilization, as a proportion."""

        self.unit = unit
        """The unit being used for all values."""

    def serialize(self) -> dict[str, Any]:
        """
        Serialize an CPUStatistics to a JSON object.

        :return: The JSON object
        """
        return {
            "avg": self.avg.magnitude,
            "min": self.min.magnitude,
            "max": self.max.magnitude,
            "unit": self.unit,
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> CPUStatistics:
        """
        Deserialize an CPUStatistics from a JSON object.

        :param data: The JSON object

        :return: The deserialized instance
        """
        return CPUStatistics(
            avg=data["avg"], min=data["min"], max=data["max"], unit=data["unit"]
        )

    def __str__(self) -> str:
        """Return a string representation of CPUStatistics."""
        s = ""
        s += f"Average: {self.avg:.2f}\n"
        s += f"Minimum: {self.min:.2f}\n"
        s += f"Maximum: {self.max:.2f}"
        return s

    @classmethod
    def max_utilization_less_than(
        cls, threshold: float, unit: Unit = Units.percent
    ) -> Validator:
        """
        Construct and invoke a validator for maximum CPU utilization.

        :param threshold: The threshold value for maximum utilization
        :param unit: the unit the threshold comes in, as a value from Units; defaults to Units.percent

        :return: The Validator that can be used to validate a Value.
        """
        threshold_w_unit = Quantity(threshold, unit)
        bool_exp: Callable[[CPUStatistics], bool] = (
            lambda stats: stats.max < threshold_w_unit
        )
        validator: Validator = Validator.build_validator(
            bool_exp=bool_exp,
            thresholds=[threshold_w_unit],
            success=f"Maximum utilization below threshold {threshold_w_unit:.2f}",
            failure=f"Maximum utilization exceeds threshold {threshold_w_unit:.2f}",
            input_types=[CPUStatistics],
        )
        return validator

    @classmethod
    def average_utilization_less_than(
        cls, threshold: float, unit: Unit = Units.percent
    ) -> Validator:
        """
        Construct and invoke a validator for average CPU utilization.

        :param threshold: The threshold value for average utilization
        :param unit: the unit the threshold comes in, as a value from Units; defaults to Units.percent

        :return: The Validator that can be used to validate a Value.
        """
        threshold_w_unit = Quantity(threshold, unit)
        bool_exp: Callable[[CPUStatistics], bool] = (
            lambda stats: stats.avg < threshold_w_unit
        )
        validator: Validator = Validator.build_validator(
            bool_exp=bool_exp,
            thresholds=[threshold_w_unit],
            success=f"Average utilization below threshold {threshold:.2f}",
            failure=f"Average utilization exceeds threshold {threshold:.2f}",
            input_types=[CPUStatistics],
        )
        return validator


# -----------------------------------------------------------------------------
# LocalProcessCPUUtilization
# -----------------------------------------------------------------------------


class LocalProcessCPUUtilization(ProcessMeasurement):
    """Measures CPU utilization for a local process."""

    def __init__(self, identifier: Optional[str] = None):
        """
        Initialize a new LocalProcessCPUUtilization measurement.

        :param identifier: A unique identifier for the measurement
        """
        super().__init__(identifier)
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
