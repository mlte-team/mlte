"""
mlte/custom_list/custom_list_names.py

Enum of the predefined custom list names.
"""

from __future__ import annotations

from strenum import StrEnum


class CustomListName(StrEnum):
    """Custom lists names."""

    QA_CATEGORIES = "qa_categories"
    QUALITY_ATTRIBUTES = "quality_attributes"
