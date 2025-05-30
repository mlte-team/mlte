"""
Unit tests for ProcessMeasurement.
"""

import os
import sys
from pathlib import Path

from mlte.evidence.artifact import Evidence
from mlte.evidence.types.string import String
from mlte.measurement.process_measurement import ProcessMeasurement
from test.support.meta import path_to_support

# The spin duration, in seconds
SPIN_DURATION = 1
SPIN_COMMAND = [
    "python3",
    os.path.join(path_to_support(), "spin.py"),
    str(SPIN_DURATION),
]


class SampleProcessMeasurement(ProcessMeasurement):
    def __call__(self, pid: int, first_arg: str, *args, **kwargs) -> Evidence:
        print(first_arg)
        return String(first_arg)

    @classmethod
    def get_output_type(cls) -> type[Evidence]:
        return String


def test_start_script_job():
    spin = os.path.join(path_to_support(), "spin.py")
    args = [f"{SPIN_DURATION}"]

    # Spawn external job; blocks until process exit
    pid = ProcessMeasurement.start_script(spin, args)

    assert pid > 0


def test_start_general_job():
    spin = os.path.join(path_to_support(), str(Path(sys.executable)))
    args = ["spin.py", f"{SPIN_DURATION}"]

    # Spawn external job; blocks until process exit
    pid = ProcessMeasurement.start_process(spin, args)

    assert pid > 0


def test_evaluate_sync() -> None:
    """Test that we can properly evaluate synchronously."""
    m = SampleProcessMeasurement("id1")

    # Dummy process for testing purposes.
    args = ["python3", "spin.py", f"{SPIN_DURATION}"]

    result = m.evaluate(args, "test")

    assert type(result) is String and result.value == "test"
    assert m.evidence_metadata and m.evidence_metadata.test_case_id == "id1"


def test_evaluate_async() -> None:
    """Test that we can properly evaluate asynchronously."""
    m = SampleProcessMeasurement("id1")

    # Dummy process for testing purposes.
    spin = os.path.join(path_to_support(), str(Path(sys.executable)))
    args = ["spin.py", f"{SPIN_DURATION}"]
    pid = ProcessMeasurement.start_process(spin, args)

    m.evaluate_async(pid, "test")
    result = m.wait_for_output()

    assert type(result) is String and result.value == "test"
    assert m.evidence_metadata and m.evidence_metadata.test_case_id == "id1"
