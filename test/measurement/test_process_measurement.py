"""
Unit test for ProcessMeasurement.
"""

import os
import sys
from pathlib import Path

from mlte.measurement import ProcessMeasurement

from ..support.meta import path_to_support

# The spin duration, in seconds
SPIN_DURATION = 5


def test_start_script_job():
    spin = os.path.join(path_to_support(), "spin.py")
    args = [f"{SPIN_DURATION}"]

    # Spawn external job; blocks until process exit
    pid = ProcessMeasurement.start_script(spin, args)

    assert pid > 0


def test_start_general_job():
    spin = os.path.join(
        path_to_support(), str(Path(sys.executable))
    )
    args = ["spin.py", f"{SPIN_DURATION}"]

    # Spawn external job; blocks until process exit
    pid = ProcessMeasurement.start_process(spin, args)

    assert pid > 0
