#!/usr/bin/env bash
export FRONTEND_DOCKERFILE=Dockerfile.wheel
export BACKEND_DOCKERFILE=Dockerfile.wheel
bash compose_envs.sh build
