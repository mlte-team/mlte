"""
test/context/test_context.py

Unit tests for MLTE context.
"""

from mlte.context import Context


def test_complete() -> None:
    _ = Context("ns0", "model0", "v0")
