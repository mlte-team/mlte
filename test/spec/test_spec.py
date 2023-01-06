"""
Unit tests for Spec functionality.
"""

import pytest
from typing import Dict, Any

from mlte.spec import Spec
from mlte.property import Property
from mlte.measurement import Measurement
from mlte.property.costs import StorageCost


class DummyProperty(Property):
    def __init__(self):
        super().__init__("DummyProperty", "A dummy measurement.")


class DummyMeasurement0(Measurement):
    def __init__(self, identifier: str):
        super().__init__(self, identifier)

    def __call__(self, value: bool) -> Dict[str, Any]:
        return {"value": value}


class DummyMeasurement1(Measurement):
    def __init__(self, identifier: str):
        super().__init__(self, identifier)

    def __call__(self, value: bool) -> Dict[str, Any]:
        return {"value": value}


def test_save(tmp_path):
    path = (tmp_path / "spec").with_suffix(".json")

    spec = Spec("MySpec", StorageCost())
    spec.save(f"{path}")
    assert path.exists() and path.is_file()


def test_load(tmp_path):
    path = (tmp_path / "spec").with_suffix(".json")

    spec = Spec("MySpec", StorageCost())
    spec.save(f"{path}")
    assert path.exists() and path.is_file()

    spec = Spec.from_file(f"{path}")
    assert spec.name == "MySpec"
    assert spec.has_property("StorageCost")


def test_collect_empty_fail():
    # Collect on empty collection with `strict = True` should fail
    spec = Spec("MySpec", DummyProperty())
    with pytest.raises(RuntimeError):
        _ = spec.collect()


def test_collect_empty_success():
    # Collect on empty collection with `strict = False` should succeed
    spec = Spec("MySpec", DummyProperty())
    _ = spec.collect(strict=False)


# TODO(Kyle): Fix to make functional
@pytest.mark.skip()
def test_collect_unique():
    # Collect with duplicated results should fail
    spec = Spec("MySpec", DummyProperty())
    m0 = DummyMeasurement0()
    m1 = DummyMeasurement1()
    _ = spec.collect(*(*m0.validate(True), *m1.validate(True)))


# TODO(Kyle): Fix to make functional
@pytest.mark.skip()
def test_collect_duplicates():
    # Collect with duplicated results should fail
    spec = Spec("MySpec", DummyProperty())
    m0 = DummyMeasurement0()
    m1 = DummyMeasurement0()
    with pytest.raises(RuntimeError):
        _ = spec.collect(*(*m0.validate(True), *m1.validate(True)))
