"""
test/measurement/memory/test_local_process_memory_consumption.py

Unit test for LocalProcessMemoryConsumption measurement.
"""

import os
import subprocess
import threading
import time
import typing
from typing import Tuple

from mlte.context.context import Context
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.measurement.memory import (
    LocalProcessMemoryConsumption,
    MemoryStatistics,
)
from mlte.spec.condition import Condition
from mlte.store.artifact.store import ArtifactStore
from mlte.validation.validator import Validator
from test.store.artifact.fixture import store_with_context  # noqa

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


def test_memory_evaluate() -> None:
    start = time.time()

    p = spin_for(5)
    m = LocalProcessMemoryConsumption("identifier")

    # Capture memory consumption; blocks until process exit
    stats = m.evaluate(p.pid)

    assert len(str(stats)) > 0
    assert int(time.time() - start) >= SPIN_DURATION


def test_memory_evaluate_async() -> None:
    start = time.time()

    p = spin_for(5)
    m = LocalProcessMemoryConsumption("identifier")

    # Capture memory consumption; blocks until process exit
    m.evaluate_async(p.pid)
    stats = m.wait_for_output()

    assert len(str(stats)) > 0
    assert int(time.time() - start) >= SPIN_DURATION


def test_memory_validate_success() -> None:
    p = spin_for(5)

    m = LocalProcessMemoryConsumption("identifier")

    # Blocks until process exit
    stats = m.evaluate(p.pid)

    vr = Condition("Succeed", [], Validator(lambda _: True))(stats)
    assert bool(vr)

    assert vr.metadata is not None
    assert vr.metadata.measurement_type, type(MemoryStatistics).__name__


def test_memory_validate_failure() -> None:
    p = spin_for(5)

    m = LocalProcessMemoryConsumption("identifier")

    # Blocks until process exit
    stats = m.evaluate(p.pid)

    vr = Condition("Fail", [], Validator(lambda _: False))(stats)
    assert not bool(vr)

    assert vr.metadata is not None
    assert vr.metadata.measurement_type, type(MemoryStatistics).__name__


def test_result_save_load(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
) -> None:
    store, ctx = store_with_context

    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id")
    )
    stats = MemoryStatistics(m, 50, 10, 800)
    stats.save_with(ctx, store)

    r: MemoryStatistics = typing.cast(
        MemoryStatistics,
        MemoryStatistics.load_with("id.value", context=ctx, store=store),
    )
    assert r.avg == stats.avg
    assert r.min == stats.min
    assert r.max == stats.max
