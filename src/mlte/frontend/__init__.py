import os
import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


app = FastAPI()
STATIC_DIR = (
    os.path.dirname(os.path.abspath(__file__)) + "/nuxt-app/.output/public"
)

app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")


def run_frontend():
    uvicorn.run(app)
