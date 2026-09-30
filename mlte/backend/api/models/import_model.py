"""Import data."""

from typing import Any

from mlte.model.base_model import BaseModel

class ImportRequest(BaseModel):
    import_data: dict[str, Any]
    """The store data to be imported"""

    force: bool
    """Indicates that existing artifacts may be overwritten."""