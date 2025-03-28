"""
mlte/measurement/process_measurement.py

Base class for measurement of external processes asynchronously.
"""

from __future__ import annotations

import threading
import time
from abc import ABC, abstractmethod
from typing import List, Optional

from mlte._private import job
from mlte.evidence.artifact import Evidence
from mlte.measurement.measurement import Measurement

# -----------------------------------------------------------------------------
# ProcessMeasurement
# -----------------------------------------------------------------------------


class ProcessMeasurement(Measurement, ABC):
    """Base class to be extended to measure external processes."""

    @staticmethod
    def start_script(script: str, arguments: List[str]) -> int:
        """
        Initialize an external Python process running training or similar script.

        :param script: The full path to a Python script with the training or equivalent process to run.
        :param arguments: A list of string arguments for the process.
        :return: the id of the process that was created.
        """
        return job.spawn_python_job(script, arguments)

    @staticmethod
    def start_process(process: str, arguments: List[str]) -> int:
        """
        Initialize an external process running training or similar.

        :param process: The full path to a process to run.
        :param arguments: A list of string arguments for the process.
        :return: the id of the process that was created.
        """
        return job.spawn_job(process, arguments)

    def __init__(self, test_case_id: Optional[str] = None):
        """
        Initialize a new ProcessMeasurement measurement.

        :param test_case_id: A unique identifier for the measurement
        """
        super().__init__(test_case_id)

        self.thread: Optional[threading.Thread] = None
        """Thread that will be used to run the measurement process."""

        self.stored_value: Optional[Evidence] = None
        """The result of the measurement."""

        self.error: str = ""
        """Any error messages from running measurement."""

    # Overriden.
    @abstractmethod
    def __call__(self, pid: int, *args, **kwargs) -> Evidence:
        """Calls for process based measurement will always have pid as the first argument.."""
        raise NotImplementedError(
            "Cannot evaluate abstract process measurement."
        )

    def evaluate(self, command: list[str], *args, **kwargs) -> Evidence:
        """Evaluate by starting the given process and waiting for it to complete."""
        if len(command) < 1:
            raise RuntimeError(
                f"Command list must as least have one item: {command}"
            )

        pid = ProcessMeasurement.start_process(command[0], command[1:])
        self.evaluate_async(pid, *args, **kwargs)
        evidence = self.wait_for_output()
        return evidence

    def evaluate_async(self, pid: int, *args, **kwargs):
        """
        Monitor an external process at `pid` in a separate thread until it stops.
        Equivalent to evaluate(), but does not return the value immediately as it works in the background.

        :param pid: The process identifier
        """

        # Evaluate the measurement
        self.error = ""
        self.stored_value = None
        self.thread = threading.Thread(
            target=lambda: self._evaluate_thread(pid, *args, **kwargs)
        )
        self.thread.start()

    def _evaluate_thread(self, pid, *args, **kwargs):
        """
        Runs the evaluate method that should implement the measurement, and stores its results when it finishes.
        """
        try:
            self.stored_value = super().evaluate(pid, *args, **kwargs)
        except Exception as e:
            self.error = f"Could not evaluate process: {e}"

    def wait_for_output(self, poll_interval: int = 1) -> Evidence:
        """
        Needed to get the output of a measurement executed in parallel using evaluate_async. Waits for the thread to finish.

        :param poll_interval: The poll interval in seconds
        :return: The resulting value of measurement execution, with semantics
        """
        # Wait for thread to finish, and return results once it is done.
        if self.thread is None:
            raise Exception(
                "Can't wait for value, no process is currently running."
            )
        while self.thread.is_alive():
            time.sleep(poll_interval)

        # If an exception was raised, return it here as an exception as well.
        if self.error != "":
            raise RuntimeError(self.error)

        if self.stored_value is None:
            raise Exception("No valid value was returned from measurement.")
        return self.stored_value
