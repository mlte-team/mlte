"""Loads and defines shared Units and Quantiies to be used."""

import pint

# Init shared registry and main Quantity construct.
Units = pint.UnitRegistry()
Quantity = Units.Quantity

# Init types for typehints.
QuantityType = pint.Quantity
UnitType = pint.Unit
