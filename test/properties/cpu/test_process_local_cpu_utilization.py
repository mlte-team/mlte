"""
Unit test for ProcessLocalCPUUtilization property.
"""


import os
import pytest
import threading
import subprocess

from mlte.platform.os import is_windows, is_nix
from mlte.properties.cpu import ProcessLocalCPUUtilization


def support_path() -> str:
    """Get the absolute path to the support directory."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "support/")


def spin_for(seconds: int):
    """Run the spin.py program for `seconds`."""
    path = os.path.join(support_path(), "spin.py")
    prog = subprocess.Popen(["python", path, f"{seconds}"])
    thread = threading.Thread(target=lambda: prog.wait())
    thread.start()
    return prog


@pytest.mark.skipif(is_windows())
def test_cpu_nix():
    prog = spin_for(5)
    prop = ProcessLocalCPUUtilization()
    stat = prop(prog.pid)
    assert len(str(stat)) > 0


@pytest.mark.skipif(is_nix())
def test_cpu_windows():
    with pytest.raises(RuntimeError):
        _ = ProcessLocalCPUUtilization()
