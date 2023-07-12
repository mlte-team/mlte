"""
mlte/serde/error.py

Error definitions for serialization / deserialization.
"""


class DeserializationError(RuntimeError):
    def __init__(self, field: str):
        super().__init__(f"Deserialization error; missing: '{field}'.")
