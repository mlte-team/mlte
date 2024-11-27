"""
mlte/model/api/serialization_exception.py

Exception used for serialization issues.
"""
from __future__ import annotations


class SerializationException(TypeError):
    """Exception used for JSON serialization issues."""

    def __init__(self, error: TypeError, object: str):
        super().__init__(
            f"Object {object} cannot be serialized into JSON, ensure all attributes are serializable: "
            + str(error)
        )
