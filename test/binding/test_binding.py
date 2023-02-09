"""
Unit tests for Binding.
"""

import pytest

import mlte
from mlte.binding import Binding


def test_init():
    b = Binding({"foo": ["bar", "baz"]})
    i = b.identifiers_for("foo")
    assert i == ["bar", "baz"] or i == ["baz", "bar"]


def test_equality0():
    a = Binding({"foo": ["bar", "baz"]})
    b = Binding({"foo": ["bar", "baz"]})
    assert a == b


def test_equality1():
    a = Binding({"foo": ["bar", "baz"]})
    b = Binding({"foo": ["baz", "bar"]})
    assert a == b


def test_equality2():
    a = Binding({"foo": ["bar", "baz"]})
    b = Binding({"bar": ["foo", "baz"]})
    assert a != b


def test_equality3():
    a = Binding({"foo": ["bar", "baz"]})
    b = Binding({"foo": ["woo", "baz"]})
    assert a != b


def test_integrity0():
    with pytest.raises(RuntimeError):
        _ = Binding({1: ["foo", "bar"]})  # type: ignore


def test_integrity1():
    with pytest.raises(RuntimeError):
        _ = Binding({"foo": "bar"})  # type: ignore


def test_integrity2():
    with pytest.raises(RuntimeError):
        _ = Binding({"foo": ["bar", 2]})  # type: ignore


def test_save_load0(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    b = Binding({"foo": ["bar", "baz"]})
    b.save()

    r = Binding.load()
    assert r == b


def test_save_load1(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    with pytest.raises(RuntimeError):
        _ = Binding.load()
