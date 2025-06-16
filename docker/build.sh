#!/usr/bin/env bash
set -e

# Build base first.
bash build_base.sh

# Now build frontend and backend images.
export FRONTEND_DOCKERFILE=docker/Dockerfile.frontend
export BACKEND_DOCKERFILE=docker/Dockerfile.backend
cd deployment
bash compose_envs.sh build backend
bash compose_envs.sh build frontend
cd ..
