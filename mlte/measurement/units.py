"""Loads and defines shared Units and Quantiies to be used."""

from typing import TypeAlias

import pint

# Init shared registry and main Quantity construct.
Units = pint.UnitRegistry()
Quantity = Units.Quantity

# Init types for typehints.
Unit: TypeAlias = pint.Unit
