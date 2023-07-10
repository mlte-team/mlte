"""
Unit test for LocalProcessCPUUtilization measurement.
"""


import os
import time
import pytest
import threading
import subprocess

from mlte._private.platform import is_windows, is_nix
from mlte.measurement.cpu import LocalProcessCPUUtilization, CPUStatistics
from mlte.validation import Condition, Success, Failure

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
    is_windows(), reason="LocalProcessCPUUtilization not supported on Windows."
)
def test_cpu_nix_evaluate() -> None:
    start = time.time()

    p = spin_for(5)
    m = LocalProcessCPUUtilization("id")

    # Capture CPU utilization; blocks until process exit
    stat = m.evaluate(p.pid)

    assert len(str(stat)) > 0
    # Test for passage of time
    assert int(time.time() - start) >= SPIN_DURATION


@pytest.mark.skipif(
    is_windows(), reason="LocalProcessCPUUtilization not supported on Windows."
)
def test_cpu_nix_evaluate_async() -> None:
    start = time.time()

    p = spin_for(5)
    m = LocalProcessCPUUtilization("id")

    # Capture CPU utilization; blocks until process exit
    m.evaluate_async(p.pid)
    stat = m.wait_for_output()

    assert len(str(stat)) > 0
    # Test for passage of time
    assert int(time.time() - start) >= SPIN_DURATION


@pytest.mark.skipif(
    is_windows(), reason="LocalProcessCPUUtilization not supported on Windows."
)
def test_cpu_nix_validate_success() -> None:
    p = spin_for(5)
    m = LocalProcessCPUUtilization("id")

    stats = m.evaluate(p.pid)

    vr = Condition("Succeed", [], lambda _: Success())(stats)
    assert bool(vr)

    # Data is accessible from validation result
    assert vr.metadata is not None
    assert vr.metadata.measurement_type, type(CPUStatistics).__name__


@pytest.mark.skipif(
    is_windows(), reason="LocalProcessCPUUtilization not supported on Windows."
)
def test_cpu_nix_validate_failure() -> None:
    p = spin_for(5)
    m = LocalProcessCPUUtilization("id")

    stats = m.evaluate(p.pid)

    vr = Condition("Fail", [], lambda _: Failure())(stats)
    assert not bool(vr)

    # Data is accessible from validation result
    assert vr.metadata is not None
    assert vr.metadata.measurement_type, type(CPUStatistics).__name__


@pytest.mark.skipif(
    is_nix(), reason="LocalProcessCPUUtilization not supported on Windows."
)
def test_cpu_windows_evaluate() -> None:
    with pytest.raises(RuntimeError):
        _ = LocalProcessCPUUtilization("id")


@pytest.mark.skipif(
    is_windows(), reason="LocalProcessCPUUtilization not supported on Windows."
)
def test_result_save_load(default_session) -> None:  # noqa
    p = spin_for(5)

    m = LocalProcessCPUUtilization("id")

    stats: CPUStatistics = m.evaluate(p.pid)
    stats.save()

    r: CPUStatistics = CPUStatistics.load("id")  # type: ignore
    assert r.avg == stats.avg
    assert r.min == stats.min
    assert r.max == stats.max
