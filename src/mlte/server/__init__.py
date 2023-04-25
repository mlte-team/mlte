import os

from flask import Flask, send_from_directory


# # TODO : Update name of the directory
REL_STATIC_DIR = "react-app/build"

app = Flask(__name__, static_folder=REL_STATIC_DIR)
STATIC_DIR = os.path.join(app.root_path, REL_STATIC_DIR)
NUXT_STATIC_DIR = os.path.join(app.root_path, 'nuxt-app/')

# @app.route(_add_static_prefix("/"))
# def serve():
#     print(os.path.join(STATIC_DIR, "index.html"), flush=True)
#     # /Users/aderr/repos/open-source-repos/mlte/src/mlte/server/react-app/build/index.html

#     if os.path.exists(os.path.join(STATIC_DIR, "index.html")):
#         return send_from_directory(STATIC_DIR, "index.html")
#     else:
#         return "Path failed", 200


# def _run_server(static_prefix=None):
#     """
#     :param static_prefix: If set, the index.html asset will be served from the static_prefix.
#                           If left None, the index.html asset will be served from the root path.
#     :return: None
#     """
#     env_map = {}
#     if static_prefix:
#         env_map[STATIC_PREFIX_ENV_VAR] = static_prefix

#     app.run("0.0.0.0", "80")


import os
import subprocess

def start_nuxt():
    print(os.getcwd(), flush=True)
    print(os.path.abspath('nuxt-app'), flush=True)
    print(os.path.join(NUXT_STATIC_DIR))

    os.chdir(os.path.join(NUXT_STATIC_DIR))
    subprocess.call(['node', '.output/server/index.mjs'])