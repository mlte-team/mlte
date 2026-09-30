

import os

from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import FileResponse

from mlte.backend.api.auth.authorization import AuthorizedUser
from mlte.backend.api.error_handlers import raise_http_internal_error
from mlte.backend.api.models.import_model import ImportRequest
from mlte.backend.core.state import state
from mlte.store.import_export.export_store import ExportSpec

# The router exported by this submodule
router = APIRouter()


@router.post("/import")
def import_store(
    *,
    current_user: AuthorizedUser,
    request: ImportRequest
) -> None:
    try:
        state.stores.import_store(
            request.import_data,
            request.force,
        )
    except Exception as ex:
        raise_http_internal_error(ex)

    return request.import_data


def cleanup_file(file_path: str) -> None:
    """Removes temporary file after response finishes."""
    if os.path.exists(file_path):
        os.remove(file_path)


@router.post("/export")
def export(
    *,
    current_user: AuthorizedUser,
    background_tasks: BackgroundTasks,
) -> FileResponse:
    try:
        file_path = state.stores.export_store(
            ExportSpec(
                state.stores.artifact_store,
                state.stores.user_store,
                state.stores.catalog_stores,
                {},
                [],
                [],
                [],
            ),
        )
    except Exception as ex:
        raise_http_internal_error(ex)

    background_tasks.add_task(cleanup_file, str(file_path))

    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type="application/octet-stream",
    )