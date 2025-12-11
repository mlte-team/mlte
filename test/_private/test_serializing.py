"""Unit tests for serialization functions."""

from mlte._private.serializing import (
    compare_callable,
    decode_callable,
    encode_callable,
)


def test_round_trip():
    bool_exp = lambda x, y: x > y  # noqa: E731

    encoded_str = encode_callable(bool_exp)
    decoded = decode_callable(encoded_str)

    assert compare_callable(bool_exp, decoded)
