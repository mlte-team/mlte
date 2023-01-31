"""
Base class for measurement of external processes.
"""

from __future__ import annotations

import threading
import time
from typing import List

from .measurement import Measurement
from .result import Result
from mlte._private.platform import is_windows
from mlte.job import job

# -----------------------------------------------------------------------------
# ProcessMeasurement
# -----------------------------------------------------------------------------

class ProcessMeasurement(Measurement):
    """Base class to be extended to measure external processes."""

    @staticmethod
    def start_process(script: str, arguments: List[str]) -> int:
        """
        Initialize an external process running training or similar script.

        :param script: The path to a Python script with the training or equivalent process to run.
        :type identifier: str

        :param arguments: A list of string arguments for the process.
        :type identifier: List[str[]
        """        
        return job.spawn_python_training_job(script, arguments)

    def __init__(self, instance: ProcessMeasurement, identifier: str):
        """
        Initialize a new ProcessMeasurement measurement.

        :param identifier: A unique identifier for the measurement
        :type identifier: str
        """
        super().__init__(instance, identifier)        
        if is_windows():
            raise RuntimeError(
                f"Measurement {self.name} is not supported on Windows."
            )
        self.thread = None
        self.results = None

    def evaluate_async(self, pid:int, *args, **kwargs):
        """
        Monitor an external process at `pid` until in a separate thread.

        :param pid: The process identifier
        :type pid: int

        :return: The result of measurement execution, with semantics
        :rtype: Result
        """

        # Evaluate the measurement
        try:
            self.thread = threading.Thread(target=lambda: self._run_call(pid, *args, **kwargs))
            self.thread.start()

            return 
        except FileNotFoundError as e:
            raise RuntimeError("External program needed to evaluate was not found: " + str(e))            
 
    def _run_call(self, pid, *args, **kwargs):
        """
        Runs the internall call, and stores its results when it finishes.
        """
        self.results = self.__call__(pid, *args, **kwargs)

    def wait_for_result(self, *args, **kwargs) -> Result:
        """
        Evaluate a measurement done by an external process, by waiting for the thread to finish.

        :return: The result of measurement execution, with semantics
        :rtype: Result
        """
        # Wait for thread to finish, and return results once it is done.
        while self.thread.is_alive():
            time.sleep(1)
        return self.results        