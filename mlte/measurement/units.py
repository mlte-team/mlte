"""Loads and defines shared Units and Quantiies to be used."""

import pint

# Init shared registry.
Units = pint.UnitRegistry()

# Export types from here, to abstract out the use of pint.
Unit = pint.Unit
Quantity = pint.Quantity
