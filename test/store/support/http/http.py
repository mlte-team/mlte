"""
Common functionality required for HTTP test support.
"""

import sys
import os
from pathlib import Path
import subprocess
import requests
from requests.exceptions import ConnectionError

from typing import List, Dict, Any, Callable

# -----------------------------------------------------------------------------
# Global Constants
# -----------------------------------------------------------------------------

# The name of the test directory in the source hierarchy
TEST_DIRECTORY_NAME = "test"

# The host on which the server runs for tests
DEFAULT_SERVER_HOST = "localhost"
# The port on which the server listens
DEFAULT_SERVER_PORT = 8080

# -----------------------------------------------------------------------------
# Request Convenience Functions
# -----------------------------------------------------------------------------


def get(
    route: str, host: str = DEFAULT_SERVER_HOST, port: int = DEFAULT_SERVER_PORT
):
    """Perform a GET request on `route`."""
    return requests.get(f"http://{host}:{port}{route}")


def post(
    route: str,
    json: Dict[str, Any],
    host: str = DEFAULT_SERVER_HOST,
    port: int = DEFAULT_SERVER_PORT,
):
    """Perform a POST request on `route` with `json`."""
    return requests.post(f"http://{host}:{port}{route}", json=json)


def delete(
    route: str, host: str = DEFAULT_SERVER_HOST, port: int = DEFAULT_SERVER_PORT
):
    """Perform a DELETE request on `route`."""
    return requests.delete(f"http://{host}:{port}{route}")


# -----------------------------------------------------------------------------
# TestDefinition
# -----------------------------------------------------------------------------


class TestDefinition:
    """Encapsulates all data required to parametrize a test."""

    # Force pytest to ignore this class
    __test__ = False

    def __init__(
        self,
        name: str,
        args: List[str],
        environment: Dict[str, Any],
        setup_fns: List[Callable[[Dict[str, Any]], None]],
        teardown_fns: List[Callable[[Dict[str, Any]], None]],
    ):
        # A human-readable identifier for the definition
        self.name = name
        # Commandline arguments passed to the server on startup
        self.args = args
        # The environment provided during server initialization
        self.environment = environment
        # The collection of setup callbacks
        self.setup_fns = setup_fns
        # The collection of teardown callbacks
        self.teardown_fns = teardown_fns
        # A key/value store into which initialization can emit artifacts
        self.artifacts: Dict[str, Any] = {}

        # The python executable
        self.interpreter = os.path.abspath(sys.executable)
        # The path to the server entrypoint
        self.program = self._find_program()

    def setup(self) -> None:
        """Run setup functions."""
        for fn in self.setup_fns:
            fn(self.artifacts)

    def teardown(self):
        """Run teardown functions."""
        for fn in self.teardown_fns:
            fn(self.artifacts)

    def start(self):
        """Start storage server process."""
        # Process arguments with information from k/v
        cmd = [
            self.interpreter,
            self.program,
            *self._process_arguments(self.args),
        ]
        # Construct subprocess environment
        env = {**os.environ.copy(), **self.environment}

        # Start the server process
        process = subprocess.Popen(
            cmd, stdout=None, stderr=None, stdin=None, env=env
        )

        exitcode = process.poll()
        if exitcode is not None:
            raise RuntimeError(f"Failed to start server process: {exitcode}")

        # Wait for server to become available
        self._wait_for_response()

        # Defer termination of the server process
        self.teardown_fns.insert(0, lambda _: process.kill())

    def _process_arguments(self, args: List[str]) -> List[str]:
        """Process arguments with textual replacement."""
        results = []
        for arg in args:
            if not arg.startswith("artifact:"):
                results.append(arg)
                continue

            assert len(arg.split(":")) == 2, "Corrupt argument."

            key = arg.split(":")[1]
            if key not in self.artifacts:
                raise RuntimeError(f"Artifact with key {key} not found.")
            results.append(self.artifacts[key])

        assert len(results) == len(args), "Broken postcondition."
        return results

    def _find_program(self) -> str:
        """Locate the storage server application entry."""
        path = Path(__file__)
        while path.name != TEST_DIRECTORY_NAME:
            path = path.parent
        path = path.parent / "src" / "mlte" / "store" / "frontend" / "server.py"
        assert path.exists(), "Failed to locate storage server program."
        return path.resolve().as_posix()

    def _wait_for_response(self):
        """Wait for a response from the server."""
        while True:
            try:
                _ = get("/healthcheck")
            except ConnectionError:
                continue
            except Exception as e:
                raise RuntimeError(f"Failed to start server: {e}") from None
            return
