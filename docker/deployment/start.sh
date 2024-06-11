#!/usr/bin/env bash
bash compose_envs.sh up -d "$@"
bash logs.sh
