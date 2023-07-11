"""
Unit test for LocalProcessMemoryConsumption measurement.
"""

import os
import subprocess
import threading
import time

import pytest

from mlte._private.platform import is_macos, is_nix, is_windows
from mlte.measurement.memory import (
    LocalProcessMemoryConsumption,
    MemoryStatistics,
)
from mlte.validation import Condition, Failure, Success

from ...fixtures import default_session  # noqa
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
    is_windows() or is_macos(),
    reason="ProcessLocalCPUUtilization not supported on Windows or macOS.",
)
def test_memory_nix_evaluate() -> None:
    start = time.time()

    p = spin_for(5)
    m = LocalProcessMemoryConsumption("identifier")

    # Capture memory consumption; blocks until process exit
    stats = m.evaluate(p.pid)

    assert len(str(stats)) > 0
    assert int(time.time() - start) >= SPIN_DURATION


@pytest.mark.skipif(
    is_windows() or is_macos(),
    reason="ProcessLocalCPUUtilization not supported on Windows or macOS.",
)
def test_memory_nix_evaluate_async() -> None:
    start = time.time()

    p = spin_for(5)
    m = LocalProcessMemoryConsumption("identifier")

    # Capture memory consumption; blocks until process exit
    m.evaluate_async(p.pid)
    stats = m.wait_for_output()

    assert len(str(stats)) > 0
    assert int(time.time() - start) >= SPIN_DURATION


@pytest.mark.skipif(
    is_windows() or is_macos(),
    reason="ProcessLocalCPUUtilization not supported on Windows or macOS.",
)
def test_memory_nix_validate_success() -> None:
    p = spin_for(5)

    m = LocalProcessMemoryConsumption("identifier")

    # Blocks until process exit
    stats = m.evaluate(p.pid)

    vr = Condition("Succeed", [], lambda _: Success())(stats)
    assert bool(vr)

    assert vr.metadata is not None
    assert vr.metadata.measurement_type, type(MemoryStatistics).__name__


@pytest.mark.skipif(
    is_windows() or is_macos(),
    reason="ProcessLocalCPUUtilization not supported on Windows or macOS.",
)
def test_memory_nix_validate_failure() -> None:
    p = spin_for(5)

    m = LocalProcessMemoryConsumption("identifier")

    # Blocks until process exit
    stats = m.evaluate(p.pid)

    vr = Condition("Fail", [], lambda _: Failure())(stats)
    assert not bool(vr)

    assert vr.metadata is not None
    assert vr.metadata.measurement_type, type(MemoryStatistics).__name__


@pytest.mark.skipif(
    is_nix(), reason="ProcessLocalCPUUtilization not supported on Windows."
)
def test_memory_windows_evaluate() -> None:
    with pytest.raises(RuntimeError):
        _ = LocalProcessMemoryConsumption("id")


@pytest.mark.skipif(
    is_windows() or is_macos(),
    reason="LocalProcessCPUUtilization not supported on Windows or macOS.",
)
def test_result_save_load(default_session) -> None:  # noqa
    p = spin_for(5)

    m = LocalProcessMemoryConsumption("identifier")

    stats: MemoryStatistics = m.evaluate(p.pid)
    stats.save()

    r: MemoryStatistics = MemoryStatistics.load("identifier")  # type: ignore
    assert r.avg == stats.avg
    assert r.min == stats.min
    assert r.max == stats.max
