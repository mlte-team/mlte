"""
mlte/api/api.py

Generic API wrapper for MLTE artifact store.
"""

from typing import Optional, Dict, Any

from mlte.api.uri import parse_uri_type, UriType
import mlte.api.local as local

# TODO(Kyle): Enforce schema of documents for each type here within API.

# -----------------------------------------------------------------------------
# Value
# -----------------------------------------------------------------------------


def read_value(
    uri: str,
    model_identifier: str,
    model_version: str,
    value_identifier: str,
    value_version: Optional[int] = None,
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    uri_type = parse_uri_type(uri)
    if uri_type == UriType.HTTP:
        raise NotImplementedError("Temporary.")
    elif uri_type == UriType.LOCAL:
        return local.read_value(
            uri,
            model_identifier,
            model_version,
            value_identifier,
            value_version,
        )
    else:
        assert False, "Unreachable."


def write_value(
    uri: str,
    model_identifier: str,
    model_version: str,
    value_identifier: str,
    value_data: Dict[str, Any],
    value_tag: Optional[str],
) -> int:
    """TODO(Kyle)"""
    uri_type = parse_uri_type(uri)
    if uri_type == UriType.HTTP:
        raise NotImplementedError("Temporary.")
    elif uri_type == UriType.LOCAL:
        return local.write_value(
            uri,
            model_identifier,
            model_version,
            value_identifier,
            value_data,
            value_tag,
        )
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
# ValidatedSpec
# -----------------------------------------------------------------------------


def read_validatedspec(
    uri: str, model_identifier: str, model_version
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    uri_type = parse_uri_type(uri)
    if uri_type == UriType.HTTP:
        raise NotImplementedError("Temporary.")
    elif uri_type == UriType.LOCAL:
        return local.read_validatedspec(uri, model_identifier, model_version)
    else:
        assert False, "Unreachable."


def write_validatedspec(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
) -> int:
    """TODO(Kyle)"""
    uri_type = parse_uri_type(uri)
    if uri_type == UriType.HTTP:
        raise NotImplementedError("Temporary.")
    elif uri_type == UriType.LOCAL:
        return local.write_validatedspec(
            uri, model_identifier, model_version, data
        )
    else:
        assert False, "Unreachable."
