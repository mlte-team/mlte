from typing import Optional, Tuple

FAKE_USER = "fake_user"
FAKE_PASS = "fake_pass"
FAKE_URI = "http://localhost:8080"
"""Default fake values for http store."""

IN_MEMORY_SQLITE_DB = "sqlite+pysqlite:///:memory:"
"""Default string to create an in memory DB."""


def get_http_defaults_if_needed(
    username: Optional[str] = None,
    password: Optional[str] = None,
    uri: Optional[str] = None,
) -> Tuple[str, str, str]:
    """Checks http values and returns default test ones if needed."""
    if username is None:
        username = FAKE_USER
    if password is None:
        password = FAKE_PASS
    if uri is None:
        uri = FAKE_URI
    return username, password, uri
