import sys
import os
import threading
import subprocess
from typing import List
from pathlib import Path


def _get_interpreter_path() -> Path:
    """Get the path to the current interpreter."""
    return Path(sys.executable)


def spawn_python_job(script_path: str, arguments: List[str]) -> int:
    """Spawn the Python job from the given script and arguments, and return its process identifier."""
    python = _get_interpreter_path()
    command = [python, script_path]
    command.extend(arguments)

    p = subprocess.Popen(command)
    thread = threading.Thread(target=lambda: p.wait())
    thread.start()
    return p.pid
