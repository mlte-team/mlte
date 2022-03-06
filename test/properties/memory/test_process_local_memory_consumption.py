"""
Unit test for ProcessLocalMemoryConsumption property.
"""

import os
import time
import pytest
import threading
import subprocess

from mlte.platform.os import is_windows, is_nix
from mlte.properties import ProcessLocalMemoryConsumption

from ...support.meta import path_to_support

# The spin duration, in seconds
SPIN_DURATION = 5


def spin_for(seconds: int):
    """Run the spin.py program for `seconds`."""
    path = os.path.join(path_to_support(), "spin.py")
    prog = subprocess.Popen(["python", path, f"{seconds}"])
    thread = threading.Thread(target=lambda: prog.wait())
    thread.start()
    return prog


@pytest.mark.skipif(
    is_windows(), reason="ProcessLocalCPUUtilization not supported on Windows."
)
def test_memory_nix():
    start = time.time()

    prog = spin_for(5)
    prop = ProcessLocalMemoryConsumption()

    # Capture memory consumption; blocks until process exit
    stat = prop(prog.pid)

    assert len(str(stat)) > 0
    assert int(time.time() - start) >= SPIN_DURATION


@pytest.mark.skipif(
    is_nix(), reason="ProcessLocalCPUUtilization not supported on Windows."
)
def test_cpu_windows():
    with pytest.raises(RuntimeError):
        _ = ProcessLocalMemoryConsumption()
