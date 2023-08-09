"""
mlte/context/context.py

MLTE session context definition.

The MLTE context defines the information necessary to
utilize the MLTE package to generate, persist, and load
MLTE evaluation artifacts.
"""


class Context:
    """
    The MLTE context establishes the context for a MLTE evaluation session.

    NOTE(Kyle): Previously, this module had an explicit dependency on global
    library state. This made testing difficult in that we had to establish the
    global MLTE context through the usual hooks (those that developers use in
    their applications). I have since refactored this to ensure that the Context
    is a standalone data structure that is then exported by the global state module.
    """

    def __init__(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> None:
        # NOTE(Kyle): Representing missing values as empty
        # string makes this significantly easier to work with
        # the type checker, although not as clean as I'd like.

        self.namespace = namespace_id
        """The context namespace."""

        self.model = model_id
        """The context model identifier."""

        self.version = version_id
        """The context model version identifier."""
