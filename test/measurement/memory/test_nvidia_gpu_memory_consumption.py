"""
test/measurement/memory/test_local_process_memory_consumption.py

Unit test for LocalProcessMemoryConsumption measurement.
"""

import importlib
import time
import typing
from collections import namedtuple
from typing import Tuple
from unittest.mock import MagicMock, patch

import pint
import pytest

from mlte.context.context import Context
from mlte.measurement.memory import (
    NvidiaGPUMemoryConsumption,
    NvidiaGPUMemoryStatistics,
)
from mlte.measurement.memory.nvidia_gpu_memory_consumption import (
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
    Returns a command that allocates some memory (4MB) on the cuda device then sleeps for dealy.
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


def has_torch_cuda() -> bool:
    """
    Checks to see if torch and cuda are available. We need both of these for this test.
    :return: True if we have access to torch and cuda.
    """
    # DESIGN NOTE: Arguably, we could use nvidia-smi alone to see if we have access to cuda, but
    # we don't have code to load the cuda device without torch. We could use a different package
    # such as cupy, but that still requires something that probabaly isn't installed.

    try:
        torch = importlib.import_module("torch")
        return bool(torch.cuda.is_available())
    except ModuleNotFoundError:
        # The module isn't there, so we can't run our experiment anyway
        return False
    except AttributeError:
        # We had some other error so we can't run the test with cuda either.
        return False


def has_pynvml():
    """
    Checks to see if pynvml is available without actually trying to import.
    :return: Tru if available for import.
    """
    import importlib.util

    spec = importlib.util.find_spec("pynvml")
    return spec is not None


# =================================================================================================
# NvidiaGPUMemoryConsumption
# =================================================================================================
def test_constructor_type():
    """ "Checks that the constructor sets up type properly."""
    m = NvidiaGPUMemoryConsumption("id", 1)

    assert (
        m.evidence_metadata
        and m.evidence_metadata.measurement.measurement_class
        == "mlte.measurement.memory.nvidia_gpu_memory_consumption.NvidiaGPUMemoryConsumption"
    )
    assert m.gpu_id == 1


def test_nvidia_faking_gpu():
    """
    This test checks to see that the underlying internal API is wired properly to get values
    from the nvml library.
    :return: None
    """
    # TODO: Should I used pint here?
    one_GiB = 1024**3
    MemInfoMock = namedtuple("MemInfoMock", ["total", "free", "used"])

    # We have to patch the path to where it was actually included to make sure we get the right
    # instance mocked
    with patch(
        "mlte.measurement.memory.nvidia_gpu_memory_consumption.import_module"
    ) as mock_import_module:
        # Configure the mock to return a specific mock object
        mem_info_mock = MemInfoMock(
            total=3 * one_GiB, free=2 * one_GiB, used=1 * one_GiB
        )

        mocked_pynvml = MagicMock()
        mocked_pynvml.nvmlDeviceGetCount.return_value = 2
        mocked_pynvml.nvmlDeviceGetHandleByIndex.return_value = 1
        mocked_pynvml.nvmlDeviceGetMemoryInfo.return_value = mem_info_mock

        mock_import_module.return_value = mocked_pynvml

        # Now, at this point import_lib is mocked and will return a fake library.
        # So, we should be able to call our function and get the value that mem_info would return
        ret_val = _get_nvml_memory_usage_bytes(0)
        assert ret_val == mem_info_mock.used


@pytest.mark.skipif(
    not has_torch_cuda(),
    reason="NvidiaGPUMemoryConsumption requires cuda to test.",
)
def test_nvidia_get_memory_usage():
    """
    Use the low level API without mocking nvml to see that it can get a value
    :return: None
    """
    # If we don't have a gpu, we'll just get some value back and shouldn't just crash
    _get_nvml_memory_usage_bytes(0)


@pytest.mark.skipif(
    has_pynvml(),
    reason="NvidiaGPUMemoryConsumption has pynvml so can't test errors.",
)
def test_nvidia_get_memory_usage_no_pynvlm():
    assert _get_nvml_memory_usage_bytes(0) == -1


@pytest.mark.skipif(
    not has_torch_cuda(),
    reason="NvidiaGPUMemoryConsumption requires cuda to test.",
)
def test_memory_evaluate() -> None:
    start = time.time()

    # NOTE: This assumes that the testing environment has access to gpu0
    m = NvidiaGPUMemoryConsumption("identifier")

    # Capture memory consumption; blocks until process exit
    delay = 2
    stats: NvidiaGPUMemoryStatistics = typing.cast(
        NvidiaGPUMemoryStatistics, m.evaluate(get_cuda_load_command(delay))
    )

    # NOTE: Because of multiple GPU users, we just need to read some >0 value.
    assert stats.max.magnitude > 0
    assert stats.max.avergae > 0
    assert stats.max.magnitude >= 0
    assert len(str(stats)) > 0
    assert int(time.time() - start) >= delay


@pytest.mark.skipif(
    not has_torch_cuda(),
    reason="NvidiaGPUMemoryConsumption requires cuda to test.",
)
def test_memory_evaluate_async() -> None:
    start = time.time()

    delay = 2
    cmd = get_cuda_load_command(delay)

    pid = ProcessMeasurement.start_process(cmd[0], cmd[1:])
    m = NvidiaGPUMemoryConsumption("identifier")

    # Capture gpu memory consumption; blocks until process exit
    m.evaluate_async(pid)
    stats = m.wait_for_output()

    # NOTE: Because of multiple GPU users, we just need to read some >0 value.
    assert len(str(stats)) > 0
    assert int(time.time() - start) >= delay


@pytest.mark.skipif(
    not has_torch_cuda(),
    reason="NvidiaGPUMemoryConsumption requires cuda to test.",
)
def test_memory_validate_success() -> None:
    m = NvidiaGPUMemoryConsumption("identifier")

    # Blocks until process exit
    delay = 2
    # TODO: Why specify units?
    stats = m.evaluate(get_cuda_load_command(delay), unit=Units.mebibyte)

    validator = Validator(bool_exp=lambda _: True, success="yay", failure="oh")
    vr = validator.validate(stats)
    assert bool(vr)


@pytest.mark.skipif(
    not has_torch_cuda(),
    reason="NvidiaGPUMemoryConsumption requires cuda to test.",
)
def test_memory_validate_failure() -> None:
    m = NvidiaGPUMemoryConsumption("identifier")

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
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
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


def test_max_consumption_less_than() -> None:
    # Default units should work across the two classes.
    m = get_sample_evidence_metadata()

    validator = NvidiaGPUMemoryStatistics.max_consumption_less_than(3)

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


def test_max_consumption_less_than_in_bytes() -> None:
    # The units shouldn't matter
    m = get_sample_evidence_metadata()

    validator = NvidiaGPUMemoryStatistics.max_consumption_less_than(
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


def test_max_consumption_less_than_invalid_unit() -> None:
    with pytest.raises(pint.UndefinedUnitError):
        _ = NvidiaGPUMemoryStatistics.max_consumption_less_than(
            3000, Units.fakeunit
        )


def test_avg_consumption_less_than() -> None:
    m = get_sample_evidence_metadata()

    validator = NvidiaGPUMemoryStatistics.average_consumption_less_than(3)

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


def test_avg_consumption_less_than_in_bytes() -> None:
    m = get_sample_evidence_metadata()

    validator = NvidiaGPUMemoryStatistics.average_consumption_less_than(
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


def test_average_consumption_less_than_invalid_unit() -> None:
    with pytest.raises(pint.UndefinedUnitError):
        _ = NvidiaGPUMemoryStatistics.average_consumption_less_than(
            3000, Units.fakeunit
        )
