#!/usr/bin/env bash

PENV=${1:-3.12}
deactivate; pyenv local $PENV && make venv-redo && source .venv/bin/activate
