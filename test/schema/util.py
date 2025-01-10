"""
test/schema/util.py
"""

import os
import pkgutil
from typing import Any, Dict, Optional

import jsonschema

from mlte._private.fixed_json import json

# The identifier for the latest schema for Value
VALUE_LATEST_SCHEMA_VERSION = "0.0.1"
# The identifier for the latest schema for Spec
SPEC_LATEST_SCHEMA_VERSION = "0.0.1"
# The identifier for the latest schema for ValidatedSpec
VALIDATEDSPEC_LATEST_SCHEMA_VERSION = "0.0.1"
# The identifier for the latest schema for Report
REPORT_LATEST_SCHEMA_VERSION = "0.0.1"

# Version identifiers for Value schemas
_VALUE_SCHEMA_VERSIONS = frozenset(("0.0.1",))
# Version identifiers for Spec schemas
_SPEC_SCHEMA_VERSIONS = frozenset(("0.0.1",))
# Version identifiers for ValidatedSpec schemas
_VALIDATEDSPEC_SCHEMA_VERSIONS = frozenset(("0.0.1",))
# Version identifier for Report schemas
_REPORT_SCHEMA_VERSIONS = frozenset(("0.0.1",))

# The name of the schema file for all schemas
_SCHEMA_FILE_NAME = "schema.json"

# -----------------------------------------------------------------------------
# Schema Validation
# -----------------------------------------------------------------------------


def validate_value_schema(
    document: Dict[str, Any], version: Optional[str] = None
):
    """
    Validate the schema of a Value document.
    :param document: The document instance
    :param version: The identifier for the schema version
    :raises ValueError: If an invalid schema is specified
    :raises ValidationError: If the instance fails validation
    """
    version = (
        version or document.get("schema_version") or VALUE_LATEST_SCHEMA_VERSION
    )
    jsonschema.validate(instance=document, schema=_find_value_schema(version))


def validate_spec_schema(
    document: Dict[str, Any], version: Optional[str] = None
):
    """
    Validate the schema of a Spec document.
    :param document: The document instance
    :param version: The identifier for the schema version
    :raises ValueError: If an invalid schema is specified
    :raises ValidationError: If the instance fails validation
    """
    version = (
        version or document.get("schema_version") or SPEC_LATEST_SCHEMA_VERSION
    )
    jsonschema.validate(instance=document, schema=_find_spec_schema(version))


def validate_validatedspec_schema(
    document: Dict[str, Any], version: Optional[str] = None
):
    """
    Validate the schema of a ValidatedSpec document.

    :param document: The document instance
    :param version: The identifier for the schema version
    :raises ValueError: If an invalid schema is specified
    :raises ValidationError: If the instance fails validation
    """
    version = (
        version or document.get("schema_version") or SPEC_LATEST_SCHEMA_VERSION
    )
    jsonschema.validate(
        instance=document, schema=_find_validatedspec_schema(version)
    )


def validate_report_schema(
    document: Dict[str, Any], version: Optional[str] = None
):
    """
    Validate the schema of a spec output document.
    :param document: The document instance
    :param version: The identifier for the schema version
    :raises ValueError: If an invalid schema is specified
    :raises RuntimeError: If the instance fails validation
    """
    version = (
        version
        or document.get("schema_version")
        or REPORT_LATEST_SCHEMA_VERSION
    )
    jsonschema.validate(instance=document, schema=_find_report_schema(version))


# -----------------------------------------------------------------------------
# Schema Resolution
# -----------------------------------------------------------------------------


def _find_schema(version: str, subdirectory: str) -> Dict[str, Any]:
    """
    Find, load, and return the JSON schema.

    :param version: The version identifier for the schema
    :type version: str
    :param subdirectory: The name of the subdirectory to perform search
    :type subdirectory: str

    :return: The loaded schema
    :rtype: Dict[str, Any]

    :raises ValueError: If an invalid schema is specified
    """
    # Construct the path to the schema file
    path = os.path.join(
        "schema", "artifact", subdirectory, f"v{version}", _SCHEMA_FILE_NAME
    )
    # Locate the artifact, load, and return it
    data = pkgutil.get_data("mlte", path)
    if data is None:
        raise ValueError(f"Schema {path} not found.")
    return json.loads(data)  # type: ignore


def _find_value_schema(version: Optional[str] = None) -> Dict[str, Any]:
    """
    Find, load, and return the JSON schema for Value output.

    :param version: The version identifier for the schema
    :type version: Optional[str]

    :return: The loaded schema
    :rtype: Dict[str, Any]

    :raises ValueError: If an invalid schema is specified
    """
    if version is None:
        version = VALUE_LATEST_SCHEMA_VERSION
    if version not in _VALUE_SCHEMA_VERSIONS:
        raise ValueError(f"Invalid value schema version {version} specified.")
    return _find_schema(version, "value")


def _find_spec_schema(version: Optional[str] = None) -> Dict[str, Any]:
    """
    Find, load, and return the JSON schema for Spec output.

    :param version: The version identifier for the schema
    :type version: Optional[str]

    :return: The loaded schema
    :rtype: Dict[str, Any]

    :raises ValueError: If an invalid schema is specified
    """
    if version is None:
        version = SPEC_LATEST_SCHEMA_VERSION
    if version not in _SPEC_SCHEMA_VERSIONS:
        raise ValueError(f"Invalid spec schema version {version} specified.")
    return _find_schema(version, "spec")


def _find_validatedspec_schema(version: Optional[str] = None) -> Dict[str, Any]:
    """
    Find, load, and return the JSON schema for ValidatedSpec output.

    :param version: The version identifier for the schema
    :type version: Optional[str]

    :return: The loaded schema
    :rtype: Dict[str, Any]

    :raises ValueError: If an invalid schema is specified
    """
    if version is None:
        version = VALIDATEDSPEC_LATEST_SCHEMA_VERSION
    if version not in _VALIDATEDSPEC_SCHEMA_VERSIONS:
        raise ValueError(f"Invalid spec schema version {version} specified.")
    return _find_schema(version, "validated")


def _find_report_schema(version: Optional[str] = None):
    """
    Find, load, and return the JSON schema for Report output.

    :param version: The version identifier for the schema
    :type version: Optional[str]

    :return: The loaded schema
    :rtype: Dict[str, Any]

    :raises ValueError: If an invalid schema is specified
    """
    if version is None:
        version = REPORT_LATEST_SCHEMA_VERSION
    if version not in _REPORT_SCHEMA_VERSIONS:
        raise ValueError(f"Invalid report schema version {version} specified.")
    return _find_schema(version, "report")
