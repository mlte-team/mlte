"""
test/measurement/cpu/test_local_process_cpu_utilization.py

Unit test for LocalProcessCPUUtilization measurement.
"""

import os
import time
import typing
from typing import Tuple

import pytest

from mlte._private.platform import is_nix, is_windows
from mlte.context.context import Context
from mlte.measurement.cpu import CPUStatistics, LocalProcessCPUUtilization
from mlte.store.artifact.store import ArtifactStore
from mlte.validation.validator import Validator
from test.evidence.types.helper import get_sample_evidence_metadata
from test.store.artifact.fixture import store_with_context  # noqa

from ...support.meta import path_to_support

# The spin duration, in seconds
SPIN_DURATION = 3
SPIN_COMMAND = [
    "python3",
    os.path.join(path_to_support(), "spin.py"),
    str(SPIN_DURATION),
]


def test_constructor_type():
    """ "Checks that the constructor sets up type properly."""
    m = LocalProcessCPUUtilization("id")

    assert (
        m.evidence_metadata
        and m.evidence_metadata.measurement.measurement_class
        == "mlte.measurement.cpu.local_process_cpu_utilization.LocalProcessCPUUtilization"
    )


@pytest.mark.skipif(
    is_windows(), reason="LocalProcessCPUUtilization not supported on Windows."
)
def test_cpu_nix_evaluate() -> None:
    start = time.time()

    m = LocalProcessCPUUtilization("id")

    # Capture CPU utilization; blocks until process exit
    stat = m.evaluate(SPIN_COMMAND)

    assert len(str(stat)) > 0
    # Test for passage of time
    assert int(time.time() - start) >= SPIN_DURATION


@pytest.mark.skipif(
    is_windows(), reason="LocalProcessCPUUtilization not supported on Windows."
)
def test_cpu_nix_evaluate_async() -> None:
    start = time.time()

    m = LocalProcessCPUUtilization("id")

    # Capture CPU utilization; blocks until process exit
    stat = m.evaluate(SPIN_COMMAND)

    assert len(str(stat)) > 0
    # Test for passage of time
    assert int(time.time() - start) >= SPIN_DURATION


@pytest.mark.skipif(
    is_windows(), reason="LocalProcessCPUUtilization not supported on Windows."
)
def test_cpu_nix_validate_success() -> None:
    m = LocalProcessCPUUtilization("id")

    stats = m.evaluate(SPIN_COMMAND)

    vr = Validator(bool_exp=lambda _: True, success="Yay", failure="oh").validate(stats)  # type: ignore
    assert bool(vr)


@pytest.mark.skipif(
    is_windows(), reason="LocalProcessCPUUtilization not supported on Windows."
)
def test_cpu_nix_validate_failure() -> None:
    m = LocalProcessCPUUtilization("id")

    stats = m.evaluate(SPIN_COMMAND)

    vr = Validator(bool_exp=lambda _: False, success="Yay", failure="oh").validate(stats)  # type: ignore
    assert not bool(vr)


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

    stats = CPUStatistics(0.5, 0.1, 0.8).with_metadata(
        get_sample_evidence_metadata()
    )
    stats.save_with(ctx, store)

    r: CPUStatistics = typing.cast(
        CPUStatistics,
        CPUStatistics.load_with("evidence.test_id", context=ctx, store=store),
    )
    assert r.avg == stats.avg
    assert r.min == stats.min
    assert r.max == stats.max


def test_max_utilization_less_than() -> None:
    m = get_sample_evidence_metadata()

    validator = CPUStatistics.max_utilization_less_than(3)

    res = validator.validate(
        CPUStatistics(avg=2, max=2, min=1).with_metadata(m)
    )
    assert bool(res)

    res = validator.validate(
        CPUStatistics(avg=2, max=4, min=1).with_metadata(m)
    )
    assert not bool(res)

    res = validator.validate(
        CPUStatistics(avg=2, max=3, min=1).with_metadata(m)
    )
    assert not bool(res)


def test_avg_utilization_less_than() -> None:
    m = get_sample_evidence_metadata()

    validator = CPUStatistics.average_utilization_less_than(3)

    res = validator.validate(
        CPUStatistics(avg=2, max=2, min=1).with_metadata(m)
    )
    assert bool(res)

    res = validator.validate(
        CPUStatistics(avg=3, max=2, min=1).with_metadata(m)
    )
    assert not bool(res)

    res = validator.validate(
        CPUStatistics(avg=4, max=2, min=1).with_metadata(m)
    )
    assert not bool(res)
