"""
mlte/store/catalog/query.py

Query and filtering functionality for catalog store operations.
"""

from __future__ import annotations

from mlte.store.query import PropertyFilter, TagFilter


class ProblemTypeTagFilter(TagFilter):
    tag_property_name: str = "problem_type"


class ProblemDomainTagFilter(TagFilter):
    tag_property_name: str = "problem_domain"


class PropertyCategoryPropertyFilter(PropertyFilter):
    property_name: str = "property_category"
