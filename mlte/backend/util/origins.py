"""
mlte/backend/util/origins.py

Host checking utilities.
"""

from typing import List


def _removeprefix(text: str, prefix: str) -> str:
    """
    Remove a prefix from a string.
    :param text: The input text
    :param prefix: The target prefix
    :return: The modified string
    """
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


def is_localhost(origin: str) -> bool:
    """
    Determine if an origin is localhost.
    :param origin: The origin
    :return: `True` if the origin is localhost, `False` otherwise
    """
    host = origin
    for protocol in ["http://", "https://"]:
        host = _removeprefix(host, protocol)

    host = host.split(":")[0]
    return host == "localhost"


def _resolve_localhost(origin: str) -> str:
    """
    Resolve the localhost origin to an IP address.
    :param origin: The input origin
    :return: The resolved origin
    """
    return origin.replace("localhost", "127.0.0.1")


def resolve_hosts(allowed_origins: List[str]) -> List[str]:
    """
    Resolve host IPs for special addresses.

    This issue manifests when origins like:

        http://localhost:8000

    are provided as arguments to the MLTE API. In this case,
    we would expect addresses like:

        http://127.0.0.1:8000

    to also constitute allowed origins. However, if manual
    host resolution is not applied (by us), this behavior is
    not observed.

    :param allowed_origins: The collection of allowed origins
    :return: The modified collection of allowed origins
    """
    origins = []
    for origin in allowed_origins:
        if is_localhost(origin):
            origins.append(origin)
            origins.append(_resolve_localhost(origin))
        else:
            origins.append(origin)
    return origins
