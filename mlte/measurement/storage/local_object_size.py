"""
mlte/measurement/storage/local_object_size.py

Storage capacity measurement for locally-stored objects.
"""

import os
from typing import Optional

from mlte.evidence.types.integer import Integer
from mlte.measurement.measurement import Measurement
from mlte.measurement.units import Unit, Units


class LocalObjectSize(Measurement):
    """Measure the size of a locally-stored object. Calculates the results by default in bytes."""

    def __init__(self, identifier: Optional[str] = None):
        """
        Initialize a new LocalObjectSize measurement.

        :param identifier: A unique identifier for the measurement
        """
        super().__init__(identifier)

    def __call__(self, path: str, unit: Unit = Units.byte) -> Integer:
        """
        Compute the size of the object at `path`.

        :param path: The path to the object
        :param unit: The unit to return the size in, defaults to byte (Units.byte).

        :return: The size of the object, in bytes
        """
        if not os.path.isfile(path) and not os.path.isdir(path):
            raise RuntimeError(f"Invalid path: {path}")

        # If the object is just a file, just get its size.
        if os.path.isfile(path):
            total_size = os.path.getsize(path)
        else:
            # Otherwise, the object must be directory, get accumulated size.
            assert os.path.isdir(
                path
            ), f"Path {path} is not a file nor a folder."
            total_size = 0
            for dirpath, _, filenames in os.walk(path):
                for name in filenames:
                    path = os.path.join(dirpath, name)
                    if not os.path.islink(path):
                        total_size += os.path.getsize(path)

        # Convert to requested unit, if any.
        size_w_unit = total_size * unit
        return Integer(size_w_unit.magnitude, unit=unit)

    # Overriden.
    @classmethod
    def get_output_type(cls) -> type[Integer]:
        return Integer
