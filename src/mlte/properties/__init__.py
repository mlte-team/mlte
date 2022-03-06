"""
User-visible interface for the `properties` sub-package.

We choose to export all properties in mlte from a flat
`properties` namespace rather than continuing to 'recurse'
into sub-namespaces for each functional area. We find 
that this structure keeps both source and documentation clean.
"""

# Disbale all linting for this file; flake8 complains that
# it can't see through these imports. In this case, this is
# is a feature not a bug so that we do not need to update
# this file constantly for new property exports.
# flake8: noqa

from ._cpu import ProcessLocalCPUUtilization as ProcessLocalCPUUtilization
from ._memory import (
    ProcessLocalMemoryConsumption as ProcessLocalMemoryConsumption,
)
