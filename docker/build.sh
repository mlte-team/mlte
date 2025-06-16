#!/usr/bin/env bash
set -e

# Build base first.
cd ..
docker build -t mlte-python . -f docker/Dockerfile.python
docker build -t mlte-node . -f docker/Dockerfile.node
cd docker

# Now build frontend and backend images.
export FRONTEND_DOCKERFILE=docker/Dockerfile.frontend
export BACKEND_DOCKERFILE=docker/Dockerfile.backend
cd deployment
bash compose_envs.sh build backend
bash compose_envs.sh build frontend
cd ..
