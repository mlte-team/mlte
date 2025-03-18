"""
Unit tests for ProcessMeasurement.
"""

import os
import sys
from pathlib import Path

from mlte.evidence.artifact import Evidence
from mlte.evidence.types.integer import Integer
from mlte.measurement.process_measurement import ProcessMeasurement
from test.support.meta import path_to_support

# The spin duration, in seconds
SPIN_DURATION = 1


class SampleProcessMeasurement(ProcessMeasurement):
    def __call__(self, pid: int, *args, **kwargs) -> Evidence:
        return Integer(pid)

    def get_output_type(self) -> type[Evidence]:
        return Integer


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


def test_evaluate_async() -> None:
    """Test that we can properly evaluate asynchronously."""
    m = SampleProcessMeasurement("id1")

    # Dummy process for testing purposes.
    spin = os.path.join(path_to_support(), str(Path(sys.executable)))
    args = ["spin.py", f"{SPIN_DURATION}"]
    pid = ProcessMeasurement.start_process(spin, args)

    m.evaluate_async(pid)
    result = m.wait_for_output()

    assert m.get_output_type() == Integer
    assert type(result) is Integer and result.value == pid
    assert m.evidence_metadata and m.evidence_metadata.test_case_id == "id1"
