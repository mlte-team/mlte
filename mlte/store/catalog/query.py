"""
mlte/store/catalog/query.py

Query and filtering functionality for catalog store operations.
"""

from __future__ import annotations

from mlte.store.query import PropertyFilter, TagFilter


class ProblemTypeTagFilter(TagFilter):
    name: str = "problem_type"


class ProblemDomainTagFilter(TagFilter):
    name: str = "problem_domain"


class PropertyCategoryPropertyFilter(PropertyFilter):
    name: str = "property_category"
