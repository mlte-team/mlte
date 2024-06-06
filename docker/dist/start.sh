#!/usr/bin/env bash
docker-compose --env-file .env --env-file .env.backend --env-file .env.frontend --env-file .env.postgres up -d --build
bash logs.sh
