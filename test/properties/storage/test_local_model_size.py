"""
Unit test for LocalModelSize property.
"""

import os
import shutil
from typing import Dict, Any

from mlte.properties.storage import LocalModelSize


def _create_file(path: str, size: int):
    """
    Create a file at `path` with size `size`.

    :param path: The path at which the file is created
    :type path: str
    :param size: The size of the file, in bytes
    :type size: int
    """
    with open(path, "w") as f:
        # TODO(Kyle): Increase functionality of this
        for _ in range(size):
            f.write("a")

    assert os.path.exists(path) and os.path.isfile(path)


def _create_fs_hierarchy(prefix: str, template: Dict[str, Any]):
    """
    Construct a directory hierarchy described by `template`.

    This function is intended to be invoked recursively.

    :param template: The template that describes the hierarchy
    """

    for name, value in template.items():
        local_prefix = os.path.join(prefix, name)
        if isinstance(value, int):
            # This (K, V) requests file creation;
            # the value is the size of the file
            _create_file(local_prefix, value)
        else:
            # Assume this (K, V) requests directory creation;
            # the value is the remainder of the template
            os.mkdir(local_prefix)
            _create_fs_hierarchy(local_prefix, value)


def create_fs_hierarchy(template: Dict[str, Any]):
    """
    Construct a directory hierarchy described by `template`.

    This function is the entry point for recursive construction.

    :param template: The template that describes the hierarchy
    """

    assert len(template) == 1, "Root of hierarchy must have size 1."
    _create_fs_hierarchy(os.getcwd(), template)


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


def test_file():
    # Test with a model represented as file
    model = {"model": 32}
    create_fs_hierarchy(model)

    prop = LocalModelSize()
    size = prop("model")

    assert size == expected_hierarchy_size(model)
    os.remove("model")


def test_directory():
    # Test with a model represented as directory
    model = {"model": {"params": 1024, "hyperparams": 32}}
    create_fs_hierarchy(model)

    prop = LocalModelSize()
    size = prop("model")

    assert size == expected_hierarchy_size(model)
    shutil.rmtree("model")
