"""
BoundSpec class implementation.
"""

from typing import Dict, Any

# -----------------------------------------------------------------------------
# BoundSpec
# -----------------------------------------------------------------------------


class BoundSpec:
    """
    BoundSpec represents the result of binding results
    to specific properties within a specification.
    """

    def __init__(self, document: Dict[str, Any]):
        """
        Initialize a BoundSpec instance.

        :param document: The data produced by the Spec
        :type document: Dict[str, Any]]
        """
        self.document = document
        """The document produced by the Spec."""
