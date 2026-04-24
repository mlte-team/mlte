"""Fixtures for store export."""

from mlte.store.export.export import ExportSpec, ALL_OPTION


ALL_EXPORT_SPEC = ExportSpec(
    models=ALL_OPTION,
    custom_lists=ALL_OPTION,
    users=ALL_OPTION,
)