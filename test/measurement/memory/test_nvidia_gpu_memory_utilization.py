"""Unit test for NvidiaGPUMemoryUtilization measurement."""

import time
import typing
from typing import Tuple

import pint
import pytest

import mlte.measurement.utility.pynvml_utils as pynvml_utils
import test.measurement.utility.test_pynvml_utils as test_pynvml_utils
from mlte.context.context import Context
from mlte.measurement.memory import (
    NvidiaGPUMemoryStatistics,
    NvidiaGPUMemoryUtilization,
)
from mlte.measurement.memory.nvidia_gpu_memory_utilization import (
    _get_nvml_memory_usage_bytes,
)
from mlte.measurement.process_measurement import ProcessMeasurement
from mlte.measurement.units import Quantity, Units
from mlte.store.artifact.store import ArtifactStore
from mlte.validation.validator import Validator
from test.evidence.types.helper import get_sample_evidence_metadata
from test.store.artifact.fixture import store_with_context  # noqa

# =================================================================================================
#  _   _ _   _ _ _ _   _
# | | | | |_(_) (_) |_(_)___ ___
# | |_| |  _| | | |  _| / -_|_-<
#  \___/ \__|_|_|_|\__|_\___/__/
# =================================================================================================


def get_cuda_load_command(delay_sec: int = 2) -> list[str]:
    """
    Returns a command that allocates some memory (4MB) on the cuda device then sleeps for delay.
    :param delay_sec: The amount of time to sleep.
    :return: A formatted single command string to hand to subprocess
    """
    # TODO: Should we stair-step for measurement purposes?
    # In theory this should allocate 4 MiB (1024 * 1204 * 32bits)
    # Example of output command we aare creating
    # python -c "import time; import torch;
    # torch.ones(1024, 1024, device='cuda', dtype=torch.int32); time.sleep(2)"
    cmd = [
        "import time",
        "import torch",
        "torch.ones(1024, 1024, device='cuda', dtype=torch.int32)",
        f"time.sleep({delay_sec})",
    ]

    # The command must be a list. So, add python and join the python command
    return ["python", "-c", "; ".join(cmd)]


# =================================================================================================
# NvidiaGPUMemoryUtilization
# =================================================================================================
def test_constructor_type():
    """ "Checks that the constructor sets up type properly."""
    m = NvidiaGPUMemoryUtilization("id", gpu_id=1)

    assert (
        m.evidence_metadata
        and m.evidence_metadata.measurement.measurement_class
        == "mlte.measurement.memory.nvidia_gpu_memory_utilization.NvidiaGPUMemoryUtilization"
    )
    assert m.gpu_id == 1


def test_constructor_type_group():
    """ "Checks that the constructor sets up type properly, with group."""
    m = NvidiaGPUMemoryUtilization("id", gpu_id=1, group="group1")

    assert (
        m.evidence_metadata
        and m.evidence_metadata.measurement.measurement_class
        == "mlte.measurement.memory.nvidia_gpu_memory_utilization.NvidiaGPUMemoryUtilization"
    )
    assert m.gpu_id == 1


@pytest.mark.skipif(
    not test_pynvml_utils.has_torch_cuda(),
    reason="NvidiaGPUMemoryUtilization requires cuda to test.",
)
def test_nvidia_get_memory_usage():
    """
    Use the low level API without mocking nvml to see that it can get a value
    :return: None
    """
    # If we don't have a gpu, we'll just get some value back and shouldn't just crash
    pynvml_utils.get_pynvml_statistic(0, _get_nvml_memory_usage_bytes)


@pytest.mark.skipif(
    test_pynvml_utils.has_pynvml(),
    reason="NvidiaGPUMemoryUtilization has pynvml so can't test errors.",
)
def test_nvidia_get_memory_usage_no_pynvml():
    # If we do NOT have pynvml then the thing should return the default values
    assert (
        pynvml_utils.get_pynvml_statistic(0, _get_nvml_memory_usage_bytes, -2)
        == -2
    )


@pytest.mark.skipif(
    not test_pynvml_utils.has_torch_cuda(),
    reason="NvidiaGPUMemoryUtilization requires cuda to test.",
)
def test_memory_evaluate() -> None:
    start = time.time()

    # NOTE: This assumes that the testing environment has access to gpu0
    m = NvidiaGPUMemoryUtilization("identifier")

    # Capture memory utilization; blocks until process exit
    delay = 2
    stats: NvidiaGPUMemoryStatistics = typing.cast(
        NvidiaGPUMemoryStatistics, m.evaluate(get_cuda_load_command(delay))
    )

    # NOTE: Because of multiple GPU users, we just need to read some >0 value.
    assert stats.max.magnitude > 0
    assert stats.avg.magnitude > 0
    assert stats.min.magnitude >= 0
    assert len(str(stats)) > 0
    assert int(time.time() - start) >= delay


@pytest.mark.skipif(
    not test_pynvml_utils.has_torch_cuda(),
    reason="NvidiaGPUMemoryUtilization requires cuda to test.",
)
def test_memory_evaluate_async() -> None:
    start = time.time()

    delay = 2
    cmd = get_cuda_load_command(delay)

    pid = ProcessMeasurement.start_process(cmd)
    m = NvidiaGPUMemoryUtilization("identifier")

    # Capture gpu memory utilization; blocks until process exit
    m.evaluate_async(pid)
    stats = m.wait_for_output()

    # NOTE: Because of multiple GPU users, we just need to read some >0 value.
    assert len(str(stats)) > 0
    assert int(time.time() - start) >= delay


@pytest.mark.skipif(
    not test_pynvml_utils.has_torch_cuda(),
    reason="NvidiaGPUMemoryUtilization requires cuda to test.",
)
def test_memory_validate_success() -> None:
    m = NvidiaGPUMemoryUtilization("identifier")

    # Blocks until process exit
    delay = 2
    # TODO: Why specify units?
    stats = m.evaluate(get_cuda_load_command(delay), unit=Units.mebibyte)

    validator = Validator(bool_exp=lambda _: True, success="yay", failure="oh")
    vr = validator.validate(stats)
    assert bool(vr)


@pytest.mark.skipif(
    not test_pynvml_utils.has_torch_cuda(),
    reason="NvidiaGPUMemoryUtilization requires cuda to test.",
)
def test_memory_validate_failure() -> None:
    m = NvidiaGPUMemoryUtilization("identifier")

    # Blocks until process exit
    delay = 2
    stats = m.evaluate(get_cuda_load_command(delay))

    vr = Validator(
        bool_exp=lambda _: False, success="yay", failure="oh"
    ).validate(stats)
    assert not bool(vr)


# =================================================================================================
# NvidiaGPUMemoryStatistics
# =================================================================================================


def test_statistics_construction():
    m = get_sample_evidence_metadata()

    stats = NvidiaGPUMemoryStatistics(1, 2, 4).with_metadata(m)
    assert stats.avg == Quantity(1, Units.mebibyte)
    assert stats.min == Quantity(2, Units.mebibyte)
    assert stats.max == Quantity(4, Units.mebibyte)
    assert stats.unit == Units.mebibyte

    stats = NvidiaGPUMemoryStatistics(4, 6, 8, Units.gibibyte).with_metadata(m)
    assert stats.avg == Quantity(4, Units.gibibyte)
    assert stats.min == Quantity(6, Units.gibibyte)
    assert stats.max == Quantity(8, Units.gibibyte)
    assert stats.unit == Units.gibibyte


def test_result_save_load(
    store_with_context: Tuple[ArtifactStore, Context],  # noqa
) -> None:
    store, ctx = store_with_context

    stats = NvidiaGPUMemoryStatistics(50, 10, 800).with_metadata(
        get_sample_evidence_metadata()
    )
    stats.save_with(ctx, store)

    r: NvidiaGPUMemoryStatistics = typing.cast(
        NvidiaGPUMemoryStatistics,
        NvidiaGPUMemoryStatistics.load_with(
            "evidence.test_id", context=ctx, store=store
        ),
    )
    assert r.avg == stats.avg
    assert r.min == stats.min
    assert r.max == stats.max


def test_max_utilization_less_than() -> None:
    # Default units should work across the two classes.
    m = get_sample_evidence_metadata()

    validator = NvidiaGPUMemoryStatistics.max_utilization_less_than(3)

    # Less than case
    res = validator.validate(
        NvidiaGPUMemoryStatistics(avg=2, max=2, min=1).with_metadata(m)
    )
    assert bool(res)

    # Greater than case
    res = validator.validate(
        NvidiaGPUMemoryStatistics(avg=2, max=4, min=1).with_metadata(m)
    )
    assert not bool(res)

    # Equals case
    res = validator.validate(
        NvidiaGPUMemoryStatistics(avg=2, max=3, min=1).with_metadata(m)
    )
    assert not bool(res)


def test_max_utilization_less_than_in_bytes() -> None:
    # The units shouldn't matter
    m = get_sample_evidence_metadata()

    validator = NvidiaGPUMemoryStatistics.max_utilization_less_than(
        3, unit=Units.bytes
    )

    # Less than case
    res = validator.validate(
        NvidiaGPUMemoryStatistics(
            avg=2, max=2, min=1, unit=Units.bytes
        ).with_metadata(m)
    )
    assert bool(res)

    # Greater than case
    res = validator.validate(
        NvidiaGPUMemoryStatistics(
            avg=2, max=4, min=1, unit=Units.bytes
        ).with_metadata(m)
    )
    assert not bool(res)

    # Equals case
    res = validator.validate(
        NvidiaGPUMemoryStatistics(
            avg=2, max=3, min=1, unit=Units.bytes
        ).with_metadata(m)
    )
    assert not bool(res)


def test_max_utilization_less_than_invalid_unit() -> None:
    with pytest.raises(pint.UndefinedUnitError):
        _ = NvidiaGPUMemoryStatistics.max_utilization_less_than(
            3000, Units.fakeunit
        )


def test_avg_utilization_less_than() -> None:
    m = get_sample_evidence_metadata()

    validator = NvidiaGPUMemoryStatistics.average_utilization_less_than(3)

    # Less than case
    res = validator.validate(
        NvidiaGPUMemoryStatistics(avg=2, max=2, min=1).with_metadata(m)
    )
    assert bool(res)

    # Greater than case
    res = validator.validate(
        NvidiaGPUMemoryStatistics(avg=4, max=2, min=1).with_metadata(m)
    )
    assert not bool(res)

    # Equals case
    res = validator.validate(
        NvidiaGPUMemoryStatistics(avg=3, max=2, min=1).with_metadata(m)
    )
    assert not bool(res)


def test_avg_utilization_less_than_in_bytes() -> None:
    m = get_sample_evidence_metadata()

    validator = NvidiaGPUMemoryStatistics.average_utilization_less_than(
        3000, Units.bytes
    )

    # Less than case
    res = validator.validate(
        NvidiaGPUMemoryStatistics(
            avg=2000, max=2000, min=1000, unit=Units.bytes
        ).with_metadata(m)
    )
    assert bool(res)

    # Greater than case
    res = validator.validate(
        NvidiaGPUMemoryStatistics(
            avg=4000, max=2000, min=1000, unit=Units.bytes
        ).with_metadata(m)
    )
    assert not bool(res)

    # Equals case
    res = validator.validate(
        NvidiaGPUMemoryStatistics(
            avg=3000, max=2000, min=1000, unit=Units.bytes
        ).with_metadata(m)
    )
    assert not bool(res)


def test_average_utilization_less_than_invalid_unit() -> None:
    with pytest.raises(pint.UndefinedUnitError):
        _ = NvidiaGPUMemoryStatistics.average_utilization_less_than(
            3000, Units.fakeunit
        )
