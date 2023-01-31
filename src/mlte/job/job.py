import sys
import os
import threading
import subprocess
from typing import List
from pathlib import Path


def _interpreter_path() -> Path:
    """Get the path to the current interpreter."""
    return Path(sys.executable)


def _script_path(script_file: str) -> Path:
    """Get the path to the training script."""
    return (Path(os.path.join(os.getcwd(), script_file))).absolute()


def spawn_python_training_job(script: str, arguments: List[str]) -> int:
    """Spawn the Python job from the given script and arguments, and return its process identifier."""
    python = _interpreter_path()
    script_path = _script_path(script)
    command = [python, script_path]
    command.extend(arguments)

    p = subprocess.Popen(command)
    thread = threading.Thread(target=lambda: p.wait())
    thread.start()
    return p.pid
