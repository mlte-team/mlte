"""
mlte/api/api.py

Generic API wrapper for MLTE artifact store.
"""

# TODO(Kyle): This entire sub-package is now deprecated in favor
# of the new implementation of the artifact store interface.

from typing import Optional, Dict, Any

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
    return {}


def write_value(
    uri: str,
    model_identifier: str,
    model_version: str,
    value_identifier: str,
    value_data: Dict[str, Any],
    value_tag: Optional[str],
) -> int:
    """TODO(Kyle)"""
    return 0


# -----------------------------------------------------------------------------
# Specification
# -----------------------------------------------------------------------------


def read_spec(uri: str, model_identifier: str, model_version) -> Dict[str, Any]:
    """TODO(Kyle)"""
    return {}


def write_spec(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
) -> int:
    """TODO(Kyle)"""
    return 0


# -----------------------------------------------------------------------------
# ValidatedSpec
# -----------------------------------------------------------------------------


def read_validatedspec(
    uri: str, model_identifier: str, model_version
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    return {}


def write_validatedspec(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
) -> int:
    """TODO(Kyle)"""
    return 0
