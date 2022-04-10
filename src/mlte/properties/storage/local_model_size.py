"""
Storage capacity measurement for locally-stored models.
"""

import os
from typing import Dict, Any

from ..property import Property


class LocalModelSize(Property):
    """Measure the size of a locally-stored model."""

    def __init__(self):
        """Initialize a new LocalModelSize property."""
        super().__init__("LocalModelSize")

    def evaluate(self, path: str) -> int:
        """
        Compute the size of the model at `path`.

        :param path: The path to the model
        :type path: str

        :return: The size of the model, in bytes
        :rtype: int
        """
        return LocalModelSize._semantics(self._evaluate(path))

    def _evaluate(self, path: str) -> Dict[str, Any]:
        """See evaluate()."""
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

    @staticmethod
    def _semantics(output: Dict[str, Any]) -> int:
        """Provide semantics for property output."""
        assert "total_size" in output, "Broken invariant."
        return int(output["total_size"])
