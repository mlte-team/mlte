import os

from flask import Flask, send_from_directory


REL_STATIC_DIR = "nuxt-app/.output/public"

app = Flask(__name__, static_folder=REL_STATIC_DIR)
STATIC_DIR = os.path.join(app.root_path, REL_STATIC_DIR)

@app.route('/')
def serve():
    print(os.path.join(STATIC_DIR, 'index.html'), flush=True)
    # /Users/aderr/repos/open-source-repos/mlte/env/lib/python3.8/site-packages/mlte/server/nuxt-app/index.html

    if os.path.exists(os.path.join(STATIC_DIR, "index.html")):
        return send_from_directory(STATIC_DIR, "index.html")
    else:
        return "Path failed", 200


def run_server():
    """
    :param static_prefix: If set, the index.html asset will be served from the static_prefix.
                          If left None, the index.html asset will be served from the root path.
    :return: None
    """
    # env_map = {}
    # if static_prefix:
        # env_map[STATIC_PREFIX_ENV_VAR] = static_prefix

    app.run("0.0.0.0", "3000")


import os
import subprocess

def start_nuxt():
    print(os.getcwd(), flush=True)
    print(os.path.abspath('nuxt-app'), flush=True)
    print(os.path.join(STATIC_DIR))

    os.chdir(os.path.join(STATIC_DIR))
    subprocess.call(['node', '.output/server/index.mjs'])