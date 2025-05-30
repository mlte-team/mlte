"""
test/schema/util.py
"""

import os
import pkgutil
from typing import Any, Dict, Optional

import jsonschema

from mlte._private.fixed_json import json

# The identifier for the latest schema for Evidence
EVIDENCE_LATEST_SCHEMA_VERSION = "0.0.1"
# The identifier for the latest schema for TestSuite
TEST_SUITE_LATEST_SCHEMA_VERSION = "0.0.1"
# The identifier for the latest schema for TestResults
TEST_RESULTS_LATEST_SCHEMA_VERSION = "0.0.1"
# The identifier for the latest schema for Report
REPORT_LATEST_SCHEMA_VERSION = "0.0.1"

# Version identifiers for Evidence schemas
_EVIDENCE_SCHEMA_VERSIONS = frozenset(("0.0.1",))
# Version identifiers for TestSuite schemas
_TEST_SUITE_SCHEMA_VERSIONS = frozenset(("0.0.1",))
# Version identifiers for TestResults schemas
_TEST_RESULTS_SCHEMA_VERSIONS = frozenset(("0.0.1",))
# Version identifier for Report schemas
_REPORT_SCHEMA_VERSIONS = frozenset(("0.0.1",))

# The name of the schema file for all schemas
_SCHEMA_FILE_NAME = "schema.json"

# -----------------------------------------------------------------------------
# Schema Validation
# -----------------------------------------------------------------------------


def validate_evidence_schema(
    document: Dict[str, Any], version: Optional[str] = None
):
    """
    Validate the schema of a Evidence document.
    :param document: The document instance
    :param version: The identifier for the schema version
    :raises ValueError: If an invalid schema is specified
    :raises ValidationError: If the instance fails validation
    """
    version = (
        version
        or document.get("schema_version")
        or EVIDENCE_LATEST_SCHEMA_VERSION
    )
    jsonschema.validate(
        instance=document, schema=_find_evidence_schema(version)
    )


def validate_test_suite_schema(
    document: Dict[str, Any], version: Optional[str] = None
):
    """
    Validate the schema of a TestSuite document.
    :param document: The document instance
    :param version: The identifier for the schema version
    :raises ValueError: If an invalid schema is specified
    :raises ValidationError: If the instance fails validation
    """
    version = (
        version
        or document.get("schema_version")
        or TEST_SUITE_LATEST_SCHEMA_VERSION
    )
    jsonschema.validate(
        instance=document, schema=_find_test_suite_schema(version)
    )


def validate_test_results_schema(
    document: Dict[str, Any], version: Optional[str] = None
):
    """
    Validate the schema of a TestResults document.

    :param document: The document instance
    :param version: The identifier for the schema version
    :raises ValueError: If an invalid schema is specified
    :raises ValidationError: If the instance fails validation
    """
    version = (
        version
        or document.get("schema_version")
        or TEST_SUITE_LATEST_SCHEMA_VERSION
    )
    jsonschema.validate(
        instance=document, schema=_find_test_results_schema(version)
    )


def validate_report_schema(
    document: Dict[str, Any], version: Optional[str] = None
):
    """
    Validate the schema of a Report output document.
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


def _find_evidence_schema(version: Optional[str] = None) -> Dict[str, Any]:
    """
    Find, load, and return the JSON schema for Evidence output.

    :param version: The version identifier for the schema
    :type version: Optional[str]

    :return: The loaded schema
    :rtype: Dict[str, Any]

    :raises ValueError: If an invalid schema is specified
    """
    if version is None:
        version = EVIDENCE_LATEST_SCHEMA_VERSION
    if version not in _EVIDENCE_SCHEMA_VERSIONS:
        raise ValueError(
            f"Invalid evidence schema version {version} specified."
        )
    return _find_schema(version, "evidence")


def _find_test_suite_schema(version: Optional[str] = None) -> Dict[str, Any]:
    """
    Find, load, and return the JSON schema for TestSuite output.

    :param version: The version identifier for the schema
    :type version: Optional[str]

    :return: The loaded schema
    :rtype: Dict[str, Any]

    :raises ValueError: If an invalid schema is specified
    """
    if version is None:
        version = TEST_SUITE_LATEST_SCHEMA_VERSION
    if version not in _TEST_SUITE_SCHEMA_VERSIONS:
        raise ValueError(
            f"Invalid test suite schema version {version} specified."
        )
    return _find_schema(version, "tests")


def _find_test_results_schema(version: Optional[str] = None) -> Dict[str, Any]:
    """
    Find, load, and return the JSON schema for TestResults output.

    :param version: The version identifier for the schema
    :type version: Optional[str]

    :return: The loaded schema
    :rtype: Dict[str, Any]

    :raises ValueError: If an invalid schema is specified
    """
    if version is None:
        version = TEST_RESULTS_LATEST_SCHEMA_VERSION
    if version not in _TEST_RESULTS_SCHEMA_VERSIONS:
        raise ValueError(
            f"Invalid test suite schema version {version} specified."
        )
    return _find_schema(version, "results")


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
