import json
import os
from typing import Annotated

from fastapi import (
    APIRouter,
    BackgroundTasks,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from fastapi.responses import FileResponse

import mlte.store.error as errors
from mlte.backend.api import codes
from mlte.backend.api.auth.authorization import AuthorizedUser
from mlte.backend.api.error_handlers import raise_http_internal_error
from mlte.backend.core.state import state
from mlte.custom_list.custom_list_names import CustomListName
from mlte.store.import_export.export_store import ExportSpec, ExportWildcard

# The router exported by this submodule
router = APIRouter()


@router.post("/import")
def import_store(
    *,
    current_user: AuthorizedUser,
    import_data: Annotated[UploadFile, File()],
    force: bool = Form(False),
) -> None:
    if not import_data.filename or not import_data.filename.endswith(".json"):
        raise HTTPException(
            status_code=codes.UNPROCESSABLE_ENTITY,
            detail="File is not of type JSON.",
        )

    try:
        file_bytes = import_data.file.read()
        parsed_json = json.loads(file_bytes)

        state.stores.import_store(
            parsed_json,
            force=force,
        )
    except errors.ErrorAlreadyExists as ex:
        raise HTTPException(
            status_code=codes.ALREADY_EXISTS, detail=f"{ex} already exists."
        ) from None
    except Exception as ex:
        raise_http_internal_error(ex)


def cleanup_file(file_path: str) -> None:
    """Removes temporary file after response finishes."""
    if os.path.exists(file_path):
        os.remove(file_path)


@router.post("/export")
def export(
    *,
    current_user: AuthorizedUser,
    models: dict[str, list[str] | ExportWildcard] | ExportWildcard,
    custom_lists: list[CustomListName] | ExportWildcard,
    users: list[str] | ExportWildcard,
    catalogs: list[str] | ExportWildcard,
    background_tasks: BackgroundTasks,
) -> FileResponse:
    try:
        file_path = state.stores.export_store(
            ExportSpec(
                state.stores.artifact_store,
                state.stores.user_store,
                state.stores.catalog_stores,
                models,
                custom_lists,
                users,
                catalogs,
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
