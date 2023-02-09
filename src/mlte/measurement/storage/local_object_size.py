"""
Storage capacity measurement for locally-stored objects.
"""

import os

from mlte.measurement import Measurement
from mlte.measurement.result import Integer


class LocalObjectSize(Measurement):
    """Measure the size of a locally-stored object."""

    def __init__(self, identifier: str):
        """
        Initialize a new LocalObjectSize measurement.

        :param identifier: A unique identifier for the measurement
        :type identifier: str
        """
        super().__init__(self, identifier)

    def __call__(self, path: str) -> Integer:
        """
        Compute the size of the object at `path`.

        :param path: The path to the object
        :type path: str

        :return: The size of the object, in bytes
        :rtype: Integer
        """
        if not os.path.isfile(path) and not os.path.isdir(path):
            raise RuntimeError(f"Invalid path: {path}")

        # If the object is just a file, return it immediately
        if os.path.isfile(path):
            return Integer(self.metadata, os.path.getsize(path))

        # Otherwise, the object must be directory
        assert os.path.isdir(path), "Broken invariant."

        total_size = 0
        for dirpath, _, filenames in os.walk(path):
            for name in filenames:
                path = os.path.join(dirpath, name)
                if not os.path.islink(path):
                    total_size += os.path.getsize(path)

        return Integer(self.metadata, total_size)
