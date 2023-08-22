"""
mlte/api/local/api.py

Value persistence API for local filesystem.
"""

from typing import Any, Dict, Optional

# The prefix that indicates a local filesystem directory is used
LOCAL_URI_PREFIX = "local://"

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


def read_spec(
    uri: str, model_identifier: str, model_version: str
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    return {}


def write_spec(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
) -> int:
    """TODO(Kyle)"""
    return 0


# -----------------------------------------------------------------------------
# Validated Specification
# -----------------------------------------------------------------------------


def read_validatedspec(
    uri: str, model_identifier: str, model_version: str
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    return {}


def write_validatedspec(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
) -> int:
    """TODO(Kyle)"""
    return 0
