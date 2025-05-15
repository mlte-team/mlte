"""Tests for unit module."""

import pytest

from mlte.measurement.units import (
    Quantity,
    Unit,
    Units,
    quantity_to_str,
    str_to_unit,
    unit_to_str,
)


@pytest.mark.parametrize(
    "input,expected_output", [(Units.meter, "meter"), (None, None)]
)
def test_unit_to_str(input: Unit, expected_output: str):
    str_unit = unit_to_str(input)
    assert str_unit == expected_output


@pytest.mark.parametrize(
    "input,expected_output", [("meter", Units.meter), (None, None)]
)
def test_str_to_unit(input: str, expected_output: Unit):
    unit = str_to_unit(input)
    assert unit == expected_output


@pytest.mark.parametrize(
    "input,input_unit,expected_output",
    [(1, Units.meter, "1 meter"), (2, None, "2")],
)
def test_quantity_to_str(input: int, input_unit: Unit, expected_output: str):
    quantity = Quantity(input, input_unit)
    assert quantity_to_str(quantity) == expected_output
