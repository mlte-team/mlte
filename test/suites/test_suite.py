"""
Unit tests for Suite functionality.
"""

import os
import pytest
from typing import Dict, Any

from mlte.suite import Suite
from mlte.property import Property
from mlte.measurement import Measurement, bind
from mlte.measurement.validation import Validator, Success
from mlte.property.costs import StorageCost


class DummyProperty(Property):
    def __init__(self):
        super().__init__("DummyProperty", "A dummy measurement.")


class DummyMeasurement0(Measurement):
    def __init__(self):
        super().__init__("DummyMeasurement0")

    def __call__(self, value: bool) -> Dict[str, Any]:
        return {"value": value}


class DummyMeasurement1(Measurement):
    def __init__(self):
        super().__init__("DummyMeasurement1")

    def __call__(self, value: bool) -> Dict[str, Any]:
        return {"value": value}


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


def test_bind0():
    # Binding to existing property should succeed
    suite = Suite("MySuite", DummyProperty())
    _ = bind(DummyMeasurement0(), suite.get_property("DummyProperty"))
    assert True


def test_bind1():
    # Binding to nonexistent property should fail
    suite = Suite("MySuite")
    with pytest.raises(RuntimeError):
        _ = bind(DummyMeasurement0(), suite.get_property("DummyProperty"))


def test_collect_empty_fail():
    # Collect on empty collection with `strict = True` should fail
    suite = Suite("MySuite", DummyProperty())
    with pytest.raises(RuntimeError):
        _ = suite.collect()


def test_collect_empty_success():
    # Collect on empty collection with `strict = False` should succeed
    suite = Suite("MySuite", DummyProperty())
    _ = suite.collect(strict=False)


def test_collect_bound_success():
    # Collect with bound measurement should succeed
    suite = Suite("MySuite", DummyProperty())
    valid = bind(
        DummyMeasurement0().with_validator(
            Validator("MyValidator", lambda _: Success())
        ),
        suite.get_property("DummyProperty"),
    )
    _ = suite.collect(*valid.validate(True))


def test_collect_unbound_failure():
    # Collect with unbound measurement should fail
    suite = Suite("MySuite", DummyProperty())
    valid = DummyMeasurement0().with_validator(
        Validator("MyValidator", lambda _: Success())
    )
    with pytest.raises(RuntimeError):
        _ = suite.collect(*valid.validate(True))


def test_collect_bound_failure():
    # Collect with measurement bound to
    # missing property should fail
    suite = Suite("MySuite", DummyProperty())
    valid = bind(
        DummyMeasurement0().with_validator(
            Validator("MyValidator", lambda _: Success())
        ),
        "DummyPropertyFoo",
    )
    with pytest.raises(RuntimeError):
        _ = suite.collect(*valid.validate(True))


def test_collect_unique():
    # Collect with duplicated results should fail
    suite = Suite("MySuite", DummyProperty())
    m0 = bind(
        DummyMeasurement0().with_validator(
            Validator("MyValidator", lambda _: Success())
        ),
        "DummyProperty",
    )
    m1 = bind(
        DummyMeasurement1().with_validator(
            Validator("MyValidator", lambda _: Success())
        ),
        "DummyProperty",
    )
    _ = suite.collect(*(*m0.validate(True), *m1.validate(True)))


def test_collect_duplicates():
    # Collect with duplicated results should fail
    suite = Suite("MySuite", DummyProperty())
    m0 = bind(
        DummyMeasurement0().with_validator(
            Validator("MyValidator", lambda _: Success())
        ),
        "DummyProperty",
    )
    m1 = bind(
        DummyMeasurement0().with_validator(
            Validator("MyValidator", lambda _: Success())
        ),
        "DummyProperty",
    )
    with pytest.raises(RuntimeError):
        _ = suite.collect(*(*m0.validate(True), *m1.validate(True)))
