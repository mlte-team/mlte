"""
Internal utilities for schema management.

Acknowledgements:
    The design of schema versioning in this project,
    and the implementation of schema file resolution
    in this file is adapted from the work by the
    TensorFlow team in the Model Card Toolkit:
    https://github.com/tensorflow/model-card-toolkit
"""

import os
import json
import pkgutil
import jsonschema
from typing import Any, Dict, Optional

# The identifier for the latest schema for suites
SUITE_LATEST_SCHEMA_VERSION = "0.0.1"
# The identifier for the latest schema for reports
REPORT_LATEST_SCHEMA_VERSION = "0.0.1"

# Version identifiers for suite schemas
_SUITE_SCHEMA_VERSIONS = frozenset(("0.0.1",))
# Version identifier for report schemas
_REPORT_SCHEMA_VERSIONS = frozenset(("0.0.1",))

# The name of the schema file for all schemas
_SCHEMA_FILE_NAME = "schema.json"

# -----------------------------------------------------------------------------
# Schema Validation
# -----------------------------------------------------------------------------


def validate_suite_schema(
    document: Dict[str, Any], version: Optional[str] = None
):
    """
    Validate the schema of a suite output document.

    :param document: The document instance
    :type document: Dict[str, Any]
    :param version: The identifier for the schema version
    :type version: Optional[str]

    :raises ValueError: If an invalid schema is specified
    :raises ValidationError: If the instance fails validation
    """
    version = (
        version or document.get("schema_version") or SUITE_LATEST_SCHEMA_VERSION
    )
    jsonschema.validate(instance=document, schema=_find_suite_schema(version))


def validate_report_schema(
    document: Dict[str, Any], version: Optional[str] = None
):
    """
    Validate the schema of a suite output document.

    :param document: The document instance
    :type document: Dict[str, Any]
    :param version: The identifier for the schema version
    :type version: Optional[str]

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
        "schema", subdirectory, f"v{version}", _SCHEMA_FILE_NAME
    )
    # Locate the artifact, load, and return it
    data = pkgutil.get_data("mlte", path)
    if data is None:
        raise ValueError(f"Schema {path} not found.")
    return json.loads(data)  # type: ignore


def _find_suite_schema(version: Optional[str] = None) -> Dict[str, Any]:
    """
    Find, load, and return the JSON schema for suite output.

    :param version: The version identifier for the schema
    :type version: Optional[str]

    :return: The loaded schema
    :rtype: Dict[str, Any]

    :raises ValueError: If an invalid schema is specified
    """
    if version is None:
        version = SUITE_LATEST_SCHEMA_VERSION
    if version not in _SUITE_SCHEMA_VERSIONS:
        raise ValueError(f"Invalid suite schema version {version} specified.")
    return _find_schema(version, "suite")


def _find_report_schema(version: Optional[str] = None):
    """
    Find, load, and return the JSON schema for report output.

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
