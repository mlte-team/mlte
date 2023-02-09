"""
Unit test for LocalProcessCPUUtilization measurement.
"""


import os
import time
import pytest
import threading
import subprocess

from mlte._private.platform import is_windows, is_nix
from mlte.measurement.cpu import LocalProcessCPUUtilization
from mlte.measurement.cpu.local_process_cpu_utilization import CPUStatistics
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

    prog = spin_for(5)
    prop = LocalProcessCPUUtilization()

    # Capture CPU utilization; blocks until process exit
    stat = prop.evaluate(prog.pid)

    assert len(str(stat)) > 0
    # Test for passage of time
    assert int(time.time() - start) >= SPIN_DURATION


@pytest.mark.skipif(
    is_windows(), reason="LocalProcessCPUUtilization not supported on Windows."
)
def test_cpu_nix_validate_success():
    prog = spin_for(5)
    prop = LocalProcessCPUUtilization().with_validator(
        Validator("Succeed", lambda _: Success())
    )

    # Evaluate and run validators
    results = prop.validate(prog.pid)
    assert len(results) == 1
    assert bool(results[0])

    # Data is accessible from validation result
    result = results[0]
    assert isinstance(result.data, CPUStatistics)


@pytest.mark.skipif(
    is_windows(), reason="LocalProcessCPUUtilization not supported on Windows."
)
def test_cpu_nix_validate_failure():
    prog = spin_for(5)
    prop = LocalProcessCPUUtilization().with_validator(
        Validator("Fail", lambda _: Failure())
    )

    # Evaluate and run validators
    results = prop.validate(prog.pid)
    assert len(results) == 1
    assert not bool(results[0])

    # Data is accessible from validation result
    result = results[0]
    assert isinstance(result.data, CPUStatistics)


@pytest.mark.skipif(
    is_nix(), reason="LocalProcessCPUUtilization not supported on Windows."
)
def test_cpu_windows_evaluate():
    with pytest.raises(RuntimeError):
        _ = LocalProcessCPUUtilization()


@pytest.mark.skipif(
    is_nix(), reason="LocalProcessCPUUtilization not supported on Windows."
)
def test_cpu_windows_validate():
    with pytest.raises(RuntimeError):
        _ = LocalProcessCPUUtilization()
