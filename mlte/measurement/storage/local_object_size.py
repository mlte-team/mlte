"""
mlte/measurement/storage/local_object_size.py

Storage capacity measurement for locally-stored objects.
"""

import os
from typing import Optional

from mlte.evidence.types.integer import Integer
from mlte.measurement.measurement import Measurement


class LocalObjectSize(Measurement):
    """Measure the size of a locally-stored object."""

    def __init__(self, identifier: Optional[str] = None):
        """
        Initialize a new LocalObjectSize measurement.

        :param identifier: A unique identifier for the measurement
        """
        super().__init__(identifier)

    def __call__(self, path: str) -> Integer:
        """
        Compute the size of the object at `path`.

        :param path: The path to the object

        :return: The size of the object, in bytes
        """
        if not os.path.isfile(path) and not os.path.isdir(path):
            raise RuntimeError(f"Invalid path: {path}")

        # If the object is just a file, return it immediately
        if os.path.isfile(path):
            return Integer(os.path.getsize(path))

        # Otherwise, the object must be directory
        assert os.path.isdir(path), "Broken invariant."

        total_size = 0
        for dirpath, _, filenames in os.walk(path):
            for name in filenames:
                path = os.path.join(dirpath, name)
                if not os.path.islink(path):
                    total_size += os.path.getsize(path)

        return Integer(total_size)

    # Overriden.
    @classmethod
    def get_output_type(cls) -> type[Integer]:
        return Integer
