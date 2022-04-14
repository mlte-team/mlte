"""
Unit tests for PropertyToken.
"""

from mlte.properties import PropertyToken


def test_equality():
    a = PropertyToken("Test")
    b = a
    assert a == b


def test_inequality():
    a = PropertyToken("Test")
    b = PropertyToken("Test")
    assert a != b
