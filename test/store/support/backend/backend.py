"""
test/store/support/backend/backend.py

Common functionality required for backend test support.
"""

from typing import List, Any, Dict, Callable


class TestDefinition:
    """Encapsulates all data required to parametrize a test."""

    # Force pytest to ignore this class
    __test__ = False

    def __init__(
        self,
        name: str,
        uri: str,
        environment: Dict[str, Any],
        setup_fns: List[Callable[[Dict[str, Any]], None]],
        teardown_fns: List[Callable[[Dict[str, Any]], None]],
    ):
        # A human-readable identifier for the definition
        self.name = name
        # The URI used during backend initialization
        self.uri = uri
        # The environment provided during server initialization
        self.environment = environment
        # The collection of setup callbacks
        self.setup_fns = setup_fns
        # The collection of teardown callbacks
        self.teardown_fns = teardown_fns
        # A key/value store into which initialization can emit artifacts
        self.artifacts: Dict[str, Any] = {}

    def setup(self) -> None:
        """Run setup functions."""
        for fn in self.setup_fns:
            fn(self.artifacts)
        self.uri = self._process_uri(self.uri)

    def teardown(self):
        """Run teardown functions."""
        for fn in self.teardown_fns:
            fn(self.artifacts)

    def _process_uri(self, uri: str) -> str:
        """Process URI with textual replacement."""
        # Perform textual replacement, if necessary
        if uri.startswith("artifact:"):
            assert len(uri.split(":")) == 2, "Corrupt URI."
            key = uri.split(":")[1]

            if key not in self.artifacts:
                raise RuntimeError(f"Artifact with key {key} not found.")
            uri = self.artifacts[key]

        return uri
