"""
Storage capacity measurement for locally-stored objects.
"""

import os
from typing import Dict, Any

from ..measurement import Measurement
from ..evaluation import Integer
from ..validation import Validator, Success, Failure


class LocalObjectSize(Measurement):
    """Measure the size of a locally-stored object."""

    def __init__(self):
        """Initialize a new LocalObjectSize measurement."""
        super().__init__("LocalObjectSize")

    def __call__(self, path: str) -> Dict[str, Any]:
        """
        Compute the size of the object at `path`.

        :param path: The path to the object
        :type path: str

        :return: The size of the object, in bytes
        :rtype: Dict
        """
        if not os.path.isfile(path) and not os.path.isdir(path):
            raise RuntimeError(f"Invalid path: {path}")

        # If the object is just a file, return it immediately
        if os.path.isfile(path):
            return {"total_size": os.path.getsize(path)}

        # Otherwise, the object must be directory
        assert os.path.isdir(path), "Broken invariant."

        total_size = 0
        for dirpath, _, filenames in os.walk(path):
            for name in filenames:
                path = os.path.join(dirpath, name)
                if not os.path.islink(path):
                    total_size += os.path.getsize(path)

        return {"total_size": total_size}

    def semantics(self, data: Dict[str, Any]) -> Integer:
        """Provide semantics for measurement output."""
        assert "total_size" in data, "Broken invariant."
        return Integer(self, data["total_size"])

    def with_validator_size_not_greater_than(
        self, threshold: int
    ) -> Measurement:
        """
        Add a validator for the size of the object.

        :param threshold: The threshold for object size, in bytes
        :type threshold: int

        :return: The measurement instance (`self`)
        :rtype: Measurement
        """
        return self.with_validator(
            Validator(
                "MaximumSize",
                lambda size: Success(
                    f"Object size {size} below threshold {threshold}"
                )
                if size.value <= threshold
                else Failure(
                    f"Object size {size} exceeds threshold {threshold}"
                ),
            )
        )
