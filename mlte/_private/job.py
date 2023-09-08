"""
mlte/_private/job.py

Optional helpers that can be used to start external processes.
"""

import subprocess
import sys
import threading
from pathlib import Path
from typing import List


def _get_interpreter_path() -> Path:
    """
    Get the path to the current interpreter.

    :return: Path to the Python executable currently being used.
    :rtype: Path
    """
    return Path(sys.executable)


def spawn_python_job(script_path: str, arguments: List[str]) -> int:
    """
    Spawn the Python job from the given script and arguments, and return its process identifier.

    :param script: The full path to a Python script with the training or equivalent process to run.
    :type script: str

    :param arguments: A list of string arguments for the process.
    :type arguments: List[str[]

    :return: Process id of the process that was created.
    :rtype: int
    """
    python_executable = str(_get_interpreter_path())
    new_arguments = [script_path, *arguments]
    return spawn_job(python_executable, new_arguments)


def spawn_job(executable: str, arguments: List[str]) -> int:
    """
    Spawn a process from the given executable and arguments, and return its process identifier.

    :param script: The full path to an executable process to run.
    :type script: str

    :param arguments: A list of string arguments for the process.
    :type arguments: List[str[]

    :return: Process id of the process that was created.
    :rtype: int
    """
    command = [executable, *arguments]

    p = subprocess.Popen(command)
    thread = threading.Thread(target=lambda: p.wait())
    thread.start()
    return p.pid
