"""
Generic API wrapper for MLTE artifact store.
"""

from typing import Optional, Dict, Any

from mlte.store.api.uri import parse_uri_type, UriType
import mlte.store.api.local as local

# TODO(Kyle): Enforce schema of documents for each type here within API.

# -----------------------------------------------------------------------------
# Result
# -----------------------------------------------------------------------------


def read_result(
    uri: str,
    model_identifier: str,
    model_version: str,
    result_identifier: str,
    result_version: Optional[int] = None,
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    uri_type = parse_uri_type(uri)
    if uri_type == UriType.HTTP:
        raise NotImplementedError("Temporary.")
    elif uri_type == UriType.LOCAL:
        return local.read_result(
            uri,
            model_identifier,
            model_version,
            result_identifier,
            result_version,
        )
    else:
        assert False, "Unreachable."


def write_result(
    uri: str,
    model_identifier: str,
    model_version: str,
    result_identifier: str,
    result_data: Dict[str, Any],
    result_tag: Optional[str],
) -> int:
    """TODO(Kyle)"""
    uri_type = parse_uri_type(uri)
    if uri_type == UriType.HTTP:
        raise NotImplementedError("Temporary.")
    elif uri_type == UriType.LOCAL:
        return local.write_result(
            uri,
            model_identifier,
            model_version,
            result_identifier,
            result_data,
            result_tag,
        )
    else:
        assert False, "Unreachable."


# -----------------------------------------------------------------------------
# Binding
# -----------------------------------------------------------------------------


def read_binding(
    uri: str, model_identifier: str, model_version
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    uri_type = parse_uri_type(uri)
    if uri_type == UriType.HTTP:
        raise NotImplementedError("Temporary.")
    elif uri_type == UriType.LOCAL:
        return local.read_binding(uri, model_identifier, model_version)
    else:
        assert False, "Unreachable."


def write_binding(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
) -> int:
    """TODO(Kyle)"""
    uri_type = parse_uri_type(uri)
    if uri_type == UriType.HTTP:
        raise NotImplementedError("Temporary.")
    elif uri_type == UriType.LOCAL:
        return local.write_binding(uri, model_identifier, model_version, data)
    else:
        assert False, "Unreachable."


# -----------------------------------------------------------------------------
# Specification
# -----------------------------------------------------------------------------


def read_spec(uri: str, model_identifier: str, model_version) -> Dict[str, Any]:
    """TODO(Kyle)"""
    uri_type = parse_uri_type(uri)
    if uri_type == UriType.HTTP:
        raise NotImplementedError("Temporary.")
    elif uri_type == UriType.LOCAL:
        return local.read_spec(uri, model_identifier, model_version)
    else:
        assert False, "Unreachable."


def write_spec(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
) -> int:
    """TODO(Kyle)"""
    uri_type = parse_uri_type(uri)
    if uri_type == UriType.HTTP:
        raise NotImplementedError("Temporary.")
    elif uri_type == UriType.LOCAL:
        return local.write_spec(uri, model_identifier, model_version, data)
    else:
        assert False, "Unreachable."


# -----------------------------------------------------------------------------
# BoundSpec
# -----------------------------------------------------------------------------


def read_boundspec(
    uri: str, model_identifier: str, model_version
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    uri_type = parse_uri_type(uri)
    if uri_type == UriType.HTTP:
        raise NotImplementedError("Temporary.")
    elif uri_type == UriType.LOCAL:
        return local.read_boundspec(uri, model_identifier, model_version)
    else:
        assert False, "Unreachable."


def write_boundspec(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
) -> int:
    """TODO(Kyle)"""
    uri_type = parse_uri_type(uri)
    if uri_type == UriType.HTTP:
        raise NotImplementedError("Temporary.")
    elif uri_type == UriType.LOCAL:
        return local.write_boundspec(uri, model_identifier, model_version, data)
    else:
        assert False, "Unreachable."
