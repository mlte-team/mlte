#!/usr/bin/env bash
set -e

bash compose_envs.sh up -d "$@"
bash logs.sh
