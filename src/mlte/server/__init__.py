import os
import sys
import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


app = FastAPI()
# TODO : Make this more resilient.
STATIC_DIR = os.path.dirname(os.path.abspath(sys.modules.get("mlte").__file__)) + "/server/nuxt-app/.output/public"

app.mount("/", StaticFiles(directory=STATIC_DIR, html = True), name="static")
    

def run_server():
    uvicorn.run(app)