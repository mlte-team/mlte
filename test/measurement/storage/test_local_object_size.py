"""
test/measurement/storage/test_local_object_size.py

Unit test for LocalObjectSize measurement.
"""

from __future__ import annotations

import typing
from pathlib import Path
from typing import Any, Dict

from mlte.evidence.types.integer import Integer
from mlte.measurement.storage import LocalObjectSize
from mlte.results.result import Result

# -----------------------------------------------------------------------------
# Directory Hierarchy Construction
# -----------------------------------------------------------------------------


def _create_file(path: Path, size: int):
    """
    Create a file at `path` with size `size`.

    :param path: The path at which the file is created
    :type path: Path
    :param size: The size of the file, in bytes
    :type size: int
    """
    with path.open("w") as f:
        # TODO(Kyle): Increase functionality of this
        for _ in range(size):
            f.write("a")

    assert path.exists() and path.is_file()


def _create_fs_hierarchy(root: Path, template: Dict[str, Any]):
    """
    Construct a directory hierarchy described by `template`.

    This function is intended to be invoked recursively.

    :param root: The path to the root from which to begin construction
    :param template: The template that describes the hierarchy
    """
    assert root.exists() and root.is_dir(), "Broken precondition."
    for name, value in template.items():
        local_prefix = root / name
        if isinstance(value, int):
            # This (K, V) requests file creation;
            # the value is the size of the file
            _create_file(local_prefix, value)
        else:
            # Assume this (K, V) requests directory creation;
            # the value is the remainder of the template
            local_prefix.mkdir()
            _create_fs_hierarchy(local_prefix, value)


def create_fs_hierarchy(root: Path, template: Dict[str, Any]):
    """
    Construct a directory hierarchy described by `template`.

    This function is the entry point for recursive construction.

    :param base: The path to the root directory for the hierarchy
    :param template: The template that describes the hierarchy
    """

    assert len(template) == 1, "Root of hierarchy must have size 1."
    _create_fs_hierarchy(root, template)


# -----------------------------------------------------------------------------
# Directory Hierarchy Analysis
# -----------------------------------------------------------------------------


def _expected_hierarchy_size(template: Dict[str, Any]) -> int:
    """
    Compute the expected size of the hierarchy from `template`.

    This function is intended to be invoked recursively.

    :param template: The template that describes the hierarchy

    :return: The total size of all files in the hierarchu
    :rtype: int
    """
    return sum(
        map(
            lambda v: v if isinstance(v, int) else _expected_hierarchy_size(v),
            template.values(),
        )
    )


def expected_hierarchy_size(template: Dict[str, Any]) -> int:
    """
    Compute the expected size of the hierarchy from `template`.

    This function is the entry point for recursive construction.

    :param template: The template that describes the hierarchy

    :return: The total size of all files in the hierarchu
    :rtype: int
    """
    assert len(template) == 1, "Root of hierarchy must have size 1."
    return _expected_hierarchy_size(template)


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


def test_constructor_type():
    """ "Checks that the constructor sets up type properly."""
    m = LocalObjectSize("id")

    assert (
        m.evidence_metadata
        and m.evidence_metadata.measurement.measurement_class
        == "mlte.measurement.storage.local_object_size.LocalObjectSize"
    )


def test_file(tmp_path):
    # Test with a model represented as file
    model = {"model": 32}
    create_fs_hierarchy(tmp_path, model)

    m = LocalObjectSize("identifier")

    size: Integer = typing.cast(Integer, m.evaluate(str(tmp_path / "model")))
    assert size.value == expected_hierarchy_size(model)


def test_directory(tmp_path):
    # Test with a model represented as directory
    model = {"model": {"params": 1024, "hyperparams": 32}}
    create_fs_hierarchy(tmp_path, model)

    m = LocalObjectSize("identifier")

    size: Integer = typing.cast(Integer, m.evaluate(str(tmp_path / "model")))
    assert size.value == expected_hierarchy_size(model)


def test_validation_less_than(tmp_path):
    create_fs_hierarchy(tmp_path, {"model": 64})

    m = LocalObjectSize("identifier")

    size: Integer = typing.cast(Integer, m.evaluate(str(tmp_path / "model")))

    # Validation success
    v = Integer.less_than(128).validate(size)
    assert isinstance(v, Result)
    assert bool(v)

    # Validation failure
    v = Integer.less_than(64).validate(size)
    assert isinstance(v, Result)
    assert not bool(v)


def test_validation_less_or_equal_to(tmp_path):
    create_fs_hierarchy(tmp_path, {"model": 64})

    m = LocalObjectSize("identifier")

    size: Integer = typing.cast(Integer, m.evaluate(str(tmp_path / "model")))

    # Validation success
    v = Integer.less_or_equal_to(64).validate(size)
    assert isinstance(v, Result)
    assert bool(v)

    # Validation failure
    v = Integer.less_or_equal_to(63).validate(size)
    assert isinstance(v, Result)
    assert not bool(v)
