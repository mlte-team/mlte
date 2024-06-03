import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Application exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def run_frontend(
    host: str,
    port: int,
) -> int:
    """
    Run the frontend UI application.
    :param host: The application host
    :param port: The application port
    :return: Return code
    """

    app = FastAPI()
    static_dir = (
        os.path.dirname(os.path.abspath(__file__)) + "/nuxt-app/.output/public"
    )

    if os.path.exists(static_dir):
        app.mount(
            "/", StaticFiles(directory=static_dir, html=True), name="static"
        )
        uvicorn.run(app, host=host, port=port)
        return EXIT_SUCCESS
    else:
        print(
            "Unable to run frontend. This is likely due to an issue with this distribution of the package."
        )
        return EXIT_FAILURE
