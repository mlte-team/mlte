#!/usr/bin/env bash
# Build base first.
cd ..
docker build -t mlte-base . -f docker/Dockerfile.mlte
cd docker

# Now build frontend and backend images.
export FRONTEND_DOCKERFILE=docker/Dockerfile.frontend
export BACKEND_DOCKERFILE=docker/Dockerfile.backend
cd deployment
bash compose_envs.sh build backend
bash compose_envs.sh build frontend
cd ..
