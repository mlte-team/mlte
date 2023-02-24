"""
Unit test for ProcessMeasurement.
"""

import os
import time

from mlte.measurement import (
    ProcessMeasurement
)

from ..support.meta import path_to_support

# The spin duration, in seconds
SPIN_DURATION = 5


def test_start_job():
    spin = os.path.join(path_to_support(), "spin.py")
    args = [f"{SPIN_DURATION}"]

    # Spawn external job; blocks until process exit
    pid = ProcessMeasurement.start_process(spin, args)

    assert pid > 0
