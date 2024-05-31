import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from mlte.frontend.config import settings


def run_frontend():
    app = FastAPI()
    static_dir = (
        os.path.dirname(os.path.abspath(__file__)) + "/nuxt-app/.output/public"
    )

    if os.path.exists(static_dir):
        app.mount(
            "/", StaticFiles(directory=static_dir, html=True), name="static"
        )
        uvicorn.run(app, host=settings.APP_HOST, port=int(settings.APP_PORT))
    else:
        print(
            "Unable to run frontend. This is likely due to an issue with this distribution of the package."
        )
