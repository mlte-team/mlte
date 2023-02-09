"""
URI parsing.
"""

from enum import Enum


class UriType(Enum):
    """Enumerates all artifact store URI types."""

    LOCAL = "LOCAL"
    HTTP = "HTTP"


def parse_uri_type(uri: str) -> UriType:
    """
    Determine the URI type from string.

    :param uri: The URI for the artifact store
    :type uri: str

    :return: The URI type
    :rtype: UriType
    """
    if uri.startswith("http://"):
        return UriType.HTTP
    elif uri.startswith("local://"):
        return UriType.LOCAL
    else:
        raise RuntimeError(f"Invalid artifact store URI provided: {uri}")
