"""Unit test for NvidiaGPUPowerUtilization measurement."""

import time
import typing
from typing import Tuple
from unittest.mock import patch

import pint
import pytest

import mlte.measurement.utility.pynvml_utils as pynvml_utils
from mlte.context.context import Context
from mlte.measurement.power import (
    NvidiaGPUPowerStatistics,
    NvidiaGPUPowerUtilization,
)
from mlte.measurement.power.nvidia_gpu_power_utilization import (
    _get_nvml_power_usage_watts,
)
from mlte.measurement.process_measurement import ProcessMeasurement
from mlte.measurement.units import Quantity, Units
from mlte.store.artifact.store import ArtifactStore
from mlte.validation.validator import Validator
from test.evidence.types.helper import get_sample_evidence_metadata
from test.measurement.utility.test_pynvml_utils import (
    has_pynvml,
    has_torch_cuda,
    make_pynvml_mocks,
)
from test.store.artifact.fixture import store_with_context  # noqa

# =================================================================================================
#  _   _ _   _ _ _ _   _
# | | | | |_(_) (_) |_(_)___ ___
# | |_| |  _| | | |  _| / -_|_-<
#  \___/ \__|_|_|_|\__|_\___/__/
# =================================================================================================


def get_cuda_load_command(delay_sec: int = 2) -> list[str]:
    """
    Returns a command that allocates some memory which should require some power.
    :param delay_sec: The amount of time to sleep.
    :return: A formatted single command string to hand to subprocess
    """
    # It doesn't really matter how much memory.
    cmd = [
        "import time",
        "import torch",
        "torch.ones(1024, 1024, device='cuda', dtype=torch.int32)",
        f"time.sleep({delay_sec})",
    ]

    # The command must be a list. So, add python and join the python command
    return ["python", "-c", "; ".join(cmd)]


def fake_gpu_command(delay_sec: float = 0.25) -> list[str]:
    """
    Returns a command that sleeps briefly imagining the gpu is doing someting,
    :param delay_sec: The amount of time to sleep.
    :return: A formatted single command string to hand to subprocess
    """

    return ["python", "-c", f"import time; time.sleep({delay_sec})"]


# =================================================================================================
# NvidiaGPUPowerUtilization
# =================================================================================================
def test_constructor_type():
    """ "Checks that the constructor sets up type properly."""
    m = NvidiaGPUPowerUtilization("id", gpu_ids=1)

    assert (
        m.evidence_metadata
        and m.evidence_metadata.measurement.measurement_class
        == "mlte.measurement.power.nvidia_gpu_power_utilization.NvidiaGPUPowerUtilization"
    )
    assert m.gpu_ids == [1]


def test_constructor_type_group():
    """ "Checks that the constructor sets up type properly, with group."""
    m = NvidiaGPUPowerUtilization("id", gpu_ids=1, group="group1")

    assert (
        m.evidence_metadata
        and m.evidence_metadata.measurement.measurement_class
        == "mlte.measurement.power.nvidia_gpu_power_utilization.NvidiaGPUPowerUtilization"
    )
    assert m.gpu_ids == [1]


@pytest.mark.skipif(
    not has_torch_cuda(),
    reason="NvidiaGPUPowerUtilization requires cuda to test.",
)
def test_nvidia_get_power_usage():
    """
    Use the low level API without mocking nvml to see that it can get a value
    :return: None
    """
    # If we don't have a gpu, we'll just get some value back and shouldn't just crash
    pynvml_utils.get_pynvml_statistic([0], _get_nvml_power_usage_watts)


@pytest.mark.skipif(
    has_pynvml(),
    reason="NvidiaGPUPowerUtilization has pynvml so can't test errors.",
)
def test_nvidia_get_power_usage_no_pynvml():
    # If we do not have pynvml then it should raise an exception
    # NOTE We do not
    with pytest.raises(Exception) as excinfo:
        pynvml_utils.get_pynvml_statistic([0], _get_nvml_power_usage_watts)
        assert "NVMLError_LibraryNotFound" in str(excinfo.value)


@pytest.mark.skipif(
    not has_torch_cuda(),
    reason="NvidiaGPUPowerUtilization requires cuda to test.",
)
def test_power_evaluate() -> None:
    start = time.time()

    # NOTE: This assumes that the testing environment has access to gpu0
    m = NvidiaGPUPowerUtilization("identifier")

    # Capture power utilization; blocks until process exit
    delay = 2
    stats: NvidiaGPUPowerStatistics = typing.cast(
        NvidiaGPUPowerStatistics, m.evaluate(get_cuda_load_command(delay))
    )

    # NOTE: Because of multiple GPU users, we just need to read some >0 value.
    assert stats.max.magnitude > 0
    assert stats.avg.magnitude > 0
    assert stats.min.magnitude >= 0
    assert len(str(stats)) > 0
    assert int(time.time() - start) >= delay


@patch("mlte.measurement.utility.pynvml_utils.import_module")
def test_power_evaluate_fake_gpu(mock_import_module):
    # We have to patch the path to where it was actually included to make sure we get the right
    # instance mocked
    mocked_pynvml, mock_handle = make_pynvml_mocks()
    mock_import_module.return_value = mocked_pynvml

    # We need to preload this with bytes
    # NOTE: The internal function returns milliwatts even thought our tool returns watts
    mocked_pynvml.nvmlDeviceGetPowerUsage.side_effect = [9000, 12000]

    start = time.time()

    # NOTE: This assumes that the testing environment has access to gpu0
    m = NvidiaGPUPowerUtilization("identifier", gpu_ids=[0, 1])

    # Capture memory utilization; blocks until process exit
    delay = 0.25
    stats: NvidiaGPUPowerStatistics = typing.cast(
        NvidiaGPUPowerStatistics, m.evaluate(fake_gpu_command(delay))
    )

    # The gpu returns milliwatts
    assert stats.max.magnitude == 12
    assert stats.avg.magnitude == 10.5
    assert stats.min.magnitude == 9
    assert len(str(stats)) > 0
    assert int(time.time() - start) >= delay


@pytest.mark.skipif(
    not has_torch_cuda(),
    reason="NvidiaGPUPowerUtilization requires cuda to test.",
)
def test_power_evaluate_async() -> None:
    start = time.time()

    delay = 2
    cmd = get_cuda_load_command(delay)

    pid = ProcessMeasurement.start_process(cmd)
    m = NvidiaGPUPowerUtilization("identifier")

    # Capture gpu power utilization; blocks until process exit
    m.evaluate_async(pid)
    stats = m.wait_for_output()

    # NOTE: Because of multiple GPU users, we just need to read some >0 value.
    assert len(str(stats)) > 0
    assert int(time.time() - start) >= delay


@pytest.mark.skipif(
    not has_torch_cuda(),
    reason="NvidiaGPUPowerUtilization requires cuda to test.",
)
def test_power_validate_success() -> None:
    m = NvidiaGPUPowerUtilization("identifier")

    # Blocks until process exit
    delay = 2
    stats = m.evaluate(get_cuda_load_command(delay))

    validator = Validator(bool_exp=lambda _: True, success="yay", failure="oh")
    vr = validator.validate(stats)
    assert bool(vr)


@pytest.mark.skipif(
    not has_torch_cuda(),
    reason="NvidiaGPUPowerUtilization requires cuda to test.",
)
def test_power_validate_failure() -> None:
    m = NvidiaGPUPowerUtilization("identifier")

    # Blocks until process exit
    delay = 2
    stats = m.evaluate(get_cuda_load_command(delay))

    vr = Validator(
        bool_exp=lambda _: False, success="yay", failure="oh"
    ).validate(stats)
    assert not bool(vr)


# =================================================================================================
# NvidiaGPUPowerStatistics
# =================================================================================================


def test_statistics_construction():
    m = get_sample_evidence_metadata()

    stats = NvidiaGPUPowerStatistics(1, 2, 4).with_metadata(m)
    assert stats.avg == Quantity(1, Units.watt)
    assert stats.min == Quantity(2, Units.watt)
    assert stats.max == Quantity(4, Units.watt)
    assert stats.unit == Units.watt

    stats = NvidiaGPUPowerStatistics(
        4000, 6000, 8000, Units.milliwatt
    ).with_metadata(m)
    assert stats.avg == Quantity(4000, Units.milliwatt)
    assert stats.min == Quantity(6000, Units.milliwatt)
    assert stats.max == Quantity(8000, Units.milliwatt)
    assert stats.unit == Units.milliwatt


def test_result_save_load(
    store_with_context: Tuple[ArtifactStore, Context],  # noqa
) -> None:
    store, ctx = store_with_context

    stats = NvidiaGPUPowerStatistics(50, 10, 800).with_metadata(
        get_sample_evidence_metadata()
    )
    stats.save_with(ctx, store)

    r: NvidiaGPUPowerStatistics = typing.cast(
        NvidiaGPUPowerStatistics,
        NvidiaGPUPowerStatistics.load_with(
            "evidence.test_id", context=ctx, store=store
        ),
    )
    assert r.avg == stats.avg
    assert r.min == stats.min
    assert r.max == stats.max


def test_max_utilization_less_than() -> None:
    # Default units should work across the two classes.
    m = get_sample_evidence_metadata()

    validator = NvidiaGPUPowerStatistics.max_utilization_less_than(3)

    # Less than case
    res = validator.validate(
        NvidiaGPUPowerStatistics(avg=2, max=2, min=1).with_metadata(m)
    )
    assert bool(res)

    # Greater than case
    res = validator.validate(
        NvidiaGPUPowerStatistics(avg=2, max=4, min=1).with_metadata(m)
    )
    assert not bool(res)

    # Equals case
    res = validator.validate(
        NvidiaGPUPowerStatistics(avg=2, max=3, min=1).with_metadata(m)
    )
    assert not bool(res)


def test_max_utilization_less_than_in_bytes() -> None:
    # The units shouldn't matter
    m = get_sample_evidence_metadata()

    validator = NvidiaGPUPowerStatistics.max_utilization_less_than(
        3, unit=Units.watt
    )

    # Less than case
    res = validator.validate(
        NvidiaGPUPowerStatistics(
            avg=2, max=2, min=1, unit=Units.watt
        ).with_metadata(m)
    )
    assert bool(res)

    # Greater than case
    res = validator.validate(
        NvidiaGPUPowerStatistics(
            avg=2, max=4, min=1, unit=Units.watt
        ).with_metadata(m)
    )
    assert not bool(res)

    # Equals case
    res = validator.validate(
        NvidiaGPUPowerStatistics(
            avg=2, max=3, min=1, unit=Units.watt
        ).with_metadata(m)
    )
    assert not bool(res)


def test_max_utilization_less_than_invalid_unit() -> None:
    with pytest.raises(pint.UndefinedUnitError):
        _ = NvidiaGPUPowerStatistics.max_utilization_less_than(
            3000, Units.fakeunit
        )


def test_avg_utilization_less_than() -> None:
    m = get_sample_evidence_metadata()

    validator = NvidiaGPUPowerStatistics.average_utilization_less_than(3)

    # Less than case
    res = validator.validate(
        NvidiaGPUPowerStatistics(avg=2, max=2, min=1).with_metadata(m)
    )
    assert bool(res)

    # Greater than case
    res = validator.validate(
        NvidiaGPUPowerStatistics(avg=4, max=2, min=1).with_metadata(m)
    )
    assert not bool(res)

    # Equals case
    res = validator.validate(
        NvidiaGPUPowerStatistics(avg=3, max=2, min=1).with_metadata(m)
    )
    assert not bool(res)


def test_avg_utilization_less_than_in_milliwats() -> None:
    m = get_sample_evidence_metadata()

    validator = NvidiaGPUPowerStatistics.average_utilization_less_than(
        3000, Units.milliwatt
    )

    # Less than case
    res = validator.validate(
        NvidiaGPUPowerStatistics(
            avg=2000, max=2000, min=1000, unit=Units.milliwatt
        ).with_metadata(m)
    )
    assert bool(res)

    # Greater than case
    res = validator.validate(
        NvidiaGPUPowerStatistics(
            avg=4000, max=2000, min=1000, unit=Units.milliwatt
        ).with_metadata(m)
    )
    assert not bool(res)

    # Equals case
    res = validator.validate(
        NvidiaGPUPowerStatistics(
            avg=3000, max=2000, min=1000, unit=Units.milliwatt
        ).with_metadata(m)
    )
    assert not bool(res)


def test_average_utilization_less_than_invalid_unit() -> None:
    with pytest.raises(pint.UndefinedUnitError):
        _ = NvidiaGPUPowerStatistics.average_utilization_less_than(
            3000, Units.fakeunit
        )
