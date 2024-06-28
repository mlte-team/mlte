#!/usr/bin/env bash
bash stop.sh
cd ..
bash build.sh
cd deployment
bash start.sh
