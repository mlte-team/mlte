"""Loads and defines shared Units and Quantiies to be used."""

from typing import Optional

import pint

# Init shared registry.
Units = pint.UnitRegistry()

# Export types from here, to abstract out the use of pint.
Unit = pint.Unit
Quantity = pint.Quantity


def unit_to_str(unit: Optional[Unit]) -> Optional[str]:
    """Coverts unit to string, returning None if it is None."""
    return str(unit) if unit else None


def str_to_unit(unit_str: Optional[str]) -> Optional[Unit]:
    """Coverts string to Unit, returning None if it is None."""
    return Units.Unit(unit_str) if unit_str else None
