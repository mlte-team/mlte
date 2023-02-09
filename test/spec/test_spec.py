"""
Unit tests for Spec functionality.
"""

import os
import pytest
from typing import Dict, Any

from mlte.spec import Spec
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
    path = os.path.join(tmp_path.as_posix(), "spec.json")

    spec = Spec("MySpec", StorageCost())
    spec.save(path)
    assert os.path.exists(path) and os.path.isfile(path)


def test_load(tmp_path):
    path = os.path.join(tmp_path.as_posix(), "spec.json")

    spec = Spec("MySpec", StorageCost())
    spec.save(path)
    assert os.path.exists(path) and os.path.isfile(path)

    spec = Spec.from_file(path)
    assert spec.name == "MySpec"
    assert spec.has_property("StorageCost")


def test_bind0():
    # Binding to existing property should succeed
    spec = Spec("MySpec", DummyProperty())
    _ = bind(DummyMeasurement0(), spec.get_property("DummyProperty"))
    assert True


def test_bind1():
    # Binding to nonexistent property should fail
    spec = Spec("MySpec")
    with pytest.raises(RuntimeError):
        _ = bind(DummyMeasurement0(), spec.get_property("DummyProperty"))


def test_collect_empty_fail():
    # Collect on empty collection with `strict = True` should fail
    spec = Spec("MySpec", DummyProperty())
    with pytest.raises(RuntimeError):
        _ = spec.collect()


def test_collect_empty_success():
    # Collect on empty collection with `strict = False` should succeed
    spec = Spec("MySpec", DummyProperty())
    _ = spec.collect(strict=False)


def test_collect_bound_success():
    # Collect with bound measurement should succeed
    spec = Spec("MySpec", DummyProperty())
    valid = bind(
        DummyMeasurement0().with_validator(
            Validator("MyValidator", lambda _: Success())
        ),
        spec.get_property("DummyProperty"),
    )
    _ = spec.collect(*valid.validate(True))


def test_collect_unbound_failure():
    # Collect with unbound measurement should fail
    spec = Spec("MySpec", DummyProperty())
    valid = DummyMeasurement0().with_validator(
        Validator("MyValidator", lambda _: Success())
    )
    with pytest.raises(RuntimeError):
        _ = spec.collect(*valid.validate(True))


def test_collect_bound_failure():
    # Collect with measurement bound to
    # missing property should fail
    spec = Spec("MySpec", DummyProperty())
    valid = bind(
        DummyMeasurement0().with_validator(
            Validator("MyValidator", lambda _: Success())
        ),
        "DummyPropertyFoo",
    )
    with pytest.raises(RuntimeError):
        _ = spec.collect(*valid.validate(True))


def test_collect_unique():
    # Collect with duplicated results should fail
    spec = Spec("MySpec", DummyProperty())
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
    _ = spec.collect(*(*m0.validate(True), *m1.validate(True)))


def test_collect_duplicates():
    # Collect with duplicated results should fail
    spec = Spec("MySpec", DummyProperty())
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
        _ = spec.collect(*(*m0.validate(True), *m1.validate(True)))
