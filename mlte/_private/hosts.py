"""
mlte/_private/hosts.py

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


def is_localhost(host: str) -> bool:
    """
    Determine if a host is localhost.
    :param host: The host
    :return: `True` if the host is localhost, `False` otherwise
    """
    host = host
    for protocol in ["http://", "https://"]:
        host = _removeprefix(host, protocol)

    host = host.split(":")[0]
    return host == "localhost"


def _resolve_localhost(host: str) -> str:
    """
    Resolve the localhost host to an IP address.
    :param host: The input host
    :return: The resolved host
    """
    return host.replace("localhost", "127.0.0.1")


def resolve_hosts(host_list: List[str]) -> List[str]:
    """
    Resolve host IPs for special addresses.

    This issue manifests when hosts like:

        http://localhost:8000

    are provided as arguments to the MLTE API. In this case,
    we would expect addresses like:

        http://127.0.0.1:8000

    to also constitute valid hosts. However, if manual
    host resolution is not applied (by us), this behavior is
    not observed.

    :param host_list: The collection of hosts
    :return: The modified collection of hosts
    """
    hosts = []
    for host in host_list:
        if is_localhost(host):
            hosts.append(host)
            hosts.append(_resolve_localhost(host))
        else:
            hosts.append(host)
    return hosts
