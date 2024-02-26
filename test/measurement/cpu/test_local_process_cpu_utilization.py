"""
test/measurement/cpu/test_local_process_cpu_utilization.py

Unit test for LocalProcessCPUUtilization measurement.
"""


import os
import subprocess
import threading
import time
from typing import Tuple

import pytest

from mlte._private.platform import is_nix, is_windows
from mlte.context.context import Context
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.measurement.cpu import CPUStatistics, LocalProcessCPUUtilization
from mlte.spec.condition import Condition
from mlte.store.artifact.store import ArtifactStore
from mlte.validation.result import Failure, Success

from ...fixture.store import store_with_context  # noqa
from ...support.meta import path_to_support

# The spin duration, in seconds
SPIN_DURATION = 3


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

    p = spin_for(SPIN_DURATION)
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

    p = spin_for(SPIN_DURATION)
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
    p = spin_for(SPIN_DURATION)
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
    p = spin_for(SPIN_DURATION)
    m = LocalProcessCPUUtilization("id")

    stats = m.evaluate(p.pid)

    vr = Condition("Fail", [], lambda _: Failure())(stats)
    assert not bool(vr)

    # Data is accessible from validation result
    assert vr.metadata is not None
    assert vr.metadata.measurement_type, type(CPUStatistics).__name__


@pytest.mark.skipif(
    is_nix(),
    reason="This test is only to identify lack of support in Windows systems.",
)
def test_cpu_windows_evaluate() -> None:
    with pytest.raises(RuntimeError):
        _ = LocalProcessCPUUtilization("id")


@pytest.mark.skipif(
    is_windows(), reason="LocalProcessCPUUtilization not supported on Windows."
)
def test_result_save_load(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
) -> None:
    store, ctx = store_with_context

    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    stats = CPUStatistics(m, 0.5, 0.1, 0.8)
    stats.save_with(ctx, store)

    r: CPUStatistics = CPUStatistics.load_with("id.value", context=ctx, store=store)  # type: ignore
    assert r.avg == stats.avg
    assert r.min == stats.min
    assert r.max == stats.max
