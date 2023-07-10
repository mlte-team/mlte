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

    def __init__(self) -> None:
        # NOTE(Kyle): Representing missing values as empty
        # string makes this significantly easier to work with
        # the type checker, although not as clean as I'd like.

        self.namespace = ""
        """The context namespace."""

        self.model = ""
        """The context model identifier."""

        self.version = ""
        """The context model version identifier."""

        self.uri = ""
        """The context artifact store URI."""

    def is_populated(self) -> bool:
        """
        Determine if the context is populated with required values.
        :return: `True` if the context is populated, `False` otherwise
        """
        return (
            self.namespace != ""
            and self.model != ""
            and self.version != ""
            and self.uri != ""
        )

    def assert_populated(self):
        """
        Determine if the context is populated; raise if not.
        :raises RuntimeError: If the context is not populated
        """
        if self.namespace == "":
            raise RuntimeError("Must set MLTE context 'namespace'.")
        if self.model == "":
            raise RuntimeError("Must set MLTE context 'model'.")
        if self.version == "":
            raise RuntimeError("Must set MLTE context 'version'.")
        if self.uri == "":
            raise RuntimeError("Must set MLTE context 'uri'.")
