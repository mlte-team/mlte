"""
Storage capacity measurement for locally-stored models.
"""

import os
from typing import Dict, Any

from ..property import Property
from ..evaluation import Integer
from ..validation import Validator, Success, Failure


class LocalModelSize(Property):
    """Measure the size of a locally-stored model."""

    def __init__(self):
        """Initialize a new LocalModelSize property."""
        super().__init__("LocalModelSize")

    def __call__(self, path: str) -> Dict[str, Any]:
        """
        Compute the size of the model at `path`.

        :param path: The path to the model
        :type path: str

        :return: The size of the model, in bytes
        :rtype: Dict
        """
        if not os.path.isfile(path) and not os.path.isdir(path):
            raise RuntimeError(f"Invalid path: {path}")

        # If the model is just a file, return it immediately
        if os.path.isfile(path):
            return {"total_size": os.path.getsize(path)}

        # Otherwise, the model must be directory
        assert os.path.isdir(path), "Broken invariant."

        total_size = 0
        for dirpath, _, filenames in os.walk(path):
            for name in filenames:
                path = os.path.join(dirpath, name)
                if not os.path.islink(path):
                    total_size += os.path.getsize(path)

        return {"total_size": total_size}

    def semantics(self, data: Dict[str, Any]) -> Integer:
        """Provide semantics for property output."""
        assert "total_size" in data, "Broken invariant."
        return Integer(self, data["total_size"])

    def add_validator_size_not_greater_than(self, threshold: int):
        """
        Add a validator for the size of the model.

        :param threshold: The threshold for model size, in bytes
        :type threshold: int
        """
        self.add_validator(
            Validator(
                "MaximumSize",
                lambda size: Success()
                if size.value <= threshold
                else Failure(
                    f"Model size {size} exceeds threshold {threshold}"
                ),
            )
        )
