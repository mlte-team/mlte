"""Unit test for pynvml_utils."""

import importlib
from importlib import import_module
from unittest.mock import MagicMock, patch

import pytest

import mlte.measurement.utility.pynvml_utils as pynvml_utils

# =================================================================================================
#  _   _ _   _ _ _ _   _
# | | | | |_(_) (_) |_(_)___ ___
# | |_| |  _| | | |  _| / -_|_-<
#  \___/ \__|_|_|_|\__|_\___/__/
# =================================================================================================


def has_pynvml():
    try:
        pynvml = import_module("pynvml")
        pynvml.nvmlInit()
        return True
    except ModuleNotFoundError:
        return False
    except AttributeError:
        return False
    except Exception:
        return False


def has_torch_cuda() -> bool:
    """
    Checks to see if torch and cuda are available. We need both of these for this test.
    :return: True if we have access to torch and cuda.
    """
    # DESIGN NOTE: Arguably, we could use nvidia-smi alone to see if we have access to cuda, but
    # we don't have code to load the cuda device without torch. We could use a different package
    # such as cupy, but that still requires something that probably isn't installed.

    try:
        torch = importlib.import_module("torch")
        return bool(torch.cuda.is_available())
    except ModuleNotFoundError:
        # The module isn't there, so we can't run our experiment anyway
        return False
    except AttributeError:
        # We had some other error so we can't run the test with cuda either.
        return False


def pynvml_dummy_fn(pynvml, handle: int, ret_val: float = 0.0) -> float:
    # We don't actually call these, but they should be value
    assert pynvml is not None
    assert isinstance(handle, int)

    return ret_val


def pynvml_stack_fn(pynvml, handle: int, values: list[int]) -> float:
    # We don't actually call these, but they should be value
    assert pynvml is not None
    assert isinstance(handle, int)

    return values.pop(0)


def make_stack_fn(values: list[int]):
    # We have the values here as a closure so we can pop them in the stack fn
    values = values.copy()
    return lambda a, b: pynvml_stack_fn(a, b, values)


def pynvml_test_import_handle(
    pynvml, handle: int, mock_pynvml, mock_handle
) -> float:
    # Check the mock handle and pass back the mocked pynvml
    assert pynvml == mock_pynvml
    assert handle == mock_handle

    return 0.0


def make_pynvml_mocks(device_count: int = 2, mock_handle: int = 1234):
    mock_pynvml = MagicMock()
    mock_pynvml.nvmlDeviceGetCount.return_value = device_count
    mock_pynvml.nvmlDeviceGetHandleByIndex.return_value = mock_handle

    return mock_pynvml, mock_handle


# =================================================================================================
#   __  __         _          _    ___ ___ _   _   _____       _
# |  \/  |___  __| |_____ __| |  / __| _ \ | | | |_   _|__ __| |_ ___
# | |\/| / _ \/ _| / / -_) _` | | (_ |  _/ |_| |   | |/ -_|_-<  _(_-<
# |_|  |_\___/\__|_\_\___\__,_|  \___|_|  \___/    |_|\___/__/\__/__/
# =================================================================================================


@patch("mlte.measurement.utility.pynvml_utils.psutil.pid_exists")
@patch("mlte.measurement.utility.pynvml_utils.import_module")
def test_aggregate_measurements_from_process(
    mock_import_module, mock_pid_exists
):
    # The aggregate checks for the pid and when it goes away, the aggreator exit5s
    mock_pid_exists.side_effect = [True, True, True, True, False]

    # Fake out the gpu code
    mocked_pynvml, _ = make_pynvml_mocks()
    mock_import_module.return_value = mocked_pynvml

    # We set the time to very small, because there are no real sub-processes involved
    minimum, maximum, average = (
        pynvml_utils.aggregate_measurements_from_process(
            pid=4,
            poll_interval=0.1,
            gpu_ids=[0],
            fn=make_stack_fn([5, 4, 3, 2]),
        )
    )
    assert minimum == 2
    assert maximum == 5
    assert average == 3.5


@patch("mlte.measurement.utility.pynvml_utils.import_module")
def test_get_statistics_faking_gpu(mock_import_module):
    """
    This tests to see if the get statistic function:
    - imports pynvml
    - Finds more gpus than our id
    - Makes a call to get handle
    :return: None
    """

    # We have to patch the path to where it was actually included to make sure we get the right
    # instance mocked
    mocked_pynvml, mock_handle = make_pynvml_mocks()
    mock_import_module.return_value = mocked_pynvml

    # Now, at this point import_lib is mocked and will return a fake library.
    # So, we should be able to call our test function and check for the handle and get back the mocked library
    ret_val = pynvml_utils.get_pynvml_statistic(
        [0],
        lambda a, b: pynvml_test_import_handle(
            a, b, mocked_pynvml, mock_handle
        ),
    )

    assert len(ret_val) == 1
    assert ret_val[0] == 0.0


def test_gpu_out_of_range():
    # We have to patch the path to where it was actually included to make sure we get the right
    # instance mocked
    with patch(
        "mlte.measurement.utility.pynvml_utils.import_module"
    ) as mock_import_module:
        mock_handle = 1234

        mocked_pynvml = MagicMock()
        mocked_pynvml.nvmlDeviceGetCount.return_value = 2
        mocked_pynvml.nvmlDeviceGetHandleByIndex.return_value = mock_handle

        mock_import_module.return_value = mocked_pynvml

        # Now, at this point import_lib is mocked and will return a fake library.
        # So, we should be able to call our test function and check for the handle and get back the mocked library
        with pytest.raises(Exception):
            pynvml_utils.get_pynvml_statistic([4], pynvml_dummy_fn)


@pytest.mark.skipif(
    has_pynvml(),
    reason="NvidiaGPUMemoryUtilization has pynvml so can't test errors.",
)
def test_pynvml_not_found():
    # TODO: In the future have a way to discriminate between different internal errors
    with pytest.raises(Exception) as excinfo:
        pynvml_utils.get_pynvml_statistic(
            [0], lambda p, h: pynvml_dummy_fn(p, h, 4.0)
        )
        assert "NVMLError_LibraryNotFound" in str(excinfo.value)


# =================================================================================================
#  ___          _    ___ ___ _   _   _____       _
# | _ \___ __ _| |  / __| _ \ | | | |_   _|__ __| |_ ___
# |   / -_) _` | | | (_ |  _/ |_| |   | |/ -_|_-<  _(_-<
# |_|_\___\__,_|_|  \___|_|  \___/    |_|\___/__/\__/__/
# =================================================================================================


def get_memory_total(pynvml, handle: int) -> float:
    memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    return int(memory_info.total)


@pytest.mark.skipif(
    not has_torch_cuda(),
    reason="NvidiaGPUMemoryUtilization requires cuda to test.",
)
def test_cuda_access():
    ret_val = pynvml_utils.get_pynvml_statistic([0], get_memory_total)
    assert len(ret_val) == 1
    assert ret_val[0] > 0
