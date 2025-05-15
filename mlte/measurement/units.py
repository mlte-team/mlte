"""Loads and defines shared Units and Quantiies to be used."""

from typing import Optional

import pint

Units = pint.UnitRegistry()
"""Unit registry, contains all common units (use lowercase and singular unit name as attribute)."""

Unit = pint.Unit
"""Type for Units."""

Quantity = pint.Quantity
"""Quantity type that contains a magnitude and a Unit."""


def quantity_to_str(quantity: Quantity) -> str:
    """Converts a quantity to string, not adding `dimensionless` if there are no units."""
    return (
        f"{quantity}"
        if str(quantity.units) != "dimensionless"
        else f"{quantity.magnitude}"
    )


def unit_to_str(unit: Optional[Unit]) -> Optional[str]:
    """Converts unit to string, returning None if it is None."""
    return str(unit) if unit else None


def str_to_unit(unit_str: Optional[str]) -> Optional[Unit]:
    """Converts string to Unit, returning None if it is None."""
    return Units.Unit(unit_str) if unit_str else None
