"""
test/fixtures/fixtures.py

Unit test support fixtures.
"""

import pytest

import mlte


@pytest.fixture(scope="function")
def default_session(tmp_path):
    """A fixture for establish MLTE artifact store context."""
    mlte.set_namespace("default")
    mlte.set_model("mymodel")
    mlte.set_version("v0.0.1")
    mlte.set_uri(f"local://{tmp_path}")
