#!/usr/bin/env bash
set -e

bash stop.sh

cd ..
bash build.sh

cd deployment
bash start.sh
