"""
Unit test for LocalProcessCPUUtilization measurement.
"""


import os
import time
import pytest
import threading
import subprocess

import mlte
from mlte._private.platform import is_windows, is_nix
from mlte.measurement.cpu import LocalProcessCPUUtilization, CPUStatistics
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
    is_windows(), reason="LocalProcessCPUUtilization not supported on Windows."
)
def test_cpu_nix_evaluate():
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
def test_cpu_nix_validate_success():
    p = spin_for(5)
    m = LocalProcessCPUUtilization("id")

    stats = m.evaluate(p.pid)

    vr = Validator("Succeed", lambda _: Success())(stats)
    assert bool(vr)

    # Data is accessible from validation result
    assert vr.result is not None
    assert isinstance(vr.result, CPUStatistics)


@pytest.mark.skipif(
    is_windows(), reason="LocalProcessCPUUtilization not supported on Windows."
)
def test_cpu_nix_validate_failure():
    p = spin_for(5)

    m = LocalProcessCPUUtilization("id")

    stats = m.evaluate(p.pid)

    vr = Validator("Fail", lambda _: Failure())(stats)
    assert not bool(vr)

    # Data is accessible from validation result
    assert vr.result is not None
    assert isinstance(vr.result, CPUStatistics)


@pytest.mark.skipif(
    is_nix(), reason="LocalProcessCPUUtilization not supported on Windows."
)
def test_cpu_windows_evaluate():
    with pytest.raises(RuntimeError):
        _ = LocalProcessCPUUtilization("id")


@pytest.mark.skipif(
    is_nix(), reason="LocalProcessCPUUtilization not supported on Windows."
)
def test_cpu_windows_validate():
    with pytest.raises(RuntimeError):
        _ = LocalProcessCPUUtilization("id")


def test_result_save_load(tmp_path):
    mlte.set_model("mymodel", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    p = spin_for(5)

    m = LocalProcessCPUUtilization("id")

    stats: CPUStatistics = m.evaluate(p.pid)
    stats.save()

    r: CPUStatistics = CPUStatistics.load("id")  # type: ignore
    assert r.avg == stats.avg
    assert r.min == stats.min
    assert r.max == stats.max
