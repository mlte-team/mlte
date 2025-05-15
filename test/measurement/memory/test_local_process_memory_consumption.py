"""
test/measurement/memory/test_local_process_memory_consumption.py

Unit test for LocalProcessMemoryConsumption measurement.
"""

import os
import time
import typing
from typing import Tuple

import pint
import pytest

from mlte.context.context import Context
from mlte.measurement.memory import (
    LocalProcessMemoryConsumption,
    MemoryStatistics,
)
from mlte.measurement.process_measurement import ProcessMeasurement
from mlte.measurement.units import Units
from mlte.store.artifact.store import ArtifactStore
from mlte.validation.validator import Validator
from test.evidence.types.helper import get_sample_evidence_metadata
from test.store.artifact.fixture import store_with_context  # noqa
from test.support.meta import path_to_support

# The spin duration, in seconds
SPIN_DURATION = 2
SPIN_COMMAND = [
    "python3",
    os.path.join(path_to_support(), "spin.py"),
    str(SPIN_DURATION),
]


def test_constructor_type():
    """ "Checks that the constructor sets up type properly."""
    m = LocalProcessMemoryConsumption("id")

    assert (
        m.evidence_metadata
        and m.evidence_metadata.measurement.measurement_class
        == "mlte.measurement.memory.local_process_memory_consumption.LocalProcessMemoryConsumption"
    )


def test_memory_evaluate() -> None:
    start = time.time()

    m = LocalProcessMemoryConsumption("identifier")

    # Capture memory consumption; blocks until process exit
    stats = m.evaluate(SPIN_COMMAND)

    assert len(str(stats)) > 0
    assert int(time.time() - start) >= SPIN_DURATION


def test_memory_evaluate_async() -> None:
    start = time.time()

    pid = ProcessMeasurement.start_process(SPIN_COMMAND[0], SPIN_COMMAND[1:])
    m = LocalProcessMemoryConsumption("identifier")

    # Capture memory consumption; blocks until process exit
    m.evaluate_async(pid)
    stats = m.wait_for_output()

    assert len(str(stats)) > 0
    assert int(time.time() - start) >= SPIN_DURATION


def test_memory_validate_success() -> None:
    m = LocalProcessMemoryConsumption("identifier")

    # Blocks until process exit
    stats = m.evaluate(SPIN_COMMAND, unit=Units.megabyte)

    validator = Validator(bool_exp=lambda _: True, success="yay", failure="oh")
    vr = validator.validate(stats)
    assert bool(vr)


def test_memory_validate_failure() -> None:

    m = LocalProcessMemoryConsumption("identifier")

    # Blocks until process exit
    stats = m.evaluate(SPIN_COMMAND)

    vr = Validator(
        bool_exp=lambda _: False, success="yay", failure="oh"
    ).validate(stats)
    assert not bool(vr)


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
        MemoryStatistics.load_with(
            "test_id.evidence", context=ctx, store=store
        ),
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


def test_max_consumption_less_than_in_bytes() -> None:
    m = get_sample_evidence_metadata()

    validator = MemoryStatistics.max_consumption_less_than(3000, Units.bytes)

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


def test_max_consumption_less_than_invalid_unit() -> None:
    with pytest.raises(pint.UndefinedUnitError):
        _ = MemoryStatistics.max_consumption_less_than(3000, Units.fakeunit)


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


def test_avg_consumption_less_than_in_bytes() -> None:
    m = get_sample_evidence_metadata()

    validator = MemoryStatistics.average_consumption_less_than(
        3000, Units.bytes
    )

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


def test_average_consumption_less_than_invalid_unit() -> None:
    with pytest.raises(pint.UndefinedUnitError):
        _ = MemoryStatistics.average_consumption_less_than(3000, Units.fakeunit)
