import os

from flask import Flask, send_from_directory


REL_STATIC_DIR = "nuxt-app/.output/public"

app = Flask(__name__, static_folder=REL_STATIC_DIR)
STATIC_DIR = os.path.join(app.root_path, REL_STATIC_DIR)

@app.route('/')
def serve():
    print(os.path.join(STATIC_DIR, "index.html"), flush=True)
    # /Users/aderr/repos/open-source-repos/mlte/env/lib/python3.8/site-packages/mlte/server/nuxt-app/.output/public/index.html
    if os.path.exists(os.path.join(STATIC_DIR, "index.html")):
        return send_from_directory(STATIC_DIR, "index.html")
    else:
        return "Path failed", 500
    

@app.route("/<path:path>")
def serve_static_file(path):
    return send_from_directory(STATIC_DIR, path)


def run_server():
    app.run("0.0.0.0", "3000")