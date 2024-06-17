"""
test/context/test_context.py

Unit tests for MLTE context.
"""

from mlte.context.context import Context


def test_complete() -> None:
    _ = Context("model0", "v0")
