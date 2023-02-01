"""
Application entry point.
"""

import argparse
import logging
import sys
from typing import Optional, Dict, Any

import uvicorn
from ..backend import Backend, initialize_backend
from ..frontend.models import Result
from fastapi import FastAPI, HTTPException

# Application exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# The deafult host address to which the server binds
DEFAULT_HOST = "localhost"
# The default port on which the server listens
DEFAULT_PORT = 8080

# -----------------------------------------------------------------------------
# Global State
# -----------------------------------------------------------------------------

# The global FastAPI application
g_app = FastAPI()

# The global backend
g_store: Backend = None  # type: ignore

# -----------------------------------------------------------------------------
# Argument Parsing
# -----------------------------------------------------------------------------


def parse_arguments():
    """Parse commandline arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host",
        type=str,
        default=DEFAULT_HOST,
        help=f"The host address to which the server binds (default: {DEFAULT_HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"The port on which the server listens (default: {DEFAULT_PORT})",
    )
    # TODO(Kyle): Set a reasonable default
    parser.add_argument(
        "--backend-uri",
        type=str,
        required=True,
        help="The URI for the backend store.",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose output."
    )
    args = parser.parse_args()
    return args.host, args.port, args.backend_uri, args.verbose


# -----------------------------------------------------------------------------
# Routes: Healthcheck
# -----------------------------------------------------------------------------


@g_app.get("/healthcheck")
async def get_healthcheck():
    return {"status": "healthy"}


# -----------------------------------------------------------------------------
# Routes: Read Metadata
# -----------------------------------------------------------------------------


@g_app.get("/metadata/model")
async def get_models():
    """Get metadata for all existing models."""
    try:
        document = g_store.read_model_metadata()
    except RuntimeError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error.")
    return document


@g_app.get("/metadata/model/{model_identifier}")
async def get_model(model_identifier: str):
    """
    Get metadata for a single model.
    :param model_identifier: The identifier for the model of interest
    :type model_identifier: str
    """
    try:
        document = g_store.read_model_metadata(model_identifier)
    except RuntimeError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error.")
    return document


# -----------------------------------------------------------------------------
# Routes: Read Results
# -----------------------------------------------------------------------------


@g_app.get(
    "/result/{model_identifier}/{model_version}/{result_identifier}/{result_version}"
)
async def get_result_version(
    model_identifier: str,
    model_version: str,
    result_identifier: str,
    result_version: int,
):
    """
    Get an individual result version.
    :param model_identifier: The identifier for the model of interest
    :type model_identifier: str
    :param model_version: The version string for the model of interest
    :type model_version: str
    :param result_identifier: The identifier for the result of interest
    :type result_identifier: str
    :param result_version: The version identifier for the result of interest
    :type result_version: int
    """
    try:
        # Read the result from the store
        document = g_store.read_result(
            model_identifier, model_version, result_identifier, result_version
        )
    except RuntimeError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error.")
    return document


@g_app.get("/result/{model_identifier}/{model_version}/{result_identifier}")
async def get_result(
    model_identifier: str,
    model_version: str,
    result_identifier: str,
):
    """
    Get an individual result.
    :param model_identifier: The identifier for the model of interest
    :type model_identifier: str
    :param model_version: The version string for the model of interest
    :type model_version: str
    :param result_identifier: The identifier for the result of interest
    :type result_identifier: str
    """
    try:
        # Result the result from the store
        document = g_store.read_result(
            model_identifier, model_version, result_identifier
        )
    except RuntimeError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error.")
    return document


@g_app.get("/result/{model_identifier}/{model_version}")
async def get_results(
    model_identifier: str,
    model_version: str,
    result_tag: Optional[str] = None,
):
    """
    Get a result or a collection of results.
    :param model_identifier: The identifier for the model of interest
    :type model_identifier: str
    :param model_version: The version string for the model of interest
    :type model_version: str
    :param result_tag: The tag for the result of interest
    :type result_tag: Optional[str]
    """
    try:
        document = g_store.read_results(
            model_identifier, model_version, result_tag
        )
    except RuntimeError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error.")
    return document


# -----------------------------------------------------------------------------
# Routes: Write Results
# -----------------------------------------------------------------------------


@g_app.post("/result/{model_identifier}/{model_version}")
async def post_result(
    model_identifier: str, model_version: str, result: Result
):
    """
    Post a result or collection of results.
    :param result: The result to write
    :type result: RequestModelResult
    """
    if len(result.versions) != 1:
        raise HTTPException(status_code=500, detail="Update this code.")

    try:
        # Write the result to the backend
        document = g_store.write_result(
            model_identifier,
            model_version,
            result.identifier,
            result.versions[0].data,
            result.tag,
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error.")

    return document


# -----------------------------------------------------------------------------
# Routes: Delete Results
# -----------------------------------------------------------------------------


@g_app.delete(
    "/result/{model_identifier}/{model_version}/{result_identifier}/{result_version}"
)
async def delete_result_version(
    model_identifier: str,
    model_version: str,
    result_identifier: str,
    result_version: int,
):
    """
    Delete an individual result version.
    :param model_identifier: The identifier for the model of interest
    :type model_identifier: str
    :param model_version: The version string for the model of interest
    :type model_version: str
    :param result_identifier: The identifier for the result of interest
    :type result_identifier: str
    :param result_version: The version identifier for the result
    :type result_version: int
    """
    try:
        document = g_store.delete_result_version(
            model_identifier, model_version, result_identifier, result_version
        )
    except RuntimeError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error.")

    return document


@g_app.delete("/result/{model_identifier}/{model_version}/{result_identifier}")
async def delete_result(
    model_identifier: str, model_version: str, result_identifier: str
):
    """
    Delete an individual result.
    :param model_identifier: The identifier for the model of interest
    :type model_identifier: str
    :param model_version: The version string for the model of interest
    :type model_version: str
    :param result_identifier: The identifier for the result of interest
    :type result_identifier: str
    """
    try:
        document = g_store.delete_result(
            model_identifier, model_version, result_identifier
        )
    except RuntimeError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error.")

    return document


@g_app.delete("/result/{model_identifier}/{model_version}")
async def delete_results(
    model_identifier: str, model_version: str, result_tag: Optional[str] = None
):
    """
    Delete a collection of results.
    :param model_identifier: The identifier for the model of interest
    :type model_identifier: str
    :param model_version: The version string for the model of interest
    :type model_version: str
    :param result_tag: The (optional) tag that identifies results of interest
    :type result_tag: Optional[str]
    """
    try:
        document = g_store.delete_results(
            model_identifier, model_version, result_tag
        )
    except RuntimeError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error.")

    return document


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def run(
    host: str,
    port: int,
    backend_uri: str,
    verbose: bool,
    **kwargs: Dict[str, Any],
) -> int:
    """
    Run the server.

    :param host: The host address to which the server binds
    :type host: str
    :param port: The port to which the server binds
    :type port: int
    :param backend_uri: The backend URI
    :type backend_uri: str
    :param verbose: Enable verbose logging
    :type verbose: bool
    :param kwargs: Catch-all for keyword arguments
    :type kwargs: Dict[str, Any]

    :return: An error code
    :rtype: int
    """
    global g_store

    logging.basicConfig(level=logging.INFO if verbose else logging.ERROR)

    # Initialize the backend store
    try:
        g_store = initialize_backend(backend_uri)
    except RuntimeError as e:
        logging.error(f"{e}")
        return EXIT_FAILURE

    uvicorn.run(g_app, host=host, port=port)
    return EXIT_SUCCESS


def main() -> int:
    host, port, backend_uri, verbose = parse_arguments()
    return run(host, port, backend_uri, verbose)


if __name__ == "__main__":
    sys.exit(main())
