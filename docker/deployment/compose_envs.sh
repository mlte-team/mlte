#!/usr/bin/env bash
# Runs docker compose with all env files, adding the commands that are passed.
docker-compose --env-file .env --env-file .env.backend --env-file .env.frontend --env-file .env.postgres "$@"
