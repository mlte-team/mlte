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
from mlte.measurement.memory import (
    LocalProcessMemoryConsumption,
    MemoryStatistics,
)
from mlte.store.artifact.store import ArtifactStore
from mlte.validation.validator import Validator
from test.store.artifact.fixture import store_with_context  # noqa
from test.evidence.types.helper import get_sample_evidence_metadata

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


def test_constructor_type():
    """ "Checks that the constructor sets up type properly."""
    m = LocalProcessMemoryConsumption("id")

    assert (
        m.evidence_metadata.measurement.measurement_class
        == "mlte.measurement.memory.local_process_memory_consumption.LocalProcessMemoryConsumption"
    )


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

    validator = Validator(bool_exp=lambda _: True, success="yay", failure="oh")
    vr = validator.validate(stats)
    assert bool(vr)

    assert vr.evidence_metadata is not None
    assert vr.evidence_metadata.measurement.measurement_class, type(
        MemoryStatistics
    ).__name__


def test_memory_validate_failure() -> None:
    p = spin_for(5)

    m = LocalProcessMemoryConsumption("identifier")

    # Blocks until process exit
    stats = m.evaluate(p.pid)

    vr = Validator(
        bool_exp=lambda _: False, success="yay", failure="oh"
    ).validate(stats)
    assert not bool(vr)

    assert vr.evidence_metadata is not None
    assert vr.evidence_metadata.measurement.measurement_class, type(
        MemoryStatistics
    ).__name__


def test_result_save_load(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
) -> None:
    store, ctx = store_with_context

    stats = MemoryStatistics(50, 10, 800).with_metadata(
        get_sample_evidence_metadata()
    )
    stats.save_with(ctx, store)

    r: MemoryStatistics = typing.cast(
        MemoryStatistics,
        MemoryStatistics.load_with("id.value", context=ctx, store=store),
    )
    assert r.avg == stats.avg
    assert r.min == stats.min
    assert r.max == stats.max


def test_max_consumption_less_than() -> None:
    m = get_sample_evidence_metadata()

    validator = MemoryStatistics.max_consumption_less_than(3)

    res = validator.validate(
        MemoryStatistics(avg=2, max=2, min=1).with_metadata(m)
    )
    assert bool(res)

    res = validator.validate(
        MemoryStatistics(avg=2, max=4, min=1).with_metadata(m)
    )
    assert not bool(res)

    res = validator.validate(
        MemoryStatistics(avg=2, max=3, min=1).with_metadata(m)
    )
    assert not bool(res)


def test_avg_consumption_less_than() -> None:
    m = get_sample_evidence_metadata()

    validator = MemoryStatistics.average_consumption_less_than(3)

    res = validator.validate(
        MemoryStatistics(avg=2, max=2, min=1).with_metadata(m)
    )
    assert bool(res)

    res = validator.validate(
        MemoryStatistics(avg=4, max=2, min=1).with_metadata(m)
    )
    assert not bool(res)

    res = validator.validate(
        MemoryStatistics(avg=3, max=2, min=1).with_metadata(m)
    )
    assert not bool(res)
