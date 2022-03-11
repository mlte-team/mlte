"""
Unit test for LocalModelSize property.
"""

from mlte.properties.storage import LocalModelSize


def test_file():
    # Test with a model represented as file
    _ = LocalModelSize()
    assert True


def test_directory():
    # Test with a model represented as directory
    _ = LocalModelSize()
    assert True
