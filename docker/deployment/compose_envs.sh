#!/usr/bin/env bash
set -e

# Sets up the proper profiles and env files depending on the store type configured, defaulting to rdbs.
export COMPOSE_PROFILES="${STORE_TYPE:=rdbs}"
export BACKEND_ENVFILE="${BACKEND_ENVFILE:-.env.backend.$STORE_TYPE}"
export FRONTEND_ENVFILE="${FRONTEND_ENVFILE:-.env.frontend}"
export POSTGRES_ENVFILE="${POSTGRES_ENVFILE:-.env.postgres}"
export HOST_FS_STORE="${HOST_FS_STORE:-./store}"

# Read versions from the tools selected by the project's mise.toml.
# mise must be installed, and `mise install` must have run.
NODE_VERSION="$(mise exec -- node -p 'process.versions.node')"
UV_VERSION="$(mise exec -- uv --version | awk '{print $2}')"
export NODE_VERSION UV_VERSION

# Runs docker compose with all env files, adding the commands that are passed.
docker compose --env-file .env --env-file "${BACKEND_ENVFILE}" --env-file "${FRONTEND_ENVFILE}" --env-file "${POSTGRES_ENVFILE}" "$@"
