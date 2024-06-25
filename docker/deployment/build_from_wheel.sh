#!/usr/bin/env bash
export FRONTEND_DOCKERFILE=docker/deployment/Dockerfile.wheel
export BACKEND_DOCKERFILE=docker/deployment/Dockerfile.wheel
bash compose_envs.sh build
