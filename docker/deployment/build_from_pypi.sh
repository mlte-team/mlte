#!/usr/bin/env bash
export FRONTEND_DOCKERFILE=docker/deployment/Dockerfile.pypi
export BACKEND_DOCKERFILE=docker/deployment/Dockerfile.pypi
bash compose_envs.sh build
