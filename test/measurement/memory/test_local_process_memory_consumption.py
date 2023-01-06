"""
Unit test for LocalProcessMemoryConsumption measurement.
"""

import os
import time
import pytest
import threading
import subprocess

from mlte._private.platform import is_windows, is_nix
from mlte.measurement.memory import (
    LocalProcessMemoryConsumption,
    MemoryStatistics,
)
from mlte.measurement.validation import Validator, Success, Failure

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
def test_memory_nix_evaluate():
    start = time.time()

    p = spin_for(5)
    m = LocalProcessMemoryConsumption("identifier")

    # Capture memory consumption; blocks until process exit
    stats = m.evaluate(p.pid)

    assert len(str(stats)) > 0
    assert int(time.time() - start) >= SPIN_DURATION


@pytest.mark.skipif(
    is_windows(), reason="ProcessLocalCPUUtilization not supported on Windows."
)
def test_memory_nix_validate_success():
    p = spin_for(5)

    m = LocalProcessMemoryConsumption("identifier")

    # Blocks until process exit
    stats = m.evaluate(p.pid)

    vr = Validator("Succeed", lambda _: Success())(stats)
    assert bool(vr)

    assert vr.result is not None
    assert isinstance(vr.result, MemoryStatistics)


@pytest.mark.skipif(
    is_windows(), reason="ProcessLocalCPUUtilization not supported on Windows."
)
def test_memory_nix_validate_failure():
    p = spin_for(5)

    m = LocalProcessMemoryConsumption("identifier")

    # Blocks until process exit
    stats = m.evaluate(p.pid)

    vr = Validator("Fail", lambda _: Failure())(stats)
    assert not bool(vr)

    assert vr.result is not None
    assert isinstance(vr.result, MemoryStatistics)


@pytest.mark.skipif(
    is_nix(), reason="ProcessLocalCPUUtilization not supported on Windows."
)
def test_memory_windows_evaluate():
    with pytest.raises(RuntimeError):
        _ = LocalProcessMemoryConsumption()


@pytest.mark.skipif(
    is_nix(), reason="ProcessLocalCPUUtilization not supported on Windows."
)
def test_memory_windows_validate():
    with pytest.raises(RuntimeError):
        _ = LocalProcessMemoryConsumption()
