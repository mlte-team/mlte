"""
Unit test for LocalProcessMemoryConsumption measurement.
"""

import os
import time
import pytest
import threading
import subprocess

from mlte._private.platform import is_windows, is_nix
from mlte.measurement.memory import LocalProcessMemoryConsumption
from mlte.measurement.memory.local_process_memory_consumption import (
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

    prog = spin_for(5)
    prop = LocalProcessMemoryConsumption()

    # Capture memory consumption; blocks until process exit
    stat = prop.evaluate(prog.pid)

    assert len(str(stat)) > 0
    assert int(time.time() - start) >= SPIN_DURATION


@pytest.mark.skipif(
    is_windows(), reason="ProcessLocalCPUUtilization not supported on Windows."
)
def test_memory_nix_validate_success():
    prog = spin_for(5)
    prop = LocalProcessMemoryConsumption().with_validator(
        Validator("Succeed", lambda _: Success())
    )

    # Capture memory consumption; blocks until process exit
    results = prop.validate(prog.pid)
    assert len(results) == 1
    assert bool(results[0])

    result = results[0]
    assert isinstance(result.data, MemoryStatistics)


@pytest.mark.skipif(
    is_windows(), reason="ProcessLocalCPUUtilization not supported on Windows."
)
def test_memory_nix_validate_failure():
    prog = spin_for(5)
    prop = LocalProcessMemoryConsumption().with_validator(
        Validator("Fail", lambda _: Failure())
    )

    # Capture memory consumption; blocks until process exit
    results = prop.validate(prog.pid)
    assert len(results) == 1
    assert not bool(results[0])

    result = results[0]
    assert isinstance(result.data, MemoryStatistics)


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
