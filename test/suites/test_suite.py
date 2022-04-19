"""
Unit tests for Suite functionality.
"""

import os

from mlte.suites import Suite
from mlte.properties.costs import StorageCost


def test_save(tmp_path):
    path = os.path.join(tmp_path.as_posix(), "suite.json")

    suite = Suite("MySuite", StorageCost())
    suite.save(path)
    assert os.path.exists(path) and os.path.isfile(path)


def test_load(tmp_path):
    path = os.path.join(tmp_path.as_posix(), "suite.json")

    suite = Suite("MySuite", StorageCost())
    suite.save(path)
    assert os.path.exists(path) and os.path.isfile(path)

    suite = Suite.from_file(path)
    assert suite.name == "MySuite"
    assert suite.has_property("StorageCost")
